import os
import uuid
from fastapi import FastAPI, File, UploadFile, Form, HTTPException

from crewai import Crew, Process
from agents import financial_analyst, investment_advisor, risk_assessor, verifier
from task import analyze_financial_document, investment_analysis, risk_assessment, verification

app = FastAPI(title="Financial Document Analyzer")


def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """
    Run the full crew with all agents and tasks in sequence.
    """
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,  # run tasks one after another
    )

    # Pass context (query + file path)
    result = financial_crew.kickoff(
        inputs={"query": query, "file_path": file_path}
    )

    # If result is a dict-like with 'final_output'
    if isinstance(result, dict) and "final_output" in result:
        final_output = result["final_output"]
    else:
        final_output = str(result)

    return final_output


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """
    Analyze a financial document and return verification, financial analysis,
    investment recommendations, and risk assessment.
    """
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Default query if missing
        if not query.strip():
            query = "Analyze this financial document for investment insights"

        # Run the crew
        response = run_crew(query=query.strip(), file_path=file_path)

        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}"
        )

    finally:
        # Clean up uploaded file (optional, can keep if you want history)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
