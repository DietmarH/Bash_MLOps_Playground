#!/bin/bash

# =============================================================================
# This script preprocessed.sh runs the program src/preprocessed.py
# and logs the execution details in the log file
# logs/preprocessed.logs.
# =============================================================================

# Log file path
LOG_FILE="logs/preprocessed.logs"

# Run preprocessing Python script
python3 src/preprocessed.py

# Get the current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ $? -eq 0 ]; then
    # Log the successful request
    echo "$TIMESTAMP - INFO - Preprocessing complete! Processed data saved." >> "$LOG_FILE"
else
    echo "$TIMESTAMP - ERROR - Error occurred during preprocessing" >> "$LOG_FILE"
fi
