import sqlite3
import sys
import json
from calculate_token_usage import decode_protobuf

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

conv_id = '6a3b73dc-8c7a-4c29-a610-2c409394a585'
db_path = fr'C:\Users\Lenovo\.gemini\antigravity-ide\conversations\{conv_id}.db'
transcript_path = fr'C:\Users\Lenovo\.gemini\antigravity-ide\brain\{conv_id}\.system_generated\logs\transcript.jsonl'

conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
cursor = conn.cursor()

cursor.execute("SELECT idx, step_type, step_payload, metadata FROM steps ORDER BY idx ASC;")
steps = cursor.fetchall()
print(f"Total steps in conversation database: {len(steps)}")

# Read user prompts from transcript.jsonl if available
transcript_prompts = {}
try:
    with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('type') == 'USER_INPUT':
                    transcript_prompts[data.get('step_index')] = data.get('content', '')
            except:
                pass
except Exception as e:
    print(f"Transcript load warning: {e}")

user_turns = []
llm_calls = []

for s_idx, stype, payload, meta in steps:
    if stype == 14:
        text = transcript_prompts.get(s_idx, "")
        if not text:
            try:
                text = payload.decode('utf-8', errors='ignore')
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

print(f"\nTotal User Inputs detected: {len(user_turns)}")
for i, u in enumerate(user_turns):
    clean_txt = u[1].strip().replace('\r', ' ').replace('\n', ' ')
    if len(clean_txt) > 80:
        clean_txt = clean_txt[:80] + "..."
    print(f"  [{i+1:2d}] Step {u[0]:4d}: {clean_txt}")

print(f"\nTotal LLM Generation Calls detected: {len(llm_calls)}")

def format_stats(calls, label):
    total_uncached = sum(c['uncached_prompt'] for c in calls)
    total_cached = sum(c['cached_prompt'] for c in calls)
    total_prompt = sum(c['total_prompt'] for c in calls)
    total_candidates = sum(c['candidates'] for c in calls)
    total_thoughts = sum(c['thoughts'] for c in calls)
    total_text = sum(c['text_out'] for c in calls)
    total_all = sum(c['total_tokens'] for c in calls)
    
    print(f"\n==================================================")
    print(f"TOKEN USAGE: {label}")
    print(f"==================================================")
    print(f"Total API Calls (LLM Generation): {len(calls):,}")
    print(f"Total Prompt Tokens (Input)     : {total_prompt:,}")
    if total_prompt > 0:
        print(f"  - Cached Prompt Tokens        : {total_cached:,} ({total_cached/total_prompt*100:.1f}%)")
        print(f"  - Uncached Prompt Tokens      : {total_uncached:,} ({total_uncached/total_prompt*100:.1f}%)")
    print(f"Total Output Tokens (Generasi)  : {total_candidates:,}")
    if total_candidates > 0:
        print(f"  - Reasoning / Thinking Tokens : {total_thoughts:,} ({total_thoughts/total_candidates*100:.1f}%)")
        print(f"  - Output Text & Tool Calls    : {total_text:,} ({total_text/total_candidates*100:.1f}%)")
    print(f"--------------------------------------------------")
    print(f"GRAND TOTAL TOKENS              : {total_all:,}")
    print(f"==================================================")
    return {
        'calls': len(calls),
        'prompt': total_prompt,
        'cached': total_cached,
        'uncached': total_uncached,
        'output': total_candidates,
        'thinking': total_thoughts,
        'text': total_text,
        'total': total_all
    }

total_stat = format_stats(llm_calls, "SELURUH SESI INI (Conversation ID: 6a3b73dc...)")

# Per User Turn breakdown
if len(user_turns) > 0:
    print("\n\n==================================================")
    print("BREAKDOWN PER PERMINTAAN USER (USER TURN)")
    print("==================================================")
    for i in range(len(user_turns)):
        u_step = user_turns[i][0]
        next_step = user_turns[i+1][0] if i + 1 < len(user_turns) else 999999
        clean_txt = user_turns[i][1].strip().replace('\r', ' ').replace('\n', ' ')
        if len(clean_txt) > 70:
            clean_txt = clean_txt[:70] + "..."
        if not clean_txt:
            clean_txt = "(Attached media / tool response / empty)"
        st_calls = [c for c in llm_calls if u_step <= c['step_idx'] < next_step]
        if st_calls:
            print(f"\n--- [Turn {i+1}] Step {u_step}: \"{clean_txt}\" ---")
            format_stats(st_calls, f"Turn {i+1}")

