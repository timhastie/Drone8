
#import <Cocoa/Cocoa.h>

@interface LiraDialogController : NSObject
@property (nonatomic, strong) NSTimer *timer;
@property (nonatomic, assign) BOOL isBusy;
@property (nonatomic, copy) NSString *currentPresetName;
@end

@implementation LiraDialogController

- (instancetype)init {
    self = [super init];
    if (self) {
        _isBusy = NO;
        _currentPresetName = @"";
        NSFileManager *fm = [NSFileManager defaultManager];
        [fm removeItemAtPath:@"/tmp/lira_load_req.token" error:nil];
        [@"" writeToFile:@"/tmp/lira_load_ready.token" atomically:YES encoding:NSUTF8StringEncoding error:nil];
        [fm removeItemAtPath:@"/tmp/lira_save_req.token" error:nil];
        [fm removeItemAtPath:@"/tmp/lira_saveas_req.token" error:nil];
        [@"" writeToFile:@"/tmp/lira_save_done.token" atomically:YES encoding:NSUTF8StringEncoding error:nil];
        [fm removeItemAtPath:@"/tmp/lira_prev_req.token" error:nil];
        [fm removeItemAtPath:@"/tmp/lira_next_req.token" error:nil];
        [self startWatching];
    }
    return self;
}

- (void)startWatching {
    self.timer = [NSTimer scheduledTimerWithTimeInterval:0.03
                                                  target:self
                                                selector:@selector(pollTriggers)
                                                userInfo:nil
                                                 repeats:YES];
    [[NSRunLoop currentRunLoop] addTimer:self.timer forMode:NSRunLoopCommonModes];
    NSLog(@"[LIRA-8 Helper] Watching triggers (Save, Save As, Load, Prev, Next)...");
}

- (NSArray<NSString *> *)allPresetPathsSorted {
    NSString *presetDir = [@"~/Music/LIRA-8/Presets" stringByExpandingTildeInPath];
    NSFileManager *fm = [NSFileManager defaultManager];
    [fm createDirectoryAtPath:presetDir withIntermediateDirectories:YES attributes:nil error:nil];
    
    NSArray *files = [fm contentsOfDirectoryAtPath:presetDir error:nil];
    NSMutableArray *liraFiles = [NSMutableArray array];
    for (NSString *f in files) {
        if ([[f pathExtension] isEqualToString:@"lira"]) {
            [liraFiles addObject:[presetDir stringByAppendingPathComponent:f]];
        }
    }
    [liraFiles sortUsingSelector:@selector(localizedStandardCompare:)];
    return liraFiles;
}

- (void)stepPresetByOffset:(NSInteger)offset {
    NSArray<NSString *> *presets = [self allPresetPathsSorted];
    if ([presets count] == 0) return;
    
    NSInteger currentIndex = 0;
    for (NSInteger i = 0; i < [presets count]; i++) {
        NSString *base = [[[presets[i] lastPathComponent] stringByDeletingPathExtension] lowercaseString];
        if ([base isEqualToString:[self.currentPresetName lowercaseString]]) {
            currentIndex = i;
            break;
        }
    }
    
    NSInteger nextIndex = (currentIndex + offset) % (NSInteger)[presets count];
    if (nextIndex < 0) nextIndex += [presets count];
    
    NSString *targetPath = presets[nextIndex];
    NSString *baseName = [[targetPath lastPathComponent] stringByDeletingPathExtension];
    self.currentPresetName = baseName;
    
    NSString *content = [NSString stringWithContentsOfFile:targetPath encoding:NSUTF8StringEncoding error:nil];
    if (content) {
        NSString *readyLira = @"/tmp/lira_load_ready.lira";
        [content writeToFile:readyLira atomically:YES encoding:NSUTF8StringEncoding error:nil];
        
        NSString *nameTarget = @"/tmp/lira_preset_name.txt";
        NSString *nameContent = [NSString stringWithFormat:@"%@;\n", baseName];
        [nameContent writeToFile:nameTarget atomically:YES encoding:NSUTF8StringEncoding error:nil];
        
        NSString *readyFlag = @"/tmp/lira_load_ready.token";
        [@"ready 1;\n" writeToFile:readyFlag atomically:YES encoding:NSUTF8StringEncoding error:nil];
        NSLog(@"[LIRA-8 Helper] Stepped to preset [%ld/%lu]: %@", (long)nextIndex + 1, (unsigned long)[presets count], baseName);
    }
}

