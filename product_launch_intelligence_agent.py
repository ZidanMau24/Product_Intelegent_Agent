import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, BaseMessage
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from textwrap import dedent
import os
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Product Intelligence Agent (Gemini Edition)",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Environment & API Key Setup ----------------
load_dotenv()

st.sidebar.header("🔑 API Configuration")
google_api_key = st.sidebar.text_input(
    "Google AI API Key",
    type="password",
    value=os.getenv("GOOGLE_API_KEY", ""),
    help="Required for Gemini agent functionality"
)
firecrawl_api_key = st.sidebar.text_input(
    "Firecrawl API Key",
    type="password",
    value=os.getenv("FIRECRAWL_API_KEY", ""),
    help="Required for web search and crawling"
)

# Set environment variables for LangChain
if google_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key
# The FirecrawlApp will use its key directly

# ---------------- Tool Definition ----------------
# We define our web crawling and searching tools using Firecrawl

@tool
def search(query: str) -> str:
    """
    Search the web for a given query using Firecrawl and return the results.
    This is best used for broad, initial research.
    """
    try:
        app = FirecrawlApp(api_key=firecrawl_api_key)
        results = app.search(query, page_options={"fetch_page_content": True})
        return f"Search results for '{query}':\n{str(results)}"
    except Exception as e:
        return f"Error during search: {e}"

@tool
def crawl(url: str) -> str:
    """
    Crawl a specific URL using Firecrawl to get its main content.
    This is best used when you have a specific link you need to analyze.
    """
    try:
        app = FirecrawlApp(api_key=firecrawl_api_key)
        content = app.crawl(url)
        return f"Crawled content from {url}:\n{content['markdown']}"
    except Exception as e:
        return f"Error during crawl: {e}"

tools = [search, crawl]

# ---------------- Multi-Agent Graph (Team) Setup ----------------

# The state for our graph, which will be passed between nodes
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]

# Helper function to create an agent runnable
def create_agent(llm, system_prompt: str, tools: list):
    return llm.with_structured_output(tools, include_raw=True)

# Define the nodes for our graph (the agents)
def create_agent_node(llm, system_message: str):
    def agent_node(state):
        prompt = HumanMessage(content=system_message)
        response = llm.invoke(state["messages"] + [prompt])
        return {"messages": [response]}
    return agent_node

# --- Main Application Logic ---
graph_app = None
if google_api_key and firecrawl_api_key:
    # Initialize the Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)

    # Agent 1: Product Launch Analyst
    launch_analyst_prompt = dedent("""
        You are the **Product Launch Analyst**. Your role is to analyze a competitor's product launch strategy.
        Focus on positioning, messaging, launch tactics, and differentiation.
        Use the provided tools to search for launch announcements, product pages, and press releases.
        Present your findings as a concise analysis.
    """)
    launch_analyst_node = create_agent_node(llm.bind_tools(tools), launch_analyst_prompt)

    # Agent 2: Market Sentiment Specialist
    sentiment_analyst_prompt = dedent("""
        You are the **Market Sentiment Specialist**. Your job is to find out what the market is saying about a product.
        Search for reviews, social media discussions (e.g., on Reddit, Twitter), and forum comments.
        Summarize the key positive and negative sentiment drivers.
    """)
    sentiment_analyst_node = create_agent_node(llm.bind_tools(tools), sentiment_analyst_prompt)

    # Agent 3: Launch Metrics Specialist
    metrics_analyst_prompt = dedent("""
        You are the **Launch Metrics Specialist**. Your task is to find publicly available data and KPIs related to a product launch.
        Look for user numbers, adoption rates, press coverage mentions, and any reported performance indicators.
        Provide a summary of the quantitative and qualitative signals of the launch's success.
    """)
    metrics_analyst_node = create_agent_node(llm.bind_tools(tools), metrics_analyst_prompt)
    
    # Supervisor Agent: The coordinator of the team
    supervisor_prompt = dedent(f"""
        You are the **Supervisor** of a product intelligence team. Your job is to coordinate the work of three specialists:
        1. Product Launch Analyst
        2. Market Sentiment Specialist
        3. Launch Metrics Specialist
        
        Based on the user's request, delegate the task to the appropriate specialist.
        Once the specialist has provided their report, review it and, if sufficient, create a final, well-structured markdown report for the user.
        The final report must include a "Sources" section listing all URLs that were crawled or searched.

        The user's request is:
    """)
    
    # Define the graph structure
    builder = StateGraph(AgentState)
    builder.add_node("launch_analyst", launch_analyst_node)
    builder.add_node("sentiment_analyst", sentiment_analyst_node)
    builder.add_node("metrics_analyst", metrics_analyst_node)
    builder.add_node("supervisor", create_agent_node(llm, supervisor_prompt))

    # Define the edges of the graph
    builder.add_edge("launch_analyst", "supervisor")
    builder.add_edge("sentiment_analyst", "supervisor")
    builder.add_edge("metrics_analyst", "supervisor")

    # The supervisor decides which agent to call first
    builder.add_conditional_edges(
        "supervisor",
        lambda state: state["messages"][-1].content,
        {
            "Product Launch Analyst": "launch_analyst",
            "Market Sentiment Specialist": "sentiment_analyst",
            "Launch Metrics Specialist": "metrics_analyst",
            "END": END,
        },
    )
    builder.set_entry_point("supervisor")
    graph_app = builder.compile()

