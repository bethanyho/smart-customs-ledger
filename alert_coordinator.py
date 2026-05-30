import datetime
import json
import os

# Define the file path for evidence logging
QUARANTINE_FILE = "quarantined_manifests.json"

# =====================================================================
# --- WEEK 13: HIGH-VISIBILITY COMMAND TERMINAL ALARMS ---
# =====================================================================
def dispatch_customs_alarm(violation_type, context_block):
    """
    Days 61, 62 & 64: Formats and prints an urgent, highly scannable terminal alert 
    frame for frontline customs officers with live situational data.
    """
    system_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract block data safely with fallbacks
    block_id = context_block.get("block_id", "UNKNOWN ID")
    container_serial = context_block.get("container_serial", "UNKNOWN SERIAL")
    last_checkpoint = context_block.get("location", "UNKNOWN LOCATION")
    
    print("\n" + "=" * 70)
    print("🚨 ALERT: AUTOMATED CHECKPOINT SECURITY VIOLATION DETECTED 🚨")
    print(f"[DISCOVERY TIMESTAMP] : {system_now}")
    print(f"[VIOLATION TYPE]      : {violation_type}")
    print(f"[TARGET BLOCK ID]     : #{block_id}")
    print(f"[TARGET CONTAINER]    : {container_serial}")
    print(f"[LAST CHECKPOINT]     : {last_checkpoint}")
    print("=" * 70)


# =====================================================================
# --- WEEK 14: AUTOMATED EVIDENTIARY QUARANTINE CONTROLS ---
# =====================================================================
def quarantine_corrupted_manifest(block, reason, operator_id="HK-OFFICER-2026-905"):
    """
    Days 66, 68 & 69: Appends threat metadata to a corrupted block dictionary 
    and writes it directly into a local JSON archive for forensic analysis.
    """
    # Create quarantine wrapper metadata package
    quarantine_payload = {
        "quarantine_timestamp": str(datetime.datetime.now()),
        "incident_responder_id": operator_id,
        "threat_classification": reason,
        "compromised_data_payload": block
    }
    
    existing_records = []
    
    # Read existing archive if it exists to avoid overwriting past evidence
    if os.path.exists(QUARANTINE_FILE):
        try:
            with open(QUARANTINE_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    existing_records = json.loads(content)
        except json.JSONDecodeError:
            existing_records = []

    # Append new evidence bundle
    existing_records.append(quarantine_payload)
    
    # Write back clean serialized JSON data array to disk
    with open(QUARANTINE_FILE, "w") as f:
        json.dump(existing_records, f, indent=4)
        
    print(f"💾 [QUARANTINE SILO] Evidence successfully archived to '{QUARANTINE_FILE}'")