import sqlite3
import json
from datetime import datetime

def decode_protobuf(data, depth=0):
    idx = 0
    res = {}
    while idx < len(data):
        byte = data[idx]
        idx += 1
        wire_type = byte & 0x07
        field_num = byte >> 3
        
        if wire_type == 0:
            val = 0
            shift = 0
            while True:
                b = data[idx]
                idx += 1
                val |= (b & 0x7F) << shift
                if not (b & 0x80):
                    break
                shift += 7
            res[f"field_{field_num}"] = val
        elif wire_type == 2:
            length = 0
            shift = 0
            while True:
                b = data[idx]
                idx += 1
                length |= (b & 0x7F) << shift
                if not (b & 0x80):
                    break
                shift += 7
            sub_data = data[idx:idx+length]
            idx += length
            if depth < 3:
                try:
                    sub_parsed = decode_protobuf(sub_data, depth+1)
                    res[f"field_{field_num}_msg"] = sub_parsed
                except:
                    res[f"field_{field_num}_bytes"] = sub_data
            else:
                res[f"field_{field_num}_bytes"] = sub_data
        elif wire_type == 1:
            idx += 8
        elif wire_type == 5:
            idx += 4
        else:
            break
    return res

db_path = r'C:\Users\Lenovo\.gemini\antigravity-ide\conversations\7fc1812d-77c0-4729-a186-6403d1a60a1b.db'
conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
cursor = conn.cursor()

# Get all steps with step_type, payload, metadata
cursor.execute("SELECT idx, step_type, step_payload, metadata FROM steps ORDER BY idx ASC;")
steps = cursor.fetchall()
print(f"Total steps in conversation database: {len(steps)}")

# Step types in antigravity:
# 14 = USER_INPUT
# 15 = PLANNER_RESPONSE (LLM generation)
# 21 = TOOL_CALL / TOOL_RESULT

user_turns = []
llm_calls = []

for s_idx, stype, payload, meta in steps:
    # Check if USER_INPUT
    if stype == 14:
        try:
            # Decode payload text
            text = payload.decode('utf-8', errors='ignore')
            user_turns.append((s_idx, text))
        except:
            pass
    elif stype == 15 and meta:
        try:
            p = decode_protobuf(meta)
            if 'field_9_msg' in p:
                usage = p['field_9_msg']
                # Extract token fields:
                # field_2 = prompt_tokens (uncached)
                # field_3 = candidates_tokens (total output)
                # field_5 = cached_content_tokens
                # field_9 = thoughts_tokens
                # field_10 = text_tokens
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
        except Exception as e:
            pass

print(f"\nTotal User Inputs detected: {len(user_turns)}")
for u in user_turns:
    snippet = u[1].replace('\n', ' ')[:80].encode('ascii', errors='replace').decode('ascii')
    print(f"  Step {u[0]:4d}: {snippet}")

print(f"\nTotal LLM Generation Calls detected: {len(llm_calls)}")

# Find when the user started Stress Test 2:
# "gunakan file di C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2"
test2_start_step = None
for u in user_turns:
    if 'Test_2' in u[1] or 'test_3.1' in u[1] or 'data dalam jumlah lebih banyak' in u[1]:
        test2_start_step = u[0]
        break

print(f"\nStress Test 2 started around Step: {test2_start_step}")

# Compute totals for entire conversation and for Stress Test 2
def sum_stats(calls, label):
    total_uncached = sum(c['uncached_prompt'] for c in calls)
    total_cached = sum(c['cached_prompt'] for c in calls)
    total_prompt = sum(c['total_prompt'] for c in calls)
    total_candidates = sum(c['candidates'] for c in calls)
    total_thoughts = sum(c['thoughts'] for c in calls)
    total_text = sum(c['text_out'] for c in calls)
    total_all = sum(c['total_tokens'] for c in calls)
    
    print(f"\n==================================================")
    print(f"TOKEN USAGE BREAKDOWN: {label}")
    print(f"==================================================")
    print(f"Total LLM API Calls      : {len(calls):,}")
    print(f"Total Input (Prompt) Tokens: {total_prompt:,}")
    print(f"  - Cached Content Tokens : {total_cached:,} ({total_cached/total_prompt*100:.1f}%)" if total_prompt else "  - Cached Content Tokens : 0")
    print(f"  - Uncached Prompt Tokens: {total_uncached:,}")
    print(f"Total Output (Gen) Tokens: {total_candidates:,}")
    print(f"  - Reasoning / Thinking  : {total_thoughts:,} ({total_thoughts/total_candidates*100:.1f}%)" if total_candidates else "  - Reasoning / Thinking  : 0")
    print(f"  - Output Text Response  : {total_text:,}")
    print(f"--------------------------------------------------")
    print(f"GRAND TOTAL TOKENS        : {total_all:,}")
    print(f"==================================================")

if test2_start_step:
    calls_test2 = [c for c in llm_calls if c['step_idx'] >= test2_start_step]
    sum_stats(calls_test2, "STRESS TEST 2 (Tahap 1 s.d. Tahap 7 pada test_3.1.xar)")

sum_stats(llm_calls, "SELURUH SESI CONVERSATION (Project V2 Test 1 + Stress Test 2)")
