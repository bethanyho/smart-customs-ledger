import geospatial_filter 
import alert_coordinator
import datetime
import hashlib
import pprint

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




def initialize_system():
    print("====================================")
    print("AEO SMART SUPPLY CHAIN LEDGER ONLINE")
    print("====================================")

initialize_system()

# Master database ledger array list
blockchain_ledger = []

print(f"Ledger Initialized. Current Block Height: {len(blockchain_ledger)}")


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
    reconstructed_footprint = location + weight + serial + prev_hash
    
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
# --- WEEKS 9 & 10: UNIFIED SYSTEM INTEGRITY AUDIT LOOP (📍 ADDED HERE) ---
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

    # Using a while loop or an index-controlled scan so we can modify the list safely
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
            
            # Week 13: Dispatch terminal alarm frame
            alert_coordinator.dispatch_customs_alarm(violation, current_block)
            # Week 14: Route to disk quarantine file
            alert_coordinator.quarantine_corrupted_manifest(current_block, violation)
            # Week 14: Evict compromised node from live runtime ledger
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
        # Day 74 & 79: Extract the spatial coordinates from the block layout
        lat = current_block.get("current_lat", 0.0)
        lon = current_block.get("current_lon", 0.0)
        
        # Pass the extracted points through your Day 75 & Day 76 compliance math
        is_spatial_valid, deviation_dist = geospatial_filter.check_spatial_corridor_compliance(lat, lon)
        risk_profile, risk_msg = geospatial_filter.classify_spatial_risk_severity(deviation_dist)
        
        # Day 78 & 79: If the detour severity crosses our threshold, route to containment
        if risk_profile == "HIGH_RISK_DEVIATION":
            violation = f"High-Risk Route Deviation Anomaly ({risk_msg})"
            is_compromised = True
            
            # Fire the alarm framework and isolate the block
            alert_coordinator.dispatch_customs_alarm(violation, current_block)
            alert_coordinator.quarantine_corrupted_manifest(current_block, violation)
            ledger.pop(idx)
            break
                
        idx += 1
                
    if not is_compromised:
        print(f"✅ [AUDIT SUCCESS] All {len(ledger)} nodes parsed smoothly. Ledger state verified as CLEAN.")
        
    return is_compromised
# =====================================================================
# --- DAY 38: UPDATED BUILDER INTEGRATING SECURITY OBJECTS ---
# =====================================================================
def create_transit_block(location, weight, cargo_type, serial, previous_hash, current_lat=22.2500, current_lon=114.1000, private_key=None, aeo_id="HK-AEO-2026-DEFAULT"):
    parsed_weight = float(weight)
    sanitized_weight = abs(parsed_weight)
    millisecond_timestamp = str(datetime.datetime.now())
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
        # Day 74: Insert coordinates inside structural layout fields
        "current_lat": float(current_lat),
        "current_lon": float(current_lon),
        "nonce": 0  
    }
    
    new_block["block_hash"] = execute_proof_of_work(new_block, difficulty=3)
    
    if private_key:
        # Re-construct signature block tracking string identically
        footprint_string = str(location) + str(sanitized_weight) + str(serial) + str(previous_hash) + str(new_block["nonce"]) + str(float(current_lat)) + str(float(current_lon))
        new_block["digital_signature"] = sign_cargo_manifest(private_key, footprint_string)
    else:
        new_block["digital_signature"] = "UNSIGNED_UNSECURED_SANDBOX_NODE"
        
    return new_block


def safe_display_block(block):
    """Prevents system crashes by using .get() fallbacks for missing keys."""
    serial = block.get("container_serial", "🚨 UNKNOWN_SERIAL")
    weight = block.get("cargo_weight_kg", 0.0)
    aeo_id = block.get("aeo_company_id", "⚠️ UNREGISTERED_AEO")
    
    print("\n--- SAFE LOG PRESENTATION ---")
    print(f"Safe Log -> Serial: {serial} | Weight: {weight} KG | AEO ID: {aeo_id}")


# Load the crypto key pairs into active system memory upfront
priv_key, pub_key = load_system_keys()

# =====================================================================
# --- PHASE 1: MANUAL MULTI-NODE TRANSIT CHECKPOINTS ---
# =====================================================================
h_node_0 = create_transit_block("Guangdong AEO Manufacturing Hub", 15000.0, "High-Density Electronics", "MSKU9918273", previous_hash="0", private_key=priv_key, aeo_id="HK-AEO-2026-0891")
blockchain_ledger.append(h_node_0)

h_node_1 = create_transit_block("Port of Shenzhen (Yantian)", 15000.0, "High-Density Electronics", "MSKU9918273", previous_hash=h_node_0["block_hash"], private_key=priv_key, aeo_id="SZ-PORT-2026-4403")
blockchain_ledger.append(h_node_1)

