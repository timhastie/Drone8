#!/bin/bash
# Gets the current Ableton project name from the window title,
# creates the project directory, and outputs the sanitized name.

BASE="/Users/timothyhastie/Downloads/LIRA-8-master/LIRA-8_PlugData/projects"

# Query Ableton's front window title via AppleScript
name=$(osascript -e '
tell application "System Events"
    try
        set winName to name of front window of (first application process whose name is "Live")
        return winName
    on error
        return "default"
    end try
end tell' 2>/dev/null)

# Strip " - Ableton Live..." suffix to get just the project name
name=$(echo "$name" | sed 's/ - Ableton Live.*//')

# Sanitize: keep only alphanumeric, underscore, hyphen (no spaces/special chars)
name=$(echo "$name" | tr -cd 'a-zA-Z0-9_-')

# Fallback if empty
if [ -z "$name" ]; then
    name="default"
fi

# Create project directory (safe even if already exists)
mkdir -p "$BASE/$name"

# Output just the project name (no newline, no spaces = single PD symbol)
printf "%s" "$name"
