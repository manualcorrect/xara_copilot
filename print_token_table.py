import sqlite3
import sys
import json
from calculate_token_usage import decode_protobuf

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

conv_id = '6a3b73dc-8c7a-4c29-a610-2c409394a585'
db_path = fr'C:\Users\Lenovo\.gemini\antigravity-ide\conversations\{conv_id}.db'
transcript_path = fr'C:\Users\Lenovo\.gemini\antigravity-ide\brain\{conv_id}\.system_generated\logs\transcript.jsonl'

conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
cursor = conn.cursor()

cursor.execute("SELECT idx, step_type, step_payload, metadata FROM steps ORDER BY idx ASC;")
steps = cursor.fetchall()

# Map transcript prompts
transcript_prompts = {}
try:
    with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('type') == 'USER_INPUT':
                    content = data.get('content', '')
                    # If content has <USER_REQUEST>, extract inside
                    if '<USER_REQUEST>' in content:
                        s = content.split('<USER_REQUEST>')[1].split('</USER_REQUEST>')[0].strip()
                    else:
                        s = content.strip()
                    transcript_prompts[data.get('step_index')] = s
            except:
                pass
except:
    pass

user_turns = []
llm_calls = []

for s_idx, stype, payload, meta in steps:
    if stype == 14:
        text = transcript_prompts.get(s_idx, "")
        if not text:
            try:
                raw = payload.decode('utf-8', errors='ignore')
                if '<USER_REQUEST>' in raw:
                    text = raw.split('<USER_REQUEST>')[1].split('</USER_REQUEST>')[0].strip()
                else:
                    text = raw.strip()
            except:
                text = ""
        user_turns.append((s_idx, text))
    elif stype == 15 and meta:
        try:
            p = decode_protobuf(meta)
            if 'field_9_msg' in p:
                usage = p['field_9_msg']
                uncached_prompt = usage.get('field_2', 0)
                candidates = usage.get('field_3', 0)
                cached_prompt = usage.get('field_5', 0)
                thoughts = usage.get('field_9', 0)
                text_out = usage.get('field_10', 0)
                total_prompt = uncached_prompt + cached_prompt
                total_tokens = total_prompt + candidates
                
                llm_calls.append({
                    'step_idx': s_idx,
                    'uncached_prompt': uncached_prompt,
                    'cached_prompt': cached_prompt,
                    'total_prompt': total_prompt,
                    'candidates': candidates,
                    'thoughts': thoughts,
                    'text_out': text_out,
                    'total_tokens': total_tokens
                })
        except:
            pass

total_uncached = sum(c['uncached_prompt'] for c in llm_calls)
total_cached = sum(c['cached_prompt'] for c in llm_calls)
total_prompt = sum(c['total_prompt'] for c in llm_calls)
total_candidates = sum(c['candidates'] for c in llm_calls)
total_thoughts = sum(c['thoughts'] for c in llm_calls)
total_text = sum(c['text_out'] for c in llm_calls)
total_all = sum(c['total_tokens'] for c in llm_calls)

print("="*80)
print("RINGKASAN TOTAL PENGGUNAAN TOKEN (SESI INI)")
print("="*80)
print(f"Total Interaksi / Steps Terdaftar : {len(steps):,}")
print(f"Total User Prompts / Requests      : {len(user_turns):,}")
print(f"Total API Calls (LLM Responses)   : {len(llm_calls):,}")
print("-" * 80)
print(f"Total Prompt (Input) Tokens        : {total_prompt:,}")
print(f"  ├─ Cached Tokens (Hemat Biaya)  : {total_cached:,} ({total_cached/total_prompt*100:.2f}%)")
print(f"  └─ Uncached Tokens (Baru)       : {total_uncached:,} ({total_uncached/total_prompt*100:.2f}%)")
print(f"Total Completion (Output) Tokens   : {total_candidates:,}")
print(f"  ├─ Reasoning / Thinking Tokens  : {total_thoughts:,} ({total_thoughts/total_candidates*100:.2f}%)")
print(f"  └─ Response Text / Tool Calls   : {total_text:,} ({total_text/total_candidates*100:.2f}%)")
print("="*80)
print(f"GRAND TOTAL SEMUA TOKEN           : {total_all:,}")
print("="*80)

print("\n" + "="*110)
print(f"{'Turn':<5} | {'Step':<5} | {'Calls':<6} | {'Prompt (Input)':<16} | {'Output (Gen)':<14} | {'Total Tokens':<14} | {'Topik / Permintaan User'}")
print("="*110)

for i in range(len(user_turns)):
    u_step = user_turns[i][0]
    next_step = user_turns[i+1][0] if i + 1 < len(user_turns) else 999999
    txt = user_turns[i][1].replace('\r', ' ').replace('\n', ' ').strip()
    if len(txt) > 40:
        txt = txt[:37] + "..."
    if not txt:
        txt = "(User input / file upload)"
    st_calls = [c for c in llm_calls if u_step <= c['step_idx'] < next_step]
    if not st_calls:
        continue
    c_p = sum(c['total_prompt'] for c in st_calls)
    c_o = sum(c['candidates'] for c in st_calls)
    c_t = sum(c['total_tokens'] for c in st_calls)
    calls_num = len(st_calls)
    print(f"#{i+1:<4} | {u_step:<5} | {calls_num:<6} | {c_p:>16,} | {c_o:>14,} | {c_t:>14,} | {txt}")

print("="*110)
