<img src="kern/docs/assets/kern.png" alt="Kern logo" width="180" />

Agent framework optimized for small models (1-7B parameters). Kern generates simple fill-in-the-blanks JSON templates instead of complex JSON Schema, so small models actually produce valid structured output.

## Install

```bash
pip install kern
```

With extras:

```bash
pip install kern[openai]       # OpenAI-compatible models
pip install kern[ollama]       # Ollama
pip install kern[anthropic]    # Claude
pip install kern[google]       # Gemini
pip install kern[ddg,mcp]      # DuckDuckGo search + MCP tools
pip install kern[all]          # Everything
```

## Quick Start

### Basic Agent

```python
from kern.agent import Agent
from kern.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="You are a helpful assistant.",
)

result = agent.run("What is the capital of France?")
print(result.content)  # "Paris"
```

### Structured Output

```python
from pydantic BaseModel, Field
from kern.agent import Agent
from kern.models.openai import OpenAIChat


class BookReview(BaseModel):
    title: str = Field(description="Book title")
    rating: int = Field(description="Rating out of 5")
    summary: str = Field(description="One-paragraph summary")
    recommended: bool


agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    response_model=BookReview,
)

result = agent.run("Review 'The Hitchhiker's Guide to the Galaxy'")
print(result.content)
# BookReview(
#     title="The Hitchhiker's Guide to the Galaxy",
#     rating=5,
#     summary="...",
#     recommended=True
# )
```

### Running with Local Models

Kern shines with local small models via OpenAI-compatible servers (llama.cpp, LM Studio, vLLM, Ollama):

```python
from kern.agent import Agent
from kern.models.openai import OpenAIChat

# Connect to any OpenAI-compatible local server
model = OpenAIChat(
    id="local-model",                    # model name (ignored by some servers)
    base_url="http://127.0.0.1:8080/v1", # your local server
    api_key="not-needed",                # placeholder for local inference
)

agent = Agent(model=model, response_model=BookReview)
result = agent.run("Review 'Dune' by Frank Herbert")
```

## Models

Kern supports any OpenAI-compatible model provider:

| Provider | Install | Usage |
|----------|---------|-------|
| OpenAI | `kern[openai]` | `from kern.models.openai import OpenAIChat` |
| Anthropic | `kern[anthropic]` | `from kern.models.anthropic import Claude` |
| Google Gemini | `kern[google]` | `from kern.models.google import Gemini` |
| Ollama | `kern[ollama]` | `from kern.models.ollama import Ollama` |
| Groq | `kern[groq]` | `from kern.models.groq import Groq` |
| Cerebras | `kern[cerebras]` | `from kern.models.cerebras import Cerebras` |
| Mistral | `kern[mistral]` | `from kern.models.mistral import MistralChat` |
| Azure | `kern[azure]` | `from kern.models.azure import AzureOpenAIChat` |
| Any OpenAI-compatible | — | `OpenAIChat(base_url="...", api_key="...")` |

## Agents

### System Instructions

```python
agent = Agent(
    model=model,
    instructions=[
        "You are a math tutor for high school students.",
        "Always show your work step by step.",
        "Use LaTeX notation for equations.",
    ],
)
```

### Agent with Tools

```python
from kern.agent import Agent
from kern.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=model,
    tools=[DuckDuckGoTools()],
    instructions="Search the web to answer questions.",
    show_tool_calls=True,
)

result = agent.run("What's the latest news about quantum computing?")
```

### Agent Teams

```python
from kern.agent import Agent
from kern.team import Team

researcher = Agent(name="Researcher", model=model, tools=[DuckDuckGoTools()])
writer = Agent(name="Writer", model=model, instructions="Write clear, engaging prose.")

team = Team(
    name="Content Team",
    mode="coordinate",   # agents collaborate
    members=[researcher, writer],
)

result = team.run("Write a brief on AI safety")
```

### Multi-turn Conversations

```python
agent = Agent(model=model)

# Each call continues the conversation
r1 = agent.run("My name is Alice")
r2 = agent.run("What's my name?")  # remembers "Alice"
```

### Streaming

```python
agent = Agent(model=model)

for chunk in agent.run("Explain photosynthesis", stream=True):
    print(chunk.content, end="", flush=True)
```

## Structured Output (Templates)

This is where Kern differs from other frameworks. Instead of sending complex JSON Schema (`$defs`, `properties`, `anyOf`, `allOf`), Kern generates flat fill-in-the-blanks templates.

