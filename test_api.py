import requests
import json
import time

time.sleep(1)

# Test WITHOUT interpretation first (faster)
payload = {
    "files": {
        "app.py": "def process_data(data):\n    return validate(data)\n\ndef validate(data):\n    return transform(data)\n\ndef transform(data):\n    return process_data(data)",
        "utils.py": "def helper():\n    pass"
    },
    "interpret": False  # No Claude interpretation yet
}

try:
    print("🚀 Testing PathOs Flask API (no interpretation)...\n")
    response = requests.post("http://localhost:5000/analyze", json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        
        print("✅ Response received!\n")
        print("=" * 70)
        print("📊 TOPOLOGY SUMMARY")
        print("=" * 70)
        summary = data["summary"]
        print(f"📦 Nodes:    {summary['node_count']}")
        print(f"🔗 Edges:    {summary['edge_count']}")
        print(f"🔁 Cycles:   {summary['cycle_count']}")
        print(f"⚡ Clusters: {summary['scc_count']}")
        print()
        
        print("=" * 70)
        print("⚠️  CONTRADICTIONS DETECTED")
        print("=" * 70)
        
        if not data["contradictions"]:
            print("✓ No contradictions found!")
        else:
            for i, c in enumerate(data["contradictions"], 1):
                severity_bars = '●' * c['severity'] + '○' * (3-c['severity'])
                print(f"\n[{i}] {c['kind'].upper()}")
                print(f"    Register:  {c['register']}")
                print(f"    Severity:  {severity_bars}")
                print(f"    Nodes:     {len(c['nodes'])}")
                print(f"    Summary:   {c['description'][:100]}...")
        
        print("\n" + "=" * 70)
        print("✓ Flask API is working! 🎉")
        print("=" * 70)
        print("\n📍 Server running at: http://localhost:5000")
        print("📍 Test endpoint:     POST /analyze")
        print("📍 Visualization:     POST /graph/visualization")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")
