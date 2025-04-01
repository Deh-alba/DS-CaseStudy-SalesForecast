from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import logging
import pickle

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
    try:
        # Convert input data to a DataFrame
        df = pd.DataFrame(data=input_data.data, columns=input_data.columns)
        
        # Log the received DataFrame
        logger.info(f"Received DataFrame: {df.head()}")

        # Make predictions
        predictions = model.predict(df)

        # Add predictions to the DataFrame
        df["predictions"] = predictions

        # Return the DataFrame as a list of dictionaries
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during prediction.")