- (void)pollTriggers {
    if (self.isBusy) return;

    NSFileManager *fm = [NSFileManager defaultManager];
    
    NSString *prevReq = @"/tmp/lira_prev_req.token";
    if ([fm fileExistsAtPath:prevReq]) {
        [fm removeItemAtPath:prevReq error:nil];
        [@"" writeToFile:@"/tmp/lira_load_ready.token" atomically:YES encoding:NSUTF8StringEncoding error:nil];
        [self stepPresetByOffset:-1];
        return;
    }

    NSString *nextReq = @"/tmp/lira_next_req.token";
    if ([fm fileExistsAtPath:nextReq]) {
        [fm removeItemAtPath:nextReq error:nil];
        [@"" writeToFile:@"/tmp/lira_load_ready.token" atomically:YES encoding:NSUTF8StringEncoding error:nil];
        [self stepPresetByOffset:1];
        return;
    }

    NSString *loadReq = @"/tmp/lira_load_req.token";
    if ([fm fileExistsAtPath:loadReq]) {
        [fm removeItemAtPath:loadReq error:nil];
        [@"" writeToFile:@"/tmp/lira_load_ready.token" atomically:YES encoding:NSUTF8StringEncoding error:nil];
        [fm removeItemAtPath:@"/tmp/lira_load_ready.lira" error:nil];
        self.isBusy = YES;
        dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
            [self handleLoadDialog];
        });
        return;
    }

    NSString *saveAsReq = @"/tmp/lira_saveas_req.token";
    if ([fm fileExistsAtPath:saveAsReq]) {
        [fm removeItemAtPath:saveAsReq error:nil];
        [@"" writeToFile:@"/tmp/lira_load_ready.token" atomically:YES encoding:NSUTF8StringEncoding error:nil];
        self.isBusy = YES;
        dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
            [self handleSaveAsDialog];
        });
        return;
    }

    NSString *saveReq = @"/tmp/lira_save_req.token";
    if ([fm fileExistsAtPath:saveReq]) {
        [fm removeItemAtPath:saveReq error:nil];
        if ([self.currentPresetName length] > 0) {
            // Overwrite existing preset file directly
            [self handleQuickOverwriteSave];
        } else {
            // No current name -> prompt Save As dialog
            self.isBusy = YES;
            dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
                [self handleSaveAsDialog];
            });
        }
        return;
    }
}

- (void)handleQuickOverwriteSave {
    NSString *presetDir = [@"~/Music/LIRA-8/Presets" stringByExpandingTildeInPath];
    NSString *filePath = [presetDir stringByAppendingPathComponent:[NSString stringWithFormat:@"%@.lira", self.currentPresetName]];
    NSString *srcTemp = @"/tmp/lira_current_save.lira";
    NSString *content = [NSString stringWithContentsOfFile:srcTemp encoding:NSUTF8StringEncoding error:nil];
    if (content) {
        [content writeToFile:filePath atomically:YES encoding:NSUTF8StringEncoding error:nil];
        NSLog(@"[LIRA-8 Helper] Overwrote existing preset: %@", filePath);
    }
}

- (void)handleLoadDialog {
    NSString *presetDir = [@"~/Music/LIRA-8/Presets" stringByExpandingTildeInPath];
    [[NSFileManager defaultManager] createDirectoryAtPath:presetDir withIntermediateDirectories:YES attributes:nil error:nil];
    
    NSString *scriptSource = [NSString stringWithFormat:
        @"set presetDir to (POSIX file \"%@\")\n"
        @"try\n"
        @"    tell application \"System Events\"\n"
        @"        set frontApp to name of first application process whose frontmost is true\n"
        @"    end tell\n"
        @"    tell application frontApp\n"
        @"        set chosenFile to choose file with prompt \"Select a LIRA-8 Preset (.lira):\" default location presetDir\n"
        @"    end tell\n"
        @"    return POSIX path of chosenFile\n"
        @"on error errStr number errNum\n"
        @"    if errNum is -128 then\n"
        @"        return \"CANCELLED\"\n"
        @"    else\n"
        @"        return \"ERROR:\" & errStr\n"
        @"    end if\n"
        @"end try\n", presetDir];
        
    NSAppleScript *appleScript = [[NSAppleScript alloc] initWithSource:scriptSource];
    NSDictionary *errorDict = nil;
    NSAppleEventDescriptor *descriptor = [appleScript executeAndReturnError:&errorDict];
    
    NSString *resultPath = [descriptor stringValue];
    NSLog(@"[LIRA-8 Helper] Load result: %@", resultPath);
    
    if (resultPath && ![resultPath isEqualToString:@"CANCELLED"] && ![resultPath hasPrefix:@"ERROR:"] && [resultPath length] > 0) {
        NSURL *url = [NSURL fileURLWithPath:resultPath];
        NSString *baseName = [[url lastPathComponent] stringByDeletingPathExtension];
        NSString *content = [NSString stringWithContentsOfFile:resultPath encoding:NSUTF8StringEncoding error:nil];
        
        if (content) {
            self.currentPresetName = baseName;
            NSString *targetPath = @"/tmp/lira_load_ready.lira";
            [content writeToFile:targetPath atomically:YES encoding:NSUTF8StringEncoding error:nil];
            
            NSString *nameTarget = @"/tmp/lira_preset_name.txt";
            NSString *nameContent = [NSString stringWithFormat:@"%@;\n", baseName];
            [nameContent writeToFile:nameTarget atomically:YES encoding:NSUTF8StringEncoding error:nil];
            
            NSString *readyFlag = @"/tmp/lira_load_ready.token";
            [@"ready 1;\n" writeToFile:readyFlag atomically:YES encoding:NSUTF8StringEncoding error:nil];
            NSLog(@"[LIRA-8 Helper] Loaded preset %@ successfully.", baseName);
        }
    }
    self.isBusy = NO;
}

