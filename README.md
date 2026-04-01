# ISOMORPH — Same Structure. Different Form.

> "CMU finds you an inspiring paper. ISOMORPH gives you working code."

ISOMORPH is a structural analogy engine for researchers. It takes a problem description in plain text, extracts its underlying mathematical and system-level structure, and retrieves analogous methods from disparate scientific domains—complete with scored mappings, failure conditions, and runnable Python primitives.

---

## 🎨 The Philosophy
Most AI search engines focus on **surface similarity** (keywords, jargon, domain overlap). ISOMORPH focuses on **structural isomorphism** (variables, constraints, equation forms). 

By stripping away domain-specific language, ISOMORPH identifies that a crack propagation problem in materials science might be structurally identical to a resource-allocation problem in biology or a fluid-flow bottleneck in engineering.

---

## 🛠️ Core Pipeline (v0.1)

ISOMORPH operates through a deterministic 6-step pipeline designed for precision and validation:

1.  **EXTRACTOR:** Groq (Llama-3) transforms raw text into a Pydantic-validated `ExtractedStructure`.
2.  **EMBEDDER:** Local `sentence-transformers` generate a 384-dimensional vector from the structure.
3.  **MATCHER:** `pgvector` performs cosine similarity search against a curated knowledge base of 300-500 methods.
4.  **SCORER:** Parallelized Groq calls score each match, documenting where the analogy holds and where it breaks.
5.  **VALIDATOR:** Sanity filter to ensure only high-confidence analogies reach the user.
6.  **PRIMITIVE FETCHER:** Attaches runnable Python code (Primitives) to the resulting analogies.

---

## 🚀 Tech Stack

- **Language:** Python 3.11+
- **API Framework:** FastAPI (Async, Pydantic v2)
- **Intelligence:** Groq (Llama-3.3-70B-Versatile)
- **Database:** PostgreSQL + `pgvector`
- **Embeddings:** `all-MiniLM-L6-v2` (Local/Fast)
- **ORM:** SQLAlchemy + Alembic
- **Containerization:** Docker + Docker Compose

---

## 📂 Project Structure

```text
isomorph/
├── backend/                # FastAPI Core
│   ├── app/
│   │   ├── api/            # Routes & Dependencies
│   │   ├── core/           # Pipeline, Extractor, Matcher, Scorer
│   │   ├── db/             # Models, Sessions, Seed Data
│   │   ├── primitives/     # Interface & Implementations
│   │   └── schemas/        # Pydantic Hard Contracts
│   ├── evaluation/         # Quality measurement tools
│   └── cli.py              # CLI Entry Point
├── frontend/               # React + Vite (Post-v0.1)
├── docs/                   # Specs & Architecture
└── docker-compose.yml      # Full Stack Orchestration
```

---

## 🚦 Getting Started (Development)

### Prerequisites
- Docker & Docker Compose
- Groq API Key

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/isomorph.git
   cd isomorph
   ```

2. **Configure environment:**
   ```bash
   cp backend/.env.example backend/.env
   # Add your GROQ_API_KEY to .env
   ```

3. **Launch the stack:**
   ```bash
   docker-compose up --build
   ```

4. **Run the CLI:**
   ```bash
   python backend/cli.py "I am trying to optimize the flow of nutrients in a synthetic soil matrix with stochastic drainage."
   ```

---

## 📉 Success Criteria

A successful run returns:
- **3-5 Analogies** from completely different scientific domains.
- **Variable Mapping:** How your "soil nutrients" map to their "system variables".
- **Failure Conditions:** Critical breakdown points where the analogy no longer applies.
- **Runnable Primitive:** A Python snippet you can run on your data immediately.

---

## 📜 License
Apache-2.0 — Created by Adarsh Solomon (2026)
