import datetime
import hashlib
import pprint

# =====================================================================
# --- CRYPTOGRAPHIC UTILITY ENCAPSULATION ---
# =====================================================================
def calculate_block_hash(block):
    """
    Accepts a standard ledger block dictionary, extracts its core identifying fields,
    and returns an immutable 64-character SHA-256 signature string.
    """
    location = str(block.get("location", "UNKNOWN"))
    weight = str(block.get("cargo_weight_kg", 0.0))
    serial = str(block.get("container_serial", "🚨 UNKNOWN"))
    # Week 6 Fix: Include the previous hash in the block footprint calculation!
    prev_hash = str(block.get("previous_hash", ""))

    combined_string = location + weight + serial + prev_hash
    
    encoded_bytes = combined_string.encode('utf-8')
    secure_signature = hashlib.sha256(encoded_bytes).hexdigest()
    
    return secure_signature


def initialize_system():
    print("====================================")
    print("AEO SMART SUPPLY CHAIN LEDGER ONLINE")
    print("====================================")

initialize_system()

# Master database ledger array list
blockchain_ledger = []

print(f"Ledger Initialized. Current Block Height: {len(blockchain_ledger)}")


# =====================================================================
# --- PHASE 1: MANUAL MULTI-NODE TRANSIT CHECKPOINTS ---
# =====================================================================

# Rather than hardcoding dead blocks without signatures, let's use our 
# dynamic block builder to establish our initial historical baseline nodes!

def create_transit_block(location, weight, cargo_type, serial, previous_hash, aeo_id="HK-AEO-2026-DEFAULT"):
    """
    Automates generation of structured blocks with millisecond stamping,
    strict input sanitization, and cryptographically secure SHA-256 digital seals.
    """
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
        "previous_hash": previous_hash  
    }
    
    new_block["block_hash"] = calculate_block_hash(new_block)
    return new_block


def safe_display_block(block):
    """Prevents system crashes by using .get() fallbacks for missing keys."""
    serial = block.get("container_serial", "🚨 UNKNOWN_SERIAL")
    weight = block.get("cargo_weight_kg", 0.0)
    aeo_id = block.get("aeo_company_id", "⚠️ UNREGISTERED_AEO")
    
    print("\n--- SAFE LOG PRESENTATION ---")
    print(f"Safe Log -> Serial: {serial} | Weight: {weight} KG | AEO ID: {aeo_id}")


# Build Initial History (Nodes 0 to 2) using proper dynamic chaining links
h_node_0 = create_transit_block("Guangdong AEO Manufacturing Hub", 15000.0, "High-Density Electronics", "MSKU9918273", previous_hash="0", aeo_id="HK-AEO-2026-0891")
blockchain_ledger.append(h_node_0)

h_node_1 = create_transit_block("Port of Shenzhen (Yantian)", 15000.0, "High-Density Electronics", "MSKU9918273", previous_hash=h_node_0["block_hash"], aeo_id="SZ-PORT-2026-4403")
blockchain_ledger.append(h_node_1)

h_node_2 = create_transit_block("Kwai Tsing Container Terminal 4, HK", 15000.0, "High-Density Electronics", "MSKU9918273", previous_hash=h_node_1["block_hash"], aeo_id="HK-TERMINAL-2026-0042")
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

# Extract current tail hash link dynamically before inserting
prev_hash_calc = blockchain_ledger[-1]["block_hash"]

dynamic_checkpoint = create_transit_block(
    location="Tuen Mun River Trade Terminal, HK",
    weight=-19450.80,
    cargo_type="Medical Devices & Equipment",
    serial="MSKU9918273",
    aeo_id="HK-TM-2026-0411",
    previous_hash=prev_hash_calc  
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
    # FIX #2: Extract the current running tail hash link dynamically for every cycle iteration
    current_tail_hash = blockchain_ledger[-1]["block_hash"]
    
    stress_block = create_transit_block(
        location=f"Stress Check Automated Zone Node-{i}",
        weight=20000.0,
        cargo_type="Stress Data Packets",
        serial="MSKU9918273",
        previous_hash=current_tail_hash  # Passed tracking hash dependency
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
        previous_hash=prev_hash_lookup
    )
    blockchain_ledger.append(linked_block)


# =====================================================================
# --- DAY 30: TERMINAL CHAIN VERIFICATION PORTAL ---
# =====================================================================
print("\n" + "📜 " * 25)
print("              CRYPTOGRAPHIC BLOCKCHAIN AUDIT LOG")
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
    
    # FIX #1: Safely read our true current master tail block signature hash token
    last_block_hash = blockchain_ledger[-1]["block_hash"] if blockchain_ledger else "0"

    interactive_block = create_transit_block(
        location=user_location,
        weight=user_weight,
        cargo_type="Standardized AEO Cargo Segment",
        serial="MSKU9918273",
        previous_hash=last_block_hash  # Passed tracking hash dependency
    )
    
    blockchain_ledger.append(interactive_block)
    
    print("\n✅ TRANSACTION SECURELY RECORDED")
    safe_display_block(interactive_block)
    print(f"   ⬅️ PREV HASH: {interactive_block['previous_hash']}")
    print(f"   🔒 CURR HASH: {interactive_block['block_hash']}")


# Fire portal at the absolute end of runtime cycle execution
run_customs_terminal_portal()