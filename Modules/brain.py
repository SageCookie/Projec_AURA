import json
import time
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from litellm import completion, exceptions
from utils.config import Config
from typing import Any

# --- 1. Schema Definition ---
class ArticleSchema(BaseModel):
    title: str
    url: str
    raw_content: str
    summary: str
    tech_score: int = Field(ge=1, le=10)
    category: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: Any):
        allowed = [
            "AI & Machine Learning", "Game Development (Unity/C#)", 
            "Web Engineering", "Cybersecurity & Reverse Engineering", 
            "Data Science & Scraping", "Other"
        ]
        if v not in allowed:
            return "Other"
        return v

# --- 2. The Brain Module ---
class TheBrain:
    def __init__(self):
        self.categories = [
            "AI & Machine Learning", "Game Development (Unity/C#)", 
            "Web Engineering", "Cybersecurity & Reverse Engineering", 
            "Data Science & Scraping", "Other"
        ]
        self.usage_file = "usage_log.json"

    def _check_rpd_limit(self):
        """Simple check for the 1.5k RPD limit."""
        try:
            with open(self.usage_file, "r") as f:
                data = json.load(f)
                today = datetime.now().strftime("%Y-%m-%d")
                return data.get(today, 0) >= 1450 # Safety buffer
        except FileNotFoundError:
            return False

    def _log_usage(self):
        today = datetime.now().strftime("%Y-%m-%d")
        data = {}
        try:
            with open(self.usage_file, "r") as f: data = json.load(f)
        except FileNotFoundError: pass
        data[today] = data.get(today, 0) + 1
        with open(self.usage_file, "w") as f: json.dump(data, f)

    def _get_system_prompt(self, is_complex: bool, is_local: bool):
        # Hardware specific 'Thinking' mode for high-tier local runs
        thinking_token = "<|think|>" if (is_complex and is_local) else ""
        
        return f"""{thinking_token}
        You are a technical data processor. Return ONLY a JSON object.
        Scoring Logic (tech_score):
        1-3: Press releases/Marketing fluff.
        4-7: Tutorials/Docs with code snippets.
        8-10: Research papers/Complex architecture/Deep-dives.

        Categories: {self.categories}
        Summary and insights must ALWAYS be in English.
        If content is not English, translate the summary to English.
        """

    def process_content(self, raw_markdown: str, url: str, force_local: bool = False) -> dict:
        # 1. Validation for Module 1 Failures
        if not raw_markdown or "[CRAWL_FAILED]" in raw_markdown[:50]:
            return {
                "title": "Crawl Failed", "url": url, "raw_content": raw_markdown,
                "summary": "Error: Source content unavailable from Module 1.",
                "tech_score": 1, "category": "Other", "timestamp": datetime.now().isoformat()
            }

        # 2. VRAM Safety: Recursive Chunking (Map-Reduce) if > 15k words
        words = raw_markdown.split()
        if len(words) > 15000:
            return self._map_reduce_summarize(raw_markdown, url)

        # 3. Model Selection & RPD Guard
        use_local = force_local or self._check_rpd_limit()
        model = Config.LOCAL_MODEL if use_local else Config.MODEL_31B
        api_key = None if use_local else Config.GEMMA_31B_KEY

        # 4. Complexity Detection (for <|think|> mode)
        is_complex = any(word in raw_markdown.lower() for word in ["research", "paper", "architecture", "kernel"])

        try:
            response = completion(
                model=model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(is_complex, use_local)},
                    {"role": "user", "content": f"Summarize this: {raw_markdown}"}
                ],
                api_key=api_key,
                response_format={ "type": "json_object" }, # Ensures JSON
                temperature=0.2
            )
            
            result_json = json.loads(response.choices[0].message.content)
            
            # 5. Final Pydantic Validation
            article = ArticleSchema(
                title=result_json.get("title", "Untitled"),
                url=url,
                raw_content=raw_markdown,
                summary=result_json.get("summary", ""),
                tech_score=result_json.get("tech_score", 1),
                category=result_json.get("category", "Other")
            )
            
            self._log_usage()
            return article.model_dump()

        except exceptions.RateLimitError:
            print("Rate limit hit. Exponential backoff recommended here.")
            time.sleep(10) # Simple backoff
            return self.process_content(raw_markdown, url, force_local=True)
        except Exception as e:
            return {"error": f"Brain processing failed: {str(e)}"}

    def _map_reduce_summarize(self, text: str, url: str) -> dict:
        # Placeholder output keeps the same shape as normal article payloads.
        return {
            "title": "Large Document (Map-Reduce Pending)",
            "url": url,
            "raw_content": text,
            "summary": "Large document Map-Reduce not yet fully implemented",
            "tech_score": 5,
            "category": "Other",
            "timestamp": datetime.now().isoformat(),
        }
    

if __name__ == "__main__":
    # 1. Initialize the Brain
    brain = TheBrain()
    
    # 2. Define a dummy article for testing
    test_content = """
    # Reinforcement Learning for Lunar Landing
    This project explores using PPO (Proximal Policy Optimization) to land a 
    lunar module in a 3D Unity environment. We focus on reward shaping and 
    sensor fusion to achieve a stable descent.
    """
    test_url = "https://example.com/lunar-rover-ai"

    print("--- Starting Brain Processing Test ---")
    
    # 3. Process the content
    # Note: This will attempt to call the Gemini API if your .env is set up!
    result = brain.process_content(test_content, test_url)

    # 4. Print the result in a readable format
    import json
    print(json.dumps(result, indent=4))
    
    print("--- Test Complete ---")