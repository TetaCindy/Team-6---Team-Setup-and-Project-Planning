#!/bin/bash
# Run the ETL pipeline

echo "Starting ETL Pipeline..."
python etl/run.py --xml data/raw/momo.xml
echo "ETL Pipeline completed!"