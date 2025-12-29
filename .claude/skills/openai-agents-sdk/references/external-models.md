# External Models Integration

Guide to using non-OpenAI models with the OpenAI Agents SDK.

## Table of Contents

1. [Overview](#overview)
2. [OpenAI-Compatible Endpoints (Recommended)](#openai-compatible-endpoints-recommended)
3. [LiteLLM Integration (Alternative)](#litellm-integration-alternative)
4. [Troubleshooting](#troubleshooting)

## Overview

The SDK supports two main methods for external models:

### Method 1: OpenAI-Compatible Endpoints (Recommended)

Use `OpenAIChatCompletionsModel` with `AsyncOpenAI` client. This is the **recommended approach** for providers that offer OpenAI-compatible APIs.

**Best for:** Gemini, OpenRouter, Groq, DeepSeek, Mistral, Together AI, Ollama, vLLM

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig

client = AsyncOpenAI(api_key="your-key", base_url="https://provider-url/v1")
model = OpenAIChatCompletionsModel(model="model-name", openai_client=client)
run_config = RunConfig(model=model, tracing_disabled=True)
```

### Method 2: LiteLLM (Alternative)

Use `LitellmModel` wrapper. This is a **fallback option** for providers without OpenAI-compatible APIs.

**Best for:** Anthropic (native API), Cohere, AI21, Bedrock, Vertex AI

```python
from agents.extensions.models.litellm_model import LitellmModel

agent = Agent(model=LitellmModel(model="anthropic/claude-3-5-sonnet-20240620"))
```

### OpenRouter vs LiteLLM - Important Distinction

These are **different things**:

| | OpenRouter | LiteLLM |
|---|------------|---------|
| **What** | Hosted API gateway/service | Python SDK/wrapper library |
| **Access** | Direct via `AsyncOpenAI` + base_url | Via `LitellmModel` class |
| **Cost** | 5% fee on API calls | Free (open-source) |
| **Hosting** | Managed by OpenRouter | Self-managed |

**OpenRouter** is a service that provides a single API endpoint to access 400+ models from various providers. Use it directly:

```python
# CORRECT: Use OpenRouter directly
client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
model = OpenAIChatCompletionsModel(model="anthropic/claude-3.5-sonnet", openai_client=client)
```

**LiteLLM** is a Python library that wraps multiple providers. While LiteLLM *can* use OpenRouter as a provider (`openrouter/model-name`), this adds an unnecessary layer since OpenRouter already has an OpenAI-compatible API.

```python
# UNNECESSARY: Using LiteLLM to access OpenRouter (adds extra layer)
# LitellmModel(model="openrouter/anthropic/claude-3.5-sonnet")

# BETTER: Use OpenRouter directly via AsyncOpenAI (shown above)
```

### When to Use Each

| Scenario | Use |
|----------|-----|
| Gemini, Groq, DeepSeek, Mistral, Together | `OpenAIChatCompletionsModel` (direct) |
| OpenRouter (access 400+ models) | `OpenAIChatCompletionsModel` (direct) |
| Ollama, vLLM (local) | `OpenAIChatCompletionsModel` (direct) |
| Anthropic (without OpenRouter) | `LitellmModel` |
| AWS Bedrock, Google Vertex AI | `LitellmModel` |
| Cohere, AI21 | `LitellmModel` |

## OpenAI-Compatible Endpoints (Recommended)

The recommended approach for external models uses `OpenAIChatCompletionsModel` with `AsyncOpenAI` client and `RunConfig`. This gives you full control over model configuration.

### Provider Base URLs

| Provider | Base URL | Example Model |
|----------|----------|---------------|
| Google Gemini | `https://generativelanguage.googleapis.com/v1beta/openai/` | `gemini-2.5-flash` |
| OpenRouter | `https://openrouter.ai/api/v1` | `anthropic/claude-3.5-sonnet` |
| Groq | `https://api.groq.com/openai/v1` | `llama-3.1-70b-versatile` |
| Together AI | `https://api.together.xyz/v1` | `meta-llama/Llama-3-70b-chat-hf` |
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| Mistral | `https://api.mistral.ai/v1` | `mistral-large-latest` |
| Fireworks | `https://api.fireworks.ai/inference/v1` | `accounts/fireworks/models/llama-v3-70b-instruct` |
| Ollama (local) | `http://localhost:11434/v1` | `llama3.1` |
| vLLM (local) | `http://localhost:8000/v1` | Your model name |

### Basic Pattern

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
import os

# 1. Create client with base_url and api_key
client = AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://provider-base-url/v1"
)

# 2. Create model using OpenAIChatCompletionsModel
model = OpenAIChatCompletionsModel(
    model="model-name",
    openai_client=client
)

# 3. Configure RunConfig (disable tracing for non-OpenAI models)
run_config = RunConfig(
    model=model,
    tracing_disabled=True
)

# 4. Create agent and run
agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant."
)

result = await Runner.run(agent, "Hello!", run_config=run_config)
```

### Google Gemini

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
import os
from dotenv import load_dotenv

load_dotenv()

# Client
gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model
GEMINI_MODEL = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",  # or gemini-2.5-pro, gemini-2.0-flash
    openai_client=gemini_client
)

# RunConfig
run_config = RunConfig(
    model=GEMINI_MODEL,
    tracing_disabled=True
)

# Agent
agent = Agent(
    name="gemini_assistant",
    instructions="You are a helpful assistant powered by Gemini."
)

# Run
result = await Runner.run(agent, "What is the capital of France?", run_config=run_config)
print(result.final_output)
```

### OpenRouter (Access 100+ Models)

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
import os

openrouter_client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Claude via OpenRouter
CLAUDE_MODEL = OpenAIChatCompletionsModel(
    model="anthropic/claude-3.5-sonnet",
    openai_client=openrouter_client
)

# Free Llama model
FREE_MODEL = OpenAIChatCompletionsModel(
    model="meta-llama/llama-3.1-8b-instruct:free",
    openai_client=openrouter_client
)

run_config = RunConfig(
    model=CLAUDE_MODEL,  # or FREE_MODEL
    tracing_disabled=True
)

agent = Agent(name="assistant", instructions="You are helpful.")
result = await Runner.run(agent, "Hello!", run_config=run_config)
```

### Groq (Ultra-Fast Inference)

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
import os

groq_client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

GROQ_MODEL = OpenAIChatCompletionsModel(
    model="llama-3.1-70b-versatile",  # or mixtral-8x7b-32768, llama-3.1-8b-instant
    openai_client=groq_client
)

run_config = RunConfig(
    model=GROQ_MODEL,
    tracing_disabled=True
)

agent = Agent(name="fast_assistant", instructions="You are a fast assistant.")
result = await Runner.run(agent, "Quick question!", run_config=run_config)
```

### DeepSeek

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
import os

deepseek_client = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

DEEPSEEK_MODEL = OpenAIChatCompletionsModel(
    model="deepseek-chat",  # or deepseek-coder
    openai_client=deepseek_client
)

run_config = RunConfig(
    model=DEEPSEEK_MODEL,
    tracing_disabled=True
)

agent = Agent(name="deepseek_assistant", instructions="You are helpful.")
result = await Runner.run(agent, "Hello!", run_config=run_config)
```

### Mistral AI

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
import os

mistral_client = AsyncOpenAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    base_url="https://api.mistral.ai/v1"
)

MISTRAL_MODEL = OpenAIChatCompletionsModel(
    model="mistral-large-latest",  # or mistral-small-latest, open-mixtral-8x22b
    openai_client=mistral_client
)

run_config = RunConfig(
    model=MISTRAL_MODEL,
    tracing_disabled=True
)

agent = Agent(name="mistral_assistant", instructions="You are helpful.")
result = await Runner.run(agent, "Hello!", run_config=run_config)
```

### Together AI

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
import os

together_client = AsyncOpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

TOGETHER_MODEL = OpenAIChatCompletionsModel(
    model="meta-llama/Llama-3-70b-chat-hf",
    openai_client=together_client
)

run_config = RunConfig(
    model=TOGETHER_MODEL,
    tracing_disabled=True
)

agent = Agent(name="assistant", instructions="You are helpful.")
result = await Runner.run(agent, "Hello!", run_config=run_config)
```

### Local Models (Ollama)

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig

# Ollama runs locally - no API key needed
ollama_client = AsyncOpenAI(
    api_key="ollama",  # Dummy key, Ollama doesn't require one
    base_url="http://localhost:11434/v1"
)

LOCAL_MODEL = OpenAIChatCompletionsModel(
    model="llama3.1",  # Must match `ollama list` output
    openai_client=ollama_client
)

run_config = RunConfig(
    model=LOCAL_MODEL,
    tracing_disabled=True
)

agent = Agent(name="local_assistant", instructions="You are a local assistant.")
result = await Runner.run(agent, "Hello!", run_config=run_config)
```

### vLLM / Local Inference Servers

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig

vllm_client = AsyncOpenAI(
    api_key="dummy",
    base_url="http://localhost:8000/v1"
)

VLLM_MODEL = OpenAIChatCompletionsModel(
    model="your-model-name",
    openai_client=vllm_client
)

run_config = RunConfig(
    model=VLLM_MODEL,
    tracing_disabled=True
)

agent = Agent(name="assistant", instructions="You are helpful.")
result = await Runner.run(agent, "Hello!", run_config=run_config)
```

### Per-Agent Model (Without RunConfig)

You can also set the model directly on the Agent:

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
import os

gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=gemini_client
)

# Model set directly on agent
agent = Agent(
    name="gemini_assistant",
    instructions="You are helpful.",
    model=gemini_model
)

# Run without run_config (but tracing may cause issues)
result = await Runner.run(agent, "Hello!")
```

### Multi-Model Setup

Use different models for different agents:

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
import os

# Fast/cheap model for simple tasks
groq_client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
FAST_MODEL = OpenAIChatCompletionsModel(model="llama-3.1-8b-instant", openai_client=groq_client)

# Smart model for complex tasks
gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
SMART_MODEL = OpenAIChatCompletionsModel(model="gemini-2.5-pro", openai_client=gemini_client)

# Agents with different models
fast_agent = Agent(name="fast", instructions="Quick responses.", model=FAST_MODEL)
smart_agent = Agent(name="smart", instructions="Detailed analysis.", model=SMART_MODEL)

# Route based on task complexity
async def route_query(query: str):
    config = RunConfig(tracing_disabled=True)
    if len(query) < 50:
        return await Runner.run(fast_agent, query, run_config=config)
    return await Runner.run(smart_agent, query, run_config=config)
```

### Global Client Setup (Alternative)

If you want all agents to use the same provider by default:

```python
from openai import AsyncOpenAI
from agents import set_default_openai_client, Agent, Runner
import os

# Set globally - all agents will use this client
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_default_openai_client(client)

# Agents use the global client
agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",  # Just the model name
    instructions="You are helpful."
)

result = Runner.run_sync(agent, "Hello!")
```

## LiteLLM Integration (Alternative)

LiteLLM is a Python SDK that wraps multiple providers. Use it **only** for providers that don't have OpenAI-compatible APIs.

### Installation

```bash
pip install "openai-agents[litellm]"
```

### When to Use LiteLLM

Use LiteLLM for providers **without** OpenAI-compatible endpoints:

| Provider | Use LiteLLM | Reason |
|----------|-------------|--------|
| Anthropic (direct) | Yes | Native API not OpenAI-compatible |
| AWS Bedrock | Yes | AWS-specific API |
| Google Vertex AI | Yes | GCP-specific API |
| Cohere | Yes | Native API not OpenAI-compatible |
| AI21 | Yes | Native API not OpenAI-compatible |

**Don't use LiteLLM for these** (use `OpenAIChatCompletionsModel` instead):
- Gemini (has OpenAI-compatible endpoint)
- OpenRouter (has OpenAI-compatible endpoint)
- Groq (has OpenAI-compatible endpoint)
- DeepSeek (has OpenAI-compatible endpoint)
- Together AI (has OpenAI-compatible endpoint)

### Anthropic Claude (via LiteLLM)

```python
from agents import Agent, Runner, RunConfig
from agents.extensions.models.litellm_model import LitellmModel
import os

os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"

claude_agent = Agent(
    name="claude",
    model=LitellmModel(model="anthropic/claude-3-5-sonnet-20240620"),
    instructions="You are Claude, a helpful AI assistant."
)

# Disable tracing for non-OpenAI models
run_config = RunConfig(tracing_disabled=True)
result = await Runner.run(claude_agent, "Hello!", run_config=run_config)
```

### AWS Bedrock (via LiteLLM)

```python
from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel
import os

os.environ["AWS_ACCESS_KEY_ID"] = "your-access-key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your-secret-key"
os.environ["AWS_REGION_NAME"] = "us-east-1"

bedrock_agent = Agent(
    name="bedrock",
    model=LitellmModel(model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0"),
    instructions="You are a helpful assistant."
)
```

### Google Vertex AI (via LiteLLM)

```python
from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/service-account.json"
os.environ["VERTEXAI_PROJECT"] = "your-project-id"
os.environ["VERTEXAI_LOCATION"] = "us-central1"

vertex_agent = Agent(
    name="vertex",
    model=LitellmModel(model="vertex_ai/gemini-1.5-pro"),
    instructions="You are a helpful assistant."
)
```

### Cohere (via LiteLLM)

```python
from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel
import os

os.environ["COHERE_API_KEY"] = "your-cohere-key"

cohere_agent = Agent(
    name="cohere",
    model=LitellmModel(model="cohere/command-r-plus"),
    instructions="You are a helpful assistant."
)
```

### Usage Tracking with LiteLLM

```python
from agents import Agent, Runner, ModelSettings, RunConfig
from agents.extensions.models.litellm_model import LitellmModel

agent = Agent(
    name="assistant",
    model=LitellmModel(model="anthropic/claude-3-5-sonnet-20240620"),
    model_settings=ModelSettings(include_usage=True)
)

run_config = RunConfig(tracing_disabled=True)
result = await Runner.run(agent, "Hello!", run_config=run_config)
print(f"Tokens used: {result.context_wrapper.usage}")
```

## Troubleshooting

### Common Issues

**1. Tracing Errors**

Non-OpenAI models may fail with tracing. Disable it:

```python
import os
os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "1"
```

Or via RunConfig:

```python
from agents import RunConfig

config = RunConfig(tracing_disabled=True)
result = await Runner.run(agent, input, run_config=config)
```

**2. Structured Output Not Supported**

Some providers don't support structured outputs. Use text parsing:

```python
# Instead of output_type, parse the response manually
agent = Agent(
    name="assistant",
    instructions="Always respond with JSON: {\"answer\": \"...\", \"confidence\": 0.0}"
)

result = Runner.run_sync(agent, "What is 2+2?")
import json
data = json.loads(result.final_output)
```

**3. API Compatibility Issues**

Use Chat Completions API instead of Responses API:

```python
from agents import set_default_openai_api

set_default_openai_api("chat_completions")
```

**4. Missing Features**

Some features only work with OpenAI:
- Hosted tools (WebSearchTool, CodeInterpreterTool)
- Multimodal inputs (images)
- Native structured outputs

Workarounds:
```python
# Use function tools instead of hosted tools
@function_tool
def search_web(query: str) -> str:
    """Search the web."""
    # Use your own search implementation
    return search_api.search(query)
```

### Provider-Specific Notes

| Provider | Access Method | Notes |
|----------|---------------|-------|
| Gemini | `OpenAIChatCompletionsModel` | Use base_url `generativelanguage.googleapis.com/v1beta/openai/` |
| OpenRouter | `OpenAIChatCompletionsModel` | Use base_url `openrouter.ai/api/v1`, 400+ models available |
| Groq | `OpenAIChatCompletionsModel` | Very fast inference, limited context windows |
| DeepSeek | `OpenAIChatCompletionsModel` | Cost-effective, good for coding |
| Together AI | `OpenAIChatCompletionsModel` | Good Llama support |
| Mistral | `OpenAIChatCompletionsModel` | European provider |
| Ollama | `OpenAIChatCompletionsModel` | Local only, model names match `ollama list` |
| Anthropic | `LitellmModel` | Use LiteLLM (no OpenAI-compatible API) |
| AWS Bedrock | `LitellmModel` | Use LiteLLM with AWS credentials |
| Vertex AI | `LitellmModel` | Use LiteLLM with GCP credentials |

### Debugging

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or for LiteLLM specifically
import litellm
litellm.set_verbose = True
```
