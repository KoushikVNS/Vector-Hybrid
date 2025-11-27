"""FastAPI application for hybrid vector + graph database."""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
from pydantic import BaseModel
from contextlib import asynccontextmanager
from db.models import Edge, EdgeCreate, Node, NodeCreate
from db import storage, search
from db.ingest import ingest_text_file
from pathlib import Path
import os


# ==================== Lifespan Management ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown."""
    # Startup
    storage.load_snapshot()
    print("✓ Application started - data loaded")
    yield
    # Shutdown
    storage.save_snapshot()
    print("✓ Application shutdown - data saved")


app = FastAPI(
    title="Hybrid Vector + Graph Database",
    description="A database supporting both vector embeddings and graph relationships",
    version="1.0.0",
    lifespan=lifespan
)

# Mount UI static files
ui_path = Path(__file__).parent / "ui"
if ui_path.exists():
    app.mount("/ui", StaticFiles(directory=str(ui_path)), name="ui")


# ==================== Request Models ====================

class VectorSearchRequest(BaseModel):
    """Request model for vector search."""
    query_text: str
    top_k: int = 5


class HybridSearchRequest(BaseModel):
    """Request model for hybrid search."""
    query_text: str
    vector_weight: float = 0.7
    graph_weight: float = 0.3
    start_id: int
    depth: int = 2
    top_k: int = 5


# ==================== Node CRUD Endpoints ====================

@app.post("/nodes", response_model=Node, tags=["Nodes"])
def create_node(node_data: NodeCreate):
    """
    Create a new node with text, metadata, and auto-generated embedding.
    
    Args:
        node_data: Node creation data with text and optional metadata
        
    Returns:
        The created Node with assigned ID and embedding
    """
    # Generate embedding from text
    embedding = search.generate_embedding(node_data.text)
    
    # Create node with embedding
    node = storage.create_node(node_data, embedding)
    return node


@app.get("/nodes/{node_id}", response_model=Node, tags=["Nodes"])
def get_node(node_id: int):
    """
    Retrieve a node by its ID.
    
    Args:
        node_id: The ID of the node to retrieve
        
    Returns:
        The Node if found
        
    Raises:
        HTTPException: 404 if node not found
    """
    node = storage.get_node(node_id)
    if node is None:
        raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
    return node


@app.put("/nodes/{node_id}", response_model=Node, tags=["Nodes"])
def update_node(node_id: int, node_data: NodeCreate):
    """
    Update a node's text, metadata, and regenerate its embedding.
    
    Args:
        node_id: The ID of the node to update
        node_data: Updated node data with text and metadata
        
    Returns:
        The updated Node
        
    Raises:
        HTTPException: 404 if node not found
    """
    # Generate new embedding from text
    embedding = search.generate_embedding(node_data.text)
    
    # Update node
    node = storage.update_node(node_id, node_data, embedding)
    if node is None:
        raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
    return node


@app.delete("/nodes/{node_id}", tags=["Nodes"])
def delete_node(node_id: int):
    """
    Delete a node and all its connected edges.
    
    Args:
        node_id: The ID of the node to delete
        
    Returns:
        Status confirmation
    """
    storage.delete_node(node_id)
    return {"status": "ok"}


# ==================== Edge CRUD Endpoints ====================

@app.post("/edges", response_model=Edge, tags=["Edges"])
def create_edge(edge_data: EdgeCreate):
    """
    Create a new edge between two nodes.
    
    Args:
        edge_data: Edge creation data with source, target, type, and optional weight
        
    Returns:
        The created Edge with assigned ID
    """
    edge = storage.create_edge(edge_data)
    return edge


@app.get("/edges/{edge_id}", response_model=Edge, tags=["Edges"])
def get_edge(edge_id: int):
    """
    Retrieve an edge by its ID.
    
    Args:
        edge_id: The ID of the edge to retrieve
        
    Returns:
        The Edge if found
        
    Raises:
        HTTPException: 404 if edge not found
    """
    edge = storage.get_edge(edge_id)
    if edge is None:
        raise HTTPException(status_code=404, detail=f"Edge {edge_id} not found")
    return edge


@app.delete("/edges/{edge_id}", tags=["Edges"])
def delete_edge(edge_id: int):
    """
    Delete an edge by its ID.
    
    Args:
        edge_id: The ID of the edge to delete
        
    Returns:
        Status confirmation
    """
    storage.delete_edge(edge_id)
    return {"status": "ok"}


# ==================== Search Endpoints ====================

@app.post("/search/vector", tags=["Search"])
def vector_search_endpoint(payload: VectorSearchRequest):
    """
    Perform vector similarity search using cosine similarity.
    
    Args:
        payload: Search request with query text and top_k parameter
        
    Returns:
        Dictionary with 'results' key containing list of (node_id, score) tuples
    """
    results = search.vector_search(
        query_text=payload.query_text,
        top_k=payload.top_k
    )
    return {"results": results}


