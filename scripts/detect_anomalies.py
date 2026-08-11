import json
import sys
import time
from pathlib import Path

LOG_FILE = Path("data/logs.jsonl")

def detect_anomalies():
    print(f"Monitoring {LOG_FILE} for anomalies...")
    if not LOG_FILE.exists():
        print(f"File {LOG_FILE} does not exist yet. Waiting...")
        
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            # Move to the end of file to only listen to new logs
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                    
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    record = json.loads(line)
                    # Check for anomalies
                    if record.get("level") == "error" or record.get("event") == "request_failed":
                        print(f"[\033[91mALERT\033[0m] ERROR DETECTED: {record.get('error_type')} | Correlation ID: {record.get('correlation_id')}")
                        
                    if "latency_ms" in record and record["latency_ms"] > 3000:
                        print(f"[\033[93mALERT\033[0m] HIGH LATENCY DETECTED: {record['latency_ms']}ms | Correlation ID: {record.get('correlation_id')}")
                        
                except json.JSONDecodeError:
                    pass
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

if __name__ == "__main__":
    detect_anomalies()
