import json

log_file = r'C:\Users\Lenovo\.gemini\antigravity-ide\brain\7fc1812d-77c0-4729-a186-6403d1a60a1b\.system_generated\logs\transcript.jsonl'
with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('type') == 'USER_INPUT':
            txt = data.get('content', '').strip().replace('\n', ' ')
            print(f"Step {data.get('step_index'):4d}: {txt[:90]}")
