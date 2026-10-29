import arcpy
import os
import pandas as pd
from datetime import datetime

class Toolbox(object):
    """Defines the ArcGIS Python Toolbox container."""
    def __init__(self):
        self.label = "Data Validation Toolbox"
        self.alias = "datavalidation"
        self.tools = [DataValidationCheck]

class DataValidationCheck(object):
    """Defines the 'Run Data Validation' geoprocessing tool."""
    def __init__(self):
        self.label = "Run Data Validation"
        self.description = "Exports spatial layers to Excel and performs multi-criteria data validation analysis."

    def getParameterInfo(self):
        """Defines the user interface parameters for the geoprocessing tool."""
        
        p1 = arcpy.Parameter(
            displayName="Draft Features Layer",
            name="draft_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        p2 = arcpy.Parameter(
            displayName="Finalized Features Layer",
            name="finalized_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        p3 = arcpy.Parameter(
            displayName="Output Folder",
            name="out_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        return [p1, p2, p3]

    def execute(self, params, messages):
        """Executes the tool's core logic: data conversion, validation, and reporting."""
        
        draft_layer = params[0].valueAsText
        finalized_layer = params[1].valueAsText
        out_folder = params[2].valueAsText

        # Generate a dynamic folder name based on the current date
        today = datetime.now().strftime("%d_%B_%Y")
        folder = os.path.join(out_folder, today)
        os.makedirs(folder, exist_ok=True)

        draft_xlsx = os.path.join(folder, "Draft_Features.xlsx")
        finalized_xlsx = os.path.join(folder, "Finalized_Features.xlsx")

        # Convert the GIS feature layers/tables directly into Excel spreadsheets
        arcpy.conversion.TableToExcel(draft_layer, draft_xlsx, "ALIAS", "CODEPAGE")
        arcpy.conversion.TableToExcel(finalized_layer, finalized_xlsx, "ALIAS", "CODEPAGE")

        def analyse(path, expected_source, expected_status):
            """
            Reads an Excel file and flags rows that do not match data integrity rules.
            """
            df = pd.read_excel(path)
            
            # Isolate rows where columns do not match the expected categorical lists
            src_mis = df[~df["Boundary_Source"].isin(expected_source)]
            stat_mis = df[~df["Process_Status"].isin(expected_status)]
            
            return df, src_mis, stat_mis

        # Run validation on the Draft Features data
        # Expected: Source must be "Unverified"; Status must be "No Data" or "In Progress"
        draft_df, draft_src, draft_stat = analyse(
            draft_xlsx, ["Unverified"], ["No Data", "In Progress"]
        )

        # Run validation on the Finalized Features data
        # Expected: Source must be from official ingestion streams; Status must be "Complete"
        final_df, final_src, final_stat = analyse(
            finalized_xlsx, ["System Ingestion", "Vendor Import", "User Submitted"], ["Complete"]
        )

        # Compile all data variations into a final, multi-tab Excel validation report
        report_path = os.path.join(folder, "Validation_Analysis_Report.xlsx")
        with pd.ExcelWriter(report_path) as writer:
            # Write Draft Layer datasets
            draft_df.to_excel(writer, "Draft_All_Records", index=False)
            draft_src.to_excel(writer, "Draft_Source_Mismatches", index=False)
            draft_stat.to_excel(writer, "Draft_Status_Mismatches", index=False)
            
            # Write Finalized Features datasets
            final_df.to_excel(writer, "Finalized_All_Records", index=False)
            final_src.to_excel(writer, "Finalized_Source_Mismatches", index=False)
            final_stat.to_excel(writer, "Finalized_Status_Mismatches", index=False)
