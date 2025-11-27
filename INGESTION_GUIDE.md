# File Ingestion & Search - Quick Test Guide

## What's New? 🎉

Your Hybrid Vector + Graph Database now has:

1. **📁 File Upload Pipeline**: Upload `.txt` files that are automatically split into chunks
2. **🔗 Auto-Graph Creation**: Chunks are linked as a sequential graph
3. **🎨 Modern UI**: Clean two-step interface (Upload → Search)
4. **🗑️ Database Reset**: Clear all data and start fresh

## How to Test (2 Minutes)

### Step 1: Start the Server

```bash
cd C:\Users\koush\OneDrive\Documents\VG\Vector
python -m uvicorn main:app --reload --port 8000
```

### Step 2: Open the UI

Open your browser to: **http://localhost:8000/ui/index.html**

### Step 3: Upload a Document

1. Click "📄 Choose a .txt file"
2. Select `sample_ml_document.txt` (provided in the project folder)
3. Click "⚡ Ingest File"
4. You should see: "✅ Success! File ingested with 10 chunks"

### Step 4: Try Different Search Modes

#### A) Vector Search (Semantic Similarity)
- Query: "What is neural network architecture?"
- Mode: 🎯 Vector Search
- Click 🔍 Search
- **Expected**: Returns chunks about neural networks, architecture, and layers

#### B) Graph Traversal (Sequential Reading)
- Mode: 🕸️ Graph Traversal
- Start Node ID: 1
- Depth: 3
- Click 🔍 Search
- **Expected**: Returns first 4 chunks in sequential order (0, 1, 2, 3)

#### C) Hybrid Search (Best of Both)
- Query: "How do you prevent overfitting?"
- Mode: ⚡ Hybrid Search
- Vector Weight: 0.7, Graph Weight: 0.3
- Start Node ID: 1
- Depth: 2
- Click 🔍 Search
- **Expected**: Returns relevant chunks about overfitting with graph context

## Compare the Results! 🔬

### Try This Experiment:

**Query**: "training and optimization"

1. **Vector Only**: Finds chunks semantically similar to "training and optimization"
2. **Graph Only**: Shows sequential chunks from a starting point
3. **Hybrid**: Combines both - finds relevant chunks AND considers their graph relationships

**Observation**: Hybrid search often gives better context because it considers both:
- Semantic relevance (vector scores)
- Document structure (graph connections)

## Demo for Judges 👨‍⚖️

**Show the pipeline in action:**

1. **Clear Database**: Click "🗑️ Clear Database" (optional, starts fresh)
2. **Upload**: Show file upload with `sample_ml_document.txt`
3. **Point out the metadata**: After upload, show the success message with node IDs and edge count
4. **Search comparison**:
   - Ask: "What is deep learning?"
   - Run all 3 modes (Vector, Graph, Hybrid)
   - Show how results differ
5. **Explain the value**: 
   - Vector = semantic search (meaning-based)
   - Graph = structural search (document flow)
   - Hybrid = combines both for better retrieval

## API Endpoints (for testing via curl/Postman)

### Upload a file:
```bash
curl -X POST "http://localhost:8000/ingest/text-file" \
  -F "file=@sample_ml_document.txt"
```

### Clear database:
```bash
curl -X POST "http://localhost:8000/admin/clear"
```

### Vector search:
```bash
curl -X POST "http://localhost:8000/search/vector" \
  -H "Content-Type: application/json" \
  -d '{"query_text": "neural networks", "top_k": 5}'
```

## What the Judges Will Love ❤️

✅ **No manual node creation** - Just upload a file!  
✅ **Automatic chunking** - Smart paragraph splitting  
✅ **Auto-graph building** - Links chunks sequentially  
✅ **Clean UX** - Clear two-step workflow  
✅ **Three search modes** - Shows different retrieval strategies  
✅ **Visual feedback** - Status messages, scores, chunk info  

## Troubleshooting

**Server not starting?**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use a different port
python -m uvicorn main:app --reload --port 8001
```

**UI not showing?**
- Make sure the `/ui` folder exists with `index.html`
- Check console for errors: F12 → Console tab

**File upload failing?**
- Only `.txt` files are supported
- Check file is readable (not locked by another program)

## Next Steps

Want to test with your own document?
1. Create any `.txt` file with multiple paragraphs
2. Upload it through the UI
3. Search and explore!

**Recommended test documents:**
- Technical documentation
- Research papers (exported as .txt)
- Articles or blog posts
- Meeting notes with sections

---

🚀 **Your hackathon submission is ready!**  
Repository: https://github.com/KoushikVNS/Vector-Hybrid
