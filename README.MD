# Project Structure

This project follows the structure below:

1. **challenge_document.pdf** – Contains a description of the project, details, results, and summary.
2. **docker-compose/** – Includes the setup to run the API with the model.
3. **notebooks/** – A folder containing all notebooks, including EDA (exploratory data analysis), model training, and prediction generation.
4. **notebooks/model/** – Stores the saved model.
5. **notebooks/data/** – Contains the file `forecast_results.parquet` with the forecast results.

## Notes
- To read the Parquet file, use **pandas**.
- If you need to rerun the notebooks, use the data creation script from the challenge to download the dataset.  
  We are not including the data here due to its size.
