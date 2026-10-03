"""
Phase 1 - Task 003-A: Data Reconnaissance Script
Purpose: Scan raw dataset directory, discover all CSV tables, and inspect basic structural metadata (row count, column count, column names).
"""

import sys
from pathlib import Path
import pandas as pd


def run_data_recon():
    # 1. Safely find project root directory (parent of 'scripts' directory)
    project_root = Path(__file__).resolve().parent.parent
    raw_data_dir = project_root / "real_estate_intelligence_dataset" / "raw"

    print("=" * 60)
    print("PHASE 1: DATA RECONNAISSANCE (TASK 003-A)")
    print(f"Scanning directory: {raw_data_dir}")
    print("=" * 60)

    # 2. Check if the raw directory exists
    if not raw_data_dir.exists():
        print(f"ERROR: Raw data directory not found at: {raw_data_dir}", file=sys.stderr)
        return False

    # 3. Discover all CSV files automatically and sort them alphabetically
    csv_files = sorted(raw_data_dir.glob("*.csv"))

    if not csv_files:
        print(f"WARNING: No CSV files found in: {raw_data_dir}", file=sys.stderr)
        return False

    print(f"Discovered {len(csv_files)} CSV files.\n")

    successful_reads = 0

    # 4. Iterate through each CSV file and display structural information
    for csv_path in csv_files:
        print("=" * 60)
        print(f"TABLE: {csv_path.name}")
        print("=" * 60)

        try:
            # Read CSV into a pandas DataFrame
            df = pd.read_csv(csv_path)

            # Extract dimensions: df.shape returns (number_of_rows, number_of_columns)
            num_rows, num_cols = df.shape

            print(f"Rows:    {num_rows:,}")
            print(f"Columns: {num_cols}")
            print("\nColumns:")
            for col in df.columns:
                print(f"  * {col}")

            print()  # Empty line for spacing
            successful_reads += 1

        except Exception as e:
            print(f"ERROR: Failed to read {csv_path.name}: {e}", file=sys.stderr)
            print()

    # 5. Summary
    print("=" * 60)
    print(f"SUMMARY: Successfully read {successful_reads}/{len(csv_files)} CSV files.")
    print("=" * 60)

    return successful_reads == len(csv_files) and len(csv_files) == 13


if __name__ == "__main__":
    success = run_data_recon()
    sys.exit(0 if success else 1)
