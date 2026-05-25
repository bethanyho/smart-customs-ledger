#  CRYPTOGRAPHIC UTILITY ENCAPSULATION ---

def calculate_block_hash(block):
    """
    Accepts a standard ledger block dictionary, extracts its core identifying fields,
    and returns an immutable 64-character SHA-256 signature string.
    """
    
    location = str(block.get("location", "UNKNOWN"))
    weight = str(block.get("cargo_weight_kg", 0.0))
    serial = str(block.get("container_serial", "🚨 UNKNOWN"))
    

    combined_string = location + weight + serial
    
    
    encoded_bytes = combined_string.encode('utf-8')
    secure_signature = hashlib.sha256(encoded_bytes).hexdigest()
    
    return secure_signature



import datetime
import hashlib




def initialize_system():
    print("====================================")
    print("AEO SMART SUPPLY CHAIN LEDGER ONLINE")
    print("====================================")

initialize_system()

blockchain_ledger =[]

print(f"Ledger Initialized. Current Block Height: {len(blockchain_ledger)}")


checkpoint_0 = {
    "block_id": 0,
    "location": "Guangdong AEO Warehouse A",
    "cargo_weight_kg": 15000.0,
    "cargo_type": "High-Density Electronics"
}
checkpoint_0["aeo_company_id"] = "HK-AEO-2026-0891"
checkpoint_0["destination_port"] = "Kwai Tsing Container Terminal 4"
checkpoint_0["container_serial"] = "MSKU9918273"


print("\n--- UPDATED CARGO COMPLIANCE BLOCK ---")

import pprint
pprint.pprint(checkpoint_0)

print(f"Target Destination Node: {checkpoint_0['location']}")


is_valid = True


if not isinstance(checkpoint_0["cargo_weight_kg"], (int, float)):
    print("🚨 CRITICAL ERROR: Weight must be a numerical decimal!")
    is_valid = False


if len(checkpoint_0["container_serial"]) != 11:
    print("🚨 CRITICAL ERROR: ISO Container Serial must be exactly 11 characters!")
    is_valid = False


if is_valid:
    print("✅ DATA INTEGRITY VERIFIED: Appending block to ledger...")
    blockchain_ledger.append(checkpoint_0)
else:
    print("❌ INGESTION BLOCKED: Corrupted data detected.")

print("\n--- POST-INGESTION METRICS ---")
print(f"Updated Ledger Block Height: {len(blockchain_ledger)}")


def display_block_manifest(block):
    print("\n" + "=" * 43)
    print(f" CONTAINER AUDIT REPORT - BLOCK #{block['block_id']}")
    print("=" * 43)
    print(f"| Governance AEO ID   : {block['aeo_company_id']}")
    print(f"| ISO Container Serial: {block['container_serial']}")
    print(f"| Current Node Vector : {block['location']}")
    print(f"| Discharged Port Link: {block['destination_port']}")
    print(f"| Cargo Weight Metric : {block['cargo_weight_kg']} KG")
    print(f"| Classification Type : {block['cargo_type']}")
    print("-" * 43)

# --- PHASE 1: MULTI-NODE TRANSIT CHECKPOINTS (Day 11) ---

# Node 0: Origin Point (The Factory Gate)
checkpoint_0 = {
    "block_id": 0,
    "timestamp": "2026-05-22 08:00:00",
    "location": "Guangdong AEO Manufacturing Hub",
    "aeo_company_id": "HK-AEO-2026-0891",
    "destination_port": "Kwai Tsing Container Terminal 4",
    "container_serial": "MSKU9918273",
    "cargo_weight_kg": 15000.0,
    "cargo_type": "High-Density Electronics",
    "status": "LOADED & SEALED"
}


