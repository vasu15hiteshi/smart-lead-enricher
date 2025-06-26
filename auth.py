import yaml, streamlit_authenticator as stauth
from pathlib import Path

def init_auth():
    # 1) Load or create credential store (YAML file)
    cred_file = Path("config/credentials.yaml")
    if not cred_file.exists():
        cred_file.parent.mkdir(exist_ok=True)
        cred_file.write_text("""
credentials:
  usernames:
    guest:
      email: guest@example.com
      name: Guest
      password: ""
""")
    with cred_file.open() as f:
        config = yaml.safe_load(f)

    authenticator = stauth.Authenticate(
        config['credentials'],
        "leadgen_cookie", "random_signature_key",
        cookie_expiry_days=1,
        preauthorized=["guest"]
    )
    return authenticator, config, cred_file