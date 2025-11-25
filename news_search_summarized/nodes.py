import os
from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict
from langgraph.graph import StateGraph, END
from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

#  Agent state 
class AgentState(TypedDict):
    question: str
    search_results: dict
    answer: str
    final_answer: str

#  Node 1- tavily search 
def search_web(state: AgentState):
    client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    search_results = client.search(
        query=state["question"],
        max_results=3,
        include_answer=True
    )
    return {"search_results": search_results}

# Node 2- generate answer
def generate_answer(state: AgentState):
    """
    Node 2: Answer Synthesis and Formatting

    Takes the search results from Tavily and formats them into a clean,
    user-friendly response with proper source attribution.
    """
    #print("🤖 Formatting answer...")

    
    ai_answer = state["search_results"].get("answer", "No answer found")

    
    sources = [f"- {result['title']}: {result['url']}" 
              for result in state["search_results"]["results"]]

    
    final_answer = f"{ai_answer}\n\nSources:\n" + "\n".join(sources)

    return {"answer": final_answer}

#  Node 3- Format answer 
def format_answer(state: AgentState):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    user_query = state.get("question", "")
    search_results = state.get("search_results", {})
    raw_answer = state.get("answer", "")

    sources_text = "\n".join([f"- {r['title']}: {r['url']}" for r in search_results.get("results", [])])

    prompt_template = ChatPromptTemplate.from_template("""
You are an intelligent summarization assistant.

User asked:
{user_query}

Below are relevant web search results and synthesized responses:
{raw_answer}

Sources:
{sources_text}

Your task:
- Summarize the findings in a detailed, factual, and well-structured manner.
- Make the response readable and insightful.
- Avoid redundancy, but include key points from multiple sources.

Final Answer:
""")

    messages = prompt_template.format_messages(
        user_query=user_query,
        raw_answer=raw_answer,
        sources_text=sources_text,
    )

    response = llm.invoke(messages)
    final_answer = response.content.strip() if hasattr(response, "content") else str(response).strip()
    return {"final_answer": final_answer}

# --- Node 4: JSON output ---
def json_output(state: AgentState):
    search_results = state.get("search_results", {})
    final_answer = state.get("final_answer", "")
    sources = [
        {"title": r["title"], "url": r["url"], "content": r.get("content", "")}
        for r in search_results.get("results", [])
    ]
    return {"json_output": {"query": state.get("question", ""), "summary": final_answer, "sources": sources}}

# agent workflow 
def create_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("search", search_web)
    workflow.add_node("result", generate_answer)
    workflow.add_node("format_answer", format_answer)
    workflow.add_node("make_json", json_output)
    workflow.set_entry_point("search")
    workflow.add_edge("search", "result")
    workflow.add_edge("result", "format_answer")
    workflow.add_edge("format_answer", "make_json")
    workflow.add_edge("make_json", END)
    return workflow.compile()