@app.get("/search/graph", tags=["Search"])
def graph_search(start_id: int, depth: int = 1):
    """
    Perform graph traversal using BFS from a starting node.
    
    Args:
        start_id: The ID of the starting node
        depth: Maximum depth to traverse (default: 1)
        
    Returns:
        Dictionary with 'nodes' key containing list of reachable node IDs
    """
    nodes = search.graph_traversal(start_id, depth)
    return {"nodes": nodes}


@app.post("/search/hybrid", tags=["Search"])
def hybrid_search_endpoint(payload: HybridSearchRequest):
    """
    Perform hybrid search combining vector similarity and graph relationships.
    
    Args:
        payload: Search request with query text, weights, start node, depth, and top_k
        
    Returns:
        Dictionary with 'results' key containing list of (node_id, score) tuples
    """
    results = search.hybrid_search(
        query_text=payload.query_text,
        vector_weight=payload.vector_weight,
        graph_weight=payload.graph_weight,
        start_id=payload.start_id,
        depth=payload.depth,
        top_k=payload.top_k
    )
    return {"results": results}


# ==================== Enhanced Search Endpoints with Edges ====================

@app.post("/search/vector/detailed", tags=["Search"])
def vector_search_detailed_endpoint(payload: VectorSearchRequest):
    """
    Perform vector similarity search and return nodes with connecting edges.
    
    Args:
        payload: Search request with query text and top_k parameter
        
    Returns:
        Dictionary with 'nodes', 'edges', 'node_count', and 'edge_count'
    """
    result = search.vector_search_with_edges(
        query_text=payload.query_text,
        top_k=payload.top_k
    )
    return result


@app.get("/search/graph/detailed", tags=["Search"])
def graph_search_detailed(start_id: int, depth: int = 1):
    """
    Perform graph traversal and return nodes with connecting edges.
    
    Args:
        start_id: The ID of the starting node
        depth: Maximum depth to traverse (default: 1)
        
    Returns:
        Dictionary with 'nodes', 'edges', 'node_count', and 'edge_count'
    """
    result = search.graph_traversal_with_edges(start_id, depth)
    return result


@app.post("/search/hybrid/detailed", tags=["Search"])
def hybrid_search_detailed_endpoint(payload: HybridSearchRequest):
    """
    Perform hybrid search and return nodes with connecting edges.
    
    Args:
        payload: Search request with query text, weights, start node, depth, and top_k
        
    Returns:
        Dictionary with 'nodes', 'edges', 'node_count', 'edge_count', and weights used
    """
    result = search.hybrid_search_with_edges(
        query_text=payload.query_text,
        vector_weight=payload.vector_weight,
        graph_weight=payload.graph_weight,
        start_id=payload.start_id,
        depth=payload.depth,
        top_k=payload.top_k
    )
    return result


# ==================== File Ingestion Endpoints ====================

@app.post("/ingest/text-file", tags=["Ingestion"])
async def ingest_text_file_endpoint(file: UploadFile = File(...)):
    """
    Upload and ingest a .txt file into the database.
    
    The file is split into chunks (paragraphs), each chunk becomes a node,
    and nodes are linked in a sequential chain with edges.
    
    Args:
        file: The uploaded text file
        
    Returns:
        Dictionary with file_name, total_chunks, and node_ids
        
    Raises:
        HTTPException: 400 if file is not a text file
    """
    # Validate file type
    if not file.filename.endswith('.txt'):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are supported"
        )
    
    # Read file content
    content = await file.read()
    text = content.decode('utf-8')
    
    # Ingest the file
    result = ingest_text_file(
        filename=file.filename,
        content=text,
        split_method="paragraph"
    )
    
    return result


@app.post("/admin/clear", tags=["Admin"])
def clear_database():
    """
    Clear all nodes and edges from the database and reset counters.
    
    WARNING: This deletes all data!
    
    Returns:
        Status confirmation
    """
    # Clear all data using the storage module's functions
    # Access the internal storage to clear it
    storage._nodes.clear()
    storage._edges.clear()
    
    # Reset ID counters
    from itertools import count
    storage._node_id_counter = count(1)
    storage._edge_id_counter = count(1)
    
    # Delete persistence file if it exists
    data_dir = Path(__file__).parent / "data"
    snapshot_file = data_dir / "storage.json"
    if snapshot_file.exists():
        os.remove(snapshot_file)
    
    return {
        "status": "ok",
        "message": "Database cleared successfully"
    }


# ==================== Root Endpoint ====================

@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint with API information.
    
    Returns:
        Welcome message and available endpoints
    """
    return {
        "message": "Hybrid Vector + Graph Database API",
        "docs": "/docs",
        "ui": "/ui/index.html",
        "endpoints": {
            "nodes": "/nodes",
            "edges": "/edges",
            "vector_search": "/search/vector",
            "graph_search": "/search/graph",
            "hybrid_search": "/search/hybrid",
            "ingest": "/ingest/text-file",
            "clear": "/admin/clear"
        }
    }
