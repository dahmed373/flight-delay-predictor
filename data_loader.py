import pandas as pd
import os

def clean_and_save_csv(input_path, output_path):
    df = pd.read_csv(input_path)

    # Drop canceled flights
    df = df[df["cancelled_code"] == "N"]

    # Convert datetime columns
    datetime_cols = [
        "scheduled_departure_dt", "scheduled_arrival_dt",
        "actual_departure_dt", "actual_arrival_dt"
    ]
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Create binary target
    df["Delayed"] = (df["departure_delay"] > 15).astype(int)

    # Feature engineering
    df["scheduled_hour"] = df["scheduled_departure_dt"].dt.hour
    df["day_of_week"] = df["scheduled_departure_dt"].dt.dayofweek

    # Drop irrelevant or high-null columns if needed
    df = df.drop(columns=["cancelled_code", "tail_number", "delay_security"])

    # Save to processed folder
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned dataset saved to {output_path}")

# ⬅️ Make sure this is not indented!
if __name__ == "__main__":
    clean_and_save_csv(
        "data/raw/may_5_2019_flights.csv",
        "data/processed/cleaned_may_5_2019.csv"
    )
