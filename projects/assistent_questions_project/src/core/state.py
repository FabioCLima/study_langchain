# assistent_questions_project/src/core/state.py
"""State Management Module for Assistant Questions Project
======================================================

Defines the shared state for the LangGraph workflow.
This version is simplified for clarity and study purposes.
"""

from typing import TypedDict

# =============================================================================
# Agent State Definition
# =============================================================================


class AgentState(TypedDict):
    """Represents the shared memory of the workflow.

    Each node in the graph reads from and writes to this state,
    allowing information to flow through the system.

    Attributes:
        original_question: The initial question from the user.
        enhanced_question: The question after being improved by the enhancer agent.
        answer: The final response from the specialist agent.
        specialization: The domain of expertise for the current session.

    """

    original_question: str
    enhanced_question: str
    answer: str
    specialization: str


# =============================================================================
# Example Usage (for understanding)
# =============================================================================

# No additional functions are needed. The nodes in your graph will be responsible
# for populating these fields directly.

# Here's how the state will look at each step of your workflow:

# 1. After the user asks a question:
#    initial_state = AgentState(
#        original_question="what is a dict?",
#        enhanced_question="",
#        answer="",
#        specialization="Python"
#    )

# 2. After the 'enhancer' node runs:
#    state_after_enhancement = AgentState(
#        original_question="what is a dict?",
#        enhanced_question="Explain what a dictionary is in Python with examples.",
#        answer="",
#        specialization="Python"
#    )

# 3. After the 'specialist' node runs:
#    final_state = AgentState(
#        original_question="what is a dict?",
#        enhanced_question="Explain what a dictionary is in Python with examples.",
#        answer="A dictionary in Python is a collection of key-value pairs...",
#        specialization="Python"
#    )
