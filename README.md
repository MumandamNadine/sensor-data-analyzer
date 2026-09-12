# Sensor Data Analyzer

A Python and pandas program that analyzes simulated smart-farm sensor data. It cleans readings, calculates summary statistics, detects alerts and exports results to CSV.

## Features

- Reads temperature, humidity and soil-moisture data
- Cleans device names and converts timestamps and measurements
- Removes missing, invalid and out-of-range readings
- Calculates count, average, minimum and maximum values
- Detects high temperature, high humidity and dry soil
- Counts alerts per reading and assigns Normal or Alert status
- Exports analyzed readings and combined alerts

## Project Files

| File | Purpose |
|---|---|
| `sensor_analyzer.py` | Main Python program |
| `sensor_data.csv` | Synthetic sample sensor data |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Excludes generated and temporary files |
| `README.md` | Project documentation |

## Input Format

```csv
device,timestamp,temperature,humidity,soil_moisture
sensor-01,2026-09-10 08:00:00,25,78,50
sensor-02,2026-09-10 08:03:00,33,86,45
```

Temperature is measured in °C. Humidity and simulated soil moisture use percentages.

## Alert Rules

| Alert | Condition |
|---|---|
| High temperature | Above 30°C |
| High humidity | Above 85% |
| Dry soil | Below 25% |

Readings must also fall within the configured validation ranges: temperature from -40°C to 80°C, and humidity and soil moisture from 0% to 100%.

These are practice settings for synthetic data, not validated agricultural recommendations.

## How to Run

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the program from the project folder:

```bash
python sensor_analyzer.py
```

## Output Files

- `analyzed_sensor_data.csv`: all valid readings with alert flags, counts and status.
- `combined_alerts.csv`: readings with at least one alert.

Running the program again overwrites these generated files.

## Sample Results

The included dataset produces:

- 10 valid readings
- 2 high-temperature alerts
- 6 high-humidity alerts
- 1 dry-soil alert
- 7 readings with at least one alert

One reading can trigger multiple alerts.

## Version History

- **V0.1:** Temperature analysis using Python's CSV module and text reports.
- **V0.2:** Multi-sensor analysis using pandas, combined alerts and CSV exports.
