import sqlite3, os, sys, json
from calculate_token_usage import decode_protobuf

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

conv_id = 'e143942d-bf60-4254-a21f-4439da715f29'
db_path = fr'C:\Users\Lenovo\.gemini\antigravity-ide\conversations\{conv_id}.db'
transcript_path = fr'C:\Users\Lenovo\.gemini\antigravity-ide\brain\{conv_id}\.system_generated\logs\transcript.jsonl'

conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
cursor = conn.cursor()
cursor.execute('SELECT idx, step_type, metadata FROM steps ORDER BY idx ASC;')
steps = cursor.fetchall()

prompts = {}
if os.path.exists(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('type') == 'USER_INPUT':
                    prompts[data.get('step_index')] = data.get('content', '')
            except:
                pass

turns = []
curr_turn = None

for s_idx, stype, meta in steps:
    if stype == 14:
        prompt_text = prompts.get(s_idx, f'Turn at step {s_idx}')
        curr_turn = {
            'step': s_idx,
            'prompt': prompt_text.strip().replace('\n', ' ')[:50],
            'calls': 0,
            'cached': 0,
            'uncached': 0,
            'out_tokens': 0
        }
        turns.append(curr_turn)
    elif stype == 15 and meta and curr_turn:
        try:
            p = decode_protobuf(meta)
            if 'field_9_msg' in p:
                usage = p['field_9_msg']
                curr_turn['calls'] += 1
                curr_turn['uncached'] += usage.get('field_2', 0)
                curr_turn['out_tokens'] += usage.get('field_3', 0)
                curr_turn['cached'] += usage.get('field_5', 0)
        except:
            pass

print("="*95)
print("              RINCIAN PENGGUNAAN TOKEN SESI (ROY DARWIN REZERIUS)")
print("="*95)

total_in_all = 0
total_cached_all = 0
total_uncached_all = 0
total_out_all = 0
total_calls_all = 0

for idx, t in enumerate(turns, 1):
    tot_in = t['cached'] + t['uncached']
    tot = tot_in + t['out_tokens']
    total_in_all += tot_in
    total_cached_all += t['cached']
    total_uncached_all += t['uncached']
    total_out_all += t['out_tokens']
    total_calls_all += t['calls']
    print(f"{idx:2d}. Step {t['step']:3d} | Calls: {t['calls']:2d} | In: {tot_in:10,d} (Cache: {t['cached']:10,d}) | Out: {t['out_tokens']:5,d} | Total: {tot:10,d} | '{t['prompt']}'")

print("="*95)
print(f"TOTAL AKUMULASI SESI:")
print(f"  - Total LLM API Calls    : {total_calls_all} calls")
print(f"  - Input / Prompt Tokens  : {total_in_all:,} tokens")
print(f"      * Cached Prompt      : {total_cached_all:,} tokens ({total_cached_all/total_in_all*100:.1f}%)")
print(f"      * Uncached Prompt    : {total_uncached_all:,} tokens ({total_uncached_all/total_in_all*100:.1f}%)")
print(f"  - Output Tokens (Gen)    : {total_out_all:,} tokens")
print(f"  - GRAND TOTAL TOKENS     : {total_in_all + total_out_all:,} tokens")
print("="*95)
