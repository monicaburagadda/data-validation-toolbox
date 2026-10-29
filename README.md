# ArcGIS Data Validation & QA/QC Toolbox

An automated ArcGIS Python Toolbox (`.pyt`) that exports spatial layer attribute tables to Excel and performs multi-criteria data validation using **Pandas**.

## 📌 Project Overview
In GIS enterprise database workflows, data entry errors (such as mismatched asset sources or processing statuses) frequently compromise database integrity. This tool automates the auditing process by converting spatial feature attributes into DataFrames, instantly isolating records that violate systemic business validation rules, and generating a clean, multi-tab Excel spreadsheet for data remediation.

## 📁 Repository Structure
* `DataValidation_Toolbox.pyt` - The self-contained ArcGIS Pro / Map Python Toolbox.
* `test_data/` - Mock tabular inputs used to test and demonstrate validation thresholds.
* `.gitignore` - Prevents local runtime Excel exports and cache files from tracking in version control.

## 🚀 Data Quality Rules Enforced

| Layer Type | Field Inspected | Expected Valid Values |
| :--- | :--- | :--- |
| **Draft Features** | `Boundary_Source` | `Unverified` |
| **Draft Features** | `Process_Status` | `No Data`, `In Progress` |
| **Finalized Features** | `Boundary_Source` | `System Ingestion`, `Vendor Import`, `User Submitted` |
| **Finalized Features** | `Process_Status` | `Complete` |

## 🛠️ Skills & Technologies Demonstrated
* **GIS Automation:** Structuring self-contained Python Toolboxes (`.pyt`) and utilizing ArcPy data conversion frameworks (`TableToExcel`).
* **Data Science & QA/QC:** Leveraging Pandas conditional filtering (`~df.isin()`) to optimize data auditing over native cursor loops.
* **Defensive Programming:** Abstracting processing logic into modular, reusable nested functions.


## 🧪 Local Testing (Without an ArcGIS License)
To allow cross-platform validation testing who may not have an active Esri ArcGIS environment setup locally, a standalone test harness is included.

### Execution Instructions:
1. Ensure your local environment has `pandas` and `openpyxl` installed:
   ```bash
   pip install pandas openpyxl
   ```
2. Clone this repository and run the test script from your terminal/command line:
   ```bash
   python test_standalone_logic.py
   ```
3. The script will parse the mock tracking sheets inside `test_data/`, execute the core spatial-attribute boundary filters, and output a time-stamped validation audit notebook inside a generated `/test_output/` subfolder.
