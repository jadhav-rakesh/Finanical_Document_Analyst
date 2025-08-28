import os
import re
import pdfplumber
from dotenv import load_dotenv
from crewai.tools import tool
from crewai_tools import SerperDevTool

# Load environment variables (for Serper search etc.)
load_dotenv()

# External search tool (optional)
search_tool = SerperDevTool()

# --- Utility: normalize extracted numbers ---
def normalize_number(val: str) -> float:
    """
    Converts financial strings like '25.0B', '($500M)', '1,200,000' into floats.
    B = Billion, M = Million, K = Thousand.
    Negative numbers in parentheses are handled too.
    """
    try:
        val = val.replace(",", "").replace("$", "").strip()
        multiplier = 1

        # Handle parentheses for negatives
        if val.startswith("(") and val.endswith(")"):
            multiplier = -1
            val = val[1:-1]

        # Handle units
        if val.upper().endswith("B"):
            return float(val[:-1]) * 1_000_000_000 * multiplier
        elif val.upper().endswith("M"):
            return float(val[:-1]) * 1_000_000 * multiplier
        elif val.upper().endswith("K"):
            return float(val[:-1]) * 1_000 * multiplier
        else:
            return float(val) * multiplier
    except:
        return None


# --- Financial Document Tool ---
@tool("financial_document_reader")
def read_data_tool(path: str = "data/sample.pdf") -> str:
    """
    Reads and extracts structured text data from a financial PDF using pdfplumber.
    Cleans formatting issues for easier downstream analysis.
    """
    try:
        text_data = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                # Extract text
                text = page.extract_text() or ""

                # Extract tables if available
                tables = page.extract_tables()
                for table in tables:
                    table_text = "\n".join([", ".join(row) for row in table if row])
                    text += "\n" + table_text

                text_data.append(text)

        # Combine text
        content = "\n".join(text_data)

        # Clean formatting
        content = re.sub(r"\n\s*\n", "\n", content)
        content = re.sub(r"[ \t]+", " ", content)

        return content.strip()

    except Exception as e:
        return f"❌ Error parsing PDF with pdfplumber: {str(e)}"


# --- Investment Analysis Tool ---
@tool("investment_analysis")
def analyze_investment_tool(financial_document_data: str) -> str:
    """
    Analyzes the financial document for investment insights.
    """
    processed_data = re.sub(r"\s{2,}", " ", financial_document_data)
    findings = {}

    # Regex patterns for financial metrics
    metrics_patterns = {
        "Revenue": r"Revenue[:\s]+\$?([\d,.()]+[MBK]?)",
        "Net Income": r"Net Income[:\s]+\$?([\d,.()]+[MBK]?)",
        "EPS": r"EPS[:\s]+\$?([\d,.()]+)",
        "Debt-to-Equity": r"Debt.?Equity[:\s]+([\d,.()]+)"
    }

    for key, pattern in metrics_patterns.items():
        match = re.search(pattern, processed_data, re.I)
        if match:
            findings[key] = match.group(1)

    # Build analysis summary
    analysis = "📊 **Investment Analysis Report**\n"
    if not findings:
        return analysis + "No key metrics could be extracted from the document.\n"

    for k, v in findings.items():
        analysis += f"- {k}: {v}\n"

    # Apply recommendation logic
    try:
        if "Debt-to-Equity" in findings:
            d2e = normalize_number(findings["Debt-to-Equity"])
            if d2e is not None:
                if d2e < 1:
                    analysis += "✅ Healthy leverage (low debt-to-equity ratio).\n"
                else:
                    analysis += "⚠️ High leverage risk (high debt-to-equity ratio).\n"

        if "Net Income" in findings and "Revenue" in findings:
            ni = normalize_number(findings["Net Income"])
            rev = normalize_number(findings["Revenue"])
            if ni is not None and rev is not None and rev > 0:
                margin = (ni / rev) * 100
                analysis += f"- Profit Margin: {margin:.2f}%\n"
                if margin > 10:
                    analysis += "✅ Strong profitability.\n"
                else:
                    analysis += "⚠️ Weak profitability.\n"
    except Exception as e:
        analysis += f"⚠️ Error in calculations: {e}\n"

    return analysis


# --- Risk Assessment Tool ---
@tool("risk_assessment")
def create_risk_assessment_tool(financial_document_data: str) -> str:
    """
    Performs risk assessment based on financial document data.
    """
    processed_data = re.sub(r"\s{2,}", " ", financial_document_data)
    findings = {}

    # Extract metrics
    metrics_patterns = {
        "Current Ratio": r"Current Ratio[:\s]+([\d,.()]+)",
        "Debt-to-Equity": r"Debt.?Equity[:\s]+([\d,.()]+)"
    }

    for key, pattern in metrics_patterns.items():
        match = re.search(pattern, processed_data, re.I)
        if match:
            findings[key] = match.group(1)

    if "volatility" in processed_data.lower():
        findings["Volatility"] = "Mentioned"

    # Build report
    assessment = "⚠️ **Risk Assessment Report**\n"
    if not findings:
        return assessment + "No specific risk metrics could be extracted.\n"

    for k, v in findings.items():
        assessment += f"- {k}: {v}\n"

    try:
        if "Current Ratio" in findings:
            cr = normalize_number(findings["Current Ratio"])
            if cr is not None:
                if cr < 1:
                    assessment += "❌ Liquidity Risk: Current ratio below 1.\n"
                elif cr < 2:
                    assessment += "⚠️ Moderate liquidity risk.\n"
                else:
                    assessment += "✅ Good liquidity position.\n"

        if "Debt-to-Equity" in findings:
            d2e = normalize_number(findings["Debt-to-Equity"])
            if d2e is not None:
                if d2e > 2:
                    assessment += "❌ High leverage risk.\n"
                elif d2e > 1:
                    assessment += "⚠️ Moderate leverage risk.\n"
                else:
                    assessment += "✅ Acceptable leverage level.\n"

        if "Volatility" in findings:
            assessment += "⚠️ Market volatility mentioned — potential risk exposure.\n"
    except Exception as e:
        assessment += f"⚠️ Error in risk calculations: {e}\n"

    return assessment
