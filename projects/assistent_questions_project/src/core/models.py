"""
Pydantic Models for Structured Data
=====================================

This module defines the Pydantic models used for structured output
from the LLMs, ensuring predictable and clean data flow.
"""
from pydantic import BaseModel, Field

class EnhancedQuestion(BaseModel):
    """Data model for a clean, enhanced question."""
    
    enhanced_question: str = Field(
        ..., 
        description="The clear, specific, and enhanced version of the user's original question."
    )


# ADICIONE ESTA CLASSE QUE ESTÁ FALTANDO
class ScopeDecision(BaseModel):
    """Data model for the scope decision."""
    is_in_scope: bool = Field(..., description="True if the question is within the specialist's scope, False otherwise.")
