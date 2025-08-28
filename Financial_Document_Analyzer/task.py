from crewai import Task
from tools import read_data_tool, analyze_investment_tool, create_risk_assessment_tool
from agents import financial_analyst, investment_advisor, risk_assessor, verifier
# Task: Analyze a financial document
analyze_financial_document = Task(
    description=(
        "Analyze the uploaded financial document at {file_path} for insights.\n"
        "User query: {query}\n"
        "Extract key financial data, summarize trends, identify risks, and provide investment recommendations."
    ),
    expected_output=(
        "A detailed financial analysis including:\n"
        "- Revenue, profit, and cash flow trends\n"
        "- Risk factors\n"
        "- Investment opportunities\n"
        "- Clear actionable recommendations"
    ),
    agent=financial_analyst,
    tools=[read_data_tool, analyze_investment_tool, create_risk_assessment_tool],
    async_execution=False,
)



# Task: Perform an investment analysis
investment_analysis = Task(
    description=(
        "Use the verified financial document and query: {query} to provide an investment-focused analysis. "
        "Identify whether the company or its sector shows potential for growth, stability, or risk. "
        "Recommend responsible investment actions based on data, such as buy/hold/sell considerations. "
        "Consider both opportunities and potential risks."
    ),
    expected_output=(
        "An investment recommendation report including:\n"
        "- Summary of financial strengths and weaknesses\n"
        "- Opportunities for investment\n"
        "- Potential risks to watch out for\n"
        "- Clear recommendation (Buy, Hold, or Sell) with rationale"
    ),
    agent=investment_advisor,
    tools=[read_data_tool, analyze_investment_tool],
    async_execution=False,
)


# Task: Conduct a risk assessment
risk_assessment = Task(
    description=(
        "Assess the financial and market risks associated with the company based on the provided financial document. "
        "Consider credit risk, liquidity risk, leverage, and market volatility. "
        "Provide a clear, structured risk assessment report for the user’s query: {query}."
    ),
    expected_output=(
        "A structured risk assessment including:\n"
        "- Identification of key risk factors\n"
        "- Evaluation of liquidity, leverage, and profitability risks\n"
        "- Market and operational risks if identifiable\n"
        "- A final risk classification (Low, Medium, or High)"
    ),
    agent=risk_assessor,
    tools=[read_data_tool, create_risk_assessment_tool],
    async_execution=False,
)


# Task: Verify uploaded financial document
verification = Task(
    description=(
        "Check whether the uploaded file is a valid financial document related to the user’s query: {query}. "
        "Look for key sections like balance sheets, income statements, or cash flow statements. "
        "Verify whether the content appears authentic and suitable for financial analysis."
    ),
    expected_output=(
        "A verification summary including:\n"
        "- Confirmation if the document is financial in nature\n"
        "- Which financial sections were identified\n"
        "- Any concerns about authenticity or completeness"
    ),
    agent=verifier,
    tools=[read_data_tool],
    async_execution=False,
)
