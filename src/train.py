"""
-------------------------------------------------------------------------------
This script runs the training of an XGBoost model to predict graphics card sales 
from the preprocessed data.

1. It starts by searching for the latest preprocessed CSV file in the 'data/processed/' directory.
2. If a standard model (model.pkl) does not exist, it loads the data, splits it into training and test sets, trains a model on this data, evaluates it, and then saves it as 'model/model.pkl'.
3. If a standard model already exists, it trains a new model on the latest data, evaluates it, and saves the model in the 'model/' folder in the format: model_YYYYMMDD_HHMM.pkl.
4. Performance metrics (RMSE, MAE, R²) are displayed and saved in the log file.
5. Any errors are handled and reported in the logs.

The models are saved in the 'model/' folder with the name 'model.pkl' for the standard model and with a timestamp for later versions.
The model metrics are recorded in the script’s log files.
-------------------------------------------------------------------------------
"""

import pandas as pd
import xgboost as xgb
import os
import logging
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Define the input and output files
INPUT_DIR = "data/processed"
MODEL_DIR = "model"
LOG_FILE = "logs/train.logs"

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)sZ - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)

def train_model():
    try:
        # Get the list of input files
        input_files = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.endswith(".csv")]
        if not input_files:
            logging.error("No CSV files found in the processed data directory.")
            return -1

        # Get the most recent file
        input_file = max(input_files, key=os.path.getmtime)
        logging.info(f"Starting model training using {input_file}")

        # Load data
        df = pd.read_csv(input_file)

        # Ensure necessary columns exist
        if "timestamp" not in df.columns or "sales" not in df.columns:
            logging.error("Required columns missing from dataset!")
            return -1

        # Convert timestamp to numeric format
        df["timestamp"] = pd.to_datetime(df["timestamp"]).astype(int) / 10**9  # Convert timestamp to seconds
        X = df[["timestamp"]]  # Using timestamp as feature
        y = df["sales"]

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define paths for model saving
        model_dir = MODEL_DIR
        os.makedirs(model_dir, exist_ok=True)

        standard_model_path = os.path.join(model_dir, "model.pkl")

        # Check for an existing standard model
        if os.path.exists(standard_model_path):
            logging.info("Existing standard model detected. Load the model.")
            model = joblib.load(standard_model_path)
        else:
            logging.info("Create a new standard model.")
            model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100)

        # Train the model
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        logging.info(f"Model evaluation metrics - RMSE: {rmse}, MAE: {mae}, R²: {r2}")

        if os.path.exists(standard_model_path):
            model_file = f"model/sales_model_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.pkl"
        else:
            # Save the model as the standard model
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            model_file = standard_model_path

        logging.info(f"Saving the standard model to {model_file}")
        joblib.dump(model, model_file)
    except Exception as e:
        logging.error(f"An error occurred during model training: {e}")
        return -1
    
    return 0

if __name__ == "__main__":
    train_model()
