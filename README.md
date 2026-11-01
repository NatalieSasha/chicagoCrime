# Crime Data Analysis and Visualization Using Python

## 1. Abstract

This academic project presents a reusable Python workflow for cleaning, exploring, visualizing, and interactively filtering recorded crime incident data. It demonstrates data preprocessing, exploratory data analysis (EDA), statistical summaries, and interactive visualization through a Streamlit dashboard.

The project supports optional dataset fields and adapts its analyses to the available data. It emphasizes descriptive analysis rather than crime prediction or enforcement decisions.

## 2. Problem Statement and Objectives

Crime records can reveal patterns across time, crime categories, and geographical areas. However, data quality, reporting practices, and coverage limitations can affect the interpretation of these patterns.

The primary objective of this project is to develop an interactive analytical system that demonstrates how Python can be used to process crime data and extract meaningful descriptive insights.

### Objectives

- Load crime datasets from CSV files.
- Clean and preprocess data by handling missing values, duplicates, and inconsistent formats.
- Perform exploratory data analysis using Pandas and NumPy.
- Generate statistical summaries of recorded incidents.
- Visualize crime distributions and temporal patterns.
- Analyze crime categories and geographical areas.
- Develop an interactive dashboard using Streamlit and Plotly.
- Provide filtering, dataset exploration, and CSV export functionality.
- Document data quality issues and analytical limitations.

## 3. Tools and Technologies

The project uses the following technologies:

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core programming language |
| Pandas | Data manipulation and preprocessing |
| NumPy | Numerical computations |
| Matplotlib | Static data visualization |
| Seaborn | Statistical visualization |
| Plotly | Interactive charts and geographical visualization |
| Streamlit | Interactive dashboard development |
| Jupyter Notebook | Exploratory data analysis |
| Pytest | Automated testing |

## 4. Dataset, Source, and Attribution

### 4.1 Dataset Description

The default dataset is a public-data snapshot obtained from the City of Chicago Data Portal's **Crimes — 2001 to Present** dataset.

- **Source:** City of Chicago Data Portal
- **Dataset ID:** `ijzp-q8t2`
- **Snapshot retrieval date:** November 1, 2026
- **Date range:** January 1, 2026, to October 24, 2026
- **Number of records:** 189,983 reported incidents

The snapshot contains selected fields relevant to crime analysis, including:

- Date
- Primary crime type
- Description
- Location description
- Police district
- Community area
- Latitude
- Longitude

An earlier full-year 2024 snapshot is retained for reference. A synthetic sample dataset, `data/sample_crime_data.csv`, is also available as a fallback for demonstrations.

### 4.2 Data Source and Attribution

The original dataset is available through the City of Chicago Data Portal.

The project's `data/README.md` documents the source, API query, attribution requirements, applicable terms, and dataset limitations.

The application loads the bundled local snapshot by default and does not require a live API connection during normal execution.

**Note:** The dataset contains reported incidents and may include preliminary or subsequently revised records. Its counts should not be interpreted as a complete measure of underlying crime prevalence.

## 5. Data Preprocessing Methodology

Data preprocessing is performed to improve consistency and reliability while preserving information needed for analysis.

The preprocessing workflow includes:

1. **Column standardization:** Headers are standardized, and common column aliases are mapped to canonical field names.
2. **Date conversion:** Date fields are converted to datetime format, with invalid values represented as missing.
3. **Category cleaning:** Crime categories and geographical labels are trimmed to remove unnecessary whitespace.
4. **Coordinate validation:** Latitude and longitude values are converted to numeric types and checked against valid geographical ranges.
5. **Duplicate detection:** Exact duplicate rows are removed while potentially legitimate repeated incidents are retained.
6. **Missing-value analysis:** Missing values are identified and reported rather than automatically removing every affected record.
7. **Preprocessing reports:** The original and cleaned datasets are compared using record counts and data quality summaries.

The original source data is preserved separately from the processed data. The preprocessing report provides information about the changes made during cleaning.

## 6. Exploratory Data Analysis (EDA)

Exploratory data analysis is used to understand the dataset's structure, identify patterns, and assess data quality.

The project supports the following analyses, depending on the fields available:

### 6.1 Dataset Overview

- Number of records and columns.
- Available crime categories.
- Number of geographical areas.
- Date range covered by the dataset.
- Missing values and duplicate records.
- Descriptive statistics for numerical columns.

### 6.2 Crime Category Analysis

- Frequency of each crime category.
- Percentage contribution of each category.
- Identification of the most frequently recorded crime types.
- Comparison of category distributions.

### 6.3 Temporal Analysis

- Incident counts over time.
- Monthly and yearly trends.
- Crime distribution by weekday.
- Hourly patterns when valid timestamps are available.

### 6.4 Geographical Analysis

- Incident counts by police district or community area.
- Comparison of recorded incidents across geographical areas.
- Visualization of valid geographical coordinates.
- Identification of areas with higher recorded incident counts.

### 6.5 Statistical Analysis

- Descriptive statistics.
- Numerical summaries.
- Correlation analysis where suitable numerical variables exist.

