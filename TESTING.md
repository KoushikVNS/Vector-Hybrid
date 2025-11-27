# Testing Guide for Graph Database

## Method 1: Using the Test Script (Automated)

### Step 1: Start the server
Open a terminal and run:
```bash
cd c:\Users\koush\OneDrive\Documents\Vector
C:/Users/koush/OneDrive/Documents/Vector/.venv/Scripts/python.exe -m uvicorn main:app --reload
```

The server will start at http://localhost:8000

### Step 2: Run the test script
Open a NEW terminal and run:
```bash
cd c:\Users\koush\OneDrive\Documents\Vector
C:/Users/koush/OneDrive/Documents/Vector/.venv/Scripts/python.exe test_api.py
```

---

## Method 2: Using Swagger UI (Interactive)

### Step 1: Start the server (same as above)

### Step 2: Open your browser
Go to: http://localhost:8000/docs

### Step 3: Test the endpoints interactively

#### Create Edges:
1. Click on `POST /edges`
2. Click "Try it out"
3. Use this JSON:
```json
{
  "source": 1,
  "target": 2,
  "type": "related_to",
  "weight": 1.0
}
```
4. Click "Execute"
5. Repeat to create more edges:
   - Node 1 → Node 3 (type: "cites")
   - Node 2 → Node 4 (type: "related_to")
   - Node 3 → Node 5 (type: "mentions")

#### Test Graph Traversal:
1. Click on `GET /search/graph`
2. Click "Try it out"
3. Enter:
   - start_id: 1
   - depth: 2
4. Click "Execute"
5. You should see all nodes reachable from node 1 within 2 hops

#### Get Edge by ID:
1. Click on `GET /edges/{edge_id}`
2. Click "Try it out"
3. Enter edge_id: 1
4. Click "Execute"

#### Delete Edge:
1. Click on `DELETE /edges/{edge_id}`
2. Click "Try it out"
3. Enter edge_id: 1
4. Click "Execute"

---

## Method 3: Using cURL (Command Line)

### Create an edge:
```bash
curl -X POST "http://localhost:8000/edges" -H "Content-Type: application/json" -d "{\"source\": 1, \"target\": 2, \"type\": \"related_to\", \"weight\": 1.0}"
```

### Get an edge:
```bash
curl "http://localhost:8000/edges/1"
```

### Graph traversal:
```bash
curl "http://localhost:8000/search/graph?start_id=1&depth=2"
```

### Delete an edge:
```bash
curl -X DELETE "http://localhost:8000/edges/1"
```

---

## Method 4: Using Python requests

```python
import requests

# Create edges
response = requests.post("http://localhost:8000/edges", json={
    "source": 1,
    "target": 2,
    "type": "related_to",
    "weight": 1.0
})
print(response.json())

# Graph traversal
response = requests.get("http://localhost:8000/search/graph?start_id=1&depth=2")
print(response.json())
```

---

## Expected Test Results

### Graph Structure:
```
Node 1 → Node 2
Node 1 → Node 3
Node 2 → Node 4
Node 3 → Node 5
Node 4 → Node 5
```

### Traversal from Node 1:
- Depth 1: [1, 2, 3]
- Depth 2: [1, 2, 3, 4, 5]
- Depth 3: [1, 2, 3, 4, 5] (same, no more nodes)

### Traversal from Node 2:
- Depth 1: [2, 1, 4]
- Depth 2: [2, 1, 4, 3, 5]

---

## Quick Start (Recommended)

1. Open Terminal 1 and run:
   ```bash
   cd c:\Users\koush\OneDrive\Documents\Vector
   C:/Users/koush/OneDrive/Documents/Vector/.venv/Scripts/python.exe -m uvicorn main:app --reload
   ```

2. Open your browser to http://localhost:8000/docs

3. Use the Swagger UI to test all endpoints interactively!
