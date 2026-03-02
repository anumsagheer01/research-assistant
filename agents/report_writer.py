from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

def report_writer_agent(topic: str, sources: list[dict], factcheck: dict) -> dict:
    print("📝Report Writer Agent: Compiling final report...")

    sources_text = ""
    citations = ""
    for i, source in enumerate(sources):
        sources_text += f"\nSource [{i+1}] — {source['title']}:\n{source.get('summary', '')}\n"
        citations += f"[{i+1}] {source['title']} — {source['url']}\n"

    prompt = f"""You are an expert research report writer. Write a structured research report.

TOPIC: {topic}

SOURCE SUMMARIES:
{sources_text}

FACT-CHECK ANALYSIS:
{factcheck['factcheck_report']}

Write the report in this structure:

# {topic}

## Executive Summary
(2-3 sentence overview)

## Key Findings
(5-7 bullet points, cite sources like [1], [2])

## Detailed Analysis
(3-4 paragraphs, cite sources throughout)

## Contradictions & Gaps
(What do sources disagree on?)

## Conclusion
(2-3 sentence wrap up)

## Sources
{citations}"""

    response = llm.invoke(prompt)
    print("Report Writer Agent: Done")
    return {
        "report": response.content,
        "citations": citations
    }
