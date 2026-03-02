from agents.search_agent import search_agent

results = search_agent("impact of AI on healthcare 2024")
for r in results:
    print(r["title"])
    print(r["url"])
    print("---")