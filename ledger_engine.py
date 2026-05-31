import geospatial_filter 
import alert_coordinator
import datetime
import hashlib
import pprint
import temporal_analyzer

# --- WEEK 8 CRYPTOGRAPHY IMPORTS ---
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

# =====================================================================
# --- CRYPTOGRAPHIC UTILITY ENCAPSULATION ---
# =====================================================================
def calculate_block_hash(block):
    location = str(block.get("location", "UNKNOWN"))
    weight = str(block.get("cargo_weight_kg", 0.0))
    serial = str(block.get("container_serial", "🚨 UNKNOWN"))
    prev_hash = str(block.get("previous_hash", ""))
    nonce = str(block.get("nonce", 0))
    # Day 74: Append new spatial parameters into the hash calculation pattern
    lat = str(block.get("current_lat", 0.0))
    lon = str(block.get("current_lon", 0.0))

    combined_string = location + weight + serial + prev_hash + nonce + lat + lon
    return hashlib.sha256(combined_string.encode('utf-8')).hexdigest()


# =====================================================================
# --- MINING PROOF-OF-WORK STUB (Required for Block Generation) ---
# =====================================================================
def execute_proof_of_work(block, difficulty=3):
    """Simple mining loop stub to allow the block generation process to succeed."""
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
    print("====================================")
    print("AEO SMART SUPPLY CHAIN LEDGER ONLINE")
    print("====================================")


# Master database ledger array list
blockchain_ledger = []


# =====================================================================
# --- DAY 36: ASYMMETRIC KEY LOADING UTILITIES ---
# =====================================================================
def load_system_keys():
    """
    Loads local PEM files back into runtime active memory objects.
    Returns a tuple: (private_key, public_key)
    """
    try:
        # Load Private Key
        with open("factory_private_key.pem", "rb") as priv_file:
            private_key = serialization.load_pem_private_key(
                priv_file.read(),
                password=None
            )
        
        # Load Public Key
        with open("customs_public_key.pem", "rb") as pub_file:
            public_key = serialization.load_pem_public_key(
                pub_file.read()
            )
            
        print("🔑 [SECURITY] Cryptographic Key Materials Loaded Successfully Into Runtime Memory.")
        return private_key, public_key
    except FileNotFoundError:
        print("🚨 [CRITICAL] Key files missing! Run security_vault.py first to generate keys.")
        return None, None