checkpoint_1 = {
    "block_id": 1,
    "timestamp": "2026-05-22 14:30:00",
    "location": "Port of Shenzhen (Yantian)",
    "aeo_company_id": "SZ-PORT-2026-4403",
    "destination_port": "Kwai Tsing Container Terminal 4",
    "container_serial": "MSKU9918273",  
    "cargo_weight_kg": 15000.0,
    "cargo_type": "High-Density Electronics",
    "status": "EXPORT CUSTOMS CLEARED"
}


checkpoint_2 = {
    "block_id": 2,
    "timestamp": "2026-05-22 19:15:00",
    "location": "Kwai Tsing Container Terminal 4, HK",
    "aeo_company_id": "HK-TERMINAL-2026-0042",
    "destination_port": "Kwai Tsing Container Terminal 4",
    "container_serial": "MSKU9918273",  
    "cargo_weight_kg": 15000.0,
    "cargo_type": "High-Density Electronics",
    "status": "ARRIVED & DISCHARGED"
}


print("\n--- INITIALIZING PHASE 1 MULTI-NODE LOGISTICS ---")
print(f"Tracking Journey for Container: {checkpoint_0['container_serial']}")
print(f"-> Node 0: {checkpoint_0['location']} | Status: {checkpoint_0['status']}")
print(f"-> Node 1: {checkpoint_1['location']} | Status: {checkpoint_1['status']}")
print(f"-> Node 2: {checkpoint_2['location']} | Status: {checkpoint_2['status']}")



blockchain_ledger.append(checkpoint_0)
blockchain_ledger.append(checkpoint_1)
blockchain_ledger.append(checkpoint_2)

print("\n--- MASTER LEDGER UPDATE ---")
print(f"📦 Successfully committed Block #0, #1, and #2 sequentially.")
print(f"Absolute Master Ledger Height: {len(blockchain_ledger)} Blocks")


print(f"Verifying index slot [2] location: {blockchain_ledger[2]['location']}")

# --- DAY 13: GEOGRAPHIC PATH PARSING PIPELINE ---

print("\n" + "🌐" * 20)
print(" LIVE SUPPLY CHAIN GEOGRAPHIC TRAIL AUDIT")
print("🌐" * 20)

# The for loop automatically steps through each block index in order
for block in blockchain_ledger:
    # Extract the tracking fields dynamically
    timestamp = block.get("timestamp", "UNKNOWN TIME")
    location = block.get("location", "UNKNOWN LOCATION")
    status = block.get("status", "PROCESSING")
    
    # Print a highly specialized chronological route stream
    print(f"📍 [{timestamp}] -> Container moved to: {location} | Status: [{status}]")

#  DAY 14: WEIGHT Track 

print("\n" + "⚖️ " * 20)
print(" LIVE SUPPLY CHAIN WEIGHT INTEGRITY AUDIT")
print("⚖️ " * 20)

# Initialize a tracking variable to hold the weight of the previous checkpoint
previous_weight = None

for block in blockchain_ledger:
    current_weight = block.get("cargo_weight_kg", 0.0)
    location = block.get("location", "UNKNOWN LOCATION")
    
    # Calculate the difference of the weights
    if previous_weight is not None:
        delta = current_weight - previous_weight
        
        # Check if the weight changed at all
        if delta != 0:
            print(f"🚨 WARNING: Weight Delta Detected at {location}! Change: {delta} KG")
        else:
            print(f"✅ Weight Verified at {location}: {current_weight} KG (Delta: 0.0 KG)")
    else:
        
        print(f"🏁 Base Weight Established at {location}: {current_weight} KG")
        
    # Update our tracker 
    previous_weight = current_weight

    
import datetime

# --- WEEK 4: UPGRADED AUTOMATED FACTORY ENGINE (Days 17 & 18) ---

