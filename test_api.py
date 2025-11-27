"""Test script for the graph database API."""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_create_edges():
    """Test creating edges between nodes."""
    print("\n=== Testing Edge Creation ===")
    
    # Create edges
    edges_to_create = [
        {"source": 1, "target": 2, "type": "related_to", "weight": 1.0},
        {"source": 1, "target": 3, "type": "cites", "weight": 0.8},
        {"source": 2, "target": 4, "type": "related_to", "weight": 1.0},
        {"source": 3, "target": 5, "type": "mentions", "weight": 0.5},
        {"source": 4, "target": 5, "type": "related_to", "weight": 1.0},
    ]
    
    created_edges = []
    for edge_data in edges_to_create:
        response = requests.post(f"{BASE_URL}/edges", json=edge_data)
        if response.status_code == 200:
            edge = response.json()
            created_edges.append(edge)
            print(f"✓ Created edge {edge['id']}: Node {edge['source']} → Node {edge['target']} ({edge['type']})")
        else:
            print(f"✗ Failed to create edge: {response.text}")
    
    return created_edges


def test_get_edge(edge_id):
    """Test retrieving an edge by ID."""
    print(f"\n=== Testing Get Edge {edge_id} ===")
    response = requests.get(f"{BASE_URL}/edges/{edge_id}")
    if response.status_code == 200:
        edge = response.json()
        print(f"✓ Retrieved edge: {json.dumps(edge, indent=2)}")
        return edge
    else:
        print(f"✗ Failed to get edge: {response.text}")
        return None


def test_graph_traversal():
    """Test graph traversal at different depths."""
    print("\n=== Testing Graph Traversal ===")
    
    # Test from node 1 at different depths
    for depth in [1, 2, 3]:
        response = requests.get(f"{BASE_URL}/search/graph?start_id=1&depth={depth}")
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Traversal from node 1, depth {depth}: {result['nodes']}")
        else:
            print(f"✗ Failed traversal: {response.text}")
    
    # Test from node 2
    response = requests.get(f"{BASE_URL}/search/graph?start_id=2&depth=2")
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Traversal from node 2, depth 2: {result['nodes']}")


def test_delete_edge(edge_id):
    """Test deleting an edge."""
    print(f"\n=== Testing Delete Edge {edge_id} ===")
    response = requests.delete(f"{BASE_URL}/edges/{edge_id}")
    if response.status_code == 200:
        print(f"✓ Deleted edge {edge_id}: {response.json()}")
    else:
        print(f"✗ Failed to delete edge: {response.text}")
    
    # Verify deletion
    response = requests.get(f"{BASE_URL}/edges/{edge_id}")
    if response.status_code == 404:
        print(f"✓ Confirmed edge {edge_id} no longer exists")
    else:
        print(f"✗ Edge {edge_id} still exists after deletion")


def test_graph_structure():
    """Visualize the graph structure."""
    print("\n=== Graph Structure ===")
    print("Node 1 → Node 2 (related_to)")
    print("Node 1 → Node 3 (cites)")
    print("Node 2 → Node 4 (related_to)")
    print("Node 3 → Node 5 (mentions)")
    print("Node 4 → Node 5 (related_to)")
    print("\nExpected traversal from Node 1:")
    print("  Depth 1: [1, 2, 3]")
    print("  Depth 2: [1, 2, 3, 4, 5]")
    print("  Depth 3: [1, 2, 3, 4, 5]")


def main():
    """Run all tests."""
    print("🧪 Starting Graph Database Tests")
    print(f"📡 Server: {BASE_URL}")
    
    try:
        # Check if server is running
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("❌ Server is not responding. Please start it with: uvicorn main:app --reload")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start it with: uvicorn main:app --reload")
        return
    
    print("✓ Server is running\n")
    
    # Show graph structure
    test_graph_structure()
    
    # Run tests
    created_edges = test_create_edges()
    
    if created_edges:
        test_get_edge(created_edges[0]['id'])
    
    test_graph_traversal()
    
    if created_edges:
        test_delete_edge(created_edges[0]['id'])
        
        # Test traversal after deletion
        print("\n=== Testing Traversal After Edge Deletion ===")
        response = requests.get(f"{BASE_URL}/search/graph?start_id=1&depth=2")
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Traversal after deletion: {result['nodes']}")
    
    print("\n✅ All tests completed!")
    print(f"\n💡 Tip: Visit {BASE_URL}/docs for interactive API documentation")


if __name__ == "__main__":
    main()