# =====================================================================
# --- DAY 37: RE-ENGINEERED RSA SIGNATURE GENERATION ---
# =====================================================================
def sign_cargo_manifest(private_key, data_string):
    """
    Encrypts a block text footprint using the private key.
    Returns a hexadecimal signature string payload.
    """
    encoded_payload = data_string.encode('utf-8')
    
    # Generate raw binary signature using enterprise PSS padding
    raw_signature = private_key.sign(
        encoded_payload,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    # Convert binary payload to hex string format for easy display
    return raw_signature.hex()


# =====================================================================
# --- DAY 39: RSA ASYMMETRIC VERIFICATION ENGINE ---
# =====================================================================
def verify_cargo_signature(public_key, block):
    """
    Decrypts the signature token using the public key and verifies authenticity.
    Returns True if valid, False if altered/forged.
    """
    signature_hex = block.get("digital_signature", "")
    if not signature_hex or signature_hex == "UNSIGNED_UNSECURED_SANDBOX_NODE":
        print(f"❌ Verification Failed on Block #{block.get('block_id')}: No authentic signature payload found!")
        return False
        
    location = str(block.get("location", "UNKNOWN"))
    weight = str(block.get("cargo_weight_kg", 0.0))
    serial = str(block.get("container_serial", "🚨 UNKNOWN"))
    prev_hash = str(block.get("previous_hash", ""))
    
    # Mirror identical structural tracking signature footprint string
    lat = str(block.get("current_lat", 22.2500))
    lon = str(block.get("current_lon", 114.1000))
    reconstructed_footprint = location + weight + serial + prev_hash + str(block.get("nonce", 0)) + lat + lon
    
    try:
        signature_bytes = bytes.fromhex(signature_hex)
        
        public_key.verify(
            signature_bytes,
            reconstructed_footprint.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        print(f"🚨 [ALERT] FORGERY OR DATA TAMPERING DETECTED ON NODE #{block.get('block_id')}!")
        return False


# =====================================================================
# --- UNIFIED SYSTEM INTEGRITY AUDIT LOOP (Layers 1 - 5) ---
# =====================================================================
def run_system_integrity_audit(ledger, public_key=None):
    """
    Audits the entire ledger. If a compromise is hit, it drops the compromised block
    from the live list, dispatches a frontline alert, and dumps the evidence to a JSON file.
    """
    print("\n🔍 [AUDIT] Initializing Continuous Master Security Audit Scan...")
    
    if not ledger:
        print("ℹ️ Ledger is completely empty. Scan skipped.")
        return False

    is_compromised = False

    # Using an index-controlled scan so we can modify the list safely
    idx = 1
    while idx < len(ledger):
        current_block = ledger[idx]
        parent_block = ledger[idx - 1]
        
        # --- LAYER 1: CHAINING LINK VALIDATION ---
        stored_prev_hash = current_block.get("previous_hash", "")
        actual_parent_hash = parent_block.get("block_hash", "")
        
        if stored_prev_hash != actual_parent_hash:
            violation = "Cryptographic Chain Link Break"
            is_compromised = True
            
            alert_coordinator.dispatch_customs_alarm(violation, current_block)
            alert_coordinator.quarantine_corrupted_manifest(current_block, violation)
            ledger.pop(idx)
            break

        # --- LAYER 2: DATA RECALCULATION VALIDATION ---
        stored_current_hash = current_block.get("block_hash", "")
        recalculated_hash = calculate_block_hash(current_block)
        
        if stored_current_hash != recalculated_hash:
            violation = "Internal Parameter Data Manipulation"
            is_compromised = True
            
            alert_coordinator.dispatch_customs_alarm(violation, current_block)
            alert_coordinator.quarantine_corrupted_manifest(current_block, violation)
            ledger.pop(idx)
            break

        # --- LAYER 3: RSA DIGITAL SIGNATURE VALIDATION ---
        if public_key:
            is_signature_valid = verify_cargo_signature(public_key, current_block)
            if not is_signature_valid:
                violation = "Asymmetric RSA Signature Forgery / Invalid Authorship"
                is_compromised = True
                
                alert_coordinator.dispatch_customs_alarm(violation, current_block)
                alert_coordinator.quarantine_corrupted_manifest(current_block, violation)
                ledger.pop(idx)
                break

        # --- LAYER 4: REAL-TIME SPATIAL CORRIDOR COMPLIANCE CHECK ---
        lat = current_block.get("current_lat", 0.0)
        lon = current_block.get("current_lon", 0.0)
        
        is_spatial_valid, deviation_dist = geospatial_filter.check_spatial_corridor_compliance(lat, lon)
        risk_profile, risk_msg = geospatial_filter.classify_spatial_risk_severity(deviation_dist)
        
        if risk_profile == "HIGH_RISK_DEVIATION":
            violation = f"High-Risk Route Deviation Anomaly ({risk_msg})"
            is_compromised = True
            
            alert_coordinator.dispatch_customs_alarm(violation, current_block)
            alert_coordinator.quarantine_corrupted_manifest(current_block, violation)
            ledger.pop(idx)
            break

        # --- LAYER 5: REAL-TIME TEMPORAL ANALYTICS CHECK ---
        parent_time = parent_block.get("timestamp")
        current_time = current_block.get("timestamp")
        
        elapsed_transit_hours = temporal_analyzer.calculate_time_delta(parent_time, current_time)
        
        if elapsed_transit_hours is not None:
            mean, std, limit = temporal_analyzer.compute_route_thresholds()
            
            print(f"⏱️  [TIME LOG] Transit from Block #{parent_block['block_id']} to #{current_block['block_id']} took {elapsed_transit_hours:.2f} hours. (Dynamic Statistical Gate: {limit:.2f}h)")
            
            if elapsed_transit_hours > limit:
                violation = f"High-Risk Temporal Anomaly (Transit took {elapsed_transit_hours:.2f}h | Exceeded 3-Sigma Limit of {limit:.2f}h)"
                is_compromised = True
                
                alert_coordinator.dispatch_customs_alarm(violation, current_block)
                alert_coordinator.quarantine_corrupted_manifest(current_block, violation)
                ledger.pop(idx)
                break
                
        idx += 1
                
    if not is_compromised:
        print(f"✅ [AUDIT SUCCESS] All nodes parsed smoothly. Ledger state verified as CLEAN.")
        
    return is_compromised


# =====================================================================
# --- DAY 38: UPDATED BUILDER INTEGRATING SECURITY OBJECTS ---
# =====================================================================
def create_transit_block(location, weight, cargo_type, serial, previous_hash, current_lat=22.2500, current_lon=114.1000, private_key=None, aeo_id="HK-AEO-2026-DEFAULT"):
    parsed_weight = float(weight)
    sanitized_weight = abs(parsed_weight)
    millisecond_timestamp = datetime.datetime.now().isoformat()
    dynamic_id = len(blockchain_ledger)
    
    new_block = {
        "block_id": dynamic_id,
        "timestamp": millisecond_timestamp,
        "location": location,
        "aeo_company_id": aeo_id,
        "destination_port": "Kwai Tsing Container Terminal 4",
        "container_serial": serial,
        "cargo_weight_kg": sanitized_weight, 
        "cargo_type": cargo_type,
        "status": "CHAINED LOGISTICS NODE",
        "previous_hash": previous_hash,
        "current_lat": float(current_lat),
        "current_lon": float(current_lon),
        "nonce": 0  
    }
    
    new_block["block_hash"] = execute_proof_of_work(new_block, difficulty=3)
    
    if private_key:
        footprint_string = str(location) + str(sanitized_weight) + str(serial) + str(previous_hash) + str(new_block["nonce"]) + str(float(current_lat)) + str(float(current_lon))
        new_block["digital_signature"] = sign_cargo_manifest(private_key, footprint_string)
    else:
        new_block["digital_signature"] = "UNSIGNED_UNSECURED_SANDBOX_NODE"
        
    return new_block


def safe_display_block(block):
    serial = block.get("container_serial", "🚨 UNKNOWN_SERIAL")
    weight = block.get("cargo_weight_kg", 0.0)
    aeo_id = block.get("aeo_company_id", "⚠️ UNREGISTERED_AEO")
    print(f"Safe Log -> Serial: {serial} | Weight: {weight} KG | AEO ID: {aeo_id}")


def run_customs_terminal_portal(priv_key):
    print("\n⌨️  HONG KONG CUSTOMS INTERACTIVE INTAKE PORTAL")
    user_location = input("Enter current checkpoint node location: ")
    user_weight = input("Enter declared container cargo weight (KG): ")
    interactive_block = create_transit_block(user_location, user_weight, "Standard AEO Cargo", "MSKU9918273", blockchain_ledger[-1]["block_hash"], private_key=priv_key)
    blockchain_ledger.append(interactive_block)
    print("✅ TRANSACTION SECURELY RECORDED")


# =====================================================================
# --- EXECUTION ENGINE CONTROL WINDOW ---
# =====================================================================
if __name__ == "__main__":
    initialize_system()
    print(f"Ledger Initialized. Current Block Height: {len(blockchain_ledger)}")
    
    # Load keys safely within runtime block
    priv_key, pub_key = load_system_keys()

    # --- PHASE 1: MANUAL MULTI-NODE TRANSIT CHECKPOINTS ---
    h_node_0 = create_transit_block("Guangdong AEO Manufacturing Hub", 15000.0, "High-Density Electronics", "MSKU9918273", previous_hash="0", private_key=priv_key, aeo_id="HK-AEO-2026-0891")
    blockchain_ledger.append(h_node_0)

    h_node_1 = create_transit_block("Port of Shenzhen (Yantian)", 15000.0, "High-Density Electronics", "MSKU9918273", previous_hash=h_node_0["block_hash"], private_key=priv_key, aeo_id="SZ-PORT-2026-4403")
    blockchain_ledger.append(h_node_1)

    h_node_2 = create_transit_block("Kwai Tsing Container Terminal 4, HK", 15000.0, "High-Density Electronics", "MSKU9918273", previous_hash=h_node_1["block_hash"], private_key=priv_key, aeo_id="HK-TERMINAL-2026-0042")
    blockchain_ledger.append(h_node_2)

    # --- GEOGRAPHIC PATH PARSING PIPELINE ---
    print("\n" + "🌐" * 20)
    print(" LIVE SUPPLY CHAIN GEOGRAPHIC TRAIL AUDIT")
    print("🌐" * 20)
    for block in blockchain_ledger:
        print(f"📍 [{block.get('timestamp')}] -> Container moved to: {block.get('location')}")

    # --- SUPPLY CHAIN WEIGHT INTEGRITY AUDIT ---
    print("\n" + "⚖️ " * 20)
    print(" LIVE SUPPLY CHAIN WEIGHT INTEGRITY AUDIT")
    print("⚖️ " * 20)
    previous_weight = None
    for block in blockchain_ledger:
        current_weight = block.get("cargo_weight_kg", 0.0)
        if previous_weight is not None:
            delta = current_weight - previous_weight
            print(f"✅ Weight Verified at {block.get('location')}: {current_weight} KG (Delta: {delta} KG)")
        else:
            print(f"🏁 Base Weight Established at {block.get('location')}: {current_weight} KG")
        previous_weight = current_weight

    # --- TESTING CELL: SANITIZATION & CLOCK SPEED ---
    print("\n" + "🔋 " * 20)
    print(" TESTING MILLISECOND STAMPS & WEIGHT DEFENSE")
    print("🔋 " * 20)
    dynamic_checkpoint = create_transit_block(
        location="Tuen Mun River Trade Terminal, HK", weight=-19450.80, cargo_type="Medical Devices",
        serial="MSKU9918273", previous_hash=blockchain_ledger[-1]["block_hash"], private_key=priv_key
    )
    blockchain_ledger.append(dynamic_checkpoint)
    safe_display_block(dynamic_checkpoint)

    # --- DAY 20: VELOCITY STRESS CHECK PIPELINE ---
    print("\n" + "⚡ " * 20)
    print(" RUNNING SYSTEM CLOCK VELOCITY STRESS CHECK")
    print("⚡ " * 20)
    for i in range(3):
        stress_block = create_transit_block(f"Stress Node-{i}", 20000.0, "Stress Packets", "MSKU9918273", blockchain_ledger[-1]["block_hash"], private_key=priv_key)
        blockchain_ledger.append(stress_block)

    # --- DAYS 27-29: AUTOMATED COUPLING PIPELINE ---
    raw_logistics_data = [
        {"loc": "Guangdong AEO Warehouse A", "wt": 15000.0, "type": "High-Density Electronics"},
        {"loc": "Port of Shenzhen (Yantian)", "wt": 15000.0, "type": "High-Density Electronics"},
        {"loc": "Kwai Tsing Container Terminal 4, HK", "wt": 15000.0, "type": "High-Density Electronics"}
    ]
    for record in raw_logistics_data:
        linked_block = create_transit_block(record["loc"], record["wt"], record["type"], "MSKU9918273", blockchain_ledger[-1]["block_hash"], private_key=priv_key)
        blockchain_ledger.append(linked_block)

    # --- INTERACTIVE PORTAL TRIGGER ---
    run_customs_terminal_portal(priv_key)
    
    # -----------------------------------------------------------------
    # 🏁 STAGE 4: INTEGRATED GEOSPATIAL CORRIDOR SIMULATION
    # -----------------------------------------------------------------
    print("\n" + "="*52)
    print(" STAGE 4: INTEGRATED GEOSPATIAL CORRIDOR SIMULATION")
    print("="*52)
    
    spatial_test_ledger = []
    
    print("\n🚢 Minting Vessel Block Alpha (On-Track Shipping Lane)...")
    b_alpha = create_transit_block("Lamma Channel Approach", 15000.0, "Electronics", "MSKU9918273", "0", current_lat=22.2100, current_lon=114.0700, private_key=priv_key)
    spatial_test_ledger.append(b_alpha)
    
    print("\n🚢 Minting Vessel Block Beta (Slightly Drifted Edge - Low Risk)...")
    b_beta = create_transit_block("Outer Channel Flank", 15000.0, "Electronics", "MSKU9918273", b_alpha["block_hash"], current_lat=22.2600, current_lon=114.0400, private_key=priv_key)
    spatial_test_ledger.append(b_beta)
    
    print("\n🚢 Minting Vessel Block Gamma (Severely Deviated Smuggling Blackspot)...")
    b_gamma = create_transit_block("Unapproved Shoreline Incursion", 15000.0, "Electronics", "MSKU9918273", b_beta["block_hash"], current_lat=22.5100, current_lon=113.7200, private_key=priv_key)
    spatial_test_ledger.append(b_gamma)
    
    print(f"\n🛂 Executing Spatial Path Audit Validation...")
    run_system_integrity_audit(spatial_test_ledger, pub_key)
    print(f"📦 Final Spatial Ledger Height: {len(spatial_test_ledger)} Blocks.")

    # -----------------------------------------------------------------
    # 🏁 STAGE 5: TEMPORAL ANOMALY PROFILING SIMULATION
    # -----------------------------------------------------------------
    print("\n" + "="*52)
    print(" STAGE 5: TEMPORAL ANOMALY PROFILING SIMULATION")
    print("="*52)
    
    mean, std, upper_gate = temporal_analyzer.compute_route_thresholds()
    print(f"📊 Baseline Gate: {upper_gate:.2f} Hours Allowed Max.")
    
    temporal_test_ledger = []
    time_start = datetime.datetime(2026, 5, 31, 10, 0, 0)
    time_normal = datetime.datetime(2026, 6, 1, 0, 0, 0)    # ✅ Handled rollover context cleanly (14h delta)
    time_delayed = datetime.datetime(2026, 6, 2, 14, 0, 0)   # 38 Hours (Fail window)

    print("\n📦 Minting Node 0 (Origin Point)...")
    t_node_0 = create_transit_block("Shenzhen Port", 12000, "Apparel", "SZ-991", "0")
    t_node_0["timestamp"] = time_start.isoformat()
    temporal_test_ledger.append(t_node_0)
    
    print("\n🚢 Minting Node 1 (Standard Compliant Voyage - 14 Hours)...")
    t_node_1 = create_transit_block("HK Entrance Alpha", 12000, "Apparel", "SZ-991", t_node_0["block_hash"])
    t_node_1["timestamp"] = time_normal.isoformat()
    temporal_test_ledger.append(t_node_1)
    
    print("\n🚢 Minting Node 2 (Critical Delayed Voyage - 38 Hours Anomaly)...")
    t_node_2 = create_transit_block("Kwai Tsing Terminal", 12000, "Apparel", "SZ-991", t_node_1["block_hash"])
    t_node_2["timestamp"] = time_delayed.isoformat()
    temporal_test_ledger.append(t_node_2)

    print(f"\n🛂 Executing Temporal Path Audit Validation...")
    run_system_integrity_audit(temporal_test_ledger, pub_key)
    print(f"📦 Final Temporal Ledger Height: {len(temporal_test_ledger)} Blocks.")
    print("=" * 52)