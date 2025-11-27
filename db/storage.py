"""In-memory storage for graph edges and nodes with JSON persistence."""
from itertools import count
from pathlib import Path
import json
from typing import Any
from db.models import Edge, EdgeCreate, Node, NodeCreate

# Node storage
_nodes: dict[int, Node] = {}
_node_id_counter = count(1)

# Edge storage
_edges: dict[int, Edge] = {}
_edge_id_counter = count(1)

# Persistence configuration
STORAGE_FILE = Path("data") / "storage.json"


# ==================== Node CRUD Functions ====================

def create_node(data: NodeCreate, embedding: list[float]) -> Node:
    """
    Create a new node and store it in memory.
    
    Args:
        data: Node creation data with text and metadata
        embedding: The vector embedding for the node
        
    Returns:
        The created Node with assigned ID
    """
    node_id = next(_node_id_counter)
    node = Node(id=node_id, embedding=embedding, **data.model_dump())
    _nodes[node_id] = node
    save_snapshot()  # Persist after creation
    return node


def get_node(node_id: int) -> Node | None:
    """
    Retrieve a node by its ID.
    
    Args:
        node_id: The ID of the node to retrieve
        
    Returns:
        The Node if found, None otherwise
    """
    return _nodes.get(node_id)


def update_node(node_id: int, data: NodeCreate, embedding: list[float]) -> Node | None:
    """
    Update an existing node's text, metadata, and embedding.
    
    Args:
        node_id: The ID of the node to update
        data: Updated node data with text and metadata
        embedding: The new vector embedding for the node
        
    Returns:
        The updated Node if found, None otherwise
    """
    if node_id not in _nodes:
        return None
    
    node = Node(id=node_id, embedding=embedding, **data.model_dump())
    _nodes[node_id] = node
    save_snapshot()  # Persist after update
    return node


def delete_node(node_id: int) -> None:
    """
    Delete a node and all its connected edges from storage.
    
    Args:
        node_id: The ID of the node to delete
    """
    # Remove the node
    _nodes.pop(node_id, None)
    
    # Remove all edges connected to this node
    edges_to_delete = [
        edge_id for edge_id, edge in _edges.items()
        if edge.source == node_id or edge.target == node_id
    ]
    for edge_id in edges_to_delete:
        _edges.pop(edge_id, None)
    
    save_snapshot()  # Persist after deletion


def get_all_nodes() -> dict[int, Node]:
    """
    Get all nodes in storage.
    
    Returns:
        Dictionary mapping node IDs to Node objects
    """
    return _nodes


# ==================== Edge CRUD Functions ====================

def create_edge(data: EdgeCreate) -> Edge:
    """
    Create a new edge and store it in memory.
    
    Args:
        data: Edge creation data with source, target, type, and optional weight
        
    Returns:
        The created Edge with assigned ID
    """
    edge_id = next(_edge_id_counter)
    edge = Edge(id=edge_id, **data.model_dump())
    _edges[edge_id] = edge
    save_snapshot()  # Persist after creation
    return edge


def get_edge(edge_id: int) -> Edge | None:
    """
    Retrieve an edge by its ID.
    
    Args:
        edge_id: The ID of the edge to retrieve
        
    Returns:
        The Edge if found, None otherwise
    """
    return _edges.get(edge_id)


def delete_edge(edge_id: int) -> None:
    """
    Delete an edge from storage.
    
    Args:
        edge_id: The ID of the edge to delete
    """
    _edges.pop(edge_id, None)
    save_snapshot()  # Persist after deletion


def get_all_edges() -> dict[int, Edge]:
    """
    Get all edges in storage.
    
    Returns:
        Dictionary mapping edge IDs to Edge objects
    """
    return _edges


# ==================== Persistence Functions ====================

def save_snapshot() -> None:
    """
    Save the current state of nodes and edges to a JSON file.
    
    This function persists all nodes and edges along with the current
    ID counter values so they can be restored on restart.
    """
    # Create data directory if it doesn't exist
    STORAGE_FILE.parent.mkdir(exist_ok=True)
    
    # Get current counter values by finding max IDs
    max_node_id = max(_nodes.keys()) if _nodes else 0
    max_edge_id = max(_edges.keys()) if _edges else 0
    
    # Prepare data for serialization
    data = {
        "nodes": {
            str(node_id): node.model_dump()
            for node_id, node in _nodes.items()
        },
        "edges": {
            str(edge_id): edge.model_dump()
            for edge_id, edge in _edges.items()
        },
        "counters": {
            "next_node_id": max_node_id + 1,
            "next_edge_id": max_edge_id + 1
        }
    }
    
    # Write to file
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_snapshot() -> None:
    """
    Load nodes and edges from the JSON file and restore ID counters.
    
    This function is called at application startup to restore the
    previous state if a snapshot exists.
    """
    global _nodes, _edges, _node_id_counter, _edge_id_counter
    
    # Check if storage file exists
    if not STORAGE_FILE.exists():
        return
    
    try:
        # Read from file
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Restore nodes
        _nodes.clear()
        for node_id_str, node_data in data.get("nodes", {}).items():
            node_id = int(node_id_str)
            _nodes[node_id] = Node(**node_data)
        
        # Restore edges
        _edges.clear()
        for edge_id_str, edge_data in data.get("edges", {}).items():
            edge_id = int(edge_id_str)
            _edges[edge_id] = Edge(**edge_data)
        
        # Restore counters
        counters = data.get("counters", {})
        next_node_id = counters.get("next_node_id", 1)
        next_edge_id = counters.get("next_edge_id", 1)
        
        # Reset the itertools counters
        _node_id_counter = count(next_node_id)
        _edge_id_counter = count(next_edge_id)
        
        print(f"✓ Loaded {len(_nodes)} nodes and {len(_edges)} edges from storage")
        
    except Exception as e:
        print(f"✗ Error loading snapshot: {e}")
        # Don't crash - start with empty storage
