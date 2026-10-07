import sqlite3
from calculate_token_usage import decode_protobuf

db_path = r'C:\Users\Lenovo\.gemini\antigravity-ide\conversations\7fc1812d-77c0-4729-a186-6403d1a60a1b.db'
conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
cursor = conn.cursor()

cursor.execute("SELECT idx, step_type, metadata FROM steps WHERE step_type = 15 AND metadata IS NOT NULL ORDER BY idx ASC;")
rows = cursor.fetchall()

calls = []
for idx, stype, meta in rows:
    p = decode_protobuf(meta)
    if 'field_9_msg' in p:
        u = p['field_9_msg']
        uncached = u.get('field_2', 0)
        candidates = u.get('field_3', 0)
        cached = u.get('field_5', 0)
        thoughts = u.get('field_9', 0)
        text_out = u.get('field_10', 0)
        total_in = uncached + cached
        total_all = total_in + candidates
        calls.append({
            'step': idx,
            'uncached': uncached,
            'cached': cached,
            'prompt': total_in,
            'candidates': candidates,
            'thoughts': thoughts,
            'text': text_out,
            'total': total_all
        })

# Stage intervals based on user prompts
stages = [
    ("Tahap 1: Nama Nasabah", 899, 955),
    ("Tahap 2: Periode Laporan", 955, 987),
    ("Tahap 3: Tanggal Cetak", 987, 1009),
    ("Tahap 4: Nomor Rekening", 1009, 1041),
    ("Tahap 5: Nomor Halaman", 1041, 1069),
    ("Tahap 6: Tanggal Transaksi 47 Baris", 1069, 1164),
    ("Tahap 7 & Resolusi Error: Ringkasan & 47 Baris Tabel", 1164, 1398),
]

print("=== RINCIAN PENGGUNAAN TOKEN PER TAHAP PADA STRESS TEST 2 ===")
for sname, start_s, end_s in stages:
    st_calls = [c for c in calls if start_s <= c['step'] < end_s]
    c_in = sum(c['cached'] for c in st_calls)
    u_in = sum(c['uncached'] for c in st_calls)
    t_in = sum(c['prompt'] for c in st_calls)
    t_out = sum(c['candidates'] for c in st_calls)
    t_th = sum(c['thoughts'] for c in st_calls)
    t_tx = sum(c['text'] for c in st_calls)
    t_tot = sum(c['total'] for c in st_calls)
    print(f"\n[{sname}] (Steps {start_s} - {end_s})")
    print(f"  Panggilan LLM : {len(st_calls)} call")
    print(f"  Prompt (Input): {t_in:,} tokens (Cached: {c_in:,} / {c_in/t_in*100:.1f}%, Uncached: {u_in:,})")
    print(f"  Output Generasi: {t_out:,} tokens (Thinking: {t_th:,}, Output: {t_tx:,})")
    print(f"  Subtotal Tokens: {t_tot:,} tokens")

test2_calls = [c for c in calls if c['step'] >= 893]
all_calls = calls

def summarize(c_list, title):
    c_in = sum(c['cached'] for c in c_list)
    u_in = sum(c['uncached'] for c in c_list)
    t_in = sum(c['prompt'] for c in c_list)
    t_out = sum(c['candidates'] for c in c_list)
    t_th = sum(c['thoughts'] for c in c_list)
    t_tx = sum(c['text'] for c in c_list)
    t_tot = sum(c['total'] for c in c_list)
    print(f"\n========================================================")
    print(f"TOTAL AKUMULASI: {title}")
    print(f"========================================================")
    print(f"Total Interaksi LLM    : {len(c_list):,} API Generation Calls")
    print(f"Total Token Input      : {t_in:,} tokens")
    print(f"  - Cached Tokens      : {c_in:,} tokens ({c_in/t_in*100:.2f}%) [Efisiensi Cache]")
    print(f"  - Uncached Tokens    : {u_in:,} tokens ({u_in/t_in*100:.2f}%)")
    print(f"Total Token Output     : {t_out:,} tokens")
    print(f"  - Reasoning/Thinking : {t_th:,} tokens ({t_th/t_out*100:.2f}%)")
    print(f"  - Response Text      : {t_tx:,} tokens ({t_tx/t_out*100:.2f}%)")
    print(f"--------------------------------------------------------")
    print(f"GRAND TOTAL TOKENS     : {t_tot:,} tokens")
    print(f"========================================================")

summarize(test2_calls, "STRESS TEST 2 (Tahap 1 s.d. Tahap 7 pada Dokumen 5 Halaman)")
summarize(all_calls, "SELURUH SESI PENGEMBANGAN MODEL (Project V2 Test 1 + Stress Test 2)")