All analyses are conditional on the availability of the required fields. Correlations are descriptive and do not establish causation.

## 7. Data Visualization

The project uses Plotly for interactive visualizations and Matplotlib for static charts.

### 7.1 Interactive Visualizations

The dashboard supports:

- Crime category distribution charts.
- Temporal trend charts.
- Weekday and hourly distribution charts.
- Geographical area comparisons.
- Interactive maps using valid coordinates.
- Statistical summaries and numerical correlations.

### 7.2 Static Chart Export

The dashboard provides an **Export Static Charts** option that generates available Matplotlib visualizations and saves them as PNG files in the `outputs/` directory.

The exported charts may include:

- Crime category counts.
- Monthly incident counts.
- Weekday incident counts.
- Yearly incident counts, when multiple years are available.
- Geographical coordinate scatter plots, when valid coordinates exist.

Charts are generated only when the required data is available.

## 8. Dashboard Features

The project includes a responsive Streamlit dashboard with navigation for the following sections:

| Section | Description |
|---|---|
| Overview | Displays incident counts, key metrics, temporal trends, and summary findings |
| Crime Categories | Examines crime frequencies, category distributions, and percentage shares |
| Temporal Analysis | Analyzes monthly, weekday, and hourly patterns |
| Geographical Analysis | Compares recorded incidents across areas and displays valid coordinates |
| Statistical Insights | Presents descriptive statistics, numerical summaries, and correlations |
| Data Quality | Reports missing values, duplicates, and preprocessing results |
| Dataset Explorer | Provides searchable, paginated data exploration and CSV export |

### 8.1 Interactive Filtering

Shared filters allow users to refine the displayed analysis by:

- Date range.
- Crime category.
- Geographical area.
- Weekday.

The selected filters update relevant metrics, charts, and analytical summaries.

### 8.2 Key Dashboard Capabilities

- Interactive Plotly visualizations.
- Dynamically calculated findings.
- Filtered dataset exploration.
- CSV export of filtered records.
- Data quality summaries.
- Static chart export.
- Support for datasets with optional fields.
- Clear labeling of public and synthetic datasets.

The dashboard distinguishes the public-data snapshot from the synthetic fallback dataset.

## 9. Project Structure

The project follows a modular structure to separate data processing, analysis, visualization, and testing.

```text
crime-data-analysis/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── eda.py
│   ├── insights.py
│   └── charts.py
│
├── data/
│   ├── README.md
│   ├── chicago_crime_2026_ytd.csv
│   └── sample_crime_data.csv
│
├── notebooks/
│   └── crime_analysis.ipynb
│
├── outputs/
│   └── [Exported PNG charts]
│
└── tests/
    └── [Automated test files]
```

*Note: The directory listing is illustrative. Refer to the actual project workspace for the complete file structure.*

### Main Components

- **`app.py`:** Runs the Streamlit dashboard.
- **`src/data_loader.py`:** Loads the dataset.
- **`src/preprocessing.py`:** Cleans and validates the data.
- **`src/eda.py`:** Performs exploratory and statistical analysis.
- **`src/insights.py`:** Generates analytical observations from the data.
- **`src/charts.py`:** Creates visualizations.
- **`data/`:** Stores datasets and source documentation.
- **`notebooks/`:** Contains the Jupyter Notebook workflow.
- **`outputs/`:** Stores exported charts.
- **`tests/`:** Contains automated tests.

## 10. Installation and Execution

### 10.1 Prerequisites

Install Python 3.11 or a compatible version and ensure that `pip` is available.

### 10.2 Windows Installation

Open PowerShell in the project directory and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Launch the dashboard:

```powershell
streamlit run app.py
```

### 10.3 Ubuntu/Linux Installation

Open a terminal in the project directory and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Launch the dashboard:

```bash
streamlit run app.py
```

Streamlit will display a local URL that can be opened in a web browser.

### 10.4 Running the Jupyter Notebook

From the project root, run:

```bash
jupyter notebook notebooks/crime_analysis.ipynb
```

Execute the notebook cells sequentially to perform data loading, preprocessing, exploratory analysis, and visualization.

### 10.5 Selecting a Different Dataset

The application loads the bundled Chicago snapshot by default.

To select a different CSV file, set the `CRIME_DATA_PATH` environment variable or enter the dataset path in the dashboard, if supported by the current implementation.

For example, in Windows PowerShell:

```powershell
$env:CRIME_DATA_PATH = "data/sample_crime_data.csv"
streamlit run app.py
```

### 10.6 Exporting Charts

Use the **Export Static Charts** option in the dashboard to save supported visualizations to the `outputs/` directory.

Alternatively, run the chart module using the project's documented command and the appropriate dataset path.

### 10.7 Running Automated Tests

Execute the test suite from the project root:

```bash
python -m pytest -q
```

The command runs the available automated tests and displays their results.

## 11. Refreshing the Dataset

The bundled snapshot can be refreshed using the City of Chicago's public data API.

The following PowerShell example requests selected fields for the 2026 calendar year:

