# diabetes-cassandra-bigdatamodel
## ELT Workflow

This project implements a three-layer Medallion architecture following the ELT paradigm:

**1. Bronze Layer (Raw Data Ingestion):**
   - Raw data (100,000+ medical patient records with 17 columns) was ingested into Apache Cassandra.
   - The `bronze_level` table stores the data in its original format, preserving all columns including categorical, numerical, discrete, and continuous features such as year, gender, age, location, race encodings, hypertension, heart disease, smoking history, BMI, HbA1c level, blood glucose, diabetes status, and clinical notes.
   - The `src/bronze.py` script handles the connection to Cassandra and the insertion of the raw data.
   - CQL scripts in `src/cql_scripts/bronze_scripts.cql` define the `bronze_level` table schema.

**2. Silver Layer (Data Cleaning):**
   - Data cleaning and basic transformations were performed using Python scripts (`src/silver.py` and utility functions in `src/utils.py`).
   - This involved standardizing categorical features (e.g., gender, location, smoking history) and converting them into numerical representations suitable for analysis and machine learning.
   - The cleaned data was loaded into the `silver_level` table in Cassandra, providing a consistent and processed dataset for further analysis.
   - CQL scripts in `src/cql_scripts/silver_scripts.cql` define the `silver_level` table schema.

**3. Gold Layer (Aggregation and Analysis):**
   - Aggregated datasets were created in Cassandra to facilitate higher-level insights.
   - `gold_diabetes_by_race_condition` table: Aggregated diabetes prevalence based on patient race and co-occurring conditions (hypertension, heart disease). The aggregation logic is implemented in `src/gold/diabetes_by_race_healthcondition.py`, and the table schema is defined in `src/cql_scripts/gold_scripts.cql`.
   - `gold_diabetes_by_location` table: Aggregated diabetes prevalence by US state. The aggregation logic is in `src/gold/diabetes_by_location.py`, and the table schema is in `src/cql_scripts/gold_scripts.cql`.

## Visualizations

The project includes three distinct visualizations generated using Matplotlib and Seaborn, with data queried from the Cassandra database:

1.  **Prevalence of Diabetes by Race and Co-occurring Conditions (Bar Chart):** Visualizes the proportion of patients with diabetes within each race category, further segmented by the presence of hypertension and/or heart disease. The data is queried from the `gold_diabetes_by_race_condition` table, and the visualization script is `src/visualizations/visualize_diabetes_by_race_healthcondition.py`.

2.  **Prevalence of Diabetes by US State (Choropleth Map):** Displays the geographic distribution of diabetes prevalence across the United States, using state-level data aggregated in the `gold_diabetes_by_location` table and a US states shapefile. The visualization script is `src/visualizations/visualize_diabetes_by_location.py`.

3.  **Comparison of Precision, Recall, and F1-Score for ML Models (Bar Chart):** Compares the performance metrics (precision, recall, and F1-score for the diabetes-positive class) of three different machine learning models (Random Forest, K-Nearest Neighbors, and Gaussian Naive Bayes) trained on the diabetes dataset. The visualization script is `src/visualizations/compare_models.py`.

## Machine Learning Model

A Random Forest Classifier was built to predict the presence of diabetes based on various patient features. The model was trained and evaluated using the cleaned data from the `silver_level` table.

- The `src/ml.py` script handles data splitting, model training, prediction, and evaluation using metrics such as accuracy, precision, recall, F1-score, and a confusion matrix.
- Feature importance was also analyzed to understand which factors were most influential in the model's predictions.
- Parameter tuning using GridSearchCV was performed to optimize the model's performance, with a focus on balancing precision and recall for the diabetes-positive class.

## Technologies Used

* **Apache Cassandra:** Distributed NoSQL database for storing and retrieving data.
* **Python:** Programming language used for data processing, analysis, and visualization.
* **Pandas:** Library for data manipulation and analysis.
* **Cassandra Driver for Python:** To connect and interact with the Cassandra database.
* **Matplotlib:** Library for creating static, interactive, and animated visualizations in Python.
* **Seaborn:** Library for making statistical graphics in Python.
* **GeoPandas:** Library for working with geospatial data (used for the choropleth map).
* **Scikit-learn:** Library for machine learning algorithms and evaluation metrics.
* **Poetry:** Dependency management and packaging tool for Python.

## Setup and Installation

1.  **Install Dependencies:**
    ```bash
    poetry install
    ```
2.  **Configure Cassandra Connection:** Ensure your Cassandra cluster is running and update the connection details (IP address, username, password) in your `src/config.py` file. Place your secure connect bundle (if applicable) in the `config/` directory.
3.  **Download Shapefile:** Download the "Admin 1 - States, Provinces" shapefile from [Natural Earth Data](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/) and extract the `ne_110m_admin_1_states_provinces` folder into the `data/` directory.
4.  **Run Scripts:** Execute the Python scripts in the `src/` and `src/visualizations/` directories to perform the ELT process, generate visualizations, and train the machine learning model.

## Potential Improvements

* Implement distributed data processing using Apache Spark with the Cassandra connector for larger datasets.
* Explore more advanced machine learning models and hyperparameter tuning techniques.
* Develop an interactive dashboard using tools like Flask or Dash to present the findings.
* Perform more in-depth feature engineering to potentially improve the predictive power of the machine learning model.

This project provides a solid foundation for analyzing medical data using a big data application and demonstrates a structured approach to the ELT workflow, data visualization, and machine learning.
