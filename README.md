## Overview

This project is a local meal recommendation system. It takes a natural-language request, turns it into structured recipe filters, searches the recipe dataset, and returns ranked recipe suggestions.

The system combines retrieval, filtering, ranking, and a simple agent workflow to help users find recipes that match nutrition, taste, time, and dietary needs.

## Features

- Search recipes using both semantic and keyword retrieval
- Filter by calories, cooking time, rating, and tags
- Parse user requests into structured meal constraints
- Use a local MCP server to expose retrieval and filtering tools
- Rank results by relevance and quality
- Run the full flow through a LangGraph workflow
- Serve the app through a Streamlit interface

## 1. Dataset Used

The project uses the rahul7star/food-recipes dataset from Hugging Face.

Link: https://huggingface.co/datasets/rahul7star/food-recipes

This dataset contains recipe records with details such as name, description, ingredients, steps, tags, calories, minutes, and rating.

## 2. Data Processing

The raw recipe data is processed before search and recommendation.

- Load the recipe records
- Clean and normalize fields
- Convert ingredients, steps, and tags into usable structures
- Store nutrition and time metadata
- Prepare searchable indexes for BM25 and vector retrieval
- Build the local Qdrant collection

This step makes the data ready for fast search and filtering.

## 3. Retrieval

The retrieval layer uses two search approaches:

- Semantic search through embeddings in Qdrant
- Keyword search through a BM25 index

Both results are combined using reciprocal rank fusion (RRF), which merges ranked lists from different retrieval methods. This gives stronger and more balanced recipe results than using one method alone.

## 4. Planner Agent

The planner agent converts a natural-language request into a structured meal request.

It extracts values like:

- main food
- meal type
- calorie limit
- time limit
- minimum rating
- dietary preferences

This agent is implemented in the planner module and uses Ollama to turn plain text into JSON that the rest of the system can understand.

## 5. Retrieval Agent

The retrieval agent takes the parsed meal request and searches the recipe database.

It does the following:

- runs hybrid search with both semantic and keyword methods
- filters recipe IDs by calories, cooking time, and rating
- loads the full recipe details for valid matches

This agent is responsible for gathering the best candidate recipes before ranking.

## 6. Ranking Agent

The ranking agent scores the retrieved recipes and creates the final recommendation list.

It looks at:

- retrieval strength
- recipe rating
- protein preference when relevant

It then orders the results and adds a short explanation for each recommendation.

## 7. MCP Server

The project includes a local MCP server that exposes recipe and retrieval tools.

Main capabilities include:

- health check
- fetch a recipe by ID
- filter recipe IDs by nutrition and time rules
- semantic search
- keyword search
- hybrid search

This server acts as the tool layer used by the recommendation workflow.

## 8. Ranking

After retrieval, the ranking agent scores candidates and orders them for the final recommendation list.

The ranking process considers:

- retrieval score
- recipe rating
- nutrition-related quality signals

This helps surface the best recipes among the matched results.

## 9. LangGraph Workflow

The project uses a LangGraph workflow to coordinate the recommendation pipeline.

The flow is simple:

- planner node parses the user request
- retrieval node gathers candidate recipes
- ranking node orders the results

This keeps the logic modular and easy to extend.

## 10. LLM

The planner uses an Ollama-based LLM to interpret user queries.

The model turns natural-language input into structured JSON data that is then converted into a meal request object. This is the key step that connects user intent to search constraints.

## 11. Streamlit Interface

The app provides a small web interface for the system.

Users can:

- enter a recipe query
- trigger recommendation generation
- see recipe cards with image, calories, time, rating, and summary
- expand each result to view ingredients and steps

The interface is set up in app/app.py and is designed for simple local use.

## Testing

The project has automated tests covering:

- Database operations
- Recipe filtering
- BM25
- Embeddings
- Qdrant
- Hybrid retrieval
- RRF
- Planner
- Ranking
- MCP-related components
- LangGraph state
- LangGraph workflow
- Real-component constraints

## Local Setup

Run these commands in PowerShell from the project folder:

```powershell
cd C:\Users\lenovo\Desktop\Recommendation-MCP

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -e .
pip install streamlit ollama qdrant-client sentence-transformers rank-bm25 langgraph mcp
```

Start Ollama and pull the model used by the planner:

```powershell
ollama pull qwen2.5:3b
```

Prepare the recipe data and indexes:

```powershell
python scripts/process_recipes.py
python scripts/bm25_index.py
python scripts/qdrant_index.py
```

Start the MCP server:

```powershell
python -m recommendation_mcp.mcp_server.server
```

Start the Streamlit app:

```powershell
streamlit run app/app.py
```

This project is designed to run locally and uses the recipe dataset, local indexes, and a local MCP server for retrieval and filtering.