else:
    st.warning("⚠️ Please enter both Google AI and Firecrawl API keys in the sidebar.")

# ---------------- UI ----------------
st.title("🚀 AI Product Intelligence Agent (Gemini Edition)")
st.markdown("*Powered by LangGraph, Gemini 1.5 Pro & Firecrawl*")
st.divider()

# Company input section
st.subheader("🏢 Company & Product Analysis")
company_name = st.text_input(
    label="Company or Product Name",
    placeholder="Enter name (e.g., Perplexity, Humane Pin, Rabbit R1)",
    label_visibility="collapsed"
)
st.divider()

# Create tabs for analysis types
analysis_tabs = st.tabs([
    "🔍 Competitor Analysis",
    "💬 Market Sentiment",
    "📈 Launch Metrics"
])

# Initialize session state for responses
if "response" not in st.session_state:
    st.session_state.response = None
if "request_type" not in st.session_state:
    st.session_state.request_type = ""


def run_analysis(request_type, company):
    st.session_state.response = None # Clear previous response
    st.session_state.request_type = request_type
    
    prompt_map = {
        "competitor": f"Analyze the launch strategy for {company}. Delegate to the Product Launch Analyst.",
        "sentiment": f"Analyze the market sentiment for {company}. Delegate to the Market Sentiment Specialist.",
        "metrics": f"Analyze the launch metrics for {company}. Delegate to the Launch Metrics Specialist."
    }
    
    initial_prompt = prompt_map.get(request_type)
    
    with st.spinner(f"🤖 The Gemini team is analyzing {company}..."):
        final_state = graph_app.invoke({"messages": [HumanMessage(content=initial_prompt)]})
        st.session_state.response = final_state['messages'][-1].content
    st.rerun()

# --- Competitor Analysis Tab ---
with analysis_tabs[0]:
    st.markdown("### 🔍 Competitor Launch Analysis")
    st.caption("Get an evidence-backed breakdown of a rival's latest launches – positioning, differentiators, pricing cues & channel mix.")
    if company_name:
        if st.button("🚀 Analyze Strategy", key="competitor_btn", type="primary", disabled=not graph_app):
            run_analysis("competitor", company_name)
        if st.session_state.request_type == "competitor" and st.session_state.response:
            st.markdown(st.session_state.response)

# --- Market Sentiment Tab ---
with analysis_tabs[1]:
    st.markdown("### 💬 Market Sentiment")
    st.caption("Get a consolidated view of social chatter & review themes, split by positive and negative drivers.")
    if company_name:
        if st.button("📊 Analyze Sentiment", key="sentiment_btn", type="primary", disabled=not graph_app):
            run_analysis("sentiment", company_name)
        if st.session_state.request_type == "sentiment" and st.session_state.response:
            st.markdown(st.session_state.response)

# --- Launch Metrics Tab ---
with analysis_tabs[2]:
    st.markdown("### 📈 Launch Metrics")
    st.caption("Find publicly available KPIs – adoption numbers, press coverage, and qualitative 'buzz' signals.")
    if company_name:
        if st.button("📈 Analyze Metrics", key="metrics_btn", type="primary", disabled=not graph_app):
            run_analysis("metrics", company_name)
        if st.session_state.request_type == "metrics" and st.session_state.response:
            st.markdown(st.session_state.response)

# ---------------- Sidebar ----------------
st.sidebar.divider()
st.sidebar.markdown("### 🤖 System Status")
if graph_app:
    st.sidebar.success("✅ Gemini Intelligence Team ready")
else:
    st.sidebar.error("❌ API keys required")
st.sidebar.divider()
st.sidebar.markdown("### 🎯 Coordinated Team")
agents_info = [
    ("🔍", "Product Launch Analyst", "GTM strategist"),
    ("💬", "Market Sentiment Specialist", "Consumer perception guru"),
    ("📈", "Launch Metrics Specialist", "Performance analyst"),
    ("👑", "Supervisor", "Team coordinator")
]
for icon, name, desc in agents_info:
    st.sidebar.markdown(f"**{icon} {name}**")
    st.sidebar.caption(desc)