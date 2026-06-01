import geospatial_filter 
import alert_coordinator
import datetime
import hashlib
import pprint
import temporal_analyzer
import os

# --- WEEK 8 CRYPTOGRAPHY IMPORTS ---
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

# =====================================================================
# --- WEEK 19: GLOBAL ENVIRONMENTAL TOGGLES ---
# =====================================================================
# Day 91: Global configuration dictionary for atmospheric contextual awareness
ENVIRONMENT_SETTINGS = {
    "typhoon_active": False
}

# Master database ledger array list
blockchain_ledger = []


# =====================================================================
# --- CRYPTOGRAPHIC UTILITY ENCAPSULATION ---
# =====================================================================
def calculate_block_hash(block):
    location = str(block.get("location", "UNKNOWN"))
    weight = str(block.get("cargo_weight_kg", 0.0))
    serial = str(block.get("container_serial", "🚨 UNKNOWN"))
    prev_hash = str(block.get("previous_hash", ""))
    nonce = str(block.get("nonce", 0))
    lat = str(block.get("current_lat", 0.0))
    lon = str(block.get("current_lon", 0.0))

    combined_string = location + weight + serial + prev_hash + nonce + lat + lon
    return hashlib.sha256(combined_string.encode('utf-8')).hexdigest()


def execute_proof_of_work(block, difficulty=3):
    target_prefix = "0" * difficulty
    block_copy = block.copy()
    while True:
        combined = (str(block_copy.get("location")) + str(block_copy.get("cargo_weight_kg")) + 
                    str(block_copy.get("container_serial")) + str(block_copy.get("previous_hash")) + 
                    str(block_copy.get("nonce")) + str(block_copy.get("current_lat")) + str(block_copy.get("current_lon")))
        computed_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        if computed_hash.startswith(target_prefix):
            return computed_hash
        block_copy["nonce"] += 1


def initialize_system():
    print("=========================================================")
    print("AEO SMART SUPPLY CHAIN LEDGER - PHASE 3 SECURE CORE READY")
    print("=========================================================")


def load_system_keys():
    try:
        with open("factory_private_key.pem", "rb") as priv_file:
            private_key = serialization.load_pem_private_key(priv_file.read(), password=None)
        with open("customs_public_key.pem", "rb") as pub_file:
            public_key = serialization.load_pem_public_key(pub_file.read())
        print("🔑 [SECURITY] Cryptographic Key Materials Loaded Successfully Into Runtime Memory.")
        return private_key, public_key
    except FileNotFoundError:
        print("🚨 [CRITICAL] Key files missing! Run security_vault.py first to generate keys.")
        return None, None


