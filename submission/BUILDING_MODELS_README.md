# Building Model Artifacts Guide

Place required model files for submission in this folder structure:

- submission/building-models/baseline/
  - baseline.idf
- submission/building-models/optimized/
  - optimized_run_001.idf
  - optimized_run_002.idf

For each optimized file, document:
- Source baseline model
- Changed parameters (setpoints, schedules, controls)
- Why changes were selected
- Associated simulation run ID

Suggested companion file:
- submission/building-models/changes_log.csv

Recommended changes_log.csv columns:
- run_id
- file_name
- object_type
- object_name
- field_name
- old_value
- new_value
- rationale
