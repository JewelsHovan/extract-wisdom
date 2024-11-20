PAPER_DIR = "papers"
OUTPUT_DIR = "output"

# Model configurations
DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o"

# Available models by provider
MODEL_CONFIGS = {
    "openai": {
        "models": ["gpt-4o", "gpt-4o-mini"],
        "api_base": None  # Uses default OpenAI API base
    },
    "openrouter": {
        "models": [
            "google/gemini-exp-1114",
            "google/gemma-2-9b-it:free",
            "google/gemini-flash-1.5-8b-exp"

        ],
        "api_base": "https://openrouter.ai/api/v1"
    },
    "gemini": {
        "models": ["gemini-1.5-flash", 'gemini-1.5-pro'],
        "api_base": "https://generativelanguage.googleapis.com/v1beta/models/"
    }
}

# Get available models for all providers
AVAILABLE_MODELS = [(provider, model) for provider, config in MODEL_CONFIGS.items() 
                   for model in config["models"]]
