"""Graph traversal and search functionality."""
from collections import deque
from typing import List, Tuple, Dict, Any
import random
import numpy as np
from db.storage import get_all_edges, get_all_nodes


# Vector dimension constant
VECTOR_DIM = 128


# ==================== Embedding Generation ====================

def generate_embedding(text: str) -> List[float]:
    """
    Generate a deterministic pseudo-random embedding vector for text.
    
    Uses hash-based seeding to ensure the same text always produces
    the same embedding across runs.
    
    Args:
        text: The text to generate an embedding for
        
    Returns:
        A list of VECTOR_DIM floats in range [0, 1)
    """
    # Seed the random generator with hash of text for determinism
    seed = hash(text) % (2**32)
    rng = random.Random(seed)
    
    # Generate VECTOR_DIM random floats
    embedding = [rng.random() for _ in range(VECTOR_DIM)]
    
    return embedding


# ==================== Vector Similarity ====================

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cosine similarity score in range [-1, 1], or 0.0 if either vector is zero
    """
    a_arr = np.array(a)
    b_arr = np.array(b)
    
    dot_product = np.dot(a_arr, b_arr)
    norm_a = np.linalg.norm(a_arr)
    norm_b = np.linalg.norm(b_arr)
    
    # Handle zero vectors
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return float(dot_product / (norm_a * norm_b))


# ==================== Vector Search ====================

def vector_search(query_text: str, top_k: int = 5) -> List[Tuple[int, float]]:
    """
    Perform vector similarity search using cosine similarity.
    
    Args:
        query_text: The search query text
        top_k: Number of top results to return (default: 5)
        
    Returns:
        List of (node_id, score) tuples sorted by score descending
    """
    # Generate query embedding
    query_embedding = generate_embedding(query_text)
    
    # Get all nodes
    nodes = get_all_nodes()
    
    # Calculate similarity for each node
    results = []
    for node_id, node in nodes.items():
        score = cosine_similarity(query_embedding, node.embedding)
        results.append((node_id, score))
    
    # Sort by score descending
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Return top_k results
    return results[:top_k]


# ==================== Graph Traversal ====================

def get_neighbors(node_id: int) -> list[int]:
    """
    Get all neighbors of a given node.
    
    Args:
        node_id: The ID of the node to find neighbors for
        
    Returns:
        List of node IDs that are neighbors (connected by edges)
    """
    neighbors = []
    edges = get_all_edges()
    
    for edge in edges.values():
        if edge.source == node_id:
            neighbors.append(edge.target)
        elif edge.target == node_id:
            neighbors.append(edge.source)
    
    return neighbors


def graph_traversal(start_id: int, depth: int = 1) -> list[int]:
    """
    Perform breadth-first search (BFS) traversal from a starting node.
    
    Args:
        start_id: The ID of the starting node
        depth: Maximum depth to traverse (default: 1)
        
    Returns:
        List of node IDs reachable within the specified depth, including start node
    """
    if depth < 0:
        return []
    
    visited = {start_id}
    result = [start_id]
    queue = deque([(start_id, 0)])
    
    while queue:
        current_node, current_depth = queue.popleft()
        
        if current_depth >= depth:
            continue
        
        neighbors = get_neighbors(current_node)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                result.append(neighbor)
                queue.append((neighbor, current_depth + 1))
    
    return result


def get_graph_distances(start_id: int, depth: int) -> dict[int, int]:
    """
    Get BFS distances from start node to all reachable nodes within depth.
    
    Args:
        start_id: The ID of the starting node
        depth: Maximum depth to traverse
        
    Returns:
        Dictionary mapping node IDs to their distance from start node
    """
    if depth < 0:
        return {}
    
    distances = {start_id: 0}
    queue = deque([(start_id, 0)])
    visited = {start_id}
    
    while queue:
        current_node, current_depth = queue.popleft()
        
        if current_depth >= depth:
            continue
        
        neighbors = get_neighbors(current_node)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = current_depth + 1
                queue.append((neighbor, current_depth + 1))
    
    return distances


# ==================== Hybrid Search ====================

def hybrid_search(
    query_text: str,
    vector_weight: float,
    graph_weight: float,
    start_id: int,
    depth: int,
    top_k: int = 5
) -> List[Tuple[int, float]]:
    """
    Perform hybrid search combining vector similarity and graph relationships.
    
    Args:
        query_text: The search query text
        vector_weight: Weight for vector similarity score
        graph_weight: Weight for graph proximity score
        start_id: Starting node ID for graph traversal
        depth: Maximum graph traversal depth
        top_k: Number of top results to return (default: 5)
        
    Returns:
        List of (node_id, combined_score) tuples sorted by score descending
    """
    # 1) Get vector scores for all nodes
    vec_results = dict(vector_search(query_text, top_k=1000))
    
    # 2) Get graph reachability and distances
    graph_distances = get_graph_distances(start_id, depth)
    
    # 3) Calculate max distance for normalization
    max_dist = max(graph_distances.values()) if graph_distances else 1
    
    # 4) Combine scores
    combined_scores = []
    
    for node_id in vec_results:
        # Vector score
        v_score = vec_results[node_id]
        
        # Graph score (normalized distance: 1 for start, decreasing with distance)
        if node_id in graph_distances:
            dist = graph_distances[node_id]
            g_score = 1.0 - (dist / max_dist) if max_dist > 0 else 1.0
        else:
            g_score = 0.0  # Not reachable
        
        # Combined score
        final_score = vector_weight * v_score + graph_weight * g_score
        combined_scores.append((node_id, final_score))
    
    # 5) Sort by final score descending
    combined_scores.sort(key=lambda x: x[1], reverse=True)
    
    # 6) Return top_k
    return combined_scores[:top_k]


# ==================== Enhanced Search with Edges ====================

def get_edges_between_nodes(node_ids: List[int]) -> List[Dict[str, Any]]:
    """
    Get all edges that connect nodes in the given list.
    
    Args:
        node_ids: List of node IDs to find edges between
        
    Returns:
        List of edge dictionaries with source, target, type, and weight
    """
    node_set = set(node_ids)
    edges = get_all_edges()
    
    result_edges = []
    for edge_id, edge in edges.items():
        if edge.source in node_set and edge.target in node_set:
            result_edges.append({
                "id": edge_id,
                "source": edge.source,
                "target": edge.target,
                "type": edge.type,
                "weight": edge.weight
            })
    
    return result_edges


def vector_search_with_edges(query_text: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Perform vector search and return nodes with connecting edges.
    
    Args:
        query_text: The search query text
        top_k: Number of top results to return
        
    Returns:
        Dictionary with 'nodes' (list of node_id, score tuples) and 'edges' (list of edge dicts)
    """
    # Get vector search results
    results = vector_search(query_text, top_k)
    
    # Get node IDs
    node_ids = [node_id for node_id, score in results]
    
    # Get edges between these nodes
    edges = get_edges_between_nodes(node_ids)
    
    return {
        "nodes": results,
        "edges": edges,
        "node_count": len(results),
        "edge_count": len(edges)
    }


