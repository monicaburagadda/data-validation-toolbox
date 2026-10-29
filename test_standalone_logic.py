"""
Standalone test script to execute data validation logic without an ArcGIS license.
This simulates the exact Pandas analytical engine used inside the ArcGIS Python Toolbox.
"""

import os
import pandas as pd
from datetime import datetime

def run_local_validation(draft_csv_path, finalized_csv_path, out_dir):
    # Setup output environment
    today = datetime.now().strftime("%d_%B_%Y")
    folder = os.path.join(out_dir, today)
    os.makedirs(folder, exist_ok=True)
    
    print(f"🚀 Initializing validation routine. Target folder: {folder}")

    def analyse(path, expected_source, expected_status):
        """Pure-Pandas core analysis function extracted from the .pyt toolbox."""
        # Read from CSV directly for local cross-platform testing
        df = pd.read_csv(path) 
        
        src_mis = df[~df["Boundary_Source"].isin(expected_source)]
        stat_mis = df[~df["Process_Status"].isin(expected_status)]
        
        return df, src_mis, stat_mis

    # Execute analytics on mock datasets
    draft_df, draft_src, draft_stat = analyse(
        draft_csv_path, ["Unverified"], ["No Data", "In Progress"]
    )

    final_df, final_src, final_stat = analyse(
        finalized_csv_path, ["System Ingestion", "Vendor Import", "User Submitted"], ["Complete"]
    )

    # Compile findings into a multi-tab workbook
    report_path = os.path.join(folder, "Local_Validation_Report.xlsx")
    with pd.ExcelWriter(report_path) as writer:
        draft_df.to_excel(writer, sheet_name="Draft_All_Records", index=False)
        draft_src.to_excel(writer, sheet_name="Draft_Source_Mismatches", index=False)
        draft_stat.to_excel(writer, sheet_name="Draft_Status_Mismatches", index=False)
        
        final_df.to_excel(writer, sheet_name="Finalized_All_Records", index=False)
        final_src.to_excel(writer, sheet_name="Finalized_Source_Mismatches", index=False)
        final_stat.to_excel(writer, sheet_name="Finalized_Status_Mismatches", index=False)


    print(f"📊 Audit complete! Mismatches captured and exported to: {report_path}")

if __name__ == "__main__":
    # Define file pathways relative to repo workspace
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DRAFT_INPUT = os.path.join(BASE_DIR, "test_data", "draft_features.csv")
    FINAL_INPUT = os.path.join(BASE_DIR, "test_data", "finalized_features.csv")
    OUTPUT_TARGET = os.path.join(BASE_DIR, "test_output")

    # Run the routine
    run_local_validation(DRAFT_INPUT, FINAL_INPUT, OUTPUT_TARGET)
