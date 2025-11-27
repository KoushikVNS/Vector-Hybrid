"""Test script to verify the vector and hybrid search implementation."""
import requests
import json

BASE_URL = "http://127.0.0.1:8001"


def test_api():
    """Test all API endpoints."""
    print("=" * 80)
    print("Testing Hybrid Vector + Graph Database API")
    print("=" * 80)
    
    # Test 1: Create nodes
    print("\n1. Creating nodes...")
    nodes_data = [
        {"text": "Python is a programming language", "metadata": {"category": "tech"}},
        {"text": "Machine learning uses algorithms", "metadata": {"category": "ai"}},
        {"text": "FastAPI is a web framework", "metadata": {"category": "tech"}},
        {"text": "Neural networks are powerful", "metadata": {"category": "ai"}},
    ]
    
    node_ids = []
    for data in nodes_data:
        response = requests.post(f"{BASE_URL}/nodes", json=data)
        if response.status_code == 200:
            node = response.json()
            node_ids.append(node["id"])
            print(f"   Created node {node['id']}: {node['text'][:50]}...")
        else:
            print(f"   Failed to create node: {response.status_code}")
    
    # Test 2: Get a node
    print(f"\n2. Retrieving node {node_ids[0]}...")
    response = requests.get(f"{BASE_URL}/nodes/{node_ids[0]}")
    if response.status_code == 200:
        node = response.json()
        print(f"   Text: {node['text']}")
        print(f"   Metadata: {node['metadata']}")
        print(f"   Embedding dimension: {len(node['embedding'])}")
    else:
        print(f"   Failed: {response.status_code}")
    
    # Test 3: Create edges
    print("\n3. Creating edges...")
    edges_data = [
        {"source": node_ids[0], "target": node_ids[1], "type": "related_to", "weight": 0.8},
        {"source": node_ids[0], "target": node_ids[2], "type": "related_to", "weight": 0.9},
        {"source": node_ids[1], "target": node_ids[3], "type": "related_to", "weight": 0.7},
    ]
    
    edge_ids = []
    for data in edges_data:
        response = requests.post(f"{BASE_URL}/edges", json=data)
        if response.status_code == 200:
            edge = response.json()
            edge_ids.append(edge["id"])
            print(f"   Created edge {edge['id']}: {edge['source']} -> {edge['target']}")
        else:
            print(f"   Failed to create edge: {response.status_code}")
    
    # Test 4: Vector search
    print("\n4. Performing vector search...")
    search_query = {
        "query_text": "programming and web development",
        "top_k": 3
    }
    response = requests.post(f"{BASE_URL}/search/vector", json=search_query)
    if response.status_code == 200:
        results = response.json()["results"]
        print(f"   Found {len(results)} results:")
        for node_id, score in results:
            print(f"   - Node {node_id}: score={score:.4f}")
    else:
        print(f"   Failed: {response.status_code}")
    
    # Test 5: Graph traversal
    print(f"\n5. Graph traversal from node {node_ids[0]}...")
    response = requests.get(f"{BASE_URL}/search/graph?start_id={node_ids[0]}&depth=2")
    if response.status_code == 200:
        nodes = response.json()["nodes"]
        print(f"   Reachable nodes: {nodes}")
    else:
        print(f"   Failed: {response.status_code}")
    
    # Test 6: Hybrid search
    print("\n6. Performing hybrid search...")
    hybrid_query = {
        "query_text": "artificial intelligence",
        "vector_weight": 0.7,
        "graph_weight": 0.3,
        "start_id": node_ids[0],
        "depth": 2,
        "top_k": 3
    }
    response = requests.post(f"{BASE_URL}/search/hybrid", json=hybrid_query)
    if response.status_code == 200:
        results = response.json()["results"]
        print(f"   Found {len(results)} results:")
        for node_id, score in results:
            print(f"   - Node {node_id}: combined score={score:.4f}")
    else:
        print(f"   Failed: {response.status_code}")
    
    # Test 7: Update node
    print(f"\n7. Updating node {node_ids[0]}...")
    update_data = {
        "text": "Python is a powerful programming language for AI",
        "metadata": {"category": "tech", "updated": "true"}
    }
    response = requests.put(f"{BASE_URL}/nodes/{node_ids[0]}", json=update_data)
    if response.status_code == 200:
        node = response.json()
        print(f"   Updated text: {node['text']}")
        print(f"   Updated metadata: {node['metadata']}")
    else:
        print(f"   Failed: {response.status_code}")
    
    # Test 8: Delete edge
    print(f"\n8. Deleting edge {edge_ids[0]}...")
    response = requests.delete(f"{BASE_URL}/edges/{edge_ids[0]}")
    if response.status_code == 200:
        print(f"   Edge deleted successfully")
    else:
        print(f"   Failed: {response.status_code}")
    
    # Test 9: Delete node
    print(f"\n9. Deleting node {node_ids[-1]}...")
    response = requests.delete(f"{BASE_URL}/nodes/{node_ids[-1]}")
    if response.status_code == 200:
        print(f"   Node deleted successfully")
    else:
        print(f"   Failed: {response.status_code}")
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running on port 8001.")
    except Exception as e:
        print(f"Error: {e}")
