import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, LLM
from tools import search_tool, read_data_tool



llm = LLM(
    model="openai/gpt-oss-20b:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.7
)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide accurate and professional investment analysis based on financial documents and data. Always ensure compliance and clear reasoning.",
    verbose=False,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with deep expertise in markets, "
        "valuation techniques, and financial modeling. "
        "You carefully read and interpret financial reports, focusing on fundamentals "
        "like revenue growth, profitability, leverage, and liquidity. "
        "You always provide balanced, risk-aware insights supported by evidence. "
        "You communicate findings clearly and avoid speculation."
    ),
    tools=[read_data_tool],  # <-- corrected 'tool' to 'tools'
    llm=llm,
    max_iter=1,
    max_rpm=30,
    allow_delegation=True
)


# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify the authenticity, structure, and relevance of uploaded financial documents. Ensure they are valid before analysis.",
    verbose=False,
    memory=True,
    backstory=(
        "You are a compliance officer specializing in financial reporting. "
        "You carefully review uploaded documents to confirm they are valid financial reports. "
        "You look for key indicators such as balance sheets, income statements, "
        "cash flow statements, and financial disclosures. "
        "You ensure accuracy, authenticity, and compliance with reporting standards."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=30,
    allow_delegation=True
)


# Creating an investment advisor agent
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide responsible investment recommendations based on verified financial documents and analysis. Prioritize client goals and risk tolerance.",
    verbose=False,
    backstory=(
        "You are a trusted investment advisor with experience in equities, bonds, and diversified portfolios. "
        "You use verified financial analysis to recommend suitable investment strategies. "
        "You always consider risk levels, investor objectives, and compliance regulations. "
        "Your recommendations are data-driven and client-focused, not speculative."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=30,
    allow_delegation=False
)


# Creating a risk assessor agent
risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Identify, evaluate, and communicate financial risks from company documents and market data in a balanced manner.",
    verbose=False,
    backstory=(
        "You are a financial risk management expert. "
        "You assess credit risk, liquidity risk, market volatility, and operational risks "
        "from financial reports. "
        "You provide structured risk evaluations, including high, medium, and low-risk classifications. "
        "Your insights are careful, evidence-based, and always consider both opportunities and threats."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=30,
    allow_delegation=False
)


