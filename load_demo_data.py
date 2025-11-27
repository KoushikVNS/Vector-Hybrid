"""
Demo Data Loader - Populate the database with sample data
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"


def load_demo_data():
    """Load the demo dataset into the database."""
    
    print("=" * 80)
    print("Loading Demo Data - Programming Concepts Knowledge Graph")
    print("=" * 80)
    
    # Load demo data from JSON
    with open("demo_data.json", "r") as f:
        data = json.load(f)
    
    print(f"\n📦 Dataset: {data['description']}")
    print(f"📊 Contains: {len(data['nodes'])} nodes, {len(data['edges'])} edges\n")
    
    # Create nodes
    print("1️⃣  Creating nodes...")
    node_id_map = {}  # Map from json position to actual node ID
    
    for idx, node_data in enumerate(data['nodes'], 1):
        response = requests.post(f"{BASE_URL}/nodes", json=node_data)
        if response.status_code == 200:
            node = response.json()
            node_id_map[idx] = node['id']
            print(f"   ✓ Node {node['id']}: {node['text'][:60]}...")
        else:
            print(f"   ✗ Failed to create node {idx}")
            return False
    
    time.sleep(0.5)
    
    # Create edges with actual node IDs
    print("\n2️⃣  Creating edges...")
    for edge_data in data['edges']:
        # Map source and target to actual IDs
        actual_edge = {
            "source": node_id_map[edge_data['source']],
            "target": node_id_map[edge_data['target']],
            "type": edge_data['type'],
            "weight": edge_data['weight']
        }
        response = requests.post(f"{BASE_URL}/edges", json=actual_edge)
        if response.status_code == 200:
            edge = response.json()
            print(f"   ✓ Edge {edge['id']}: {edge['source']} --[{edge['type']}]--> {edge['target']}")
        else:
            print(f"   ✗ Failed to create edge")
    
    print("\n" + "=" * 80)
    print("✅ Demo data loaded successfully!")
    print("=" * 80)
    print(f"\n🌐 Visit http://127.0.0.1:8000/docs to explore the API")
    print(f"📝 Node IDs: {list(node_id_map.values())}")
    
    return node_id_map


if __name__ == "__main__":
    try:
        node_ids = load_demo_data()
        if node_ids:
            print(f"\n💡 TIP: Use node ID {list(node_ids.values())[0]} as start_id in hybrid search")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the server is running:")
        print("   python -m uvicorn main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")
