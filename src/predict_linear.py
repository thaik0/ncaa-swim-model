import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

def predict_championship():
    print("Predicting taper meet times")
    
    df = pd.read_csv("data/raw/generated_history.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    
    # pick an event and a season
    target_event = "200 Free"
    target_season_start = datetime(2025, 8, 1) # this current season
    championship_date = datetime(2026, 2, 28) # Ivy League Champs
    
    # filter for just this season's dual meets (SCY only)
    season_data = df[
        (df['Event'] == target_event) & 
        (df['Date'] >= target_season_start) & 
        (df['Course'] == "SCY")
    ].copy()
    
    season_data = season_data.sort_values('Date')
    
    if season_data.empty:
        print(f"No data found for {target_event} in this season.")
        return

    season_data['Day_Num'] = (season_data['Date'] - season_data['Date'].min()).dt.days
    
    X = season_data['Day_Num'].values
    y = season_data['Time'].values
    
    # Fit a line (y = mx + b) linear regression
    # m = slope (how much faster a swimmer gets per day)
    # b = intercept (their starting time in Sept)
    m, b = np.polyfit(X, y, 1)
    
    print(f"Stats for {target_event}:")
    print(f"   Starting Time (Sept): {b:.2f}s")
    print(f"   Improvement Rate: {m*7:.3f} seconds per week") # m is per day, *7 for week
    
    days_until_champs = (championship_date - season_data['Date'].min()).days
    predicted_time = (m * days_until_champs) + b
    
    print(f"PREDICTED IVY LEAGUE TIME: {predicted_time:.2f}s")
    
    plt.figure(figsize=(10, 6))
    
    plt.scatter(season_data['Date'], season_data['Time'], color='blue', label='In-Season Swims')
    
    x_range = np.linspace(0, days_until_champs, num=50)
    y_trend = (m * x_range) + b
    
    date_range = [season_data['Date'].min() + pd.Timedelta(days=d) for d in x_range]
    
    plt.plot(date_range, y_trend, color='red', linestyle='--', label='Projected Taper Line')
    
    plt.scatter(championship_date, predicted_time, color='gold', s=200, marker='*', label='Predicted Time', zorder=5)
    
    plt.title(f"Taper Projection: {target_event}", fontsize=14)
    plt.ylabel("Time (Seconds)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    
    plt.savefig("data/processed/prediction.png")
    print("Chart saved to data/processed/prediction.png")
    plt.show()

if __name__ == "__main__":
    predict_championship()