def sign_cargo_manifest(private_key, data_string):
    encoded_payload = data_string.encode('utf-8')
    raw_signature = private_key.sign(
        encoded_payload,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return raw_signature.hex()


def verify_cargo_signature(public_key, block):
    signature_hex = block.get("digital_signature", "")
    if not signature_hex or signature_hex == "UNSIGNED_UNSECURED_SANDBOX_NODE":
        return False
        
    location = str(block.get("location", "UNKNOWN"))
    weight = str(block.get("cargo_weight_kg", 0.0))
    serial = str(block.get("container_serial", "🚨 UNKNOWN"))
    prev_hash = str(block.get("previous_hash", ""))
    lat = str(block.get("current_lat", 22.2500))
    lon = str(block.get("current_lon", 114.1000))
    reconstructed_footprint = location + weight + serial + prev_hash + str(block.get("nonce", 0)) + lat + lon
    
    try:
        signature_bytes = bytes.fromhex(signature_hex)
        public_key.verify(
            signature_bytes,
            reconstructed_footprint.encode('utf-8'),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


# =====================================================================
# --- WEEK 19: UNIFIED TEMPORAL RISK MODULE ---
# =====================================================================
def evaluate_temporal_risk(parent_block, current_block):
    """
    Day 95: Aggregates time parsing, 3-sigma thresholds, and typhoon mitigations 
    to output structured contextual risk analysis.
    Returns: (is_anomaly, message)
    """
    parent_time = parent_block.get("timestamp")
    current_time = current_block.get("timestamp")
    
    elapsed_transit_hours = temporal_analyzer.calculate_time_delta(parent_time, current_time)
    if elapsed_transit_hours is None:
        return False, "Initial tracking link establishing baseline."

    # Retrieve base dynamic limits calculated from historical data
    _, _, base_limit = temporal_analyzer.compute_route_thresholds()
    
    # Day 92: Apply condition to step up dynamic window limit during typhoons
    if ENVIRONMENT_SETTINGS.get("typhoon_active", False):
        allowed_limit = base_limit * 2.5
    else:
        allowed_limit = base_limit

    # Evaluation phase
    if elapsed_transit_hours > allowed_limit:
        # If breach matches a genuine timing issue outside context parameters
        return True, f"High-Risk Temporal Anomaly ({elapsed_transit_hours:.2f}h vs limit {allowed_limit:.2f}h)"
    
    elif elapsed_transit_hours > base_limit and ENVIRONMENT_SETTINGS.get("typhoon_active", False):
        # Day 94: Log tracking event to note weather suppression condition
        print("⚠️  [ENVIRONMENT LOG] Transit Delay Noted but Suppressed: Severe Weather Protocol Active")
        return False, "Delay accepted due to Typhoon condition."

    return False, f"Compliant transit window ({elapsed_transit_hours:.2f}h / {allowed_limit:.2f}h limit)."


# =====================================================================
# --- WEEK 20: SPACE-TIME INTEL CORRELATION (THE ANCHOR ALERT) ---
# =====================================================================
def detect_illegal_anchorage(block):
    """
    Day 97 & 98: Evaluates geographic location and speed metrics to detect 
    clandestine mid-sea hovering anomalies.
    """
    lat = block.get("current_lat", 0.0)
    lon = block.get("current_lon", 0.0)
    speed_knots = block.get("vessel_speed_knots", 12.0)
    hours_stationary = block.get("hours_stationary", 0.0)

    # Day 96 & 97: Check spatial lane intersection via geospatial filter module
    is_spatial_valid, _ = geospatial_filter.check_spatial_corridor_compliance(lat, lon)
    
    # Check if ship has dropped velocity while drifting out of bounds
    if not is_spatial_valid and 0.0 <= speed_knots <= 2.0:
        # Day 98: Cross-reference tracking window durations inside risk pocket
        if hours_stationary > 3.0:
            return "CRITICAL: PROBABLE OFFSHORE CONTRABAND TRANSFER"
        return "WARNING: SUSPICIOUS STATIONARY DRIFT DETECTED"
        
    return "SAFE_STATUS"


# =====================================================================
# --- INTEGRITY AUDIT RE-ENGINEERING ---
# =====================================================================
def run_system_integrity_audit(ledger, public_key=None):
    print("\n🔍 [AUDIT] Running Secure Pipeline Validation Suite...")
    if not ledger:
        return False

    is_compromised = False
    idx = 1
    
    while idx < len(ledger):
        current_block = ledger[idx]
        parent_block = ledger[idx - 1]
        violation = None

        # 1. Cryptographic Chain Links
        if current_block.get("previous_hash") != parent_block.get("block_hash"):
            violation = "Cryptographic Chain Link Break"
        
        # 2. Key Payload Integrity
        elif current_block.get("block_hash") != calculate_block_hash(current_block):
            violation = "Internal Parameter Data Manipulation"
            
        # 3. Asymmetric RSA Verification 
        elif public_key and not verify_cargo_signature(public_key, current_block):
            violation = "Asymmetric RSA Signature Forgery / Invalid Authorship"
            
        # 4. Week 20: Space-Time Anchorage Check
        else:
            anchorage_status = detect_illegal_anchorage(current_block)
            if anchorage_status == "CRITICAL: PROBABLE OFFSHORE CONTRABAND TRANSFER":
                violation = anchorage_status

        # 5. Week 19: Contextual Environmental Check
        if not violation:
            is_time_anomaly, time_msg = evaluate_temporal_risk(parent_block, current_block)
            if is_time_anomaly:
                violation = time_msg

        # Route to Quarantine Container Terminal Pipeline if any check triggers a violation
        if violation:
            is_compromised = True
            print(f"🚨 [PIPELINE INCIDENT FLAG] {violation}")
            alert_coordinator.dispatch_customs_alarm(violation, current_block)
            # Day 100: Ensure direct hand-off to Month 4 file archiving tracking system
            alert_coordinator.quarantine_corrupted_manifest(current_block, violation)
            ledger.pop(idx)
            break
        idx += 1
                
    if not is_compromised:
        print(f"✅ [AUDIT CLEAN] State validated successfully.")
    return is_compromised


def create_transit_block(location, weight, cargo_type, serial, previous_hash, current_lat=22.2500, current_lon=114.1000, speed=14.0, station_hours=0.0, private_key=None):
    new_block = {
        "block_id": len(blockchain_ledger),
        "timestamp": datetime.datetime.now().isoformat(),
        "location": location,
        "container_serial": serial,
        "cargo_weight_kg": abs(float(weight)), 
        "cargo_type": cargo_type,
        "previous_hash": previous_hash,
        "current_lat": float(current_lat),
        "current_lon": float(current_lon),
        "vessel_speed_knots": float(speed),
        "hours_stationary": float(station_hours),
        "nonce": 0  
    }
    new_block["block_hash"] = execute_proof_of_work(new_block, difficulty=3)
    if private_key:
        fp = str(location) + str(new_block["cargo_weight_kg"]) + str(serial) + str(previous_hash) + str(new_block["nonce"]) + str(float(current_lat)) + str(float(current_lon))
        new_block["digital_signature"] = sign_cargo_manifest(private_key, fp)
    else:
        new_block["digital_signature"] = "UNSIGNED_UNSECURED_SANDBOX_NODE"
    return new_block


def run_customs_terminal_portal(priv_key):
    """Encapsulated inside code setup so that running automated non-interactive tasks won't freeze."""
    print("\n⌨️  HONG KONG CUSTOMS INTERACTIVE INTAKE PORTAL")
    user_location = input("Enter current checkpoint node location: ")
    user_weight = input("Enter declared container cargo weight (KG): ")
    interactive_block = create_transit_block(user_location, user_weight, "Standard AEO Cargo", "MSKU9918273", blockchain_ledger[-1]["block_hash"], private_key=priv_key)
    blockchain_ledger.append(interactive_block)
    print("✅ TRANSACTION SECURELY RECORDED")


# =====================================================================
# --- AUTOMATED VALIDATION SUITE ---
# =====================================================================
if __name__ == "__main__":
    initialize_system()
    priv_key, pub_key = load_system_keys()

    # -----------------------------------------------------------------
    # 🏁 WEEK 19 TESTING: WEATHER CONTEXT SIMULATION
    # -----------------------------------------------------------------
    print("\n" + "="*52)
    print(" STAGE 5: WEATHER CONTEXT & TYPHOON SUPPRESSION TESTS")
    print("="*52)
    
    # Day 93: Turn on Severe Weather protocol
    ENVIRONMENT_SETTINGS["typhoon_active"] = True
    print("🌀 ENVIRONMENT STATUS: Severe Typhoon Protocol Initialized.")
    
    weather_ledger = []
    t_start = datetime.datetime(2026, 5, 31, 10, 0, 0)
    t_delayed = datetime.datetime(2026, 6, 1, 18, 0, 0)  # 32 Hours Total Transit Delta
    
    w_node_0 = create_transit_block("Shenzhen Port Terminal", 15000, "Electronics", "MSKU-W1", "0")
    w_node_0["timestamp"] = t_start.isoformat()
    weather_ledger.append(w_node_0)
    
    w_node_1 = create_transit_block("Kwai Tsing Terminal 4", 15000, "Electronics", "MSKU-W1", w_node_0["block_hash"])
    w_node_1["timestamp"] = t_delayed.isoformat()
    weather_ledger.append(w_node_1)
    
    # Run audit - Should pass seamlessly as the alarm is suppressed
    run_system_integrity_audit(weather_ledger, pub_key)
    print(f"📦 Weather Ledger Height: {len(weather_ledger)} Blocks (No drops occurred).")

    # -----------------------------------------------------------------
    # 🏁 WEEK 20 TESTING: ANCHOR ALERT SPACE-TIME FUSION
    # -----------------------------------------------------------------
    print("\n" + "="*52)
    print(" STAGE 6: GEOSPATIAL ANCHOR ANOMALY INCIDENT DETECTION")
    print("="*52)
    
    # Revert weather status to default track
    ENVIRONMENT_SETTINGS["typhoon_active"] = False
    fusion_ledger = []
    
    print("\n🚢 Step 1: Vessel traveling inside normal coordinates...")
    f_node_0 = create_transit_block("Lamma Channel Lane", 22000, "Apparel", "MSKU-F1", "0", current_lat=22.2100, current_lon=114.0700, speed=15.5)
    fusion_ledger.append(f_node_0)
    
    # Day 99: Drop positioning coordinates inside unapproved Lantau Island border lane, 
    # dropping speed down to 0.5 knots for a 5-hour duration
    print("\n🚢 Step 2: Tracking suspicious anchorage deployment (Lantau Coast)...")
    f_node_1 = create_transit_block(
        location="Unapproved Lantau Off-Grid Incursion", 
        weight=22000, 
        cargo_type="Apparel", 
        serial="MSKU-F1", 
        previous_hash=f_node_0["block_hash"], 
        current_lat=22.5100,      # Out of bounds coordinate axis 
        current_lon=113.7200, 
        speed=0.5,                # Low velocity footprint
        station_hours=5.0         # Hover duration > 3 Hours limit
    )
    fusion_ledger.append(f_node_1)
    
    print(f"\n🛂 Passing tracking records into secure defense grid...")
    run_system_integrity_audit(fusion_ledger, pub_key)
    
    # Verified: The malicious node drops immediately from live runtime ledger structure
    print(f"📦 Phase 3 Complete Tracker: {len(fusion_ledger)} Nodes retained inside verified state.")
    print("=" * 52)