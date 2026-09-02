/*
 * LIRA-8 preset dialog helper - Windows port of Helper/lira_dialog_helper.m
 *
 * Watches <drive>:\tmp on every fixed drive for the token files the Pd patch
 * writes (the patch's "/tmp/..." paths resolve to \tmp on the DAW's current
 * drive), shows native Open/Save dialogs, and manages the preset library in
 * %USERPROFILE%\Music\LIRA-8\Presets.
 *
 * Build (cross-compile from macOS/Linux):
 *   x86_64-w64-mingw32-gcc -O2 -municode -mwindows -o LIRA-8-helper.exe \
 *       lira_helper_win.c -lcomdlg32 -lshlwapi
 */
#include <windows.h>
#include <commdlg.h>
#include <shlwapi.h>
#include <stdio.h>
#include <wchar.h>

#define MAX_PRESETS 4096
#define DLGBUF 32768

static WCHAR g_tmp[MAX_PATH];        /* active \tmp dir for this transaction */
static WCHAR g_drives[26][8];        /* fixed-drive \tmp dirs, e.g. C:\tmp   */
static int   g_ndrives;
static WCHAR g_presets[MAX_PATH];    /* %USERPROFILE%\Music\LIRA-8\Presets   */
static WCHAR g_current[MAX_PATH];    /* current preset base name, "" = none  */
static HWND  g_owner;                /* hidden topmost owner for dialogs     */

static void tmp_path(WCHAR *out, const WCHAR *name)
{
    _snwprintf(out, MAX_PATH, L"%ls\\%ls", g_tmp, name);
    out[MAX_PATH - 1] = 0;
}

static void log_msg(const char *msg, DWORD err)
{
    WCHAR p[MAX_PATH];
    tmp_path(p, L"lira_helper.log");
    FILE *f = _wfopen(p, L"ab");
    if (f) {
        if (err) fprintf(f, "%s (err=%lu)\r\n", msg, (unsigned long)err);
        else     fprintf(f, "%s\r\n", msg);
        fclose(f);
    }
}

static BOOL file_exists(const WCHAR *path)
{
    DWORD a = GetFileAttributesW(path);
    return a != INVALID_FILE_ATTRIBUTES && !(a & FILE_ATTRIBUTE_DIRECTORY);
}

/* Atomically place raw bytes at path: write path.new, then rename over.
 * Retries around Pd's 50ms polling reads. */
static BOOL put_bytes(const WCHAR *path, const char *bytes, DWORD len)
{
    WCHAR tmpf[MAX_PATH + 8];
    _snwprintf(tmpf, MAX_PATH + 8, L"%ls.new", path);
    tmpf[MAX_PATH + 7] = 0;
    for (int attempt = 0; attempt < 20; attempt++) {
        HANDLE h = CreateFileW(tmpf, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS,
                               FILE_ATTRIBUTE_NORMAL, NULL);
        if (h != INVALID_HANDLE_VALUE) {
            DWORD written = 0;
            BOOL ok = WriteFile(h, bytes, len, &written, NULL);
            CloseHandle(h);
            if (ok && written == len &&
                MoveFileExW(tmpf, path, MOVEFILE_REPLACE_EXISTING))
                return TRUE;
        }
        Sleep(5);
    }
    log_msg("put_bytes failed", GetLastError());
    return FALSE;
}

/* Atomically place a copy of src at dst (copy to dst.new, rename over). */
static BOOL put_copy(const WCHAR *src, const WCHAR *dst)
{
    WCHAR tmpf[MAX_PATH + 8];
    _snwprintf(tmpf, MAX_PATH + 8, L"%ls.new", dst);
    tmpf[MAX_PATH + 7] = 0;
    for (int attempt = 0; attempt < 20; attempt++) {
        if (CopyFileW(src, tmpf, FALSE) &&
            MoveFileExW(tmpf, dst, MOVEFILE_REPLACE_EXISTING))
            return TRUE;
        Sleep(5);
    }
    log_msg("put_copy failed", GetLastError());
    return FALSE;
}

/* "<name>;\n" as UTF-8 into \tmp\lira_preset_name.txt */
static BOOL write_name_file(const WCHAR *base)
{
    char utf8[1024];
    int n = WideCharToMultiByte(CP_UTF8, 0, base, -1, utf8,
                                (int)sizeof(utf8) - 4, NULL, NULL);
    if (n <= 0) return FALSE;
    utf8[n - 1] = ';';           /* n includes the NUL terminator */
    utf8[n] = '\n';
    WCHAR p[MAX_PATH];
    tmp_path(p, L"lira_preset_name.txt");
    return put_bytes(p, utf8, (DWORD)(n + 1));
}

/* The load handshake the Pd patch expects. Order matters: the ready flag is
 * written LAST and only if everything before it succeeded. */