- (void)handleSaveAsDialog {
    NSString *presetDir = [@"~/Music/LIRA-8/Presets" stringByExpandingTildeInPath];
    [[NSFileManager defaultManager] createDirectoryAtPath:presetDir withIntermediateDirectories:YES attributes:nil error:nil];
    
    NSString *defaultName = [self.currentPresetName length] > 0 ? [NSString stringWithFormat:@"%@.lira", self.currentPresetName] : @"MyPreset.lira";
    
    NSString *scriptSource = [NSString stringWithFormat:
        @"set presetDir to (POSIX file \"%@\")\n"
        @"try\n"
        @"    tell application \"System Events\"\n"
        @"        set frontApp to name of first application process whose frontmost is true\n"
        @"    end tell\n"
        @"    tell application frontApp\n"
        @"        set chosenFile to choose file name with prompt \"Save LIRA-8 Preset As:\" default name \"%@\" default location presetDir\n"
        @"    end tell\n"
        @"    return POSIX path of (chosenFile as text)\n"
        @"on error errStr number errNum\n"
        @"    if errNum is -128 then\n"
        @"        return \"CANCELLED\"\n"
        @"    else\n"
        @"        return \"ERROR:\" & errStr\n"
        @"    end if\n"
        @"end try\n", presetDir, defaultName];
        
    NSAppleScript *appleScript = [[NSAppleScript alloc] initWithSource:scriptSource];
    NSDictionary *errorDict = nil;
    NSAppleEventDescriptor *descriptor = [appleScript executeAndReturnError:&errorDict];
    
    NSString *resultPath = [descriptor stringValue];
    NSLog(@"[LIRA-8 Helper] Save As result: %@", resultPath);
    
    if (resultPath && ![resultPath isEqualToString:@"CANCELLED"] && ![resultPath hasPrefix:@"ERROR:"] && [resultPath length] > 0) {
        if (![resultPath hasSuffix:@".lira"]) {
            resultPath = [resultPath stringByAppendingString:@".lira"];
        }
        NSURL *url = [NSURL fileURLWithPath:resultPath];
        NSString *baseName = [[url lastPathComponent] stringByDeletingPathExtension];
        
        NSString *srcTemp = @"/tmp/lira_current_save.lira";
        NSString *content = [NSString stringWithContentsOfFile:srcTemp encoding:NSUTF8StringEncoding error:nil];
        if (content) {
            self.currentPresetName = baseName;
            [content writeToFile:resultPath atomically:YES encoding:NSUTF8StringEncoding error:nil];
            
            // Automatically execute the load handshake so Pure Data displays the new name!
            NSString *targetPath = @"/tmp/lira_load_ready.lira";
            [content writeToFile:targetPath atomically:YES encoding:NSUTF8StringEncoding error:nil];
            
            NSString *nameTarget = @"/tmp/lira_preset_name.txt";
            NSString *nameContent = [NSString stringWithFormat:@"%@;\n", baseName];
            [nameContent writeToFile:nameTarget atomically:YES encoding:NSUTF8StringEncoding error:nil];
            
            NSString *readyFlag = @"/tmp/lira_load_ready.token";
            [@"ready 1;\n" writeToFile:readyFlag atomically:YES encoding:NSUTF8StringEncoding error:nil];
            NSLog(@"[LIRA-8 Helper] Saved As & Loaded preset %@ successfully to %@", baseName, resultPath);
        }
    }
    self.isBusy = NO;
}

@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        [NSApplication sharedApplication];
        [NSApp setActivationPolicy:NSApplicationActivationPolicyAccessory];
        
        LiraDialogController *controller = [[LiraDialogController alloc] init];
        (void)controller;
        
        [NSApp run];
    }
    return 0;
}
