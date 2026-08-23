import sys, re

def parse(path):
    txt=open(path, encoding='utf-8', errors='replace').read()
    parts=re.split(r'(?<!\\);', txt)
    stack=[]; canvases=[]
    for p in parts:
        s=' '.join(p.split())
        if not s: continue
        t=s.split()
        if t[0]=='#N' and len(t)>1 and t[1]=='canvas':
            cv={'name':t[6] if len(t)>6 else '?','objs':[],'conns':[]}
            stack.append(cv); canvases.append(cv); continue
        if not stack: continue
        cv=stack[-1]
        if t[0]!='#X': continue     # PD skips unparseable records
        k=t[1] if len(t)>1 else ''
        if k=='restore':
            d=stack.pop()
            if stack: stack[-1]['objs'].append('SUBPATCH['+d['name']+'] '+s)
            continue
        if k=='connect':
            try: cv['conns'].append(tuple(int(x) for x in t[2:6]))
            except ValueError: pass
        elif k in ('obj','msg','floatatom','symbolatom','text','listbox','graph'):
            cv['objs'].append(s)
    return canvases

cvs=parse(sys.argv[1])
for cv in cvs:
    bad=[c for c in cv['conns'] if c[0]>=len(cv['objs']) or c[2]>=len(cv['objs'])]
    if bad: print(f"OUT-OF-RANGE '{cv['name']}' ({len(cv['objs'])} objs): {bad}")
main=cvs[0]
print(f"main '{main['name']}': {len(main['objs'])} objs, {len(main['conns'])} connects")
if len(sys.argv)>2:
    pat=sys.argv[2]
    for i,o in enumerate(main['objs']):
        if re.search(pat,o): print(i, o[:120])
    print("--- connects touching those ---")
    idx={i for i,o in enumerate(main['objs']) if re.search(pat,o)}
    for c in main['conns']:
        if c[0] in idx or c[2] in idx:
            print(f"  {c[0]}:{c[1]} -> {c[2]}:{c[3]}   [{main['objs'][c[0]][:55]}] -> [{main['objs'][c[2]][:55]}]")
