#!/bin/bash

# ==============================================================================
# Script: collect.sh
# Description:
#   This script queries an API every minute for 3 minutes to retrieve sales data
#   for the following graphics card models:
#     - rtx3060
#     - rtx3070
#     - rtx3080
#     - rtx3090
#     - rx6700
#
#   The collected data is appended to a copy of the file:
#     data/raw/sales_data.csv
#
#   The output file is saved in the format:
#     data/raw/sales_YYYYMMDD_HHMM.csv
#   with the following columns:
#     timestamp, model, sales
#
#   Collection activity (requests, queried models, results, errors)
#   is recorded in a log file:
#     logs/collect.logs
#
#   The log should be human-readable and must include:
#     - The date and time of each request
#     - The queried models
#     - The retrieved sales data
#     - Any possible errors
# ==============================================================================

# URL of the API endpoint
URL_BASE="http://0.0.0.0:5000/"
# Graphic card models to query
GRAPHIC_CARD_MODELS=("rtx3060" "rtx3070" "rtx3080" "rtx3090" "rx6700")
# Output file path
OUTPUT_FILE="data/raw/sales_data.csv"
# Log file path
LOG_FILE="logs/collect.logs"

# Write the header if the file does not exist yet
if [ ! -f "$OUTPUT_FILE" ]; then
    # data columns
    DATA_HEADER="timestamp,model,sales"
    # Write the header to the output file
    echo "$DATA_HEADER" > "$OUTPUT_FILE"
fi 

# Iterate over all graphic card models 
for model in "${GRAPHIC_CARD_MODELS[@]}"; do
    # Get the current timestamp
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    # API request to retrieve sales data
    SALES=$(curl -s "$URL_BASE/$model")

    # Check for errors
    if [ -z "$SALES" ]; then
        ERROR_MSG="Error retrieving data for model: $model"
        echo "$TIMESTAMP - $ERROR_MSG" >> "$LOG_FILE"
    else
        # Append the data to the output file
        echo "$TIMESTAMP,$model,$SALES" >> "$OUTPUT_FILE"
        # Log the successful request
        echo "$TIMESTAMP - Queried model: $model - Sales: $SALES" >> "$LOG_FILE"
    fi
done
