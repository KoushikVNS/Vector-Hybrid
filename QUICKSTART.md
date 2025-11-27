# 🚀 Quick Start Guide - Hackathon Submission

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
cd Vector
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python -m uvicorn main:app --reload --port 8000
```

### 3. Load Demo Data
```bash
# In a new terminal
python load_demo_data.py
```

### 4. Access the Application

- **Web UI:** http://127.0.0.1:8000/ui/index.html
- **API Docs:** http://127.0.0.1:8000/docs
- **API Root:** http://127.0.0.1:8000/

---

## 📊 Demo Walkthrough (60 seconds)

### Test Vector Search
```bash
curl -X POST "http://localhost:8000/search/vector" \
  -H "Content-Type: application/json" \
  -d '{"query_text": "machine learning", "top_k": 3}'
```

### Test Graph Search
```bash
curl "http://localhost:8000/search/graph?start_id=1&depth=2"
```

### Test Hybrid Search
```bash
curl -X POST "http://localhost:8000/search/hybrid" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "artificial intelligence",
    "vector_weight": 0.7,
    "graph_weight": 0.3,
    "start_id": 1,
    "depth": 2,
    "top_k": 5
  }'
```

---

## 📁 Project Structure

```
Vector/
├── main.py                      # FastAPI app + endpoints
├── requirements.txt             # Dependencies
├── README.md                    # Full documentation
├── DEMO_SCRIPT.md              # Detailed demo instructions
├── ARCHITECTURE.md             # System architecture
├── QUICKSTART.md               # This file
│
├── db/
│   ├── models.py               # Data models (Node, Edge)
│   ├── storage.py              # Storage + persistence
│   └── search.py               # Search algorithms
│
├── ui/
│   └── index.html              # Web interface
│
├── data/
│   └── storage.json            # Auto-generated data file
│
├── demo_data.json              # Sample dataset
├── load_demo_data.py           # Data loader script
└── simple_test.py              # Automated tests
```

---

## 🎯 Key Features to Demo

### 1. **Node CRUD**
- Create nodes with text + metadata
- Auto-generated embeddings
- Full CRUD support

### 2. **Edge CRUD**
- Connect nodes with typed relationships
- Weighted edges
- Cascade deletion

### 3. **Vector Search**
- Semantic similarity using cosine distance
- Find content by meaning, not keywords
- Ranked results

### 4. **Graph Search**
- BFS traversal
- Find connected nodes
- Configurable depth

### 5. **Hybrid Search** ⭐
- Best of both worlds
- Weighted combination
- Context-aware results

### 6. **Persistence**
- Automatic JSON save/load
- Survives server restarts
- Human-readable format

---

## 💡 Hackathon Talking Points

### Problem Solved
"Traditional databases are either good at semantic search OR relationship queries. We built a hybrid system that does BOTH, giving you smarter, context-aware results for AI applications."

### Technical Innovation
- Combines vector embeddings with graph traversal
- Configurable weight system for different use cases
- Clean architecture, type-safe, production-ready design

### Use Cases
1. **RAG Systems** - Better context retrieval for LLMs
2. **Recommendation Engines** - Similar + connected items
3. **Knowledge Graphs** - Semantic + structural queries
4. **Research Discovery** - Papers by topic + citations

### Why It Matters
- Vector-only DBs miss relationships
- Graph-only DBs miss semantics
- Hybrid approach captures both

---

## 🔥 Demo Tips

### Best Demo Flow
1. Show UI first (visual, impressive)
2. Run all three search types with same query
3. Compare results to show hybrid advantage
4. Show API docs (auto-generated, professional)
5. Mention extensibility (real embeddings, SQL, etc.)

### Good Demo Queries
- "machine learning and AI" (finds ML, TensorFlow, Python)
- "web development frameworks" (finds FastAPI, React, JavaScript)
- "artificial intelligence" (shows Deep Learning connections)

### Weight Adjustments to Show
- `0.9 vector, 0.1 graph` → Semantic-focused
- `0.5 vector, 0.5 graph` → Balanced
- `0.1 vector, 0.9 graph` → Connectivity-focused

---

## 📈 Next Steps (If Asked)

### Production Enhancements
- Real embeddings (sentence-transformers, OpenAI)
- PostgreSQL + pgvector backend
- FAISS/Annoy for vector indexing
- Authentication & rate limiting
- Caching layer (Redis)
- Monitoring & observability

### Scaling Strategy
- Horizontal scaling with load balancer
- Read replicas for search
- Write-ahead log for consistency
- Microservices architecture

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use different port
python -m uvicorn main:app --port 8001
```

### Import errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### No demo data
```bash
# Ensure server is running first
python load_demo_data.py
```

### CORS errors in UI
- UI must be accessed via server: `http://127.0.0.1:8000/ui/index.html`
- Don't open `index.html` directly as a file

---

## 📞 Support

**Documentation:**
- README.md - Full documentation
- DEMO_SCRIPT.md - Detailed demo walkthrough
- ARCHITECTURE.md - System design

**API Docs:**
- Interactive: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## ✅ Submission Checklist

- [x] All CRUD operations working
- [x] Vector search implemented
- [x] Graph search implemented
- [x] Hybrid search implemented
- [x] Persistence working
- [x] API documented
- [x] Web UI created
- [x] Demo data prepared
- [x] Architecture documented
- [x] Tests passing

---

**🎉 You're ready to present! Good luck with the hackathon!**
