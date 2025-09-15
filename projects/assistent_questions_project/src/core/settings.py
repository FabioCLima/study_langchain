"""
Settings Module for Assistant Questions Project
==============================================

Handles project configuration, API keys, and LLM settings.
Following existing patterns with Pydantic for validation and security.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings


# =============================================================================
# 1. CONSTANTS (Following existing pattern)
# =============================================================================

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.5
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 2.0
DEFAULT_LOG_LEVEL = "INFO"


# =============================================================================
# 2. SETTINGS CLASS (Using Pydantic BaseSettings)
# =============================================================================

class ProjectSettings(BaseSettings):
    """
    Project settings using Pydantic for validation and security.
    
    Automatically loads from .env file and environment variables.
    API keys are stored as SecretStr for security.
    """
    
    # OpenAI Configuration
    openai_api_key: SecretStr = Field(
        ..., 
        description="OpenAI API key (required)"
    )
    
    # LangSmith Configuration  
    langsmith_tracing: bool = Field(
        default=True, 
        description="Enable LangSmith tracing"
    )
    langsmith_endpoint: str = Field(
        default="https://api.smith.langchain.com",
        description="LangSmith API endpoint"
    )
    langsmith_api_key: Optional[SecretStr] = Field(
        default=None, 
        description="LangSmith API key (optional)"
    )
    langsmith_project: str = Field(
        default="Assistant Questions Project",
        description="LangSmith project name"
    )
    
    # LLM Configuration
    llm_model: str = Field(
        default=DEFAULT_MODEL,
        description="OpenAI model to use"
    )
    llm_temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        ge=MIN_TEMPERATURE,
        le=MAX_TEMPERATURE,
        description="LLM temperature for response randomness"
    )
    llm_max_tokens: Optional[int] = Field(
        default=None,
        gt=0,
        description="Maximum tokens in LLM response"
    )
    
    # Logging Configuration
    log_level: str = Field(
        default=DEFAULT_LOG_LEVEL,
        description="Logging level"
    )
    log_file: str = Field(
        default="assistant_questions.log",
        description="Log file path"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True
        
        # Hide sensitive fields in string representation
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
        }
    
    @field_validator("llm_model")
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """Validate OpenAI model name."""
        if not v.strip():
            msg = "Model name cannot be empty"
            raise ValueError(msg)
        return v.strip()
    
    @field_validator("langsmith_project")
    @classmethod
    def validate_project_name(cls, v: str) -> str:
        """Validate project name."""
        if not v.strip():
            msg = "Project name cannot be empty"
            raise ValueError(msg)
        return v.strip()
    
    def get_openai_key(self) -> str:
        """
        Safely get OpenAI API key as string.
        
        Returns:
            str: The OpenAI API key
        """
        return self.openai_api_key.get_secret_value()
    
    def get_langsmith_key(self) -> Optional[str]:
        """
        Safely get LangSmith API key as string.
        
        Returns:
            Optional[str]: The LangSmith API key or None
        """
        return self.langsmith_api_key.get_secret_value() if self.langsmith_api_key else None
    
    def mask_sensitive_data(self) -> dict[str, str]:
        """
        Return settings with masked sensitive data for logging.
        
        Returns:
            dict: Settings with masked API keys
        """
        masked_openai = f"***{self.get_openai_key()[-4:]}" if self.openai_api_key else "Not set"
        langsmith_key = self.get_langsmith_key()
        masked_langsmith = f"***{langsmith_key[-4:]}" if langsmith_key else "Not set"
        
        return {
            "llm_model": self.llm_model,
            "llm_temperature": str(self.llm_temperature),
            "openai_api_key": masked_openai,
            "langsmith_api_key": masked_langsmith,
            "langsmith_project": self.langsmith_project,
            "langsmith_tracing": str(self.langsmith_tracing),
        }


# =============================================================================
# 3. LLM FACTORY (Following existing setup_llm pattern)
# =============================================================================

class LLMFactory:
    """Factory class for creating configured LLM instances."""
    
    def __init__(self, settings: ProjectSettings) -> None:
        """
        Initialize LLM factory with project settings.
        
        Args:
            settings: ProjectSettings instance with configuration
        """
        self.settings = settings
    
    def create_llm(
        self,
        temperature: Optional[float] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> ChatOpenAI:
        """
        Create a configured ChatOpenAI instance.
        
        Args:
            temperature: Override default temperature
            model: Override default model
            max_tokens: Override default max_tokens
            
        Returns:
            ChatOpenAI: Configured LLM instance
        """
        return ChatOpenAI(
            api_key=self.settings.get_openai_key(),
            model=model or self.settings.llm_model,
            temperature=temperature if temperature is not None else self.settings.llm_temperature,
            max_tokens=max_tokens or self.settings.llm_max_tokens,
        )
    
    def create_enhancement_llm(self) -> ChatOpenAI:
        """Create LLM optimized for question enhancement (low temperature)."""
        return self.create_llm(temperature=0.1)
    
    def create_specialist_llm(self) -> ChatOpenAI:
        """Create LLM optimized for specialist responses (default temperature)."""
        return self.create_llm()


# =============================================================================
# 4. GLOBAL SETTINGS INSTANCE
# =============================================================================

def load_settings() -> ProjectSettings:
    """
    Load and validate project settings from environment.
    
    Returns:
        ProjectSettings: Validated project settings
        
    Raises:
        ValueError: If required settings are missing or invalid
    """
    # Ensure .env is loaded
    load_dotenv()
    
    try:
        return ProjectSettings()
    except Exception as e:
        error_msg = f"Failed to load project settings: {e}"
        raise ValueError(error_msg) from e


# Global settings instance
settings: Optional[ProjectSettings] = None


def get_settings() -> ProjectSettings:
    """
    Get global settings instance (singleton pattern).
    
    Returns:
        ProjectSettings: Global settings instance
    """
    global settings  # noqa: PLW0603
    if settings is None:
        settings = load_settings()
    return settings


def get_llm_factory() -> LLMFactory:
    """
    Get configured LLM factory.
    
    Returns:
        LLMFactory: Factory for creating LLM instances
    """
    return LLMFactory(get_settings())


# =============================================================================
# 5. CONVENIENCE FUNCTIONS (Following existing patterns)
# =============================================================================

def setup_llm(
    temperature: Optional[float] = None,
    model: Optional[str] = None,
) -> ChatOpenAI:
    """
    Setup LLM following existing pattern from question_assistant.py.
    
    Args:
        temperature: Model temperature (default: from settings)
        model: Model name (default: from settings)
        
    Returns:
        ChatOpenAI: Configured LLM instance
    """
    factory = get_llm_factory()
    return factory.create_llm(temperature=temperature, model=model)


# =============================================================================
# 6. EXAMPLE USAGE AND TESTING
# =============================================================================

if __name__ == "__main__":
    # Example: Test the settings loading
    try:
        project_settings = get_settings()
        factory = get_llm_factory()
        
        print("✅ Settings loaded successfully!")
        print("📊 Configuration summary:")
        for key, value in project_settings.mask_sensitive_data().items():
            print(f"   {key}: {value}")
        
        print("\n🤖 Testing LLM creation:")
        llm = setup_llm()
        print(f"   Model: {llm.model_name}")
        print(f"   Temperature: {llm.temperature}")
        
        print("\n✨ All tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure your .env file has OPENAI_API_KEY set")