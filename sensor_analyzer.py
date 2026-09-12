import pandas as pd

data = pd.read_csv("sensor_data.csv")

# Remove accidental spaces from column names
data.columns = data.columns.str.strip()

# Clean device names
data["device"] = data["device"].astype("string").str.strip()

# Convert empty device names into missing values
data["device"] = data["device"].replace("", pd.NA)

# Convert timestamps
data["timestamp"] = pd.to_datetime(
    data["timestamp"],
    errors="coerce"
)

# Convert sensor measurements
numeric_columns = [
    "temperature",
    "humidity",
    "soil_moisture"
]

for column in numeric_columns:
    data[column] = pd.to_numeric(
        data[column],
        errors="coerce"
    )

# Columns required for a valid reading
required_columns = [
    "device",
    "timestamp",
    "temperature",
    "humidity",
    "soil_moisture"
]

# Find rows containing missing or invalid values
invalid_rows = data[
    data[required_columns].isna().any(axis=1)
]


# Remove invalid rows
clean_data = data.dropna(
    subset=required_columns
).copy()

# Check acceptable measurement ranges
valid_ranges = (
    clean_data["humidity"].between(0, 100)
    & clean_data["soil_moisture"].between(0, 100)
    & clean_data["temperature"].between(-40, 80)
)

clean_data = clean_data[valid_ranges].copy()

# Arrange readings chronologically
clean_data = clean_data.sort_values("timestamp")

sensor_columns = [
    "temperature",
    "humidity",
    "soil_moisture"
]

# Calculate summary statistics
summary = clean_data[sensor_columns].agg(
    ["count", "mean", "min", "max"]
).round(2)

#create alerts
def find_high_temperature(data,threshold):
    condition = data["temperature"] > threshold
    result = data.loc[condition, ["temperature","device","timestamp"]]
    return result

def find_high_humidity(data,threshold):
    condition = data["humidity"]> threshold
    result = data.loc[condition, ["humidity","device","timestamp"]]
    return result

def find_dry_soil(data,threshold):
    condition = data["soil_moisture"]<threshold
    result = data.loc[condition, ["soil_moisture","device","timestamp"]]
    return result

alert_temp=find_high_temperature(clean_data, 30)
alert_hum=find_high_humidity(clean_data, 85)
alert_soil=find_dry_soil(clean_data, 25)
analyzed_data=clean_data.copy()
alert_columns = [
    "high_temperature",
    "high_humidity",
    "dry_soil"
]
analyzed_data["high_temperature"] = (analyzed_data["temperature"] > 30)
analyzed_data["high_humidity"] = (analyzed_data["humidity"] > 85)
analyzed_data["dry_soil"] = (analyzed_data["soil_moisture"] < 25)
analyzed_data["alert_count"] = analyzed_data[alert_columns].sum(axis=1)

analyzed_data["status"] = "Normal"
condition = analyzed_data["alert_count"] > 0
analyzed_data.loc[condition, "status"] = "Alert"
combined_alerts=analyzed_data[analyzed_data["alert_count"]>0]
print("Summary Statistics:")
print(summary)
analyzed_data.to_csv("analyzed_sensor_data.csv", index=False)
combined_alerts.to_csv("combined_alerts.csv", index=False)