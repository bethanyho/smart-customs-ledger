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

    