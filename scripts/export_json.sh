#!/bin/bash
# Export dashboard data to JSON

echo "Exporting dashboard data..."
python etl/run.py --export-only
echo "Export completed! Check data/processed/dashboard.json"