import re

class DataProcessor:
    def __init__(self):
        self.industry_keywords = {
            "SaaS": ["software", "platform", "subscription", "cloud", "api"],
            "E-commerce": ["shop", "store", "buy", "cart", "product", "shipping"],
            "Fintech": ["bank", "payment", "finance", "crypto", "investment"],
            "Healthcare": ["medical", "health", "patient", "clinic", "doctor"]
        }

    def clean_text(self, text: str, max_chars: int = 4000):
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text[:max_chars]

    def detect_industry(self, text: str):
        text_lower = text.lower()
        for industry, keywords in self.industry_keywords.items():
            if any(word in text_lower for word in keywords):
                return industry
        return "General Business"

    def process(self, raw_data: dict):
        cleaned_content = self.clean_text(raw_data["content"])
        industry = self.detect_industry(cleaned_content)
        
        return {
            "url": raw_data["url"],
            "title": raw_data["title"],
            "description": raw_data["description"],
            "cleaned_content": cleaned_content,
            "industry_guess": industry
        }