def create_transit_block(location, weight, cargo_type, serial, aeo_id="HK-AEO-2026-DEFAULT"):
    """
    Automates generation of structured blocks with millisecond stamping,
    strict input sanitization, and encapsulated cryptographic seals.
    """
    # Input Sanitization Layer
    parsed_weight = float(weight)
    sanitized_weight = abs(parsed_weight)
    
    #  Millisecond Timestamp Enforcement
    millisecond_timestamp = str(datetime.datetime.now())
    
    # Auto-calculate incremental Block ID
    dynamic_id = len(blockchain_ledger)
    
    # Construct the basic block layout dictionary
    new_block = {
        "block_id": dynamic_id,
        "timestamp": millisecond_timestamp,
        "location": location,
        "aeo_company_id": aeo_id,
        "destination_port": "Kwai Tsing Container Terminal 4",
        "container_serial": serial,
        "cargo_weight_kg": sanitized_weight, 
        "cargo_type": cargo_type,
        "status": "AUTOMATED PRODUCTION GATE"
    }
    
   
    # Generate the cryptographic seal using our new encapsulated utility function
    new_block["block_hash"] = calculate_block_hash(new_block)
    
    return new_block


def safe_display_block(block):
    """Prevents system crashes by using .get() fallbacks for missing keys."""
    serial = block.get("container_serial", "🚨 UNKNOWN_SERIAL")
    weight = block.get("cargo_weight_kg", 0.0)
    aeo_id = block.get("aeo_company_id", "⚠️ UNREGISTERED_AEO")
    
    print("\n--- SAFE LOG PRESENTATION ---")
    print(f"Safe Log -> Serial: {serial} | Weight: {weight} KG | AEO ID: {aeo_id}")


# --- TESTING CELL: SANITIZATION & CLOCK SPEED ---
print("\n" + "🔋 " * 20)
print(" TESTING MILLISECOND STAMPS & WEIGHT DEFENSE")
print("🔋 " * 20)


dynamic_checkpoint = create_transit_block(
    location="Tuen Mun River Trade Terminal, HK",
    weight=-19450.80,  # <-- Negative input
    cargo_type="Medical Devices & Equipment",
    serial="MSKU9918273",
    aeo_id="HK-TM-2026-0411"
)

# Render results
safe_display_block(dynamic_checkpoint)
print(f"| Microsecond/Millisecond Timestamp: {dynamic_checkpoint['timestamp']}")
print(f"| Auto-Calculated Target Block ID: {dynamic_checkpoint['block_id']}")
print("=" * 43)



def run_customs_terminal_portal():
    print("\n" + "⌨️ " * 20)
    print(" HONG KONG CUSTOMS INTERACTIVE INTAKE PORTAL")
    print("⌨️ " * 20)
    
   
    user_location = input("Enter current checkpoint node location: ")
    user_weight = input("Enter declared container cargo weight (KG): ")
    

    interactive_block = create_transit_block(
        location=user_location,
        weight=user_weight,
        cargo_type="Standardized AEO Cargo Segment",
        serial="MSKU9918273"
    )
    
    # Commit the newly built interactive block directly to the live database array
    blockchain_ledger.append(interactive_block)
    
    print("\n✅ TRANSACTION SECURELY RECORDED")
    safe_display_block(interactive_block)


run_customs_terminal_portal()


# --- DAY 20: VELOCITY STRESS CHECK PIPELINE ---

print("\n" + "⚡ " * 20)
print(" RUNNING SYSTEM CLOCK VELOCITY STRESS CHECK")
print("⚡ " * 20)

# Generate 10 blocks sequentially at maximum compiler processing speed
for i in range(10):
    stress_block = create_transit_block(
        location=f"Stress Check Automated Zone Node-{i}",
        weight=20000.0,
        cargo_type="Stress Data Packets",
        serial="MSKU9918273"
    )
    blockchain_ledger.append(stress_block)
    # Print the precise microsecond tracking data to verify progression
    print(f"⚡ Minted Block #{stress_block['block_id']} | Microsecond Stamp: {stress_block['timestamp']}")

print(f"\n Master Ledger Height After Stress Validation: {len(blockchain_ledger)} Blocks")
print("=" * 60)