### Simple Models

```python
class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    cook_time_minutes: int
```

Template sent to the model:

```json
{"name": "string", "ingredients": ["string"], "cook_time_minutes": "integer"}
```

### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class Person(BaseModel):
    name: str
    address: Address
```

Template:

```json
{"name": "string", "address": {"street": "string", "city": "string", "zip_code": "string"}}
```

### Union Types

```python
from typing import Union

class TextBlock(BaseModel):
    text: str

class CodeBlock(BaseModel):
    code: str
    language: str

class Page(BaseModel):
    blocks: list[Union[TextBlock, CodeBlock]]
```

Template — both alternatives shown flat:

```json
{"blocks": [{"text": "string"}, {"code": "string", "language": "string"}]}
```

### Literal Enums

```python
from typing import Literal

class Article(BaseModel):
    title: str
    status: Literal["draft", "published", "archived"]
```

Template:

```json
{"title": "string", "status": "draft"|"published"|"archived"}
```

### Field Descriptions

```python
class Quiz(BaseModel):
    question: str = Field(description="The quiz question")
    options: list[str] = Field(description="4 multiple choice options")
    answer: int = Field(description="Index of the correct option (0-3)")
```

Template includes a separate descriptions block so the model knows what each field means.

## JSON Repair

Small models produce malformed JSON — missing quotes, trailing commas, broken escapes. Kern fixes it automatically:

```python
from kern.repair import extract_json

# Handles markdown code blocks, leading text, LaTeX, malformed JSON
data = extract_json("""
Here's the result:
```json
{"title": "Hello World", "items": [1, 2, 3,]}
```
""")
# {"title": "Hello World", "items": [1, 2, 3]}
```

### LaTeX Protection

When models output math like `\frac{a}{b}`, JSON parsers break because `\f` is a form-feed escape character. Kern doubles backslashes before parsing:

```python
from kern.repair import extract_json

data = extract_json('{"formula": "\\frac{1}{2} + \\theta"}')
# Parsed correctly — LaTeX preserved
```

## Tools

```python
from kern.tools import (
    DuckDuckGoTools,    # pip install kern[ddg]
    ExaTools,           # pip install kern[exa]
    FirecrawlTools,     # pip install kern[firecrawl]
    TavilyTools,        # pip install kern[tavily]
    GitHubTools,        # pip install kern[github]
    MCPTools,           # pip install kern[mcp]
    YFinanceTools,      # pip install kern[yfinance]
    NewspaperTools,     # pip install kern[newspaper]
    CalculatorTools,    # built-in
    PythonTools,        # built-in
    FileTools,          # built-in
)
```

### Custom Tools

```python
from kern.tools import Toolkit

class MyTools(Toolkit):
    def __init__(self):
        super().__init__(name="my_tools")
        self.register(self.get_weather)

    def get_weather(self, city: str) -> str:
        """Get the current weather for a city."""
        return f"The weather in {city} is sunny and 72°F"

agent = Agent(model=model, tools=[MyTools()])
```

## Storage

```python
from kern.agent import Agent
from kern.storage.agent.postgres import PgAgentStorage  # kern[postgres]

agent = Agent(
    model=model,
    storage=PgAgentStorage(
        table_name="agent_sessions",
        db_url="postgresql://localhost:5432/mydb",
    ),
)
```

Supported: Postgres, SQLite, Redis, MongoDB, GCS, Firestore, MySQL.

## Knowledge Bases

```python
from kern.knowledge.text import TextKnowledgeBase
from kern.vectordb.pgvector import PgVector  # kern[pgvector]

knowledge = TextKnowledgeBase(
    vector_db=PgVector(
        table_name="recipes",
        db_url="postgresql://localhost:5432/mydb",
    ),
)

agent = Agent(model=model, knowledge=knowledge)
agent.knowledge.load(references=["path/to/recipes.txt"])
```

## Workflows

```python
from kern.workflows import Workflow

class ResearchWorkflow(Workflow):
    research_step: Agent = Field(...)
    write_step: Agent = Field(...)

    def run(self, topic: str):
        research = self.research_step.run(f"Research {topic}")
        article = self.write_step.run(f"Write about: {research.content}")
        return article

wf = ResearchWorkflow(
    research_step=Agent(name="Researcher", tools=[DuckDuckGoTools()]),
    write_step=Agent(name="Writer"),
)
result = wf.run(topic="renewable energy")
```

## License

Apache License 2.0
