import json
with open(r'C:\Users\mr.yo\.gemini\antigravity-ide\brain\eb6ac8aa-15e1-4c63-a951-03195e1683c0\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Detailed Browser Subagent Actions' in line:
            data = json.loads(line)
            print("FOUND SUBAGENT REPORT:")
            print(data.get('content', '')[:2000])
