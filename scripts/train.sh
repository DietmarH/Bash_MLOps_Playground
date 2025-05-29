#!/bin/bash

# -----------------------------------------------------------------------------
# This script train.sh runs the Python program src/train.py.
# This program trains a prediction model and saves the final model
# in the model/ directory. The script also logs all execution details
# in the file logs/train.logs.
# -----------------------------------------------------------------------------

LOG_FILE="logs/train.logs"

# Get the current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "$TIMESTAMP - INFO - Model Training started." >> "$LOG_FILE"

# Run Python script for training and log outputs
python3 src/train.py

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
if [ $? -eq 0 ]; then
    echo "$TIMESTAMP - INFO - Training completed successfully." >> "$LOG_FILE"
else
    echo "$TIMESTAMP - ERROR - Training failed with return code $?" >> "$LOG_FILE"
fi
