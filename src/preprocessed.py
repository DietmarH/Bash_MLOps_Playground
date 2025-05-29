"""
-------------------------------------------------------------------------------
This script `preprocessed.py` retrieves data from the latest CSV file created 
in the 'data/raw/' directory.

1. It applies preprocessing to the data.
   
2. The results of the preprocessing are saved in a new CSV file 
   in the 'data/processed/' directory, with a name formatted as 
   'sales_processed_YYYYMMDD_HHMM.csv'.
   
3. All preprocessing steps are logged in the 
   'logs/preprocessed.logs' file to ensure detailed tracking of the process.

Any errors or anomalies are also logged to ensure traceability.
-------------------------------------------------------------------------------
"""

# Define the input and output files
INPUT_FILE = "data/raw/sales_data.csv"
OUTPUT_DIR = "data/processed/"
LOG_FILE = "logs/preprocessed.logs"

import pandas as pd
import logging
from datetime import datetime
from pathlib import Path 

# Ensure the output directory exist
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def preprocess_data():
    """
    Preprocess the data from the input file and save it to the output file.
    """ 

    # Configure logging
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)sZ - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )
    
    try: 
        input_file = INPUT_FILE
        
        logging.info(f"Starting preprocessing of data from {input_file}")
        # Load the data 
        data = pd.read_csv(input_file)
        logging.info(f"Data loaded successfully from {input_file}")
        
        # drop rows with missing values 
        data_cleaned = data.dropna()
        
        # Convert timestamp to numeric format
        df["time_seconds"] = pd.to_datetime(df["timestamp"]).astype(int) / 10**9  # Convert timestamp to seconds

        # Remove timestamp column if it exists
        df = df.drop("column_name", axis=1)

        # ----- Add more preprocessing steps here if needed -----

        logging.info("Missing values dropped.")

        # Save the processed data 
        output_file = OUTPUT_DIR + f"sales_processed_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        data_cleaned.to_csv(output_file, index=False)
        logging.info(f"Processed data saved to {output_file}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return -1
        
    return 0           


if __name__ == "__main__":
    preprocess_data()
