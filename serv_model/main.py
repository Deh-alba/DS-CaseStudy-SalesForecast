from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import logging
import pickle

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler to write logs to a file
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Initialize FastAPI app
app = FastAPI(title="Request Model API", version="1.0.0")

# Load your trained model (ensure the path is correct)
with open("models/xgb_model.pkl", "rb") as f:
    model = pickle.load(f)

# Define the request schema
class DataFrameInput(BaseModel):
    data: list  # List of rows (each row is a list of values)
    columns: list  # List of column names



@app.post("/predict")
async def predict(input_data: DataFrameInput):
    print("input_data", input_data)


    try:
        # Convert input data to a DataFrame
        df = pd.DataFrame(data=input_data.data, columns=input_data.columns)
        
        # Log the received DataFrame
        logger.info(f"Received DataFrame: {df.head()}")

        # Define the features expected by the model
        model_features = [
            "month", "sell_price", "day_of_week", "is_weekend", "is_holiday",
            "lag_7", "lag_14", "lag_28", "rolling_mean_7", "rolling_mean_14",
            "rolling_mean_28", "price_change"
        ]

        # Ensure the input DataFrame contains the required features
        if not set(model_features).issubset(df.columns):
            missing_features = set(model_features) - set(df.columns)
            raise ValueError(f"Missing required features: {missing_features}")

        # Filter the DataFrame to include only the model features
        df_model_input = df[model_features]

        # Encode categorical columns (if any) into numeric values
        for col in df_model_input.select_dtypes(include=['object']).columns:
            df_model_input[col] = df_model_input[col].astype('category').cat.codes

        # Make predictions
        predictions = model.predict(df_model_input)

        # Add predictions to the original DataFrame
        df["predictions"] = predictions

        # Return only the relevant columns in the response
        response_columns = ["item_id", "date", "d", "predictions"]
        return df[response_columns].to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during prediction.")