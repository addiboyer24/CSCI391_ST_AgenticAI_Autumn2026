"""
Chapter 3 — Anatomy of an Agent
Coffee Shop Ordering Agent

This example demonstrates the basic anatomy of an agent using a
ReAct-style loop:

    USER
      ↓
    THOUGHT
      ↓
    ACTION
      ↓
    TOOL CALL
      ↓
    OBSERVATION
      ↓
    THOUGHT
      ↓
    ACTION
      ↓
    ...

The LLM produces the THOUGHT and ACTION.

The Python program executes the ACTION and produces the OBSERVATION.

The loop continues until the LLM calls final_answer().

The agent can run in two modes:

    python coffee_agent.py online
    python coffee_agent.py offline

ONLINE:
    Uses OpenRouter.

OFFLINE:
    Uses a local llama.cpp server.
"""

import argparse
import json
import os
from dataclasses import dataclass, field
from typing import Any, Callable

import requests
from dotenv import load_dotenv


# ============================================================================
# CONFIGURATION
# ============================================================================

load_dotenv()

MAX_STEPS = 10

# ---------------------------------------------------------------------------
# Online LLM — OpenRouter
# ---------------------------------------------------------------------------

OPENROUTER_URL = (
    "https://openrouter.ai/api/v1/chat/completions"
)

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "nvidia/nemotron-3-super-120b-a12b:free",
)

# ---------------------------------------------------------------------------
# Offline LLM — local llama.cpp server
# ---------------------------------------------------------------------------

LOCAL_LLM_URL = os.getenv(
    "LOCAL_LLM_URL",
    "http://127.0.0.1:8080/v1/chat/completions",
)

LOCAL_LLM_MODEL = os.getenv(
    "LOCAL_LLM_MODEL",
    "Qwen/Qwen3-4B-GGUF:Q4_K_M",
)


# ============================================================================
# DATA / APPLICATION STATE
# ============================================================================

MENU = {
    "coffee": 3.00,
    "tea": 2.50,
    "muffin": 2.75,
    "cookie": 1.50,
}

ORDER: list[dict[str, Any]] = []


# ============================================================================
# SYSTEM PROMPT
# ============================================================================

SYSTEM_PROMPT = """
You are a coffee shop ordering assistant.

Your job is to help the user build a coffee shop order.

You have access to three tools:

- get_menu
- add_to_order
- final_answer

You operate using a ReAct-style loop:

1. THOUGHT
   Decide what needs to happen next.

2. ACTION
   Select a tool if you need information or need to modify the order.

3. OBSERVATION
   After a tool is executed, examine its result.

4. THOUGHT
   Decide what to do next based on the observation.

Continue this loop until the user's request has been completely handled.

Rules:

1. Use get_menu when you need to know what items are available or their prices.
2. Use add_to_order to add items to the user's order.
3. You may call tools multiple times if necessary.
4. Do not invent menu items or prices.
5. When the order is complete, ALWAYS call final_answer.
6. Never answer the user directly without calling final_answer.
7. The final_answer call is the terminal state of the agent.

The Python program, not you, executes the tools.
You only request the tool calls.
"""


# ============================================================================
# TOOLS
# ============================================================================

def get_menu():
    """
    Return the available menu items and prices.
    """

    menu_lines = [
        f"{item}: ${price:.2f}"
        for item, price in MENU.items()
    ]

    return {
        "menu": menu_lines,
    }


def add_to_order(
    item: str,
    quantity: int,
):
    """
    Add an item to the current order.
    """

    item = item.lower().strip()

    if item not in MENU:
        return {
            "success": False,
            "message": f"'{item}' is not on the menu.",
        }

    if quantity <= 0:
        return {
            "success": False,
            "message": "Quantity must be greater than zero.",
        }

    ORDER.append(
        {
            "item": item,
            "quantity": quantity,
        }
    )

    return {
        "success": True,
        "message": (
            f"Added {quantity} {item}"
            f"{'s' if quantity != 1 else ''} to the order."
        ),
    }


def final_answer(
    answer: str,
    order: list[dict[str, Any]],
    total: float,
    confidence: str,
):
    """
    Terminal tool.

    Calling this tool means the agent has finished its work.
    """

    return {
        "answer": answer,
        "order": order,
        "total": total,
        "confidence": confidence,
    }


