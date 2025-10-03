#!/usr/bin/env python3
import pandas as pd
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        prog="borough_complaints.py",
        description=(
            "Count the number of complaints per borough and complaint type "
            "from a given dataset within a specified date range."
        ),
        epilog="Example: python borough_complaints.py -i data.csv -s 2024-01-01 -e 2024-01-31 -o results.csv"
    )
    parser.add_argument("-i", "--input_file", required=True, help="Path to input CSV file")
    parser.add_argument("-s", "--start_date", required=True, help="Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM)")
    parser.add_argument("-e", "--end_date", required=True, help="End date (YYYY-MM-DD or YYYY-MM-DD HH:MM)")
    parser.add_argument("-o", "--output_file", help="Path to output CSV file (optional)")

    args = parser.parse_args()

    # Expand ~ and make absolute
    input_path = os.path.abspath(os.path.expanduser(args.input_file))

    # Parse start and end dates
    try:
        start_dt = pd.to_datetime(args.start_date)
        end_dt = pd.to_datetime(args.end_date)
    except Exception:
        print("Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM", file=sys.stderr)
        sys.exit(2)

    if end_dt < start_dt:
        print("End date must be on or after start date", file=sys.stderr)
        sys.exit(2)

    # Load CSV
    try:
        df = pd.read_csv(input_path, low_memory=False)
    except FileNotFoundError:
        print(f"File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    # Hardcoded column names
    data_created = "Created Date"
    incident_type = "Complaint Type"
    borough = "Borough"

    # Check columns exist
    for col in [data_created, incident_type, borough]:
        if col not in df.columns:
            print(f'Missing required column: "{col}"', file=sys.stderr)
            sys.exit(1)

    # Normalize borough text
    df[borough] = df[borough].astype(str).str.strip().str.title()

    # Convert Created Date to datetime
    df[data_created] = pd.to_datetime(
    df[data_created],
    format="%m/%d/%Y %I:%M:%S %p",
    errors="coerce"
    )

    # Filter by date range
    df_filtered = df.loc[(df[data_created] >= start_dt) & (df[data_created] <= end_dt)].copy()

    # Group and count
    counts = (
        df_filtered
        .groupby([incident_type, borough], dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values(["count", incident_type, borough], ascending=[False, True, True])
    )

    # Output
    if args.output_file:
        out_path = os.path.abspath(os.path.expanduser(args.output_file))
        counts.to_csv(out_path, index=False)
    else:
        print(counts.to_csv(index=False), end="")

if __name__ == "__main__":
    main()