h_node_2 = create_transit_block("Kwai Tsing Container Terminal 4, HK", 15000.0, "High-Density Electronics", "MSKU9918273", previous_hash=h_node_1["block_hash"], private_key=priv_key, aeo_id="HK-TERMINAL-2026-0042")
blockchain_ledger.append(h_node_2)


print("\n--- INITIALIZING PHASE 1 MULTI-NODE LOGISTICS ---")
print(f"Tracking Journey for Container: {blockchain_ledger[0]['container_serial']}")
print(f"-> Node 0: {blockchain_ledger[0]['location']} | Status: CHAINED")
print(f"-> Node 1: {blockchain_ledger[1]['location']} | Status: CHAINED")
print(f"-> Node 2: {blockchain_ledger[2]['location']} | Status: CHAINED")

print("\n--- MASTER LEDGER UPDATE ---")
print(f"📦 Successfully committed Block #0, #1, and #2 sequentially.")
print(f"Absolute Master Ledger Height: {len(blockchain_ledger)} Blocks")


# =====================================================================
# --- GEOGRAPHIC PATH PARSING PIPELINE ---
# =====================================================================
print("\n" + "🌐" * 20)
print(" LIVE SUPPLY CHAIN GEOGRAPHIC TRAIL AUDIT")
print("🌐" * 20)

for block in blockchain_ledger:
    timestamp = block.get("timestamp", "UNKNOWN TIME")
    location = block.get("location", "UNKNOWN LOCATION")
    status = block.get("status", "PROCESSING")
    print(f"📍 [{timestamp}] -> Container moved to: {location} | Status: [{status}]")


# =====================================================================
# --- SUPPLY CHAIN WEIGHT INTEGRITY AUDIT ---
# =====================================================================
print("\n" + "⚖️ " * 20)
print(" LIVE SUPPLY CHAIN WEIGHT INTEGRITY AUDIT")
print("⚖️ " * 20)

previous_weight = None
for block in blockchain_ledger:
    current_weight = block.get("cargo_weight_kg", 0.0)
    location = block.get("location", "UNKNOWN LOCATION")
    
    if previous_weight is not None:
        delta = current_weight - previous_weight
        if delta != 0:
            print(f"🚨 WARNING: Weight Delta Detected at {location}! Change: {delta} KG")
        else:
            print(f"✅ Weight Verified at {location}: {current_weight} KG (Delta: 0.0 KG)")
    else:
        print(f"🏁 Base Weight Established at {location}: {current_weight} KG")
        
    previous_weight = current_weight


# =====================================================================
# --- TESTING CELL: SANITIZATION & CLOCK SPEED ---
# =====================================================================
print("\n" + "🔋 " * 20)
print(" TESTING MILLISECOND STAMPS & WEIGHT DEFENSE")
print("🔋 " * 20)

prev_hash_calc = blockchain_ledger[-1]["block_hash"]

dynamic_checkpoint = create_transit_block(
    location="Tuen Mun River Trade Terminal, HK",
    weight=-19450.80,
    cargo_type="Medical Devices & Equipment",
    serial="MSKU9918273",
    previous_hash=prev_hash_calc,
    private_key=priv_key,
    aeo_id="HK-TM-2026-0411"
)
blockchain_ledger.append(dynamic_checkpoint)

safe_display_block(dynamic_checkpoint)
print(f"| Microsecond/Millisecond Timestamp: {dynamic_checkpoint['timestamp']}")
print(f"| Auto-Calculated Target Block ID: {dynamic_checkpoint['block_id']}")
print("=" * 43)


# =====================================================================
# --- DAY 20: VELOCITY STRESS CHECK PIPELINE ---
# =====================================================================
print("\n" + "⚡ " * 20)
print(" RUNNING SYSTEM CLOCK VELOCITY STRESS CHECK")
print("⚡ " * 20)

for i in range(10):
    current_tail_hash = blockchain_ledger[-1]["block_hash"]
    
    stress_block = create_transit_block(
        location=f"Stress Check Automated Zone Node-{i}",
        weight=20000.0,
        cargo_type="Stress Data Packets",
        serial="MSKU9918273",
        previous_hash=current_tail_hash,
        private_key=priv_key
    )
    blockchain_ledger.append(stress_block)
    print(f"⚡ Minted Block #{stress_block['block_id']} | Microsecond Stamp: {stress_block['timestamp']}")

print(f"\n Master Ledger Height After Stress Validation: {len(blockchain_ledger)} Blocks")
print("=" * 60)


# =====================================================================
# --- DAYS 27-29: AUTOMATED COUPLING PIPELINE ---
# =====================================================================
raw_logistics_data = [
    {"loc": "Guangdong AEO Warehouse A", "wt": 15000.0, "type": "High-Density Electronics"},
    {"loc": "Port of Shenzhen (Yantian)", "wt": 15000.0, "type": "High-Density Electronics"},
    {"loc": "Kwai Tsing Container Terminal 4, HK", "wt": 15000.0, "type": "High-Density Electronics"},
    {"loc": "Tuen Mun River Trade Terminal, HK", "wt": 14200.5, "type": "Medical Devices & Equipment"}
]

