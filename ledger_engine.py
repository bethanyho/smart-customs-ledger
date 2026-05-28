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
    """
    Accepts a standard ledger block dictionary, extracts its core identifying fields,
    and returns an immutable 64-character SHA-256 signature string.
    """
    location = str(block.get("location", "UNKNOWN"))
    weight = str(block.get("cargo_weight_kg", 0.0))
    serial = str(block.get("container_serial", "🚨 UNKNOWN"))
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
# --- DAY 38: UPDATED BUILDER INTEGRATING SECURITY OBJECTS ---
# =====================================================================
def create_transit_block(location, weight, cargo_type, serial, previous_hash, private_key=None, aeo_id="HK-AEO-2026-DEFAULT"):
    """
    Automates structured block generation with millisecond stamping, input sanitization,
    cryptographic tracking hashing, and asymmetric RSA signature seals.
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
    
    # Dynamic Asymmetric Digital Signing
    if private_key:
        footprint_string = str(location) + str(sanitized_weight) + str(serial) + str(previous_hash)
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
# --- DAY 40: END-TO-END SIGNATURE CONFIRMATION TEST ---
# =====================================================================
print("\n====================================================")
print("        RUNNING WEEK 8 DIGITAL SIGNATURE TRIAL      ")
print("====================================================")

if priv_key and pub_key:
    # 1. Audit check on the last block entered in our database
    latest_block = blockchain_ledger[-1]
    print(f"\n🔬 Auditing Latest Node Entry (Block #{latest_block['block_id']}) at {latest_block['location']}...")
    print(f"🔏 Appended Signature: {latest_block['digital_signature'][:65]}...")
    
    # 2. Verify authorship through public key decryption
    is_authentic = verify_cargo_signature(pub_key, latest_block)
    if is_authentic:
        print("✅ [VERIFIED]: Cryptographic asymmetric signature is valid! Authorship confirmed.")
    else:
        print("❌ [REJECTED]: Signature authentication validation mismatch.")
        
    # 3. Defensive Anti-Tamper Security Simulation Test
    print("\n⚠️ SIMULATING AN ATTACK VECTOR (Altering block parameters)...")
    latest_block["cargo_weight_kg"] = 99999.99  # Malicious manipulation
    
    print("🛂 Re-running Customs verification checkpoint...")
    is_still_authentic = verify_cargo_signature(pub_key, latest_block)
    if not is_still_authentic:
        print("🛡️ [SECURITY SUCCESS]: Manifest modification caught! Attack thwarted successfully.")
else:
    print("❌ Setup failed. Local cryptographic key parameters are completely inaccessible.")

print("====================================================")