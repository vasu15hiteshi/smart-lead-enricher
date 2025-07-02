import requests
from bs4 import BeautifulSoup
import re

def get_basic_info(website_url):
    info = {
        "email_found": False,
        "emails": [],
        "has_blog": False,
        "has_social": False,
        "social_links": [],
        "blog_links": [],
    }
    try:
        resp = requests.get(website_url, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # --- Find emails ---
            emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", resp.text))
            info["emails"] = list(emails)
            info["email_found"] = len(emails) > 0

            # --- Find social links ---
            social_domains = ["twitter.com", "facebook.com", "linkedin.com", "instagram.com", "youtube.com"]
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if any(domain in href for domain in social_domains):
                    info["has_social"] = True
                    info["social_links"].append(href)
                if "blog" in href.lower():
                    info["has_blog"] = True
                    info["blog_links"].append(href)
    except Exception as e:
        print(f"Scraper get_basic_info error: {e}")
    return info
