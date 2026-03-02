from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent

sources = search_agent("impact of AI on healthcare 2024")
sources = summarizer_agent(sources)

for s in sources:
    print(f"\n {s['title']}")
    print(s['summary'])
    print("---")