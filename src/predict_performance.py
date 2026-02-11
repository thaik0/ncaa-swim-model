import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

def predict_with_taper_factor():
    print("Trying to predict taper better")
    
    df = pd.read_csv("data/raw/generated_history.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    
    target_event = "100 Free"
    current_season_start = datetime(2025, 8, 1)
    championship_date = datetime(2026, 2, 28) # Ivy League Champs
    
    # We look at all swims before this season to find average drop
    past_data = df[
        (df['Event'] == target_event) & 
        (df['Date'] < current_season_start) & 
        (df['Course'] == "SCY")
    ]
    
    if past_data.empty:
        taper_drop_percent = 0.03 # just estimate
    else:
        # find in-season average (excluding the fastest championship swim)
        # assume the fastest swim of the year was the championship
        best_time_past = past_data['Time'].min()
        avg_time_past = past_data[past_data['Time'] > best_time_past]['Time'].mean()
        
        # calculate the drop percentage
        taper_drop_percent = (avg_time_past - best_time_past) / avg_time_past
        print(f"past ({target_event}):")
        print(f"    avg in season time: {avg_time_past:.2f}s")
        print(f"    championship best:  {best_time_past:.2f}s")
        print(f"    estimated taper:  {taper_drop_percent*100:.2f}% drop")

    # 4. ANALYZE CURRENT SEASON
    current_data = df[
        (df['Event'] == target_event) & 
        (df['Date'] >= current_season_start) & 
        (df['Course'] == "SCY")
    ]
    
    if current_data.empty:
        print("no swims this season")
        return

    current_avg = current_data['Time'].mean()
    current_best = current_data['Time'].min()
    
    print(f"current ({target_event}):")
    print(f"   season average: {current_avg:.2f}s")
    print(f"   season unrested best: {current_best:.2f}s")
    
    # apply estimated taper factor to current average
    predicted_time = current_avg * (1 - taper_drop_percent)
    
    print(f"   predicted ivy champs time: {predicted_time:.2f}s")
    
    # 6. VISUALIZATION
    plt.figure(figsize=(10, 6))
    
    # Plot Current Season Swims
    plt.scatter(current_data['Date'], current_data['Time'], color='blue', label='In-Season Swims', s=80, alpha=0.7)
    
    # Plot the Average Line
    plt.axhline(current_avg, color='gray', linestyle='--', label='In-Season Avg')
    
    # Plot the Prediction
    plt.scatter(championship_date, predicted_time, color='gold', s=300, marker='*', label='Tapered Prediction', zorder=5)
    
    # Draw an arrow showing the drop
    plt.annotate(
        f"-{taper_drop_percent*100:.1f}% Taper",
        xy=(championship_date, predicted_time), 
        xytext=(championship_date - pd.Timedelta(days=45), current_avg),
        arrowprops=dict(facecolor='black', shrink=0.05),
        fontsize=12
    )

    # Formatting
    plt.title(f"Championship Prediction: {target_event}", fontsize=14)
    plt.ylabel("Time (Seconds)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    
    output_path = "data/processed/taper_prediction.png"
    plt.savefig(output_path)
    print(f"\chart saved to {output_path}")
    plt.show()

if __name__ == "__main__":
    predict_with_taper_factor()