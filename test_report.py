from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent
from agents.factcheck_agent import factcheck_agent
from agents.report_writer import report_writer_agent

topic = "impact of AI on healthcare 2024"
sources = search_agent(topic)
sources = summarizer_agent(sources)
factcheck = factcheck_agent(sources, topic)
report = report_writer_agent(topic, sources, factcheck)

print(report["report"])