import streamlit as st
from google.oauth2 import id_token
from google.auth.transport import requests
import google_auth_oauthlib.flow

# Load secrets
CLIENT_ID = st.secrets["google"]["client_id"]
CLIENT_SECRET = st.secrets["google"]["client_secret"]
REDIRECT_URI = st.secrets["google"]["redirect_uri"]

# Function to create Google OAuth Flow
def get_google_auth_flow():
    return google_auth_oauthlib.flow.Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
        redirect_uri=REDIRECT_URI,
    )

# Custom CSS for Styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #FF8A00, #E52E71);
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            color: white;
        }
        .subtitle {
            text-align: center;
            font-size: 1.5em;
            color: white;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 20px;
        }
        .button {
            display: flex;
            align-items: center;
            gap: 10px;
            background: #4285F4;
            color: white;
            font-size: 18px;
            padding: 12px 25px;
            border-radius: 30px;
            text-decoration: none;
            transition: 0.3s;
            box-shadow: 0px 5px 10px rgba(0,0,0,0.2);
        }
        .button:hover {
            background: #2C6FDB;
            box-shadow: 0px 8px 15px rgba(0,0,0,0.3);
        }
        .button img {
            width: 20px;
        }
        .signup-btn {
            background: #34A853;
            margin-top: 10px;
        }
        .signup-btn:hover {
            background: #2B8A3E;
        }
        .logout-btn {
            background: #FF4B2B;
            margin-top: 15px;
        }
        .logout-btn:hover {
            background: #E14020;
        }
        .user-info {
            text-align: center;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- UI Content ---
st.markdown("<h1 class='title'>🍽️ Food Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subtitle'>🔐 Secure Login with Google</h3>", unsafe_allow_html=True)

auth_url = (
    f"https://accounts.google.com/o/oauth2/auth?"
    f"client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    f"&scope=openid%20email%20profile"
)

# Google Login Button
st.markdown(
    f"""
    <div class="container">
        <a href="{auth_url}" class="button">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png">
            Login with Google
        </a>
        <a href="https://accounts.google.com/signup" class="button signup-btn">Sign Up</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Handle Google OAuth Response
query_params = st.experimental_get_query_params()

if "code" in query_params and "user_email" not in st.session_state:
    flow = get_google_auth_flow()
    flow.fetch_token(code=query_params["code"][0])
    
    credentials = flow.credentials
    id_info = id_token.verify_oauth2_token(credentials.id_token, requests.Request(), CLIENT_ID)

    st.session_state["user_email"] = id_info["email"]
    st.session_state["user_name"] = id_info.get("name", "User")
    st.session_state["user_picture"] = id_info.get("picture", "")

# --- Show Welcome Message for Logged-In Users ---
if "user_email" in st.session_state:
    st.markdown(f"<h3 class='user-info'>✅ Welcome, {st.session_state['user_name']}!</h3>", unsafe_allow_html=True)
    st.image(st.session_state["user_picture"], width=100)
    st.markdown(f"<h4 class='user-info'>📧 Email: {st.session_state['user_email']}</h4>", unsafe_allow_html=True)

    # Logout Button
    st.markdown(
        """
        <div class="container">
            <a href="#" class="button logout-btn">Logout</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_set_query_params()
        st.success("You have been logged out. Please refresh the page.")
        st.stop()