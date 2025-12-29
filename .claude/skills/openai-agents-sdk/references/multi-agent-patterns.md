# Multi-Agent Orchestration Patterns

Patterns for building multi-agent systems with the OpenAI Agents SDK.

## Table of Contents

1. [LLM-Driven Orchestration](#llm-driven-orchestration)
2. [Code-Based Orchestration](#code-based-orchestration)
3. [Common Patterns](#common-patterns)
4. [Best Practices](#best-practices)

## LLM-Driven Orchestration

Let the LLM decide how to route and delegate tasks.

### Triage Pattern

Central agent routes to specialists:

```python
from agents import Agent

# Specialist agents
billing_agent = Agent(
    name="billing_specialist",
    instructions="""You handle billing inquiries:
    - Account balances
    - Payment history
    - Invoice questions
    - Refund requests"""
)

tech_agent = Agent(
    name="tech_support",
    instructions="""You handle technical issues:
    - Bug reports
    - Feature questions
    - Integration help
    - Troubleshooting"""
)

sales_agent = Agent(
    name="sales",
    instructions="""You handle sales inquiries:
    - Pricing questions
    - Plan comparisons
    - Upgrade requests
    - Demo scheduling"""
)

# Triage agent
triage = Agent(
    name="triage",
    instructions="""You are the first point of contact.
    Understand the customer's need and route to the appropriate specialist:
    - billing_specialist: billing, payments, refunds
    - tech_support: technical issues, bugs, features
    - sales: pricing, upgrades, demos

    Always greet the customer warmly before routing.""",
    handoffs=[billing_agent, tech_agent, sales_agent]
)
```

### Hierarchical Delegation

Nested handoffs for complex workflows:

```python
# Level 2 specialists
refund_processor = Agent(
    name="refund_processor",
    instructions="Process refund requests. Verify eligibility and initiate refund."
)

payment_investigator = Agent(
    name="payment_investigator",
    instructions="Investigate failed or disputed payments."
)

# Level 1 specialist (can delegate further)
billing_agent = Agent(
    name="billing_specialist",
    instructions="""Handle billing inquiries.
    - For refunds, delegate to refund_processor
    - For payment issues, delegate to payment_investigator""",
    handoffs=[refund_processor, payment_investigator]
)

# Entry point
triage = Agent(
    name="triage",
    instructions="Route to billing_specialist for any billing matters.",
    handoffs=[billing_agent]
)
```

### Prompt Engineering for Routing

```python
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

triage = Agent(
    name="triage",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}

    You are a customer service triage agent.

    Available specialists:
    - billing_specialist: All billing, payment, and refund questions
    - tech_support: Technical issues and troubleshooting
    - sales: Pricing, plans, and upgrades

    Guidelines:
    1. Greet the customer
    2. Understand their primary need
    3. Route to the most appropriate specialist
    4. If unclear, ask one clarifying question""",
    handoffs=[billing_agent, tech_agent, sales_agent]
)
```

## Code-Based Orchestration

Deterministic control flow for predictable behavior.

### Sequential Pipeline

Chain agents in order:

```python
from agents import Agent, Runner

researcher = Agent(
    name="researcher",
    instructions="Research the topic thoroughly. Gather facts and sources."
)

analyst = Agent(
    name="analyst",
    instructions="Analyze the research. Identify key insights and patterns."
)

writer = Agent(
    name="writer",
    instructions="Write a clear, engaging report based on the analysis."
)

async def research_pipeline(topic: str) -> str:
    # Step 1: Research
    research = await Runner.run(researcher, f"Research: {topic}")

    # Step 2: Analyze
    analysis = await Runner.run(
        analyst,
        f"Analyze this research:\n\n{research.final_output}"
    )

    # Step 3: Write
    report = await Runner.run(
        writer,
        f"Write a report based on:\n\n{analysis.final_output}"
    )

    return report.final_output
```

### Parallel Execution

Run independent agents concurrently:

```python
import asyncio
from agents import Agent, Runner

sentiment_agent = Agent(
    name="sentiment",
    instructions="Analyze the sentiment of the text. Return: positive, negative, or neutral."
)

topic_agent = Agent(
    name="topics",
    instructions="Extract the main topics from the text. Return as a list."
)

entity_agent = Agent(
    name="entities",
    instructions="Extract named entities (people, places, organizations) from the text."
)

async def analyze_text(text: str) -> dict:
    # Run all analyses in parallel
    results = await asyncio.gather(
        Runner.run(sentiment_agent, text),
        Runner.run(topic_agent, text),
        Runner.run(entity_agent, text)
    )

    return {
        "sentiment": results[0].final_output,
        "topics": results[1].final_output,
        "entities": results[2].final_output
    }
```

### Evaluation Loop

Iterate until quality criteria met:

```python
from pydantic import BaseModel

class EvaluationResult(BaseModel):
    score: int  # 1-10
    feedback: str
    passes: bool

writer = Agent(
    name="writer",
    instructions="Write content based on the prompt and any feedback provided."
)

evaluator = Agent(
    name="evaluator",
    instructions="""Evaluate the content on:
    - Clarity (1-10)
    - Completeness (1-10)
    - Accuracy (1-10)

    Provide specific feedback for improvement.
    Set passes=True if average score >= 8.""",
    output_type=EvaluationResult
)

async def write_with_feedback(prompt: str, max_iterations: int = 3) -> str:
    content = ""
    feedback = ""

    for i in range(max_iterations):
        # Generate/revise content
        writer_input = f"Prompt: {prompt}"
        if feedback:
            writer_input += f"\n\nPrevious feedback: {feedback}"

        content_result = await Runner.run(writer, writer_input)
        content = content_result.final_output

        # Evaluate
        eval_result = await Runner.run(
            evaluator,
            f"Evaluate this content:\n\n{content}"
        )

        if eval_result.final_output.passes:
            return content

        feedback = eval_result.final_output.feedback

    return content  # Return best effort
```

### Structured Routing

Use structured output for deterministic routing:

```python
from pydantic import BaseModel
from enum import Enum

class Department(str, Enum):
    BILLING = "billing"
    TECH = "tech"
    SALES = "sales"
    GENERAL = "general"

class Classification(BaseModel):
    department: Department
    confidence: float
    reasoning: str

classifier = Agent(
    name="classifier",
    instructions="Classify the customer inquiry into the appropriate department.",
    output_type=Classification
)

agents = {
    Department.BILLING: billing_agent,
    Department.TECH: tech_agent,
    Department.SALES: sales_agent,
    Department.GENERAL: general_agent
}

async def route_inquiry(inquiry: str) -> str:
    # Classify
    classification = await Runner.run(classifier, inquiry)
    dept = classification.final_output.department

    # Route deterministically
    agent = agents[dept]
    result = await Runner.run(agent, inquiry)

    return result.final_output
```

## Common Patterns

### Supervisor Pattern

Manager agent coordinates workers:

```python
from agents import Agent, function_tool

# Worker tools
@function_tool
async def assign_research(topic: str) -> str:
    """Assign research task to research agent."""
    result = await Runner.run(researcher, topic)
    return result.final_output

@function_tool
async def assign_writing(content: str) -> str:
    """Assign writing task to writer agent."""
    result = await Runner.run(writer, content)
    return result.final_output

supervisor = Agent(
    name="supervisor",
    instructions="""You coordinate a team to complete tasks.

    Available workers:
    - assign_research: Get research on a topic
    - assign_writing: Get content written

    Break down complex requests and coordinate the team.""",
    tools=[assign_research, assign_writing]
)
```

### Debate Pattern

Multiple agents discuss to reach consensus:

```python
async def debate(question: str, rounds: int = 3) -> str:
    optimist = Agent(
        name="optimist",
        instructions="Argue for the positive aspects and opportunities."
    )

    skeptic = Agent(
        name="skeptic",
        instructions="Argue for caution and potential risks."
    )

    moderator = Agent(
        name="moderator",
        instructions="Synthesize the arguments into a balanced conclusion."
    )

    discussion = f"Question: {question}\n\n"

    for i in range(rounds):
        opt = await Runner.run(optimist, discussion + "Present your argument.")
        discussion += f"\nOptimist: {opt.final_output}\n"

        skep = await Runner.run(skeptic, discussion + "Present your counterargument.")
        discussion += f"\nSkeptic: {skep.final_output}\n"

    conclusion = await Runner.run(moderator, discussion + "Provide your conclusion.")
    return conclusion.final_output
```

### Fallback Chain

Try agents in order until success:

```python
async def fallback_chain(query: str) -> str:
    agents = [primary_agent, backup_agent, general_agent]

    for agent in agents:
        try:
            result = await Runner.run(agent, query)
            if result.final_output and "I don't know" not in result.final_output:
                return result.final_output
        except Exception:
            continue

    return "I'm sorry, I couldn't help with that request."
```

## Best Practices

### 1. Specialize Agents

Create focused agents rather than generalists:

```python
# Good: Focused agent
refund_agent = Agent(
    name="refund_specialist",
    instructions="""You process refund requests ONLY.

    Steps:
    1. Verify order exists
    2. Check refund eligibility (30-day policy)
    3. Process refund or explain denial

    You do NOT handle: billing inquiries, tech support, sales."""
)

# Avoid: Overloaded agent
# support_agent = Agent(
#     name="support",
#     instructions="Handle billing, tech support, sales, refunds, ..."
# )
```

### 2. Clear Handoff Boundaries

Define explicit routing criteria:

```python
triage = Agent(
    name="triage",
    instructions="""Route based on keywords and intent:

    → billing_specialist:
      - "refund", "charge", "invoice", "payment"
      - Questions about money/billing

    → tech_support:
      - "error", "bug", "broken", "not working"
      - Technical problems

    → sales:
      - "pricing", "upgrade", "plan", "discount"
      - Purchase decisions

    If unclear, ask: "Is this about billing, a technical issue, or purchasing?" """,
    handoffs=[billing_agent, tech_agent, sales_agent]
)
```

### 3. Monitor and Iterate

Track performance and refine:

```python
from agents import Agent, RunConfig

config = RunConfig(
    trace_include_sensitive_data=True,
    workflow_name="customer_support"
)

# Run with tracing
result = await Runner.run(triage, inquiry, run_config=config)

# Analyze traces in OpenAI dashboard or external processor
```

### 4. Handle Edge Cases

Plan for routing failures:

```python
fallback_agent = Agent(
    name="fallback",
    instructions="""You handle requests that don't fit other categories.

    1. Try to help directly if possible
    2. If you can't help, apologize and offer to connect with a human
    3. Collect contact info for follow-up"""
)

triage = Agent(
    name="triage",
    instructions="Route to specialists. If no specialist fits, use fallback.",
    handoffs=[billing_agent, tech_agent, sales_agent, fallback_agent]
)
```
