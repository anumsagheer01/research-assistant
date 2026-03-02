from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

def factcheck_agent(sources: list[dict], topic: str) -> dict:
    print("🕵🏼Fact-Check Agent: Cross-referencing sources...")

    all_summaries = ""
    for i, source in enumerate(sources):
        all_summaries += f"\nSource {i+1} — {source['title']}:\n{source.get('summary', '')}\n"

    prompt = f"""You are a fact-checking agent. You have summaries from {len(sources)} sources about: "{topic}".

Identify:
1. Claims multiple sources AGREE on (consensus)
2. Claims sources CONTRADICT each other on
3. Claims only ONE source mentions

Summaries:
{all_summaries}

Respond in this exact format:

CONSENSUS POINTS:
- [point 1]

CONTRADICTIONS/CONFLICTS:
- [conflict or "None found"]

SINGLE-SOURCE CLAIMS TO NOTE:
- [claim or "None"]"""

    response = llm.invoke(prompt)
    print("Fact-Check Agent: Done")
    return {"factcheck_report": response.content}