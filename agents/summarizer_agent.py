from langchain_groq import ChatGroq
import os
import time
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

def summarizer_agent(sources: list[dict]) -> list[dict]:
    print(f"📚Summarizer Agent: Summarizing {len(sources)} sources...")

    for i, source in enumerate(sources):
        content = source.get("raw_content") or source.get("snippet", "")
        if not content.strip():
            source["summary"] = "No content available to summarize."
            continue

        prompt = f"""You are a research summarizer. Read the following content and extract the 3-5 most important key points.

Source title: {source['title']}
Content: {content}

Return ONLY a clean bullet point list of key findings. No intro, no outro."""

        response = llm.invoke(prompt)
        source["summary"] = response.content
        print(f"Summarized source {i+1}/{len(sources)}: {source['title'][:50]}")
        time.sleep(1)

    print("Summarizer Agent: All sources summarized")
    return sources