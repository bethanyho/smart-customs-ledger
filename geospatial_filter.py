# =====================================================================
# --- WEEKS 15 & 16: GEOSPATIAL FILTER INTELLIGENCE MODULE ---
# =====================================================================
# Day 72: Import geometric structural classes from shapely
from shapely.geometry import Polygon, Point

# Day 73: Define a high-precision safe maritime shipping corridor entering HK waters
# Coordinates follow a realistic entry path from outer waters toward Kwai Tsing
HK_SAFE_SHIPPING_CORRIDOR_COORDINATES = [
    (22.1500, 114.0000),  # Southern Entry Gate Point A
    (22.1800, 114.0500),  # Channel Guideway Point B
    (22.2500, 114.1000),  # Lamma Channel Approach Point C
    (22.3200, 114.1200),  # Victoria Harbour West Gate Point D
    (22.3400, 114.1100),  # Kwai Tsing Terminal Berth Buffer
    (22.2800, 114.0600),  # West Lamma Boundary Flank
    (22.1600, 113.9800)   # Outermost Boundary Flank
]

# Instantiate the digital geofence Polygon object globally
SAFE_CORRIDOR = Polygon(HK_SAFE_SHIPPING_CORRIDOR_COORDINATES)


def check_spatial_corridor_compliance(current_lat, current_lon, safe_corridor_polygon=SAFE_CORRIDOR):
    """
    Day 75: Evaluates whether a ship's current GPS coordinate location Point falls 
    safely inside the designated safe maritime corridor polygon.
    Returns: Tuple (is_inside: bool, distance_deg: float)
    """
    # Create an active tracking point object from real-time coordinates
    vessel_point = Point(current_lat, current_lon)
    
    # Check containment compliance using the native .contains() method
    is_inside = safe_corridor_polygon.contains(vessel_point)
    
    if is_inside:
        return True, 0.0
    else:
        # Day 76: Calculate distance from the point to the nearest edge of the polygon corridor
        # Note: In a raw production app, this degree value is converted to KM via Haversine,
        # but for our simulation threshold, we use decimal degree distance units.
        deviation_distance = vessel_point.distance(safe_corridor_polygon)
        return False, deviation_distance


def classify_spatial_risk_severity(deviation_distance, threshold=0.03):
    """
    Days 77 & 78: Classifies the operational threat profile based on boundary proximity.
    Threshold 0.03 degrees translates roughly to a ~3.2 KM buffer zone in South China.
    """
    if deviation_distance == 0.0:
        return "NORMAL_OPERATION", "Low Risk: Inside Safe Channel Lanes."
    elif deviation_distance <= threshold:
        # Day 77: Minor navigational adjustments
        return "MINOR_ADJUSTMENT", "Low Risk: Minor route deviation detected. Vessel adjusting path."
    else:
        # Day 78: Intentional detour toward unapproved coastlines/blackspots
        return "HIGH_RISK_DEVIATION", "CRITICAL Threat: Severe route anomaly toward unauthorized shoreline!"