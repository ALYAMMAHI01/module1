pip install langchain langchain-openai
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
import math


def calculator(expression: str) -> str:
    """
    Safely evaluate math expressions
    """
    try:
        allowed = {
            "sqrt": math.sqrt,
            "pow": pow,
            "abs": abs
        }
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

calculator_tool = Tool(
    name="Calculator",
    func=calculator,
    description=(
        "Use for ALL math operations. "
        "Input must be a valid math expression "
        "(e.g., '25 * 4', 'sqrt(16)', 'pow(2,3)')."
    )
)


math_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

math_agent = initialize_agent(
    tools=[calculator_tool],
    llm=math_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


reflection_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def reflect_on_answer(question: str, answer: str) -> str:
    """
    Second agent reflects on the math agent's output
    """
    prompt = f"""
You are a reflection agent.

Original Question:
{question}

Math Agent Answer:
{answer}

Tasks:
1. Verify the correctness of the answer
2. Explain the reasoning in simple steps
3. If incorrect, provide the corrected answer

Reflection:
"""
    response = reflection_llm.invoke(prompt)
    return response.content


def run_multi_agent(question: str):
    print(f"\n QUESTION: {question}")

    # Agent 1: Math
    math_result = math_agent.run(question)
    print(f"\n MATH AGENT RESULT:\n{math_result}")

    # Agent 2: Reflection
    reflection = reflect_on_answer(question, math_result)
    print(f"\n REFLECTION AGENT OUTPUT:\n{reflection}")


questions = [
    "What is (12 + 8) * 3?",
    "What is the square root of 225?",
    "If I buy 4 items at $7.50 each, what is the total?"
]

for q in questions:
    run_multi_agent(q)
