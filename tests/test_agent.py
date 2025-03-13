import pytest
from src.agent.llm_agent import LLMAgent, QueryRequest

@pytest.fixture
def sample_query():
    """Create a sample query for testing."""
    return QueryRequest(
        question="What is the average price?",
        context={
            "columns": ["price", "size", "bedrooms"],
            "summary": {
                "price": {
                    "mean": 500000,
                    "std": 100000,
                    "min": 300000,
                    "max": 700000
                }
            },
            "row_count": 100
        }
    )

@pytest.mark.asyncio
async def test_valid_query(sample_query):
    """Test successful query processing."""
    agent = LLMAgent(model_name="llama3:8b")
    response = await agent.process_query(sample_query)
    
    assert isinstance(response, str)
    assert "Error" not in response
    assert len(response) > 0

@pytest.mark.asyncio
async def test_empty_question():
    """Test handling of empty questions."""
    agent = LLMAgent()
    query = QueryRequest(question="", context={})
    response = await agent.process_query(query)
    
    assert "Error" in response
    assert "Question cannot be empty" in response

@pytest.mark.asyncio
async def test_invalid_context():
    """Test handling of invalid context."""
    agent = LLMAgent()
    query = QueryRequest(
        question="What is the average price?",
        context={}
    )
    response = await agent.process_query(query)
    
    assert "No data available" in response