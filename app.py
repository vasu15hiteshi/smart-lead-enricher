# app.py
# -------------------------------------------------------------------
import streamlit as st
import pandas as pd

from auth      import init_auth
from scraper   import get_basic_info      # your scraper
from scorer    import score, enrich_company      # weighted scorer and real enrichment

# ---------- AUTH INITIALISATION ------------------------------------
authenticator, _, _ = init_auth()

# ---------- SIMPLE LANDING CHOICE ----------------------------------
choice = st.radio("Welcome!", ["Login", "Sign Up", "Continue as guest"])

# Default: do NOT show the app until permitted
go_ahead = False

if choice == "Login":
    # New API ➜ just call; results live in st.session_state
    authenticator.login("main")           # location first
    if st.session_state.get("authentication_status"):
        st.success(f"Welcome back, {st.session_state.get('name')}!")
        go_ahead = True
    elif st.session_state.get("authentication_status") is False:
        st.error("Username / password is incorrect")
    else:
        st.info("Enter your credentials and press **Login**")

elif choice == "Sign Up":
    try:
        if authenticator.register_user("main", preauthorization=False):
            st.success("✅ Registered! Please choose *Login* to sign in.")
    except Exception as e:
        st.error(e)
    st.stop()                             # halt here after registration

else:  # Continue as guest
    st.session_state["authentication_status"] = True
    st.session_state["name"] = "Guest"
    go_ahead = True

# Optional logout button (only when logged in)
if st.session_state.get("authentication_status"):
    authenticator.logout("sidebar")

# ---------- MAIN APP BODY ------------------------------------------
def run_app_body():
    st.title("Smart Lead Enricher & Scorer")
    st.write("Upload a CSV with columns: company, website")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    # ---------- SIDEBAR FILTERS ----------
    with st.sidebar:
        st.header("Scoring Weights & Filters")

        w_tech = st.slider("Tech Stack Weight", 0, 10, 3)
        w_size = st.slider("Employee Count Weight", 0, 10, 2)
        w_email = st.slider("Email Found Weight", 0, 10, 2)
        w_social = st.slider("Social/Blog Presence Weight", 0, 10, 1)
        w_keyword = st.slider("Keyword Match Weight", 0, 10, 2)

        min_emp = st.number_input("Min Employees", 0, 10000, 0)
        max_emp = st.number_input("Max Employees", 0, 10000, 10000)
        tech_filter = st.text_input("Tech Stack Filter (comma separated)").split(",")
        tech_filter = [t.strip() for t in tech_filter if t.strip()]

    # ---------- FILE UPLOAD & PROCESS ----------
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if not set(["company", "website"]).issubset(df.columns):
            st.error("CSV must have 'company' and 'website' columns.")
        else:
            enriched = [enrich_company(row.to_dict()) for _, row in df.iterrows()]
            for info in enriched:
                info["score"] = score(
                    info,
                    tech_filter, min_emp, max_emp,
                    w_tech, w_size, w_email, w_social, w_keyword
                )
            result_df = pd.DataFrame(enriched)
            result_df = result_df.sort_values("score", ascending=False)
            st.dataframe(result_df)
            st.download_button(
                label="Download Results as CSV",
                data=result_df.to_csv(index=False),
                file_name="scored_companies.csv",
                mime="text/csv"
            )

# ---------- RUN APP IF PERMITTED -----------------------------------
if go_ahead:
    run_app_body()

# --- Placeholder enrichment function ---
def enrich_company(row):
    # In real use, replace with actual enrichment logic/API calls
    return {
        "company": row["company"],
        "website": row["website"],
        "employees": 100,  # placeholder
        "techs": ["Python", "AWS"],  # placeholder
        "email_found": True,  # placeholder
        "has_blog": True,  # placeholder
        "has_social": False,  # placeholder
        "funding": "Seed",  # placeholder
        "title": "AI ecommerce analytics platform"  # placeholder
    }
