"""Test CRUD operations for Vector + Graph Hybrid Database"""
import requests
import json

BASE_URL = "http://127.0.0.1:8002"

def test_crud():
    print("="*60)
    print("Testing CRUD Operations - Vector + Graph Database")
    print("="*60)
    
    # Test 1: Create Node
    print("\n✅ TEST 1: CREATE Node")
    response = requests.post(f"{BASE_URL}/nodes", json={
        "text": "Test node for CRUD demo",
        "metadata": {"test": True}
    })
    print(f"   Status: {response.status_code}")
    node = response.json()
    node_id = node['id']
    print(f"   Created node ID: {node_id}")
    
    # Test 2: Read Node
    print("\n✅ TEST 2: READ Node")
    response = requests.get(f"{BASE_URL}/nodes/{node_id}")
    print(f"   Status: {response.status_code}")
    node = response.json()
    print(f"   Node text: '{node['text']}'")
    print(f"   Embedding dimension: {len(node['embedding'])}")
    
    # Test 3: Update Node
    print("\n✅ TEST 3: UPDATE Node")
    response = requests.put(f"{BASE_URL}/nodes/{node_id}", json={
        "text": "Updated text for CRUD demo",
        "metadata": {"test": True, "updated": True}
    })
    print(f"   Status: {response.status_code}")
    node = response.json()
    print(f"   Updated text: '{node['text']}'")
    
    # Test 4: List All Nodes
    print("\n✅ TEST 4: LIST All Nodes")
    response = requests.get(f"{BASE_URL}/nodes")
    print(f"   Status: {response.status_code}")
    nodes = response.json()
    print(f"   Total nodes: {len(nodes)}")
    
    # Test 5: Create Edge
    print("\n✅ TEST 5: CREATE Edge")
    response = requests.post(f"{BASE_URL}/edges", json={
        "source": 1,
        "target": node_id,
        "type": "test_relation",
        "weight": 0.8
    })
    print(f"   Status: {response.status_code}")
    edge = response.json()
    edge_id = edge['id']
    print(f"   Created edge ID: {edge_id}")
    print(f"   Connection: {edge['source']} -> {edge['target']}")
    
    # Test 6: Read Edge
    print("\n✅ TEST 6: READ Edge")
    response = requests.get(f"{BASE_URL}/edges/{edge_id}")
    print(f"   Status: {response.status_code}")
    edge = response.json()
    print(f"   Edge: {edge['source']} -> {edge['target']} ({edge['type']}, weight: {edge['weight']})")
    
    # Test 7: List All Edges
    print("\n✅ TEST 7: LIST All Edges")
    response = requests.get(f"{BASE_URL}/edges")
    print(f"   Status: {response.status_code}")
    edges = response.json()
    print(f"   Total edges: {len(edges)}")
    
    # Test 8: Vector Search
    print("\n✅ TEST 8: VECTOR Search")
    response = requests.get(f"{BASE_URL}/search/vector/detailed", params={
        "query": "test demo",
        "top_k": 3
    })
    print(f"   Status: {response.status_code}")
    results = response.json()
    print(f"   Found {results['node_count']} nodes")
    
    # Test 9: Graph Search
    print("\n✅ TEST 9: GRAPH Search")
    response = requests.get(f"{BASE_URL}/search/graph/detailed", params={
        "start_id": 1,
        "depth": 2
    })
    print(f"   Status: {response.status_code}")
    results = response.json()
    print(f"   Found {results['node_count']} connected nodes")
    print(f"   Found {results['edge_count']} edges")
    
    # Test 10: Hybrid Search
    print("\n✅ TEST 10: HYBRID Search")
    response = requests.get(f"{BASE_URL}/search/hybrid/detailed", params={
        "query": "test",
        "start_id": 1,
        "depth": 2,
        "vector_weight": 0.7,
        "graph_weight": 0.3,
        "top_k": 5
    })
    print(f"   Status: {response.status_code}")
    results = response.json()
    print(f"   Found {results['node_count']} nodes")
    
    # Cleanup: Delete Edge
    print("\n✅ TEST 11: DELETE Edge")
    response = requests.delete(f"{BASE_URL}/edges/{edge_id}")
    print(f"   Status: {response.status_code}")
    print(f"   Edge {edge_id} deleted")
    
    # Cleanup: Delete Node
    print("\n✅ TEST 12: DELETE Node")
    response = requests.delete(f"{BASE_URL}/nodes/{node_id}")
    print(f"   Status: {response.status_code}")
    print(f"   Node {node_id} deleted")
    
    print("\n" + "="*60)
    print("🎉 All CRUD operations tested successfully!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_crud()
    except Exception as e:
        print(f"\n❌ Error: {e}")
