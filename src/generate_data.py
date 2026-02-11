import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_history():
    print("Creating a plethora of data for testing analysis")
    
    # my SCY personal bests!
    scy_pbs = {
        "50 Free": 21.03,
        "100 Free": 45.30,
        "200 Free": 99.12,   # 1:39.12
        "500 Free": 274.10,  # 4:34.10
        "100 Fly": 49.94,
        "200 Fly": 111.98,   # 1:51.98
        "200 IM": 112.26     # 1:52.26
    }
    
    start_date = datetime(2023, 8, 1)
    end_date = datetime(2026, 2, 1)
    
    all_results = []
    current_date = start_date

    while current_date < end_date:
        month = current_date.month
        
        # SCY runs from August (8) to March (3)
        # LCM runs from April (4) to July (7)
        if month >= 8 or month <= 3:
            course = "SCY"
        else:
            course = "LCM"

        if course == "SCY":
            meet_name = f"Cornell vs {np.random.choice(['Columbia', 'Harvard', 'Penn', 'Yale'])}"
            # generally agreed upon in-season unrested fatigue (2-6% slower)
            fatigue = np.random.uniform(0.02, 0.06)
            
            # championship taper, where swimmers are fully rested
            if month == 2 or month == 3:
                meet_name = "Ivy League Championships"
                fatigue = -0.01 # could drop time
        else:
            meet_name = f"Speedo Sectionals {np.random.choice(['Austin', 'Indy', 'Clovis'])}"
            # generally agreed upon in-season unrested fatigue (2-6% slower)
            fatigue = np.random.uniform(0.02, 0.06) 
            
            # championship taper, where swimmers are fully rested
            if month == 7:
                meet_name = "Summer Nationals"
                fatigue = -0.01 

        for event, base_time in scy_pbs.items():
            
            # convert to LCM if needed (approx 1.14x conversion factor)
            # different for every swimmer, will address in later versions
            time_standard = base_time * 1.14 if course == "LCM" else base_time
            
            variance = np.random.uniform(0.0, 0.5)
            final_time = time_standard + (time_standard * fatigue) + variance
            
            all_results.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Meet": meet_name,
                "Event": event,
                "Time": round(final_time, 2),
                "Course": course
            })
        
        # meets every 2-3 weeks
        days_next = np.random.randint(14, 24)
        current_date += timedelta(days=days_next)

    df = pd.DataFrame(all_results)
    output_path = "data/raw/generated_history.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows. (Every event swum at {len(df['Meet'].unique())} meets)")

if __name__ == "__main__":
    generate_history()