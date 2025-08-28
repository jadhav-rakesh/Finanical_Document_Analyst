# Financial Document Analyzer

A FastAPI-based AI system for analyzing financial documents.  
It verifies uploaded financial PDFs, extracts structured data, provides professional financial analysis, generates investment recommendations, and conducts risk assessments using **CrewAI agents** and **custom tools**.

---

##  Features

- **Document Verification** → Checks if uploaded files are valid financial reports.  
- **Financial Analysis** → Extracts and interprets revenue, net income, EPS, leverage ratios, etc.  
- **Investment Insights** → Provides data-driven Buy/Hold/Sell recommendations.  
- **Risk Assessment** → Evaluates liquidity, leverage, and market risks.  

---

##  Bugs Found & Fixes

### 🔹 Deterministic Bugs
| Issue | Before | Fix |
|-------|--------|-----|
| **LLM undefined** | `llm = llm` (self-referencing) | Properly initialized `LLM` object with OpenRouter model + API key. |
| **Agent param mismatch** | `tool=[...]` | Corrected to `tools=[...]`. |
| **Endpoint/task name conflict** | Both named `analyze_financial_document` | Renamed FastAPI endpoint → `analyze_financial_document_endpoint`. |
| **PDF reader missing** | Used undefined `Pdf` class | Replaced with `pdfplumber` for reliable parsing. |
| **File cleanup** | Sometimes left undeleted | Added safe cleanup in `finally` block. |

### 🔹 Inefficient Prompts
| Agent | Before | After |
|-------|--------|-------|
| Financial Analyst | Over-dramatic, speculative, “make up facts” | Professional, evidence-based, compliance-aware |
| Verifier | Approved any document (even grocery list) | Validates presence of balance sheet, income, cash flow statements |
| Investment Advisor | Pushed meme stocks/crypto | Provides risk-aware, client-focused advice |
| Risk Assessor | Ignored real risk, “YOLO volatility” | Structured low/medium/high risk evaluations |

---

## ⚙️ Setup Instructions

### 1. Clone repo & install dependencies
```bash
git clone https://github.com/jadhav-rakesh/Finanical_Document_Analyst.git
cd Finanical_Document_Analyst
pip install -r requirements.txt
```

### 2. Set environment variables

Create a .env file:
```bash
OPENROUTER_API_KEY=your_openrouter_key
```

### 3. Run FastAPI server
```bash
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

##  API Documentation
🔹 Health Check
Endpoint
```bash
GET /
```
Response
```bash
{ "message": "Financial Document Analyzer API is running" }
```

🔹 Analyze Financial Document
Endpoint
```bash
POST /analyze
```
Parameters

- file → PDF file (UploadFile)

- query → Analysis request (string, optional)

Example Request (cURL)
```bash
curl -X POST "http://127.0.0.1:8001/analyze" \
  -F "file=@sample_financials.pdf" \
  -F "query=Analyze revenue growth and risks"
```

Example Response
```bash
{
  "status": "success",
  "query": "Analyze revenue growth and risks",
  "analysis": "📊 Investment Analysis Report\n- Revenue: $25M\n- Net Income: $2.5M\n- Profit Margin: 10.0%\n✅ Strong profitability.\n⚠️ Moderate leverage risk.\n",
  "file_processed": "sample_financials.pdf"
}
```
📂 Project Structure
```bash
.
├── main.py                # FastAPI app & endpoints
├── agents.py              # Agents (Analyst, Verifier, Advisor, Risk Assessor)
├── task.py                # CrewAI task definitions
├── tools.py               # PDF parsing, investment & risk tools
├── requirements.txt       # Python dependencies
└── data/                  # Uploaded financial documents
```
