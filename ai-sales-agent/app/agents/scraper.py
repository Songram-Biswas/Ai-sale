# import requests
# from bs4 import BeautifulSoup
# import logging
# from app.config import Config

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class DataCollectionAgent:
#     def __init__(self):
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#         }

#     def scrape(self, url: str):
#         try:
#             logger.info(f"Starting scrape for: {url}")
#             response = requests.get(url, headers=self.headers, timeout=15)
#             response.raise_for_status()
            
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             for script in soup(["script", "style"]):
#                 script.decompose()

#             title = soup.title.string if soup.title else ""
#             meta_desc = ""
#             description_tag = soup.find("meta", attrs={"name": "description"})
#             if description_tag:
#                 meta_desc = description_tag.get("content", "")

#             body_content = soup.get_text(separator=' ')
            
#             return {
#                 "url": url,
#                 "title": title.strip() if title else "No Title",
#                 "description": meta_desc.strip(),
#                 "content": body_content
#             }
            
#         except Exception as e:
#             logger.error(f"Scraping failed for {url}: {str(e)}")
#             return {
#                 "url": url,
#                 "title": "Error",
#                 "description": "",
#                 "content": f"Failed to retrieve data: {str(e)}"
#             }
import requests
from bs4 import BeautifulSoup

class DataCollectionAgent:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def scrape(self, url: str):
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.title.string if soup.title else "No Title"
            # অপ্রয়োজনীয় ট্যাগ বাদ দাও
            for s in soup(['script', 'style', 'nav', 'footer']):
                s.decompose()
                
            return {
                "url": url,
                "title": str(title),
                "description": "",
                "content": soup.get_text()[:4000] # প্রথম ৪০০০ ক্যারেক্টার
            }
        except Exception as e:
            return {"title": "Error", "content": str(e)}            