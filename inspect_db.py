import sqlite3
import json

db_path = r'C:\Users\Lenovo\.gemini\antigravity-ide\conversations\7fc1812d-77c0-4729-a186-6403d1a60a1b.db'
conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
cursor = conn.cursor()

# Check trajectory_metadata_blob
cursor.execute("SELECT id, data FROM trajectory_metadata_blob;")
for row in cursor.fetchall():
    print(f"trajectory_metadata_blob {row[0]}: {row[1][:200] if row[1] else None}")

# Check gen_metadata
cursor.execute("SELECT idx, data, size FROM gen_metadata LIMIT 5;")
for row in cursor.fetchall():
    print(f"\ngen_metadata idx {row[0]}:")
    try:
        val = json.loads(row[1])
        print("  json keys:", list(val.keys()) if isinstance(val, dict) else type(val))
        print("  content:", val)
    except:
        print("  raw:", row[1][:200])

# Check steps metadata
cursor.execute("SELECT idx, step_type, metadata FROM steps WHERE metadata IS NOT NULL AND metadata != '' LIMIT 5;")
for row in cursor.fetchall():
    print(f"\nstep {row[0]} ({row[1]}) metadata:")
    try:
        val = json.loads(row[2])
        print("  json keys:", list(val.keys()) if isinstance(val, dict) else type(val))
        print("  content:", val)
    except:
        print("  raw:", row[2][:200])
