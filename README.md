<div align="center" id="top">
  <picture>
    <source width="120" media="(prefers-color-scheme: dark)" srcset="kern/docs/assets/kern-dark.png">
    <source width="120" media="(prefers-color-scheme: light)" srcset="kern/docs/assets/kern-light.png">
    <img width="120" src="kern/docs/assets/kern-light.png" alt="Kern Logo">
  </picture>

### Small Models. Big Impact.

Lightweight agent framework optimized for small language models (1B–7B).

Kern replaces heavyweight JSON Schema prompting with lightweight fill-in-the-blanks templates so constrained models can reliably produce structured outputs.

[Installation](#installation) •
[Quick Start](#quick-start) •
[Structured Output](#structured-output) •
[Local Models](#local-models) •
[Tools](#tools)

</div>

---

# Why Kern?

Most agent frameworks assume:
- reliable structured outputs
- large context windows
- strong reasoning models
- perfect tool-calling

That works for frontier models.

It breaks on smaller local models.

Small models often struggle with:
- malformed JSON
- schema drift
- nested structures
- hallucinated fields
- retry loops
- token overhead

Kern is designed specifically for constrained models by minimizing orchestration complexity.

Instead of generating massive JSON schemas like:

```json
{
  "$defs": {...},
  "properties": {...},
  "anyOf": [...],
  "allOf": [...]
}
```

Kern generates lightweight templates:

```json
{
  "title": "string",
  "rating": "integer",
  "summary": "string"
}
```

This dramatically reduces formatting pressure while preserving structured outputs.

---

# Designed For

- Local LLMs
- Ollama
- llama.cpp
- LM Studio
- Edge AI systems
- Low-VRAM deployments
- Laptop-scale agents
- Efficient inference pipelines

---

# Features

- Lightweight structured outputs
- Automatic JSON repair
- Multi-agent workflows
- Tool calling
- Streaming responses
- Knowledge bases
- Persistent memory
- OpenAI-compatible providers
- Local-model friendly architecture

---

# Installation

```bash
pip install kern-ai
```

## Extras

```bash
pip install kern-ai[openai]
pip install kern-ai[ollama]
pip install kern-ai[anthropic]
pip install kern-ai[google]
pip install kern-ai[ddg,mcp]
pip install kern-ai[all]
```

---

# Quick Start

## Basic Agent

```python
from kern.agent import Agent
from kern.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="You are a helpful assistant.",
)

result = agent.run("What is the capital of France?")
print(result.content)
```

---

# Structured Output

## Simple Schema

```python
from pydantic import BaseModel
from kern.agent import Agent

class BookReview(BaseModel):
    title: str
    rating: int
    summary: str
    recommended: bool

agent = Agent(
    model=model,
    output_schema=BookReview,
)

result = agent.run("Review Dune by Frank Herbert")
print(result.content)
```

## Template Sent to the Model

```json
{
  "title": "string",
  "rating": "integer",
  "summary": "string",
  "recommended": "boolean"
}
```

Instead of deeply nested JSON Schema definitions.

---

# Local Models

Kern is designed to work well with small local models through OpenAI-compatible inference servers.

Compatible with:
- Ollama
- llama.cpp
- LM Studio
- vLLM
- OpenWebUI backends

```python
from kern.agent import Agent
from kern.models.openai import OpenAIChat

model = OpenAIChat(
    id="local-model",
    base_url="http://127.0.0.1:8080/v1",
    api_key="not-needed",
)

agent = Agent(model=model)
```

---

# JSON Repair

Small models frequently generate malformed JSON.

Kern automatically repairs:
- trailing commas
- broken escapes
- markdown-wrapped JSON
- partial formatting issues
- LaTeX escape problems

```python
from kern.repair import extract_json

data = extract_json("""
```json
{"title": "Hello", "items": [1,2,3,]}
```
""")
```

---

# Tools

```python
from kern.tools import (
    DuckDuckGoTools,
    CalculatorTools,
    PythonTools,
    FileTools,
)
```

Supports:
- DuckDuckGo
- Tavily
- Exa
- Firecrawl
- GitHub
- MCP
- YFinance
- Custom tools

---

# Multi-Agent Teams

```python
from kern.agent import Agent
from kern.team import Team

researcher = Agent(name="Researcher", model=model)
writer = Agent(name="Writer", model=model)

team = Team(
    name="Content Team",
    members=[researcher, writer],
)

result = team.run("Write a report on AI safety")
```

---

# Streaming

```python
for chunk in agent.run("Explain quantum computing", stream=True):
    print(chunk.content, end="")
```

---

# Philosophy

Kern is built around a simple idea:

> Small models should still be capable of reliable agent workflows.

Instead of assuming more intelligence,
Kern reduces orchestration complexity.

---

# Acknowledgements

Kern originally started as an experimental fork inspired by Agno.

The project evolved into a separate framework focused specifically on constrained-model orchestration, lightweight structured outputs, and local-model reliability.

Huge credit to the Agno ecosystem and contributors for the original inspiration.

---

# License

Apache License 2.0
