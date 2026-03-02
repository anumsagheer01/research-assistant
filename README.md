## Multi-Agent Research Assistant

In a nutshell: Four AI agents that search the web, read the pages, check if sources agree with each other, and then write you a proper report, with citations you can click.

**[Try it live →](https://huggingface.co/spaces/anumsagheer/research-assistant)**


### What it does

You type a research topic. Four AI agents work in sequence, one after another:

1. One searches the live web and pulls real sources
2. One reads every source and extracts the key points
3. One cross-references everything and flags if sources contradict each other
4. One writes a clean, structured report with citations

The whole thing runs in under 60 seconds and you get a PDF you can download.


### Why I built this instead of just using ChatGPT

Honestly, the architecture is the whole point. ChatGPT is one model answering from memory, its knowledge has a cutoff date and it doesn't cite anything verifiable. This project is different in a few real ways:

- **It searches the live web.** Every report pulls from sources published today, not from training data.
- **It's multi-agent.** Four specialized agents each do one job well, rather than one model doing everything. 
- **It actually cites sources.** Every claim links back to a real URL. You can verify anything in the report.
- **It flags contradictions.** The fact-check agent specifically looks for cases where sources disagree, something ChatGPT doesn't do at all.
- **The output is a document, not a chat message.** A structured PDF saved to AWS S3 that you can download and share.


### How it works

```
You type a topic
       │
       ▼
LangGraph Orchestrator
       │
       ├──► Search Agent (Tavily API)
       │         hits the live web, grabs top 5-10 sources
       │
       ├──► Summarizer Agent (Groq + LLaMA 3.1)
       │         reads each source, pulls out key findings
       │
       ├──► Fact-Check Agent (Groq + LLaMA 3.1)
       │         compares sources, flags anything that conflicts
       │
       └──► Report Writer Agent (Groq + LLaMA 3.1)
                 compiles the full report with [1][2] citations
                         │
                         ▼
               saved as PDF to AWS S3
               download link sent back to you
```

The reason I used LangGraph specifically is that it lets you define the agents as a proper state graph, each agent gets the output of the previous one, the shared state is explicit, and you can extend the pipeline without breaking anything. It's much cleaner than just chaining functions.


### Tech stack

| Tool | What it's doing |
|---|---|
| LangGraph | Orchestrating the agents as a state graph |
| Groq + LLaMA 3.1 | Running the summarizer, fact-checker, and report writer |
| Tavily API | Real-time web search |
| AWS S3 + boto3 | Storing the generated PDFs in the cloud |
| ReportLab | Converting the report text into a PDF |
| Streamlit | The frontend UI |
| HuggingFace Spaces | Free deployment |


### Project structure

```
research-assistant/
│
├── app.py                      # the Streamlit UI
│
├── agents/
│   ├── search_agent.py         # searches the web via Tavily
│   ├── summarizer_agent.py     # reads sources and extracts key points
│   ├── factcheck_agent.py      # cross-references and flags conflicts
│   └── report_writer.py        # writes the final report
│
├── graph/
│   └── pipeline.py             # LangGraph state graph wiring everything together
│
├── utils/
│   └── s3_handler.py           # PDF generation and S3 upload
│
├── .streamlit/
│   └── config.toml             # Streamlit config for HuggingFace deployment
│
└── requirements.txt
```


### Running it locally

```bash
git clone https://github.com/anumsagheer/research-assistant.git
cd research-assistant
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file with:
```
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_key
AWS_BUCKET_NAME=your_bucket
AWS_REGION=us-east-1
```

Then:
```bash
streamlit run app.py
```


## API keys (all free)   

| Service | Free tier | Link |
|---|---|---|
| Groq | 14,400 requests/day | [console.groq.com](https://console.groq.com) |
| Tavily | 1,000 searches/month | [tavily.com](https://tavily.com) |
| AWS S3 | 5GB free forever | [aws.amazon.com](https://aws.amazon.com) |


## What I'd add next

- Memory across sessions so it can build on previous research
- A comparison mode where you can research two topics side by side
- Source quality scoring so low-quality sites get weighted less
- Email delivery so reports land in your inbox automatically