```powershell
$uri = "https://data.cityofchicago.org/resource/ijzp-q8t2.csv?`$select=id%2Cdate%2Cprimary_type%2Cdescription%2Clocation_description%2Cdistrict%2Ccommunity_area%2Clatitude%2Clongitude&`$where=date%20between%20%272026-01-01T00%3A00%3A00%27%20and%20%272026-12-31T23%3A59%3A59%27&`$limit=250000&`$order=date"

Invoke-WebRequest -Uri $uri -OutFile "data/chicago_crime_2026_ytd.csv"
```

**Important considerations:**

- The query retrieves records matching the specified date range; it does not guarantee that the dataset contains a complete year of records.
- The API may return preliminary or revised records.
- Confirm the actual date coverage and record count after downloading.
- Check whether the provider's API limits, terms, and attribution requirements have changed.
- Preserve a copy of the previous snapshot if reproducibility is important.

The dashboard uses the local CSV file during normal execution and does not require a live API connection.

## 12. Findings and Results

The following findings were calculated from the bundled 2026 year-to-date Chicago crime snapshot described in this project's documentation.

### 12.1 Dataset Summary

| Metric | Result |
|---|---:|
| Total reported incidents | 189,983 |
| Distinct recorded crime categories | 30 |
| Police districts represented | 24 |
| Dataset start date | January 1, 2026 |
| Latest recorded date in the snapshot | October 24, 2026 |
| Exact duplicate rows identified | 0 |

### 12.2 Most Frequently Recorded Crime Categories

| Crime Category | Recorded Incidents | Percentage |
|---|---:|---:|
| Theft | 41,003 | 21.6% |
| Battery | 35,009 | 18.4% |
| Criminal Damage | 20,838 | 11.0% |

Theft was the most frequently recorded category in this snapshot, followed by battery and criminal damage.

### 12.3 Geographical and Temporal Observations

- **Police district:** District 12 recorded the largest number of incidents, with 12,517.
- **Weekday:** Friday had the highest recorded weekday count, with 28,243 incidents.
- **Location description:** Approximately 0.450% of records had missing location descriptions.
- **Coordinates:** Approximately 0.204% of records had missing latitude and longitude values.
- **Community area:** Approximately 0.001% of records had missing community area values.

These observations describe the records in the selected snapshot. They do not establish the underlying prevalence of crime in the corresponding categories or areas.

### 12.4 Dynamic Findings

The dashboard recalculates relevant findings based on the currently selected date range, crime categories, and geographical areas.

Consequently, the values displayed in the dashboard may differ from the full-dataset findings presented above.

## 13. Limitations

The project has several limitations that must be considered when interpreting its results.

1. **Reported incidents versus actual prevalence:** Recorded incidents do not represent every crime that occurs.
2. **Reporting differences:** Reporting practices and data collection methods can affect the recorded counts.
3. **Geographical differences:** Areas with different populations cannot be fairly compared using raw counts alone.
4. **No population denominators:** Population-adjusted crime rates are not calculated because suitable population data is not included.
5. **Preliminary records:** The source data may be incomplete, preliminary, or subsequently revised.
6. **Temporal comparability:** Changes in reporting practices, category definitions, and data coverage may affect comparisons over time. The provider advises caution when comparing records across periods.
7. **Missing data:** Missing locations, dates, or coordinates may limit certain analyses.
8. **Approximate coordinates:** Geographical coordinates may be approximate or rounded and must not be used to infer exact addresses.
9. **Descriptive analysis only:** Statistical associations do not establish causation.
10. **No predictive or operational decisions:** The dashboard is an academic analytical tool, not a crime prediction system or an operational decision-making platform.

## 14. Future Enhancements

The project could be extended through the following improvements:

- Integrating additional documented public crime datasets.
- Supporting configurable schemas for different CSV formats.
- Adding more comprehensive data validation and preprocessing reports.
- Incorporating suitable population data to calculate population-normalized rates.
- Improving geographical visualizations.
- Supporting comparisons across documented reporting periods.
- Adding additional statistical analysis where appropriate.
- Improving automated test coverage.
- Enhancing accessibility and responsive dashboard design.

Any additional analysis should be supported by suitable data and documented assumptions.

## 15. Conclusion

This project demonstrates how Python-based data analysis and visualization techniques can be applied to recorded crime incident data.

Using Pandas and NumPy, the workflow performs data preprocessing, validation, and exploratory analysis. Matplotlib, Seaborn, and Plotly provide static and interactive visualizations, while Streamlit brings the analytical results together in an interactive dashboard.

The application allows users to examine crime categories, temporal distributions, geographical patterns, and data quality while applying filters and exporting selected records.

The project also emphasizes the importance of data provenance, preprocessing transparency, and responsible interpretation. By distinguishing recorded counts from actual crime prevalence and documenting the limitations of the dataset, it provides a practical demonstration of descriptive data analytics.

Overall, the project meets the academic objective of demonstrating data preprocessing, exploratory data analysis, statistical summaries, and visualization using Python, while providing a reusable foundation for further analytical work.
