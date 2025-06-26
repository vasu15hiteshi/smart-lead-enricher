import requests
import os

CLEARBIT_API_KEY = os.getenv("CLEARBIT_API_KEY")  # Set in your Streamlit Cloud secrets
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")      # Set in your Streamlit Cloud secrets

def enrich_company(row):
    domain = row["website"].replace("https://", "").replace("http://", "").split("/")[0]
    info = {
        "company": row["company"],
        "website": row["website"],
        "employees": None,
        "techs": [],
        "email_found": False,
        "has_blog": False,
        "has_social": False,
        "funding": None,
        "title": "",
    }

    # --- Clearbit Enrichment ---
    try:
        resp = requests.get(
            f"https://company.clearbit.com/v2/companies/find?domain={domain}",
            auth=(CLEARBIT_API_KEY, '')
        )
        if resp.status_code == 200:
            data = resp.json()
            info["employees"] = data.get("metrics", {}).get("employees")
            info["title"] = data.get("description", "")
            info["techs"] = data.get("tech", [])
            info["has_blog"] = bool(data.get("blog"))
            info["has_social"] = bool(data.get("facebook") or data.get("twitter") or data.get("linkedin"))
            info["funding"] = data.get("metrics", {}).get("raised")
    except Exception as e:
        pass  # Handle/log errors as needed

    # --- Hunter.io Email Finder ---
    try:
        resp = requests.get(
            f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}"
        )
        if resp.status_code == 200:
            data = resp.json()
            info["email_found"] = len(data.get("data", {}).get("emails", [])) > 0
    except Exception as e:
        pass

    return info

def score(info,
          tech_filter, min_emp, max_emp,
          w_tech, w_size, w_email, w_social, w_keyword):
    score = 0

    # --- Tech‑stack filter (hard gate) ---
    if tech_filter:                                  # user picked at least one tool
        if not any(t.lower() in [x.lower() for x in info["techs"]] for t in tech_filter):
            return 0                                # disqualify if no desired tech

    # --- Scoring starts here -------------
    title = info.get("title", "").lower()
    for kw in ["ai", "ecommerce", "analytics"]:
        if kw in title:
            score += w_keyword

    for tech in info.get("techs", []):
        if tech.lower() in [t.lower() for t in tech_filter]:
            score += w_tech

    if info.get("email_found"):
        score += w_email
    if info.get("has_blog") or info.get("has_social"):
        score += w_social

    size = info.get("employees") or 0
    if min_emp <= size <= max_emp:
        score += w_size

    return score