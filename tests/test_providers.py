import os
import pytest
from dotenv import load_dotenv
from paper_analyzer import PaperAnalyzer
from models import create_model_config
from config import MODEL_CONFIGS

# Load environment variables
load_dotenv()

# Test constants
TEST_PDF_PATH = os.path.join(os.path.dirname(__file__), "data/sample.pdf")
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Setup test environment
@pytest.fixture(scope="session")
def api_keys():
    """Load API keys from environment variables"""
    return {
        "openai": os.getenv("OPENAI_API_KEY"),
        "openrouter": os.getenv("OPENROUTER_API_KEY"),
        "gemini": os.getenv("GOOGLE_API_KEY")
    }

@pytest.fixture(scope="session")
def test_pdf():
    """Ensure test PDF exists"""
    os.makedirs(os.path.dirname(TEST_PDF_PATH), exist_ok=True)
    if not os.path.exists(TEST_PDF_PATH):
        raise FileNotFoundError(f"Test PDF not found at {TEST_PDF_PATH}. Please add a sample PDF for testing.")
    return TEST_PDF_PATH

@pytest.fixture(autouse=True)
def setup_teardown():
    """Setup and teardown for each test"""
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    yield
    # Cleanup output directory after tests
    for file in os.listdir(TEST_OUTPUT_DIR):
        os.remove(os.path.join(TEST_OUTPUT_DIR, file))

def test_model_configs():
    """Test that model configurations are properly defined"""
    assert "openai" in MODEL_CONFIGS
    assert "openrouter" in MODEL_CONFIGS
    assert "gemini" in MODEL_CONFIGS
    
    for provider, config in MODEL_CONFIGS.items():
        assert "models" in config
        assert isinstance(config["models"], list)
        assert len(config["models"]) > 0
        assert "api_base" in config

@pytest.mark.parametrize("provider", ["openai", "openrouter", "gemini"])
def test_provider_authentication(api_keys, provider):
    """Test API key authentication for each provider"""
    api_key = api_keys[provider]
    assert api_key is not None, f"API key for {provider} not found in environment variables"
    
    model_name = MODEL_CONFIGS[provider]["models"][0]
    model_config = create_model_config(
        provider=provider,
        model_name=model_name,
        api_key=api_key,
        api_base=MODEL_CONFIGS[provider]["api_base"]
    )
    
    # Test model creation
    chat_model = model_config.create_chat_model()
    assert chat_model is not None

@pytest.mark.parametrize("provider", ["openai", "openrouter", "gemini"])
def test_basic_query(api_keys, test_pdf, provider):
    """Test basic query functionality for each provider"""
    api_key = api_keys[provider]
    model_name = MODEL_CONFIGS[provider]["models"][0]
    
    analyzer = PaperAnalyzer(
        test_pdf,
        api_key=api_key,
        model_name=model_name,
        provider=provider,
        output_dir=TEST_OUTPUT_DIR
    )
    
    # Test document loading
    analyzer.load_document()
    assert analyzer.document is not None
    
    # Test custom query
    test_query = "What is the main topic of this paper?"
    response = analyzer.custom_query(test_query)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.parametrize("provider", ["openai", "openrouter", "gemini"])
def test_error_handling(provider):
    """Test error handling with invalid configurations"""
    with pytest.raises(Exception):
        # Test with invalid API key
        analyzer = PaperAnalyzer(
            TEST_PDF_PATH,
            api_key="invalid_key",
            model_name=MODEL_CONFIGS[provider]["models"][0],
            provider=provider
        )
        analyzer.custom_query("Test query")

def test_cross_provider_comparison(api_keys, test_pdf):
    """Compare responses across different providers"""
    test_query = "What is the main topic of this paper?"
    responses = {}
    
    for provider in ["openai", "openrouter", "gemini"]:
        analyzer = PaperAnalyzer(
            test_pdf,
            api_key=api_keys[provider],
            model_name=MODEL_CONFIGS[provider]["models"][0],
            provider=provider,
            output_dir=TEST_OUTPUT_DIR
        )
        analyzer.load_document()
        responses[provider] = analyzer.custom_query(test_query)
    
    # Verify all providers returned non-empty responses
    for provider, response in responses.items():
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
