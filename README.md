# TraceLens

TraceLens is a production-grade, cloud-native observability analysis system that analyzes distributed system failures using AWS CloudWatch Logs Insights and a deterministic RAG-based analysis engine.

---

## Features

- CloudWatch Logs Insights integration
- Trace-based log correlation
- Deterministic event timeline construction
- Retrieval-Augmented Generation (RAG) for failure patterns
- Root cause analysis with confidence scoring
- Stateless FastAPI API
- AWS Lambda + API Gateway deployment
- AWS Free Tier compatible
- Zero hallucination guarantee

---

## Architecture Overview

1. Fetch logs from CloudWatch Logs Insights
2. Filter and normalize logs by `trace_id`
3. Build deterministic event timeline
4. Retrieve known failure patterns via RAG
5. Perform evidence-based root cause analysis
6. Generate confidence-scored explanation
7. Return structured JSON response

---

## Requirements

- Python 3.10
- AWS Account
- CloudWatch Logs with `trace_id` field
- AWS CLI configured

---

## Local Development (Optional)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn tracelens.api.main:app --reload
