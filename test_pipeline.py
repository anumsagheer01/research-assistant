from graph.pipeline import run_research_pipeline

result = run_research_pipeline(
    topic="impact of AI on healthcare 2024",
    depth="quick"
)

print("\n" + "="*50)
print("FINAL REPORT:")
print("="*50)
print(result["report"])