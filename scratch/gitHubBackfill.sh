#!/usr/bin/env bash

set -euo pipefail

GITHUB_USER="surajm20061998"
TARGET_FILE="scratch/tmp"

MESSAGES=(
    "Practicing"
    "Interview Prep"
    "Interview Practice"
    "More Questions"
    "ScratchWork"
)

# Verify we're inside a git repository
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
    echo "Error: Run this script inside a Git repository."
    exit 1
}

# Verify GitHub remote
REMOTE_URL="$(git remote get-url origin 2>/dev/null || true)"

if [[ "$REMOTE_URL" != *"$GITHUB_USER"* ]]; then
    echo "Error: origin does not appear to belong to $GITHUB_USER"
    echo "Current origin: $REMOTE_URL"
    exit 1
fi

mkdir -p "$(dirname "$TARGET_FILE")"
touch "$TARGET_FILE"

# Start date: March 1st of current year (or specify year)
YEAR=$(date +%Y)
START_DATE="$YEAR-03-01"
END_DATE="$YEAR-09-01"

# Convert dates to seconds since epoch for comparison
START_EPOCH=$(date -d "$START_DATE" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$START_DATE" +%s)
END_EPOCH=$(date -d "$END_DATE" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$END_DATE" +%s)

CURRENT_DATE="$START_DATE"
CURRENT_EPOCH="$START_EPOCH"

while [ "$CURRENT_EPOCH" -le "$END_EPOCH" ]; do
    # Randomly add 400-800 lines
    NUM_LINES=$((1400 + RANDOM % 401))
    
    {
        echo ""
        echo "# Scratch work for $CURRENT_DATE"
        for ((i=1; i<=NUM_LINES; i++)); do
            echo "scratch_${RANDOM}_${i} = $((RANDOM % 10000))"
        done
    } >> "$TARGET_FILE"
    
    # Random commit message
    MESSAGE="${MESSAGES[$((RANDOM % ${#MESSAGES[@]}))]}"
    
    # Generate random time (between 8 AM and 11 PM for realism)
    HOUR=$((8 + RANDOM % 16))  # 8 to 23
    MINUTE=$((RANDOM % 60))
    SECOND=$((RANDOM % 60))
    
    # Format time with leading zeros
    TIME=$(printf "%02d:%02d:%02d" $HOUR $MINUTE $SECOND)
    
    # Full datetime for commit
    COMMIT_DATETIME="$CURRENT_DATE $TIME"
    
    git add "$TARGET_FILE"
    
    # Commit with specific random date and time
    GIT_COMMITTER_DATE="$COMMIT_DATETIME" git commit --date="$COMMIT_DATETIME" -m "$MESSAGE - $CURRENT_DATE"
    
    echo "Committed for: $CURRENT_DATE at $TIME"
    
    # Move to next day
    CURRENT_EPOCH=$((CURRENT_EPOCH + 86400))  # Add 24 hours in seconds
    CURRENT_DATE=$(date -d "@$CURRENT_EPOCH" +%Y-%m-%d 2>/dev/null || date -j -f "%s" "$CURRENT_EPOCH" +%Y-%m-%d)
done

# Push all commits at once
git push origin HEAD

echo "Done."
echo "Committed for all dates from $START_DATE to $END_DATE"