# 🔍 Hybrid Vector + Graph Database for AI Retrieval

A powerful database system that combines **vector embeddings** (semantic search) with **graph relationships** (connectivity search) to enable intelligent retrieval for AI applications. Built for the DevForge/Devfolio hackathon.

## 🎯 Problem Statement

Traditional databases fall short when dealing with AI-powered retrieval systems:

- **Vector-only databases** (like Pinecone, Weaviate) understand *similarity* but ignore *relationships*
- **Graph-only databases** (like Neo4j) understand *connections* but miss *semantic meaning*

**Our Solution:** A hybrid approach that combines both paradigms, giving you the best of both worlds.

## ✨ Why Hybrid Search?

Imagine searching for research papers:

- **Vector Search** finds papers with similar topics but might miss important citations
- **Graph Search** finds connected papers through citations but might miss semantically relevant ones
- **Hybrid Search** finds papers that are both semantically similar AND connected through citations

**Result:** More relevant, contextually aware results for RAG systems, recommendation engines, and knowledge graphs.

## 🚀 Features

### Core Functionality
- ✅ **Node CRUD** - Create, read, update, and delete nodes with text, metadata, and embeddings
- ✅ **Edge CRUD** - Manage directed relationships between nodes with types and weights
- ✅ **Vector Search** - Semantic similarity search using cosine similarity (128-dim embeddings)
- ✅ **Graph Traversal** - BFS-based traversal to find connected nodes up to specified depth
- ✅ **Hybrid Search** - Weighted combination of vector similarity and graph proximity

### Technical Features
- ✅ **JSON Persistence** - Automatic save/load of all data
- ✅ **REST API** - FastAPI with automatic OpenAPI documentation
- ✅ **Type Safety** - Full Pydantic models with validation
- ✅ **Deterministic Embeddings** - Consistent hash-based vectors for testing

## 🛠️ Tech Stack

- **Framework:** FastAPI (modern, fast async API)
- **Language:** Python 3.11+
- **Vector Math:** NumPy
- **Data Models:** Pydantic v2
- **Storage:** JSON (in-memory with persistence)
- **Server:** Uvicorn (ASGI server)

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup

```bash
# Clone or navigate to the project
cd Vector

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🎮 Usage Examples

### 1. Create Nodes

```bash
# Create a node with text and metadata
curl -X POST "http://localhost:8000/nodes" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Python is a versatile programming language",
    "metadata": {"category": "programming", "language": "en"}
  }'

# Response:
{
  "id": 1,
  "text": "Python is a versatile programming language",
  "metadata": {"category": "programming", "language": "en"},
  "embedding": [0.234, 0.567, ...] # 128-dimensional vector
}
```

### 2. Create Edges (Relationships)

```bash
# Create a relationship between two nodes
curl -X POST "http://localhost:8000/edges" \
  -H "Content-Type: application/json" \
  -d '{
    "source": 1,
    "target": 2,
    "type": "related_to",
    "weight": 0.9
  }'
```

### 3. Vector Search (Semantic Similarity)

```bash
# Find nodes semantically similar to query
curl -X POST "http://localhost:8000/search/vector" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "programming languages and web development",
    "top_k": 5
  }'

# Response:
{
  "results": [
    [1, 0.923],  # node_id, similarity_score
    [3, 0.876],
    [5, 0.834]
  ]
}
```

### 4. Graph Search (Traversal)

```bash
# Find all nodes connected within 2 hops
curl -X GET "http://localhost:8000/search/graph?start_id=1&depth=2"

# Response:
{
  "nodes": [1, 2, 3, 5, 7]  # All reachable node IDs
}
```

### 5. Hybrid Search (Combined)

```bash
# Best of both worlds: semantic similarity + graph proximity
curl -X POST "http://localhost:8000/search/hybrid" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "machine learning algorithms",
    "vector_weight": 0.7,
    "graph_weight": 0.3,
    "start_id": 1,
    "depth": 2,
    "top_k": 5
  }'

# Response:
{
  "results": [
    [4, 0.891],  # High combined score: similar + connected
    [2, 0.847],
    [6, 0.823]
  ]
}
```

## 🔧 Configuration

### Adjusting Search Weights

In hybrid search, you can control the balance:

- `vector_weight: 0.7, graph_weight: 0.3` - Prioritize semantic similarity (good for diverse content)
- `vector_weight: 0.5, graph_weight: 0.5` - Balanced approach (recommended default)
- `vector_weight: 0.3, graph_weight: 0.7` - Prioritize connectivity (good for citation networks)

### Storage Location

Data is automatically persisted to `data/storage.json`. The file is:
- Created automatically on first write
- Loaded on application startup
- Saved after every create/update/delete operation

## 📊 Project Structure

```
Vector/
├── main.py                 # FastAPI application & endpoints
├── requirements.txt        # Python dependencies
├── db/
│   ├── __init__.py
│   ├── models.py          # Pydantic data models
│   ├── storage.py         # In-memory storage + persistence
│   └── search.py          # Vector, graph, and hybrid search
├── data/
│   └── storage.json       # Persisted nodes and edges
├── ui/
│   └── index.html         # Optional web interface
└── README.md              # This file
```

## 🧪 Testing

Run the included test suite:

```bash
python simple_test.py
```

This will:
1. Create sample nodes and edges
2. Test vector search
3. Test graph traversal
4. Test hybrid search
5. Verify CRUD operations

## 🎯 Use Cases

### 1. Research Paper Discovery
- **Vector:** Find papers on similar topics
- **Graph:** Find papers through citation network
- **Hybrid:** Find relevant papers that are also cited by your starting paper

### 2. Product Recommendations
- **Vector:** Similar products by description
- **Graph:** Products frequently bought together
- **Hybrid:** Similar products that others also purchased

### 3. Knowledge Base / RAG
- **Vector:** Semantically relevant documents
- **Graph:** Related documents by category/author
- **Hybrid:** Contextually relevant documents from connected sources

### 4. Content Discovery
- **Vector:** Similar articles by topic
- **Graph:** Articles from same author or series
- **Hybrid:** Related content from your followed authors

## 🚧 Future Enhancements

- [ ] Real embeddings using sentence-transformers or OpenAI
- [ ] PostgreSQL backend with pgvector
- [ ] FAISS/Annoy indexing for faster vector search
- [ ] GraphQL API support
- [ ] Authentication & API keys
- [ ] Batch operations
- [ ] Real-time updates via WebSockets
- [ ] Multi-tenancy support

## 📝 API Reference

### Nodes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/nodes` | Create a new node |
| GET | `/nodes/{id}` | Get node by ID |
| PUT | `/nodes/{id}` | Update node |
| DELETE | `/nodes/{id}` | Delete node (cascades to edges) |

### Edges

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/edges` | Create a new edge |
| GET | `/edges/{id}` | Get edge by ID |
| DELETE | `/edges/{id}` | Delete edge |

### Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search/vector` | Vector similarity search |
| GET | `/search/graph` | Graph traversal (BFS) |
| POST | `/search/hybrid` | Hybrid search (vector + graph) |

## 👥 Contributing

This project was built for the DevForge/Devfolio hackathon. Contributions, issues, and feature requests are welcome!

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built for DevForge/Devfolio Hackathon Problem Statement 1
- Inspired by modern vector databases (Pinecone, Weaviate) and graph databases (Neo4j)
- Designed for RAG (Retrieval-Augmented Generation) systems

---

**Made with ❤️ for intelligent information retrieval**
