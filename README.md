# Post-Disaster AI Agents Backend

This repository hosts the **backend intelligence layer** for the fullstack [PostDisaster-Ai-Agentic-Alert-System](https://github.com/AbhyDev/PostDisaster-Ai-Agentic-Alert-System). It focuses on disaster intelligence gathering and response planning powered by multi-agent workflows and Google Gemini models. The frontend consumes the JSON summaries generated here to present timely situation awareness dashboards.

## ✨ Highlights
- Multi-agent crisis analysis orchestrated with [CrewAI](https://docs.crewai.com/).
- Retrieval-augmented generation over curated DOCX situation reports.
- Satellite image triage via Gemini Flash to locate city markers in imagery.
- Persistent Chroma vector store (`db/`) for fast, incremental reruns.
- Pluggable tools for resource allocation and dispatch projections.

## 🧭 Architecture
```
Cities.docx ─▶ DOCXSearchTool ─┐
                                │     ┌────────────┐
                                ├────▶│ data_collector (Agent)
                                │     └────────────┘
                                │            │ context
                                ▼            ▼
                        Crew Tasks & Context Chaining
                                │
   resourcing() tool ───────────┤
   helping() tool ─────────────▶│
                                ▼
        needs_analyst ▷ help_dispatcher ▷ resource_allocator ▷ damage_analyser
                                │
                                ▼
                     Structured agent_outputs JSON
                                │
                                ▼
                    Frontend alert visualizations
```
- `PostDisaster_System.ipynb` defines the agents, task graph, and JSON reshaping logic.
- `docx` knowledge is loaded once and cached in Chroma (`db/`). Delete the folder to force re-ingestion when documents change.
- `satellite.py` is a standalone Gemini Flash client that extracts the city label from a marked satellite snapshot, feeding upstream routing decisions.

## 🛠️ Prerequisites
- Python 3.10+
- Google Cloud project with Gemini 1.5/2.0 API access.
- System audio libraries if you enable the optional `pyttsx3` synthesis (see `requirements.txt`).

## ⚙️ Setup
1. Install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Configure secrets:
   - Copy `.env.example` (if available) or create `.env`.
   - Set `GOOGLE_API_KEY` (required by both the notebook and `satellite.py`).

3. Prepare data assets:
   - Ensure `Cities.docx` and any supplemental DOCX sources live at the project root.
   - Place annotated satellite imagery (e.g., `DummySatelliteImage.png`) alongside `satellite.py` or adjust paths accordingly.

## 🚀 Running the Workflows
### Notebook-driven multi-agent analysis
1. Launch Jupyter and open `PostDisaster_System.ipynb`.
2. Execute cells sequentially; the Crew `kickoff()` cell triggers:
   - Document retrieval through `DOCXSearchTool` with Gemini embeddings.
   - Five collaborating agents, each producing a 30–40 word situational brief.
   - Assembly of a `agent_outputs` dictionary keyed by agent role names.
3. The final cell prints a JSON string ready for the frontend API.

> **Tip:** Update `city_map` (Cell 3) and `Analysed_Site` (Cell 6) when onboarding new cities. Always keep the indices synchronized with external references.

### Satellite city detector
Run the script directly to verify Gemini access and detect the city marker:

```bash
python satellite.py
```

It loads the configured Gemini Flash model once and reuses the global client for subsequent calls.

## 📦 Project Conventions
- Agent goals and expected outputs are limited to 30–40 words to keep alerts concise.
- Task `context` arrays ensure downstream agents receive upstream summaries—preserve this chain when modifying or adding agents.
- Utility tools (`resourcing`, `helping`) live in the notebook; new tools should follow the `@tool` decorator pattern so CrewAI can invoke them.
- Generated artifacts (images, JSON snapshots) belong in `Output_Images/` to stay aligned with the frontend build pipeline.

## ✅ Verification Checklist
- Run the notebook after any knowledge base change; delete `db/` beforehand to refresh embeddings.
- Execute the `try` block in `satellite.py` to confirm Gemini connectivity.
- Inspect `agent_outputs` for missing keys before handing data off to the frontend.

## 🧩 Extensibility Ideas
- Add new modalities (audio, geospatial overlays) by extending the notebook and reusing the existing task orchestration.
- When exposing REST endpoints, mirror the notebook’s JSON schema (`Needs Analyst Agent`, `Help Dispatcher Agent`, etc.) so the frontend can deserialize without changes.
- For additional documents, drop them next to `Cities.docx` and update the DOCX tool glide path as needed.

## 📄 License
Licensed under the [Apache License 2.0](./LICENSE).

---
For automation tips aimed at AI coding agents, see [`.github/copilot-instructions.md`](.github/copilot-instructions.md).
