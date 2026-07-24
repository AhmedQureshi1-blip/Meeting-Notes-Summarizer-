"""
Meeting Notes Summarizer - Core Module
Handles the summarization logic with token tracking and cost estimation.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import tiktoken


class TokenTracker:
    """Tracks token usage and costs for API calls."""
    
    # Pricing (as of 2024) - GPT-3.5-turbo
    INPUT_COST_PER_1K_TOKENS = 0.0005
    OUTPUT_COST_PER_1K_TOKENS = 0.0015
    
    def __init__(self, log_file: str = "token_usage.json"):
        self.log_file = log_file
        self.session_tokens = {"input": 0, "output": 0}
        self.session_cost = 0.0
        self._load_history()
    
    def _load_history(self):
        """Load historical usage data."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []
        else:
            self.history = []
    
    def _save_history(self):
        """Save usage history to file."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "input_tokens": self.session_tokens["input"],
            "output_tokens": self.session_tokens["output"],
            "total_tokens": self.session_tokens["input"] + self.session_tokens["output"],
            "cost": self.session_cost
        }
        self.history.append(entry)
        
        # Keep only last 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        with open(self.log_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def count_tokens(self, text: str, model: str = "gpt-3.5-turbo") -> int:
        """Count tokens in text using tiktoken."""
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except:
            # Fallback: approximate tokens (1 token ≈ 4 characters)
            return len(text) // 4
    
    def log_usage(self, input_tokens: int, output_tokens: int):
        """Log token usage and update costs."""
        self.session_tokens["input"] += input_tokens
        self.session_tokens["output"] += output_tokens
        
        input_cost = (input_tokens / 1000) * self.INPUT_COST_PER_1K_TOKENS
        output_cost = (output_tokens / 1000) * self.OUTPUT_COST_PER_1K_TOKENS
        self.session_cost += input_cost + output_cost
        
        self._save_history()
    
    def get_session_stats(self) -> Dict:
        """Get current session statistics."""
        total_tokens = self.session_tokens["input"] + self.session_tokens["output"]
        return {
            "input_tokens": self.session_tokens["input"],
            "output_tokens": self.session_tokens["output"],
            "total_tokens": total_tokens,
            "cost": self.session_cost
        }
    
    def get_monthly_estimate(self, daily_usage: Dict) -> Dict:
        """Estimate monthly costs based on daily usage."""
        return {
            "estimated_monthly_tokens": daily_usage["total_tokens"] * 30,
            "estimated_monthly_cost": daily_usage["cost"] * 30
        }
    
    def reset_session(self):
        """Reset current session counters."""
        self.session_tokens = {"input": 0, "output": 0}
        self.session_cost = 0.0


class MeetingSummarizer:
    """Main summarization class with robust error handling."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.tracker = TokenTracker()
        self.model = "gpt-3.5-turbo"
    
    def _validate_input(self, text: str) -> Tuple[bool, str]:
        """Validate input text."""
        if not text or not text.strip():
            return False, "Input text cannot be empty."
        
        if len(text) < 50:
            return False, "Input text is too short. Please provide at least 50 characters."
        
        if len(text) > 100000:
            return False, "Input text is too long. Maximum 100,000 characters allowed."
        
        return True, ""
    
    def _chunk_text(self, text: str, max_chunk_size: int = 3000) -> List[str]:
        """Split text into chunks for processing."""
        chunks = []
        current_chunk = ""
        sentences = text.split('. ')
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chunk_size:
                current_chunk += sentence + ". "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def summarize(self, text: str, summary_length: str = "medium") -> Dict:
        """
        Summarize meeting notes with comprehensive error handling.
        
        Args:
            text: Meeting notes text
            summary_length: 'short', 'medium', or 'long'
        
        Returns:
            Dict with summary, token usage, and cost
        """
        # Validate input
        is_valid, error_msg = self._validate_input(text)
        if not is_valid:
            return {
                "success": False,
                "error": error_msg,
                "summary": None,
                "stats": None
            }
        
        try:
            # Count input tokens
            input_tokens = self.tracker.count_tokens(text, self.model)
            
            # Generate summary (simulated for demo - replace with actual API call)
            summary = self._generate_summary(text, summary_length)
            
            # Count output tokens
            output_tokens = self.tracker.count_tokens(summary, self.model)
            
            # Log usage
            self.tracker.log_usage(input_tokens, output_tokens)
            
            return {
                "success": True,
                "summary": summary,
                "stats": self.tracker.get_session_stats(),
                "error": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Summarization failed: {str(e)}",
                "summary": None,
                "stats": self.tracker.get_session_stats()
            }
    
    def _generate_summary(self, text: str, length: str) -> str:
        """
        Generate summary using OpenAI API or fallback method.
        This is a simulated version - replace with actual API call in production.
        """
        # Simulated summary generation (replace with actual OpenAI API call)
        # For demo purposes, we'll create a simple extractive summary
        
        sentences = text.split('. ')
        num_sentences = {
            "short": 3,
            "medium": 5,
            "long": 8
        }.get(length, 5)
        
        # Take first and last sentences for a basic summary
        if len(sentences) <= num_sentences:
            summary = '. '.join(sentences)
        else:
            first_half = sentences[:num_sentences//2]
            last_half = sentences[-(num_sentences//2):]
            summary = '. '.join(first_half + last_half)
        
        return summary[:2000]  # Limit summary length
    
    def batch_summarize(self, texts: List[str], summary_length: str = "medium") -> List[Dict]:
        """
        Summarize multiple texts in batch.
        
        Args:
            texts: List of meeting notes texts
            summary_length: 'short', 'medium', or 'long'
        
        Returns:
            List of result dicts
        """
        results = []
        for i, text in enumerate(texts):
            result = self.summarize(text, summary_length)
            result["index"] = i
            results.append(result)
        
        return results


def test_summarizer():
    """Test the summarizer with sample data."""
    sample_text = """
    Meeting Notes - Weekly Team Sync
    Date: January 15, 2024
    Attendees: John, Sarah, Mike, Emily
    
    1. Project Status Update
    - The frontend development is 80% complete
    - Backend API integration is in progress
    - Testing phase will begin next week
    
    2. Budget Discussion
    - Current budget allocation: $50,000
    - Additional funding requested for Q2
    - Need approval by end of month
    
    3. Action Items
    - John to complete API documentation by Friday
    - Sarah to prepare presentation for stakeholders
    - Mike to coordinate with QA team
    
    4. Next Meeting
    - Scheduled for January 22, 2024
    - Agenda: Final review before launch
    """
    
    summarizer = MeetingSummarizer()
    result = summarizer.summarize(sample_text, "medium")
    
    print("Summary Result:")
    print(f"Success: {result['success']}")
    print(f"Summary: {result['summary']}")
    print(f"Stats: {result['stats']}")


if __name__ == "__main__":
    test_summarizer()