def graph_traversal_with_edges(start_id: int, depth: int = 1) -> Dict[str, Any]:
    """
    Perform graph traversal and return nodes with connecting edges.
    
    Args:
        start_id: The ID of the starting node
        depth: Maximum depth to traverse
        
    Returns:
        Dictionary with 'nodes' (list of node IDs) and 'edges' (list of edge dicts)
    """
    # Get traversal results
    node_ids = graph_traversal(start_id, depth)
    
    # Get edges between these nodes
    edges = get_edges_between_nodes(node_ids)
    
    return {
        "nodes": node_ids,
        "edges": edges,
        "node_count": len(node_ids),
        "edge_count": len(edges)
    }


def hybrid_search_with_edges(
    query_text: str,
    vector_weight: float,
    graph_weight: float,
    start_id: int,
    depth: int,
    top_k: int = 5
) -> Dict[str, Any]:
    """
    Perform hybrid search and return nodes with connecting edges.
    
    Args:
        query_text: The search query text
        vector_weight: Weight for vector similarity score
        graph_weight: Weight for graph proximity score
        start_id: Starting node ID for graph traversal
        depth: Maximum graph traversal depth
        top_k: Number of top results to return
        
    Returns:
        Dictionary with 'nodes' (list of node_id, score tuples) and 'edges' (list of edge dicts)
    """
    # Get hybrid search results
    results = hybrid_search(query_text, vector_weight, graph_weight, start_id, depth, top_k)
    
    # Get node IDs
    node_ids = [node_id for node_id, score in results]
    
    # Get edges between these nodes
    edges = get_edges_between_nodes(node_ids)
    
    return {
        "nodes": results,
        "edges": edges,
        "node_count": len(results),
        "edge_count": len(edges),
        "vector_weight": vector_weight,
        "graph_weight": graph_weight
    }
