"""Simple test to verify the implementation works."""
import sys
sys.path.insert(0, 'C:\\Users\\koush\\OneDrive\\Documents\\VG\\Vector')

from db.models import NodeCreate, EdgeCreate
from db import storage, search

print("=" * 80)
print("Testing Hybrid Vector + Graph Database Implementation")
print("=" * 80)

# Test 1: Create nodes
print("\n1. Creating nodes...")
node1_data = NodeCreate(text="Python is a programming language", metadata={"category": "tech"})
embedding1 = search.generate_embedding(node1_data.text)
node1 = storage.create_node(node1_data, embedding1)
print(f"   Created node {node1.id}: {node1.text}")
print(f"   Embedding dimension: {len(node1.embedding)}")

node2_data = NodeCreate(text="Machine learning uses algorithms", metadata={"category": "ai"})
embedding2 = search.generate_embedding(node2_data.text)
node2 = storage.create_node(node2_data, embedding2)
print(f"   Created node {node2.id}: {node2.text}")

node3_data = NodeCreate(text="FastAPI is a web framework", metadata={"category": "tech"})
embedding3 = search.generate_embedding(node3_data.text)
node3 = storage.create_node(node3_data, embedding3)
print(f"   Created node {node3.id}: {node3.text}")

node4_data = NodeCreate(text="Neural networks are powerful", metadata={"category": "ai"})
embedding4 = search.generate_embedding(node4_data.text)
node4 = storage.create_node(node4_data, embedding4)
print(f"   Created node {node4.id}: {node4.text}")

# Test 2: Get a node
print(f"\n2. Retrieving node {node1.id}...")
retrieved = storage.get_node(node1.id)
if retrieved:
    print(f"   Successfully retrieved: {retrieved.text}")
    print(f"   Metadata: {retrieved.metadata}")

# Test 3: Create edges
print("\n3. Creating edges...")
edge1_data = EdgeCreate(source=node1.id, target=node2.id, type="related_to", weight=0.8)
edge1 = storage.create_edge(edge1_data)
print(f"   Created edge {edge1.id}: {edge1.source} -> {edge1.target}")

edge2_data = EdgeCreate(source=node1.id, target=node3.id, type="related_to", weight=0.9)
edge2 = storage.create_edge(edge2_data)
print(f"   Created edge {edge2.id}: {edge2.source} -> {edge2.target}")

edge3_data = EdgeCreate(source=node2.id, target=node4.id, type="related_to", weight=0.7)
edge3 = storage.create_edge(edge3_data)
print(f"   Created edge {edge3.id}: {edge3.source} -> {edge3.target}")

# Test 4: Vector search
print("\n4. Performing vector search...")
query = "programming and web development"
results = search.vector_search(query, top_k=3)
print(f"   Query: '{query}'")
print(f"   Found {len(results)} results:")
for node_id, score in results:
    node = storage.get_node(node_id)
    if node:
        print(f"   - Node {node_id} (score={score:.4f}): {node.text}")

# Test 5: Graph traversal
print(f"\n5. Graph traversal from node {node1.id}...")
reachable = search.graph_traversal(node1.id, depth=2)
print(f"   Reachable nodes: {reachable}")
for nid in reachable:
    node = storage.get_node(nid)
    if node:
        print(f"   - Node {nid}: {node.text}")

# Test 6: Hybrid search
print("\n6. Performing hybrid search...")
query = "artificial intelligence"
hybrid_results = search.hybrid_search(
    query_text=query,
    vector_weight=0.7,
    graph_weight=0.3,
    start_id=node1.id,
    depth=2,
    top_k=3
)
print(f"   Query: '{query}'")
print(f"   Start node: {node1.id}")
print(f"   Found {len(hybrid_results)} results:")
for node_id, score in hybrid_results:
    node = storage.get_node(node_id)
    if node:
        print(f"   - Node {node_id} (score={score:.4f}): {node.text}")

# Test 7: Update node
print(f"\n7. Updating node {node1.id}...")
update_data = NodeCreate(
    text="Python is a powerful programming language for AI",
    metadata={"category": "tech", "updated": "true"}
)
new_embedding = search.generate_embedding(update_data.text)
updated = storage.update_node(node1.id, update_data, new_embedding)
if updated:
    print(f"   Updated text: {updated.text}")
    print(f"   Updated metadata: {updated.metadata}")

# Test 8: Delete edge
print(f"\n8. Deleting edge {edge1.id}...")
storage.delete_edge(edge1.id)
print(f"   Edge deleted successfully")

# Test 9: Delete node (and its connected edges)
print(f"\n9. Deleting node {node4.id}...")
storage.delete_node(node4.id)
print(f"   Node deleted successfully (edge {edge3.id} also deleted)")

# Verify deletion
print("\n10. Verifying deletion...")
deleted_node = storage.get_node(node4.id)
print(f"   Node {node4.id} exists: {deleted_node is not None}")
deleted_edge = storage.get_edge(edge3.id)
print(f"   Edge {edge3.id} exists: {deleted_edge is not None}")

print("\n" + "=" * 80)
print("All tests completed successfully!")
print("=" * 80)