# ============================================================================
# TOOL REGISTRY
# ============================================================================

TOOLS: dict[str, Callable[..., Any]] = {
    "get_menu": get_menu,
    "add_to_order": add_to_order,
    "final_answer": final_answer,
}


# ============================================================================
# TOOL SCHEMAS
# ============================================================================

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Get the coffee shop menu and prices.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_order",
            "description": "Add an item to the user's coffee shop order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The menu item to add.",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The number of items to add.",
                    },
                },
                "required": [
                    "item",
                    "quantity",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "final_answer",
            "description": (
                "Finish the interaction and return the completed order."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": (
                            "A natural-language response to the user."
                        ),
                    },
                    "order": {
                        "type": "array",
                        "description": "The completed order.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "item": {
                                    "type": "string",
                                },
                                "quantity": {
                                    "type": "integer",
                                },
                            },
                            "required": [
                                "item",
                                "quantity",
                            ],
                        },
                    },
                    "total": {
                        "type": "number",
                        "description": "The total cost of the order.",
                    },
                    "confidence": {
                        "type": "string",
                        "description": (
                            "Confidence in the completed order, "
                            "such as high, medium, or low."
                        ),
                    },
                },
                "required": [
                    "answer",
                    "order",
                    "total",
                    "confidence",
                ],
            },
        },
    },
]


# ============================================================================
# RUN RESULT
# ============================================================================

@dataclass
class RunResult:
    status: str
    answer: str | None = None
    order: list[dict[str, Any]] = field(default_factory=list)
    total: float | None = None
    confidence: str | None = None
    steps: int = 0


# ============================================================================
# LLM REQUEST
# ============================================================================

def chat(
    messages: list[dict[str, Any]],
    mode: str,
) -> dict[str, Any]:
    """
    Send the conversation to either OpenRouter or a local llama.cpp server.

    Both providers expose an OpenAI-compatible API, so the request format
    remains the same.
    """

    if mode == "online":

        if not OPENROUTER_API_KEY:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not configured."
            )

        url = OPENROUTER_URL
        model = OPENROUTER_MODEL

        headers = {
            "Authorization": (
                f"Bearer {OPENROUTER_API_KEY}"
            ),
            "Content-Type": "application/json",
        }

    else:

        url = LOCAL_LLM_URL
        model = LOCAL_LLM_MODEL

        headers = {
            "Content-Type": "application/json",
        }

    print()
    print("[LLM]")
    print(f"Mode: {mode}")
    print(f"Model: {model}")
    print(f"Endpoint: {url}")

    response = requests.post(
        url,
        headers=headers,
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                *messages,
            ],
            "tools": TOOLS_SCHEMA,
            "tool_choice": "auto",
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    print()
    print("[DEBUG] Response JSON:")
    print(
        json.dumps(
            data,
            indent=2,
        )
    )

    return data["choices"][0]["message"]


# ============================================================================
# AGENT LOOP
# ============================================================================