static void run_load_handshake(const WCHAR *lira_path, const WCHAR *base)
{
    WCHAR ready[MAX_PATH], flag[MAX_PATH];
    tmp_path(ready, L"lira_load_ready.lira");
    if (!put_copy(lira_path, ready)) { log_msg("load: copy failed", 0); return; }
    wcsncpy(g_current, base, MAX_PATH - 1);
    g_current[MAX_PATH - 1] = 0;
    if (!write_name_file(base)) { log_msg("load: name write failed", 0); return; }
    tmp_path(flag, L"lira_load_ready.token");
    if (!put_bytes(flag, "ready 1;\n", 9))
        log_msg("load: ready flag failed - load will not fire", 0);
}

/* strip directory + ".lira" extension into out */
static void base_name(const WCHAR *path, WCHAR *out)
{
    const WCHAR *p = wcsrchr(path, L'\\');
    const WCHAR *q = wcsrchr(path, L'/');
    if (q > p) p = q;
    p = p ? p + 1 : path;
    wcsncpy(out, p, MAX_PATH - 1);
    out[MAX_PATH - 1] = 0;
    size_t len = wcslen(out);
    if (len > 5 && _wcsicmp(out + len - 5, L".lira") == 0) out[len - 5] = 0;
}

/* --- preset directory listing, Explorer-style natural ordering --------- */
static WCHAR g_list[MAX_PRESETS][MAX_PATH];
static int g_nlist;

static int cmp_names(const void *a, const void *b)
{
    return StrCmpLogicalW((const WCHAR *)a, (const WCHAR *)b);
}

