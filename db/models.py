"""Data models for the hybrid database."""
from pydantic import BaseModel
from typing import Dict, List


class NodeCreate(BaseModel):
    """Model for creating a new node."""
    text: str
    metadata: Dict[str, str] = {}


class Node(NodeCreate):
    """Model representing a node with an assigned ID and embedding."""
    id: int
    embedding: List[float]


class EdgeCreate(BaseModel):
    """Model for creating a new edge between nodes."""
    source: int
    target: int
    type: str
    weight: float = 1.0


class Edge(EdgeCreate):
    """Model representing an edge with an assigned ID."""
    id: int