def run(
    question: str,
    mode: str,
) -> RunResult:

    # Reset application state for every run.
    ORDER.clear()

    messages = [
        {
            "role": "user",
            "content": question,
        }
    ]

    print()
    print("=" * 70)
    print("STARTING AGENT")
    print("=" * 70)

    for step in range(1, MAX_STEPS + 1):

        print()
        print(f"--- REACT STEP {step} ---")

        # ====================================================================
        # THOUGHT
        # ====================================================================
        #
        # The LLM receives the conversation and decides what should happen
        # next.
        #
        # The LLM is NOT executing Python here.
        #
        # It is deciding what action the agent should take.
        # ====================================================================

        print()
        print("[THOUGHT]")
        print("LLM is deciding what to do next...")

        assistant = chat(
            messages,
            mode,
        )

        # ====================================================================
        # ADD ASSISTANT MESSAGE TO CONVERSATION
        # ====================================================================

        messages.append(assistant)

        # ====================================================================
        # ACTION
        # ====================================================================
        #
        # The assistant message may contain tool calls.
        #
        # A tool call is the LLM saying:
        #
        #     "I want the program to execute this function."
        #
        # The LLM itself does not execute the Python function.
        # ====================================================================

        tool_calls = assistant.get(
            "tool_calls",
            [],
        )

        if not tool_calls:

            print()
            print("[ACTION]")
            print("LLM did not request a tool.")

            print()
            print("[STATUS]")
            print(
                "halted — agent stopped without "
                "reaching final_answer."
            )

            return RunResult(
                status="halted",
                steps=step,
            )

        # ====================================================================
        # EXECUTE TOOL CALLS
        # ====================================================================

        for tool_call in tool_calls:

            name = tool_call["function"]["name"]

            arguments = json.loads(
                tool_call["function"]["arguments"]
            )

            print()
            print("[ACTION]")
            print(
                f"LLM requested tool call: {name}"
            )

            print()
            print("[TOOL CALL]")
            print(
                f"Executing Python function: "
                f"{name}(**{arguments})"
            )

            # =================================================================
            # VALIDATE TOOL
            # =================================================================

            if name not in TOOLS:

                raise ValueError(
                    f"Unknown tool '{name}'."
                )

            # =================================================================
            # TERMINAL ACTION
            # =================================================================
            #
            # final_answer is the terminal state.
            #
            # Unlike the other tools, it does not generate another
            # observation that goes back into the ReAct loop.
            # =================================================================

            if name == "final_answer":

                result = TOOLS[name](
                    **arguments
                )

                print()
                print("[TERMINAL ACTION]")
                print(
                    "final_answer was called."
                )

                print()
                print("[STATUS]")
                print(
                    "answered — agent reached "
                    "its terminal state."
                )

                return RunResult(
                    status="answered",
                    answer=result["answer"],
                    order=result["order"],
                    total=result["total"],
                    confidence=result["confidence"],
                    steps=step,
                )

            # =================================================================
            # EXECUTE TOOL
            # =================================================================
            #
            # THIS is where the Python runtime actually executes the
            # action selected by the LLM.
            # =================================================================

            result = TOOLS[name](
                **arguments
            )

            # =================================================================
            # OBSERVATION
            # =================================================================
            #
            # The Python function has returned a result.
            #
            # That result becomes an observation for the LLM.
            # =================================================================

            print()
            print("[OBSERVATION]")
            print(
                json.dumps(
                    result,
                    indent=2,
                )
            )

            # Add the tool result to the conversation.
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(result),
                }
            )

            print()
            print(
                "Observation added to conversation."
            )
            print(
                "Returning to THOUGHT..."
            )

    # =========================================================================
    # STEP BUDGET EXCEEDED
    # =========================================================================

    print()
    print("[STATUS]")
    print(
        "budget_exceeded — maximum number "
        "of ReAct steps reached."
    )

    return RunResult(
        status="budget_exceeded",
        steps=MAX_STEPS,
    )


# ============================================================================
# COMMAND-LINE ARGUMENTS
# ============================================================================

def parse_args():
    """
    Parse the command-line arguments.

    Examples:

        python coffee_agent.py online
        python coffee_agent.py offline
    """

    parser = argparse.ArgumentParser(
        description="Coffee Shop ReAct Agent"
    )

    parser.add_argument(
        "mode",
        choices=[
            "online",
            "offline",
        ],
        help=(
            "LLM mode: "
            "online uses OpenRouter; "
            "offline uses the local llama.cpp server."
        ),
    )

    return parser.parse_args()


# ============================================================================
# INTERACTIVE ENTRY POINT
# ============================================================================

if __name__ == "__main__":

    args = parse_args()

    print()
    print("=" * 70)
    print("COFFEE SHOP ORDERING AGENT")
    print("=" * 70)

    print()
    print("This agent demonstrates a ReAct-style loop:")
    print()
    print(
        "THOUGHT → ACTION → TOOL CALL → "
        "OBSERVATION → THOUGHT → ..."
    )

    print()
    print(
        f"Running in {args.mode.upper()} mode."
    )

    print()
    print(
        "Type an order or question for the coffee shop."
    )

    print()

    question = input(
        "What would you like to order? "
    )

    result = run(
        question,
        args.mode,
    )

    print()
    print("=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    print(
        json.dumps(
            result.__dict__,
            indent=2,
        )
    )