for record in raw_logistics_data:
    if len(blockchain_ledger) == 0:
        prev_hash_lookup = "0"
    else:
        last_block = blockchain_ledger[-1]
        prev_hash_lookup = last_block["block_hash"]
    
    linked_block = create_transit_block(
        location=record["loc"],
        weight=record["wt"],
        cargo_type=record["type"],
        serial="MSKU9918273",
        previous_hash=prev_hash_lookup,
        private_key=priv_key
    )
    blockchain_ledger.append(linked_block)


# =====================================================================
# --- DAY 30: TERMINAL CHAIN VERIFICATION PORTAL ---
# =====================================================================
print("\n" + "📜 " * 25)
print("               CRYPTOGRAPHIC BLOCKCHAIN AUDIT LOG")
print("📜 " * 25)

for block in blockchain_ledger:
    print(f"🧱 BLOCK ID: {block['block_id']} | Location: {block['location']}")
    print(f"   ⬅️ PREV HASH: {block['previous_hash']}")
    print(f"   🔒 CURR HASH: {block['block_hash']}")
    print("-" * 75)

print(f"\n Master Ledger Verified Height: {len(blockchain_ledger)} Blocks Securely Interlocked.")
print("=" * 75)


def run_customs_terminal_portal():
    print("\n" + "⌨️ " * 20)
    print(" HONG KONG CUSTOMS INTERACTIVE INTAKE PORTAL")
    print("⌨️ " * 20)
    
    user_location = input("Enter current checkpoint node location: ")
    user_weight = input("Enter declared container cargo weight (KG): ")
    
    last_block_hash = blockchain_ledger[-1]["block_hash"] if blockchain_ledger else "0"

    interactive_block = create_transit_block(
        location=user_location,
        weight=user_weight,
        cargo_type="Standardized AEO Cargo Segment",
        serial="MSKU9918273",
        previous_hash=last_block_hash,
        private_key=priv_key
    )
    
    blockchain_ledger.append(interactive_block)
    
    print("\n✅ TRANSACTION SECURELY RECORDED")
    safe_display_block(interactive_block)
    print(f"   ⬅️ PREV HASH: {interactive_block['previous_hash']}")
    print(f"   🔒 CURR HASH: {interactive_block['block_hash']}")


# Fire portal at the end of historic sequence calculation
run_customs_terminal_portal()


# =====================================================================
# --- WEEKS 15 & 16: INTEGRATED GEOSPATIAL SIMULATION SUITE ---
# =====================================================================
if __name__ == "__main__":
    print("\n====================================================")
    print("   STAGE 4: INTEGRATED GEOSPATIAL CORRIDOR SIMULATION")
    print("====================================================")
    
    # Reinitalize clean sandboxed testing history tracking layout arrays
    spatial_test_ledger = []
    
    # 1. Append a completely valid block (Inside Channel Lanes)
    print("\n🚢 Minting Vessel Block Alpha (On-Track Shipping Lane)...")
    block_alpha = create_transit_block(
        location="Lamma Channel Inbound Approach", weight=15000.0, cargo_type="Electronics",
        serial="MSKU9918273", previous_hash="0", current_lat=22.2100, current_lon=114.0700, private_key=priv_key
    )
    spatial_test_ledger.append(block_alpha)
    
    # 2. Append a block with minor drifting characteristics (Minor Adjustment - Low Risk)
    print("\n🚢 Minting Vessel Block Beta (Slightly Drifted Outer Channel Edge)...")
    block_beta = create_transit_block(
        location="Outer Channel Flank Checkpoint", weight=15000.0, cargo_type="Electronics",
        serial="MSKU9918273", previous_hash=block_alpha["block_hash"], current_lat=22.2600, current_lon=114.0400, private_key=priv_key
    )
    spatial_test_ledger.append(block_beta)
    
    # 3. Append a severely deviated block (High-Risk Deviation Anomaly)
    print("\n🚢 Minting Vessel Block Gamma (Severely Deviated Near Remote Island Smuggling Blackspot)...")
    block_gamma = create_transit_block(
        location="Unapproved Shoreline Incursion Zone", weight=15000.0, cargo_type="Electronics",
        serial="MSKU9918273", previous_hash=block_beta["block_hash"], current_lat=22.5100, current_lon=113.7200, private_key=priv_key
    )
    spatial_test_ledger.append(block_gamma)
    
    print(f"\n📊 Initial Spatial Ledger Height: {len(spatial_test_ledger)} Blocks.")
    
    # 4. Fire the automated background audit engine loop to catch spatial anomalies
    print("\n🛂 Customs launching real-time spatial path validation audit...")
    run_system_integrity_audit(spatial_test_ledger, pub_key)
    
    print(f"\n📦 Final Active Spatial Ledger Height: {len(spatial_test_ledger)} Blocks (High-risk threats extracted to quarantine file).")
    print("====================================================")