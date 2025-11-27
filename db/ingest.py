"""
Text file ingestion module.
Handles splitting text into chunks and creating nodes + edges.
"""

from typing import List, Dict, Tuple
from db.models import NodeCreate
from db.storage import create_node, create_edge
from db.search import generate_embedding


def split_text_into_chunks(text: str, method: str = "paragraph") -> List[str]:
    """
    Split text into chunks based on the specified method.
    
    Args:
        text: The full text content to split
        method: "paragraph" (split by blank lines) or "lines" (every N lines)
    
    Returns:
        List of text chunks (non-empty)
    """
    chunks = []
    
    if method == "paragraph":
        # Split by double newlines (blank lines)
        paragraphs = text.split("\n\n")
        for para in paragraphs:
            cleaned = para.strip()
            if cleaned:
                chunks.append(cleaned)
    
    elif method == "lines":
        # Split every 10 lines
        lines = text.split("\n")
        chunk_size = 10
        for i in range(0, len(lines), chunk_size):
            chunk = "\n".join(lines[i:i+chunk_size]).strip()
            if chunk:
                chunks.append(chunk)
    
    # Fallback: if no chunks created, treat entire text as one chunk
    if not chunks and text.strip():
        chunks = [text.strip()]
    
    return chunks


def ingest_text_file(
    filename: str,
    content: str,
    split_method: str = "paragraph"
) -> Dict:
    """
    Ingest a text file: split into chunks, create nodes, link with edges.
    
    Args:
        filename: Original filename
        content: Full text content
        split_method: How to split the text
    
    Returns:
        Dict with file_name, total_chunks, node_ids
    """
    # Split into chunks
    chunks = split_text_into_chunks(content, method=split_method)
    
    # Create nodes for each chunk
    node_ids = []
    for idx, chunk_text in enumerate(chunks):
        # Generate embedding for this chunk
        embedding = generate_embedding(chunk_text)
        
        # Create node with metadata
        node_data = NodeCreate(
            text=chunk_text,
            metadata={
                "file_name": filename,
                "chunk_index": str(idx),  # Convert to string for Pydantic
                "source": "file_upload"
            },
            embedding=embedding
        )
        
        node = create_node(node_data, embedding)
        node_ids.append(node.id)
    
    # Create edges to link chunks in a chain (chunk i → chunk i+1)
    edge_ids = []
    for i in range(len(node_ids) - 1):
        edge = create_edge(
            source_id=node_ids[i],
            target_id=node_ids[i + 1],
            edge_type="next",
            weight=1.0
        )
        edge_ids.append(edge.id)
    
    return {
        "file_name": filename,
        "total_chunks": len(chunks),
        "node_ids": node_ids,
        "edge_count": len(edge_ids)
    }
