# =====================================================================
# --- WEEKS 17 & 18: TEMPORAL ANALYTICS & STATISTICAL INTELLIGENCE ---
# =====================================================================
from datetime import datetime
import pandas as pd
import os

# Day 81: Parse ISO strings safely
def calculate_time_delta(time_str1, time_str2):
    """
    Day 81 & 84: Converts ISO timestamp strings into datetime objects with error protection.
    Returns: float (hours elapsed) or None if corrupted.
    """
    try:
        dt1 = datetime.fromisoformat(str(time_str1))
        dt2 = datetime.fromisoformat(str(time_str2))
        
        # Day 82: Calculate time differences in fractional hours
        delta = dt2 - dt1
        elapsed_hours = delta.total_seconds() / 3600.0
        return elapsed_hours
    except (ValueError, TypeError, KeyError) as e:
        # Day 84: Graceful anomaly tracking fallback routine preventing execution crashes
        print(f"⚠️  [TEMPORAL ERROR] Corrupted or missing timestamp layout detected: {e}")
        return None


# Day 88 & 89: Statistical Boundary Engine
def compute_route_thresholds(csv_path="historical_voyages.csv"):
    """
    Day 88: Loads historical database records into a Pandas DataFrame and 
    calculates the arithmetic mean and statistical standard deviation.
    """
    if not os.path.exists(csv_path):
        print(f"⚠️  [DATA EXCEPTION] Historical log missing. Using fallback thresholds.")
        return 14.0, 1.0, 17.0  # Fallback: mean, std, limit
        
    df = pd.read_csv(csv_path)
    route_mean = float(df["duration_hours"].mean())
    route_std = float(df["duration_hours"].std())
    
    # Day 89: 3-Sigma Rule Optimization Threshold Boundary Gate
    # Upper statistical limit = Mean + (3 * Standard Deviation)
    upper_statistical_gate = route_mean + (3 * route_std)
    
    return route_mean, route_std, upper_statistical_gate