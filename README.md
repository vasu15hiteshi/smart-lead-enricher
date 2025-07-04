# Smart Lead Enricher

Smart Lead Enricher is a Streamlit web application that enriches and scores company leads from a CSV file. It uses APIs (Clearbit, Hunter.io) and web scraping to gather company data, then applies customizable scoring based on tech stack, employee count, email/social/blog presence, and keywords.

## Features
- **User Authentication** (with guest access)
- **CSV Upload** (expects columns: `company`, `website`)
- **Automated Enrichment** using:
  - Clearbit API (company info)
  - Hunter.io API (email discovery)
  - Web scraping (emails, social, blog links)
- **Customizable Scoring** with sidebar weights and filters
- **Downloadable Results** as CSV

## Setup Instructions

### 1. Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd smart-lead-enricher
   ```
2. **(Optional) Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set API keys as environment variables:**
   - `CLEARBIT_API_KEY`
   - `HUNTER_API_KEY`
   
   Example (Linux/macOS):
   ```bash
   export CLEARBIT_API_KEY=your_clearbit_key
   export HUNTER_API_KEY=your_hunter_key
   ```
   On Windows (CMD):
   ```cmd
   set CLEARBIT_API_KEY=your_clearbit_key
   set HUNTER_API_KEY=your_hunter_key
   ```
5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

### 2. Streamlit Cloud Deployment
- Ensure your `requirements.txt` is up to date.
- Add your API keys as [secrets in Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management):
  - `CLEARBIT_API_KEY`
  - `HUNTER_API_KEY`
- Push your code to your connected repository. Streamlit Cloud will auto-install dependencies and run the app.

## Usage
1. Open the app in your browser (local or Streamlit Cloud link).
2. Log in, sign up, or continue as guest.
3. Upload a CSV file with `company` and `website` columns.
4. Adjust scoring weights and filters in the sidebar.
5. View enriched and scored leads, and download results as CSV.

## File Structure
- `app.py` - Main Streamlit app
- `auth.py` - Authentication logic
- `scorer.py` - Enrichment and scoring logic
- `scraper.py` - Web scraping utilities
- `requirements.txt` - Python dependencies
- `config/credentials.yaml` - User credentials (auto-generated)
- `data/` - Sample or user-uploaded data

## Contact
For questions or support, contact: [hiteshivasu@gmail.com] 