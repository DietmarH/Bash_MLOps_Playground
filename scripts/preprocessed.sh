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

if [ $? -eq 0 ]; then
    # Get the current timestamp
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    # Log the successful request
    echo "$TIMESTAMP - INFO - Preprocessing complete! Processed data saved." >> "$LOG_FILE"
else
    # Get the current timestamp
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "$TIMESTAMP - ERROR - Error occurred during preprocessing" >> "$LOG_FILE"
fi
