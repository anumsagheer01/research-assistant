from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent
from agents.factcheck_agent import factcheck_agent
from agents.report_writer import report_writer_agent

# This defines the shared state that passes between all agents
class ResearchState(TypedDict):
    topic: str
    depth: str
    sources: List[dict]
    factcheck: dict
    report: str
    citations: str

# Each function below is one node in the graph

def run_search(state: ResearchState) -> ResearchState:
    print("\nStarting Search Agent...")
    num_results = 10 if state["depth"] == "deep" else 5
    sources = search_agent(state["topic"], num_results=num_results)
    return {**state, "sources": sources}

def run_summarizer(state: ResearchState) -> ResearchState:
    print("\nStarting Summarizer Agent...")
    sources = summarizer_agent(state["sources"])
    return {**state, "sources": sources}

def run_factcheck(state: ResearchState) -> ResearchState:
    print("\nStarting Fact-Check Agent...")
    factcheck = factcheck_agent(state["sources"], state["topic"])
    return {**state, "factcheck": factcheck}

def run_report_writer(state: ResearchState) -> ResearchState:
    print("\nStarting Report Writer Agent...")
    result = report_writer_agent(state["topic"], state["sources"], state["factcheck"])
    return {**state, "report": result["report"], "citations": result["citations"]}

# Build the graph
def build_pipeline():
    graph = StateGraph(ResearchState)

    # Add each agent as a node
    graph.add_node("search", run_search)
    graph.add_node("summarizer", run_summarizer)
    graph.add_node("factcheck", run_factcheck)
    graph.add_node("report_writer", run_report_writer)

    # Define the flow: search → summarizer → factcheck → report_writer → END
    graph.set_entry_point("search")
    graph.add_edge("search", "summarizer")
    graph.add_edge("summarizer", "factcheck")
    graph.add_edge("factcheck", "report_writer")
    graph.add_edge("report_writer", END)

    return graph.compile()

def run_research_pipeline(topic: str, depth: str = "quick") -> dict:
    pipeline = build_pipeline()
    
    initial_state = {
        "topic": topic,
        "depth": depth,
        "sources": [],
        "factcheck": {},
        "report": "",
        "citations": ""
    }
    
    final_state = pipeline.invoke(initial_state)
    return final_state