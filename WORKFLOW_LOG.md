# Agent Collaboration Workflow Log

**Project:** ⚽ FIFA World Cup 2026 Travel Agent  
**Course:** Deep Generative Models  
**Tools Used:** Claude (claude.ai), Ollama (Llama3), SDXL Turbo, ControlNet

---

## Phase 1 — Ideation and Planning

### Prompt Used
```
我想做一個 FIFA World Cup 2026 旅遊規劃 AI Agent，
結合 RAG 知識庫、本地 LLM 推理、以及 Diffusion 圖像生成。
請幫我規劃系統架構和技術選型。
```

### Agent Output
Claude proposed a three-layer architecture:
- **Data Layer** — Wikipedia-based knowledge base + FAISS vector index
- **LLM Layer** — Ollama (Llama3) for itinerary generation
- **Generation Layer** — SDXL Turbo for travel poster creation

### Decision
Adopted the proposed stack. Selected Gradio for UI due to rapid prototyping capability.

---

## Phase 2 — Architecture Design and Task Decomposition

### Prompt Used
```
請幫我把這個專案拆解成具體的 Python 檔案，
每個檔案負責什麼功能，執行順序是什麼？
```

### Agent Output
Claude decomposed the project into:

| File | Responsibility |
|------|---------------|
| `generate_kb.py` | Knowledge base generation |
| `build_index.py` | FAISS index construction |
| `rag.py` | Vector retrieval class |
| `llm_agent.py` | LLM prompt and inference |
| `image_generator.py` | Diffusion image generation |
| `app.py` | Gradio UI integration |

### Key Decision
Agent identified that `build_kb.py` and `generate_kb.py` were redundant. Resolved by keeping only `generate_kb.py` (covers 16 cities vs. 6, with structured stadium/schedule data).

---

## Phase 3 — Code Generation and Implementation

### 3.1 Knowledge Base Generation

**Prompt Used:**
```
幫我寫 generate_kb.py，從 Wikipedia 抓取 16 個 FIFA 2026 主辦城市的資料，
加入球場名稱、賽事備註，存成結構化 .txt 檔。
```

**Technical Bottleneck Resolved:**  
Wikipedia API 需要 `user_agent` 參數，否則請求會被拒絕。Agent 自動加入正確的 header 設定。

---

### 3.2 FAISS Index Construction

**Prompt Used:**
```
幫我寫 build_index.py，讀取 kb/ 資料夾的所有 .txt，
用 SentenceTransformer 做 embedding，建立 FAISS IndexFlatL2。
```

**Result:** Successfully indexed all city documents + tournament schedule into `data/worldcup.index`.

---

### 3.3 Multi-Agent Architecture (Upgrade)

**Prompt Used:**
```
目前只有一個 LLM agent 做所有事情，
我想升級成 Multi-Agent 架構，拆成行程、美食、預算三個 Agent 平行執行。
```

**Agent Design Decision:**  
Claude recommended `concurrent.futures.ThreadPoolExecutor` for parallel execution over `asyncio`, because Ollama's REST API is synchronous and thread-based parallelism is simpler to implement correctly.

**Files Generated:**
- `agents/itinerary_agent.py`
- `agents/food_agent.py`
- `agents/budget_agent.py`
- `orchestrator.py`

**Result:** 3x speed improvement over sequential execution.

---

### 3.4 ControlNet Image Generation (Upgrade)

**Prompt Used:**
```
把圖像生成從 SDXL Turbo 升級成 ControlNet，
根據城市地標圖片做 Canny 邊緣偵測，再生成風格化海報。
城市地標圖片從網路自動抓取。
```

**Technical Bottleneck 1 — Wikipedia 403 Error:**

```
requests.exceptions.HTTPError: 403 Client Error: Forbidden
requests.exceptions.ConnectTimeout
```

**Root Cause:** Wikipedia blocks requests without a proper `User-Agent` header. Fallback URL also timed out due to network restrictions.

**Resolution by Agent:**
```python
# 加入 User-Agent header
HEADERS = {
    "User-Agent": "WorldCupTravelAgent/1.0 (educational project)"
}
# 網路失敗時改用 PIL 本地生成佔位圖，不再發第二次網路請求
def make_placeholder(city: str) -> Image.Image:
    img = Image.new("RGB", (512, 512), color=(30, 80, 50))
    ...
```

**Technical Bottleneck 2 — Model Selection:**  
SDXL Turbo is not compatible with ControlNet pipelines. Agent recommended switching to `runwayml/stable-diffusion-v1-5` + `lllyasviel/sd-controlnet-canny` with `UniPCMultistepScheduler`.

**Files Modified:**
- `landmark_fetcher.py` — city landmark fetching with local fallback
- `image_generator.py` — replaced SDXL Turbo with ControlNet pipeline

---

## Phase 4 — UI Encapsulation and Finalization

**Prompt Used:**
```
把 Gradio UI 改成分頁式介面，
行程、美食、預算、海報、RAG 各一個分頁。
Travel Poster 分頁左右並排顯示地標原圖和 AI 生成圖。
```

**Result:** UI restructured from single-output `gr.Interface` to multi-tab `gr.Blocks` layout.

---

## Summary of Technical Bottlenecks Resolved by Agent

| # | Problem | Resolution |
|---|---------|------------|
| 1 | `build_kb.py` 和 `generate_kb.py` 功能重疊 | 保留功能較完整的 `generate_kb.py`，刪除舊版 |
| 2 | Wikipedia API 需要 User-Agent | Agent 自動補上正確 header |
| 3 | 單一 LLM agent 速度慢 | 改為 ThreadPoolExecutor 平行執行 |
| 4 | Wikipedia 圖片 403 + Timeout | 改用本地 PIL 生成 fallback 佔位圖 |
| 5 | SDXL Turbo 不支援 ControlNet | 切換至 SD v1.5 + ControlNet Canny pipeline |

---

## Tools and Models Used

| Tool / Model | Purpose |
|---|---|
| Claude (claude.ai) | Architecture design, code generation, debugging |
| Ollama + Llama3 | Local LLM inference for travel planning |
| SentenceTransformer (all-MiniLM-L6-v2) | Document embedding |
| FAISS | Vector similarity search |
| SD v1.5 + ControlNet Canny | Landmark-guided poster generation |
| wikipediaapi | Knowledge base data source |
| Gradio | Interactive web UI |
