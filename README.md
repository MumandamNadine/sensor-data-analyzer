# Sensor Data Analyzer

A Python program that reads temperature sensor data from a CSV file, cleans invalid readings, calculates summary statistics, identifies high-temperature readings, and generates a text report.

## Features

- Reads sensor data from CSV
- Converts temperature values to numbers
- Skips invalid readings
- Calculates count, average, minimum, and maximum temperature
- Creates alerts for temperatures above a chosen threshold
- Saves the results in a text report

## Project Structure

```text
Sensor_Data_analyzer/
├── sensor_analyzer.py
├── sensor_data.csv
├── README.md
└── sensor_report.txt