static void list_presets(void)
{
    g_nlist = 0;
    WCHAR pat[MAX_PATH];
    _snwprintf(pat, MAX_PATH, L"%ls\\*.lira", g_presets);
    pat[MAX_PATH - 1] = 0;
    WIN32_FIND_DATAW fd;
    HANDLE h = FindFirstFileW(pat, &fd);
    if (h == INVALID_HANDLE_VALUE) return;
    do {
        if (!(fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
            && g_nlist < MAX_PRESETS) {
            wcsncpy(g_list[g_nlist], fd.cFileName, MAX_PATH - 1);
            g_list[g_nlist][MAX_PATH - 1] = 0;
            g_nlist++;
        }
    } while (FindNextFileW(h, &fd));
    FindClose(h);
    qsort(g_list, (size_t)g_nlist, sizeof(g_list[0]), cmp_names);
}

static void step_preset(int offset)
{
    list_presets();
    if (g_nlist == 0) return;
    int cur = 0;
    WCHAR curbase[MAX_PATH];
    for (int i = 0; i < g_nlist; i++) {
        base_name(g_list[i], curbase);
        if (_wcsicmp(curbase, g_current) == 0) { cur = i; break; }
    }
    int next = (cur + offset) % g_nlist;
    if (next < 0) next += g_nlist;
    WCHAR full[MAX_PATH + MAX_PATH], nb[MAX_PATH];
    _snwprintf(full, MAX_PATH + MAX_PATH, L"%ls\\%ls", g_presets, g_list[next]);
    full[MAX_PATH + MAX_PATH - 1] = 0;
    base_name(full, nb);
    run_load_handshake(full, nb);
}

/* --- dialogs ----------------------------------------------------------- */
static const WCHAR FILTER[] = L"LIRA-8 Presets (*.lira)\0*.lira\0All Files\0*.*\0";
static WCHAR g_dlgfile[DLGBUF];

static void after_dialog(void)
{
    /* keep our CWD off whatever folder the user browsed to, and swallow any
     * requests that queued up while a modal dialog was open */
    SetCurrentDirectoryW(g_tmp);
    static const WCHAR *toks[] = { L"lira_load_req.token", L"lira_save_req.token",
        L"lira_saveas_req.token", L"lira_prev_req.token", L"lira_next_req.token",
        L"lira_new_req.token" };
    for (int d = 0; d < g_ndrives; d++)
        for (int t = 0; t < 6; t++) {
            WCHAR p[MAX_PATH];
            _snwprintf(p, MAX_PATH, L"%ls\\%ls", g_drives[d], toks[t]);
            p[MAX_PATH - 1] = 0;
            DeleteFileW(p);
        }
}

static void prep_dialog(void)
{
    SetForegroundWindow(g_owner);   /* best effort; owner is topmost */
}

static void handle_load_dialog(void)
{
    g_dlgfile[0] = 0;
    OPENFILENAMEW ofn;
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = g_owner;
    ofn.lpstrFilter = FILTER;
    ofn.lpstrFile = g_dlgfile;
    ofn.nMaxFile = DLGBUF;
    ofn.lpstrInitialDir = g_presets;
    ofn.lpstrTitle = L"Select a LIRA-8 Preset (.lira)";
    ofn.Flags = OFN_FILEMUSTEXIST | OFN_HIDEREADONLY;
    prep_dialog();
    BOOL ok = GetOpenFileNameW(&ofn);
    if (!ok) {
        DWORD e = CommDlgExtendedError();
        if (e) log_msg("load dialog error", e);
        after_dialog();
        return;
    }
    WCHAR nb[MAX_PATH];
    base_name(g_dlgfile, nb);
    run_load_handshake(g_dlgfile, nb);
    after_dialog();
}

static void handle_saveas_dialog(void)
{
    if (g_current[0]) {
        wcsncpy(g_dlgfile, g_current, DLGBUF - 8);
        g_dlgfile[DLGBUF - 8] = 0;
    } else {
        wcscpy(g_dlgfile, L"MyPreset");
    }
    OPENFILENAMEW ofn;
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = g_owner;
    ofn.lpstrFilter = FILTER;
    ofn.lpstrFile = g_dlgfile;
    ofn.nMaxFile = DLGBUF - 8;      /* leave room to force ".lira" */
    ofn.lpstrInitialDir = g_presets;
    ofn.lpstrTitle = L"Save LIRA-8 Preset As";
    ofn.lpstrDefExt = L"lira";
    ofn.Flags = OFN_OVERWRITEPROMPT | OFN_HIDEREADONLY;
    prep_dialog();
    BOOL ok = GetSaveFileNameW(&ofn);
    if (!ok) {
        DWORD e = CommDlgExtendedError();
        if (e) log_msg("saveas dialog error", e);
        after_dialog();
        return;
    }
    /* force the .lira extension like the macOS helper does */
    size_t len = wcslen(g_dlgfile);
    if (len < 5 || _wcsicmp(g_dlgfile + len - 5, L".lira") != 0)
        wcscat(g_dlgfile, L".lira");
    WCHAR src[MAX_PATH];
    tmp_path(src, L"lira_current_save.lira");
    if (!put_copy(src, g_dlgfile)) {
        MessageBoxW(g_owner, L"LIRA-8: saving the preset FAILED. See C:\\tmp\\lira_helper.log",
                    L"LIRA-8", MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND);
        after_dialog();
        return;
    }
    WCHAR nb[MAX_PATH];
    base_name(g_dlgfile, nb);
    /* auto-run the load handshake so Pd shows the new name */
    run_load_handshake(g_dlgfile, nb);
    after_dialog();
}

static void handle_quick_save(void)
{
    WCHAR src[MAX_PATH], dst[MAX_PATH + MAX_PATH];
    tmp_path(src, L"lira_current_save.lira");
    if (!file_exists(src)) {
        MessageBoxW(g_owner, L"LIRA-8: save FAILED (no capture file found). See C:\\tmp\\lira_helper.log",
                    L"LIRA-8", MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND);
        log_msg("quick save: lira_current_save.lira missing", 0);
        return;
    }
    _snwprintf(dst, MAX_PATH + MAX_PATH, L"%ls\\%ls.lira", g_presets, g_current);
    dst[MAX_PATH + MAX_PATH - 1] = 0;
    if (!put_copy(src, dst))
        MessageBoxW(g_owner, L"LIRA-8: saving the preset FAILED. See C:\\tmp\\lira_helper.log",
                    L"LIRA-8", MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND);
}

/* --- polling ----------------------------------------------------------- */
/* Atomic token consumption: open with DELETE_ON_CLOSE; only a successful
 * open (and therefore deletion) counts, so an action can never double-fire. */
static BOOL take_token(const WCHAR *name)
{
    WCHAR p[MAX_PATH];
    tmp_path(p, name);
    HANDLE h = CreateFileW(p, DELETE,
                           FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
                           NULL, OPEN_EXISTING, FILE_FLAG_DELETE_ON_CLOSE, NULL);
    if (h == INVALID_HANDLE_VALUE) return FALSE;
    CloseHandle(h);
    return TRUE;
}

static BOOL write_empty(const WCHAR *name)
{
    WCHAR p[MAX_PATH];
    tmp_path(p, name);
    return put_bytes(p, "", 0);
}

/* returns TRUE if a token was handled on the active g_tmp */
static BOOL poll_once(void)
{
    if (take_token(L"lira_new_req.token")) {
        g_current[0] = 0;
        return TRUE;
    }
    if (take_token(L"lira_prev_req.token")) {
        write_empty(L"lira_load_ready.token");
        step_preset(-1);
        return TRUE;
    }
    if (take_token(L"lira_next_req.token")) {
        write_empty(L"lira_load_ready.token");
        step_preset(1);
        return TRUE;
    }
    if (take_token(L"lira_load_req.token")) {
        WCHAR p[MAX_PATH];
        write_empty(L"lira_load_ready.token");
        tmp_path(p, L"lira_load_ready.lira");
        DeleteFileW(p);
        handle_load_dialog();
        return TRUE;
    }
    if (take_token(L"lira_saveas_req.token")) {
        write_empty(L"lira_load_ready.token");
        handle_saveas_dialog();
        return TRUE;
    }
    if (take_token(L"lira_save_req.token")) {
        if (g_current[0]) handle_quick_save();
        else              handle_saveas_dialog();
        return TRUE;
    }
    return FALSE;
}

int WINAPI wWinMain(HINSTANCE hInst, HINSTANCE hPrev, PWSTR cmd, int show)
{
    (void)hPrev; (void)cmd; (void)show;

    /* single instance (treat access-denied as "already running") */
    HANDLE m = CreateMutexW(NULL, TRUE, L"Local\\Lira8HelperMutex");
    DWORD me = GetLastError();
    if (me == ERROR_ALREADY_EXISTS || (m == NULL && me == ERROR_ACCESS_DENIED))
        return 0;

    /* hidden topmost owner window so dialogs come to the front */
    WNDCLASSW wc;
    ZeroMemory(&wc, sizeof(wc));
    wc.lpfnWndProc = DefWindowProcW;
    wc.hInstance = hInst;
    wc.lpszClassName = L"Lira8HelperOwner";
    RegisterClassW(&wc);
    g_owner = CreateWindowExW(WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
                              L"Lira8HelperOwner", L"LIRA-8", WS_POPUP,
                              0, 0, 0, 0, NULL, NULL, hInst, NULL);

    /* a \tmp dir on every fixed drive (Pd's "/tmp" is drive-relative) */
    DWORD mask = GetLogicalDrives();
    g_ndrives = 0;
    for (int i = 0; i < 26 && g_ndrives < 26; i++) {
        if (!(mask & (1u << i))) continue;
        WCHAR root[8];
        _snwprintf(root, 8, L"%lc:\\", (wint_t)(L'A' + i));
        root[7] = 0;
        if (GetDriveTypeW(root) != DRIVE_FIXED) continue;
        _snwprintf(g_drives[g_ndrives], 8, L"%lc:\\tmp", (wint_t)(L'A' + i));
        g_drives[g_ndrives][7] = 0;
        CreateDirectoryW(g_drives[g_ndrives], NULL);
        g_ndrives++;
    }
    if (g_ndrives == 0) { wcscpy(g_drives[0], L"C:\\tmp"); g_ndrives = 1; }

    /* %USERPROFILE%\Music\LIRA-8\Presets */
    WCHAR home[MAX_PATH] = L"";
    GetEnvironmentVariableW(L"USERPROFILE", home, MAX_PATH);
    WCHAR d[MAX_PATH];
    _snwprintf(d, MAX_PATH, L"%ls\\Music", home);          d[MAX_PATH-1]=0; CreateDirectoryW(d, NULL);
    _snwprintf(d, MAX_PATH, L"%ls\\Music\\LIRA-8", home);  d[MAX_PATH-1]=0; CreateDirectoryW(d, NULL);
    _snwprintf(g_presets, MAX_PATH, L"%ls\\Music\\LIRA-8\\Presets", home);
    g_presets[MAX_PATH - 1] = 0;
    CreateDirectoryW(g_presets, NULL);

    g_current[0] = 0;

    /* per-drive startup: clear stale tokens, arm ready/done flags, cap log */
    for (int i = 0; i < g_ndrives; i++) {
        wcscpy(g_tmp, g_drives[i]);
        WCHAR lp[MAX_PATH];
        tmp_path(lp, L"lira_helper.log");
        WIN32_FILE_ATTRIBUTE_DATA fa;
        if (GetFileAttributesExW(lp, GetFileExInfoStandard, &fa)
            && (fa.nFileSizeHigh || fa.nFileSizeLow > 1048576))
            DeleteFileW(lp);
        take_token(L"lira_load_req.token");
        take_token(L"lira_save_req.token");
        take_token(L"lira_saveas_req.token");
        take_token(L"lira_new_req.token");
        take_token(L"lira_prev_req.token");
        take_token(L"lira_next_req.token");
        write_empty(L"lira_load_ready.token");
        write_empty(L"lira_save_done.token");
    }
    wcscpy(g_tmp, g_drives[0]);
    SetCurrentDirectoryW(g_tmp);
    log_msg("[LIRA-8 Helper] watching (Save, Save As, Load, Prev, Next, New)", 0);

    for (;;) {
        for (int i = 0; i < g_ndrives; i++) {
            wcscpy(g_tmp, g_drives[i]);
            if (poll_once()) break;
        }
        Sleep(30);
    }
    return 0;
}
