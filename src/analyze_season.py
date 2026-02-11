import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def analyze_season():
    df = pd.read_csv("data/raw/generated_history.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    
    event_name = "100 Free"
    data = df[df['Event'] == event_name].sort_values('Date')
    
    fig, ax = plt.subplots(figsize=(14, 7))
    scy = data[data['Course'] == 'SCY']
    ax.scatter(scy['Date'], scy['Time'], color='blue', label='SCY (Yards)', s=100, zorder=3)

    lcm = data[data['Course'] == 'LCM']
    ax.scatter(lcm['Date'], lcm['Time'], color='red', label='LCM (Meters)', s=100, zorder=3)
    
    ax.plot(data['Date'], data['Time'], color='gray', linestyle='--', alpha=0.3, zorder=2)

    years = data['Date'].dt.year.unique()
    for year in years:
        ax.axvspan(pd.Timestamp(f"{year}-01-01"), pd.Timestamp(f"{year}-03-31"), color='lightblue', alpha=0.2)
        ax.axvspan(pd.Timestamp(f"{year}-04-01"), pd.Timestamp(f"{year}-07-31"), color='orange', alpha=0.1)   
        ax.axvspan(pd.Timestamp(f"{year}-08-01"), pd.Timestamp(f"{year}-12-31"), color='lightblue', alpha=0.2)

    ax.set_title(f"Season Progression: {event_name} (SCY vs LCM)", fontsize=16)
    ax.set_ylabel("Time (Seconds)", fontsize=12)
    ax.legend()
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.savefig("data/processed/season_split.png")
    print("Chart saved to data/processed/LCM_SCY.png")
    plt.show()

if __name__ == "__main__":
    analyze_season()