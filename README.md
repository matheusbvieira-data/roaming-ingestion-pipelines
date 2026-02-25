# Automated Ingestion Pipelines
[![tests](https://github.com/matheusbvieira-data/roaming-ingestion-pipelines/actions/workflows/test-pipeline.yml/badge.svg)](https://github.com/matheusbvieira-data/roaming-ingestion-pipelines/actions/workflows/test-pipeline.yml)
[![codecov](https://codecov.io/gh/matheusbvieira-data/roaming-ingestion-pipelines/graph/badge.svg?token=s37tetAlhE)](https://codecov.io/gh/matheusbvieira-data/roaming-ingestion-pipelines)

## 📌 Context & Business Problem
In a previous scenario, the generation of critical business reports relied on manual data consolidation from multiple sources.
This process was inefficient and error-prone:
* **Operational Cost:** Analytical team spent multiple hours on repetitive tasks instead of analysis.
* **High Latency:** Reports took from **1 to 2 weeks** to be delivered after the closing period to stakeholders. Caused by manual downloads of data and data cleaning tasks.
* **Decision Delay:** Stakeholders acted on outdated information because dashboards needed to be updated manually.

## 🚀 The Solution
I engineered several automated pipelines using Python to handle the extraction, transformation, and loading of data.
* **Key Impacts:** 
    - **No more** manual downloads from DCH repository to get crucial data for analysis needed.
    - Dashboards can now be updated **automatically** with the latest info.
    - Higher quality data cause by automated data cleaning pipelines.
* **Reliability:** Eliminated manual copy-paste errors.
* **Scalability:** The script handles annual data volumes exceeding 100GB of information.

> **Note:** This repository demonstrates the logic used in the real-world scenario. All proprietary data has been replaced with synthetic data generated via `Faker` to ensure confidentiality.

## ⚙️ Architecture
The pipelines follows an EL flow (no T in here because we want raw quality data into the Data Warehouse on bronze layer):
1. **Extract**: 
    - Gets raw data stored in csv files from DCH (Data Clearing House).
    - Uses `Pandas` and `Great_Expectations` to ensure data quality.
2. **Load:** Upload retrieved data to the Data Warehouse using `Teradata ML` as we use Teradata Database as our Data Warehouse.

## 🛠️ Tools Used
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Teradata](https://img.shields.io/badge/teradata-%230000ff.svg?style=for-the-badge&logo=teradata&logoColor=white)

This project uses [Great Expectations](https://github.com/great-expectations/great_expectations) for data validation.

## 💻 How To Run

### Prerequisites
* Python 3.13+
* Virtualenv

### Installation & Execution
This project uses a `Makefile` to simplify command execution.

1.  **Install Dependencies:**
    ```bash
    make install
    ```

2.  **Run the Pipeline:**
    ```bash
    make run
    ```

3.  **Run Tests:**
    ```bash
    make test
    ```
