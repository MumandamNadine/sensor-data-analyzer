import csv
from pathlib import Path


def load_readings(file_path):
    with file_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader)


def convert_temperatures(readings):
    valid_readings = []

    for reading in readings:
        try:
            reading["temperature"] = float(reading["temperature"])
            valid_readings.append(reading)
        except (ValueError, TypeError):
            device = reading.get("device", "unknown device")
            print(f"Skipping invalid reading from {device}")

    return valid_readings


def analyze_temperatures(readings):
    if not readings:
        return {
            "count": 0,
            "average": None,
            "minimum": None,
            "maximum": None
        }

    temperatures = []

    for reading in readings:
        temperatures.append(reading["temperature"])

    return {
        "count": len(temperatures),
        "average": round(sum(temperatures) / len(temperatures), 2),
        "minimum": min(temperatures),
        "maximum": max(temperatures)
    }


def create_temperature_alerts(readings, threshold):
    alerts = []

    for reading in readings:
        if reading["temperature"] > threshold:
            alerts.append(
                f'{reading["device"]} has a high temperature of '
                f'{reading["temperature"]}°C'
            )

    return alerts


def write_report(report_path, summary, alerts):
    with report_path.open("w", encoding="utf-8") as report_file:
        report_file.write("Sensor Data Report\n")
        report_file.write("==================\n")
        report_file.write(f"Valid readings: {summary['count']}\n")
        report_file.write(
            f"Average temperature: {summary['average']}°C\n"
        )
        report_file.write(
            f"Minimum temperature: {summary['minimum']}°C\n"
        )
        report_file.write(
            f"Maximum temperature: {summary['maximum']}°C\n"
        )

        report_file.write("\nTemperature Alerts\n")
        report_file.write("------------------\n")

        if alerts:
            for alert in alerts:
                report_file.write(alert + "\n")
        else:
            report_file.write("No high-temperature alerts.\n")


def main():
    project_folder = Path(__file__).resolve().parent
    file_path = project_folder / "sensor_data.csv"
    report_path = project_folder / "sensor_report.txt"

    try:
        readings = load_readings(file_path)
    except FileNotFoundError:
        print(f"CSV file not found: {file_path}")
        return

    readings = convert_temperatures(readings)
    summary = analyze_temperatures(readings)
    alerts = create_temperature_alerts(readings, 30)

    print(summary)

    for alert in alerts:
        print(alert)

    write_report(report_path, summary, alerts)
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
