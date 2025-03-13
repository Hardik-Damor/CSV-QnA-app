from pydantic import BaseModel
import ollama
from typing import Dict, Any, Optional
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class RateLimitError(Exception):
    """Raised when query rate limit is exceeded"""
    pass

class QueryRequest(BaseModel):
    question: str
    context: Dict[str, Any]

class LLMAgent:
    def __init__(self, model_name: str = "llama3:8b", rate_limit_seconds: int = 1):
        self.model = model_name
        self.rate_limit = rate_limit_seconds
        self.last_query_time: Optional[datetime] = None

    async def process_query(self, query: QueryRequest) -> str:
        """Process a query with rate limiting."""
        try:
            if self._is_rate_limited():
                raise RateLimitError(f"Please wait {self.rate_limit} seconds between queries")

            if not query.question.strip():
                return "Error: Question cannot be empty"

            self.last_query_time = datetime.now()
            context = self._format_context(query.context)
            
            if "No data available" in context:
                return context

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a data analysis assistant specialized in analyzing numerical data."
                    },
                    {
                        "role": "user", 
                        "content": self._create_prompt(query.question, context)
                    }
                ]
            )
            
            return response['message']['content']
            
        except RateLimitError:
            raise
        except Exception as e:
            logger.error(f"Query processing failed: {str(e)}")
            return f"Error: {str(e)}"

    def _is_rate_limited(self) -> bool:
        """Check if the request should be rate limited."""
        if self.last_query_time is None:
            return False
        time_since_last = datetime.now() - self.last_query_time
        return time_since_last.total_seconds() < self.rate_limit

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format the context data for the prompt."""
        if not context:
            return "No data available for analysis"

        sections = []
        if 'row_count' in context:
            sections.append(f"Total rows: {context['row_count']}")
        if 'columns' in context:
            sections.append(f"Available columns: {', '.join(context['columns'])}")
        if 'summary' in context:
            sections.append("\nSummary statistics:")
            for col, stats in context['summary'].items():
                stats_str = json.dumps(stats, indent=2)
                sections.append(f"  {col}:\n{stats_str}")
        return "\n".join(sections)

    def _create_prompt(self, question: str, context: str) -> str:
        """Create a structured prompt for the model."""
        return f"""Please analyze this data:

{context}

Question: {question}

Please provide:
1. A direct answer with specific numbers
2. Any relevant statistics from the data
3. Important patterns or trends (if any)
4. Data limitations (if applicable)
"""