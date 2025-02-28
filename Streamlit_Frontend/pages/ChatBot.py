import streamlit as st
import openai  # OpenAI's official library

if "user_email" not in st.session_state:
    st.warning("🔐 Please log in to access this page.")
    st.stop()

# Streamlit UI Configuration
st.set_page_config(page_title="Health Advice Chatbot", layout="centered")
st.title("🩺 Health Advice Chatbot")
st.write("Get preliminary health advice based on your queries. **Note:** This is not a substitute for professional medical advice.")

# Fetch API key (Stored in st.secrets or entered manually)
api_key = st.secrets.get("OPENAI_API_KEY", "")
api_key = st.text_input("🔑 Enter OpenAI API Key", type="password", value=api_key)

# Query type selection
query_type = st.selectbox("📌 Select Query Type", ["Symptom Checker", "Preventive Measures", "General Health Advice", "Medical Terms", "First Aid"])

# User input with character limit
user_input = st.text_area("✍️ Enter your query here:", max_chars=300, help="Keep your query brief (max 300 characters).")

# Token limit selection
max_tokens = st.slider("🔢 Max Response Length (Tokens)", min_value=50, max_value=300, value=150)

if st.button("🚀 Get Advice"):
    if not user_input:
        st.warning("⚠️ Please enter a query before submitting.")
    elif not api_key:
        st.warning("⚠️ Please enter a valid OpenAI API key.")
    else:
        # Generate appropriate prompt based on query type
        query_mapping = {
            "Symptom Checker": f"User has described the following symptoms: {user_input}. What could be the potential conditions?",
            "Preventive Measures": f"Provide preventive measures for: {user_input}.",
            "General Health Advice": f"Give general health advice on the topic: {user_input}.",
            "Medical Terms": f"Explain the following medical term: {user_input}.",
            "First Aid": f"Provide first aid tips for: {user_input}."
        }
        user_message = query_mapping[query_type]

        # Set OpenAI API key
        openai.api_key = api_key

        # Display loading indicator
        with st.spinner("Fetching response..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant providing health advice."},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=max_tokens
                )

                # Extract and display the response
                advice = response['choices'][0]['message']['content'].strip()

                st.success("✅ Response Received:")
                st.write(advice)

            except openai.error.OpenAIError as e:
                st.error(f"❌ OpenAI API Error: {e}")
            except Exception as e:
                st.error(f"⚠️ Unexpected Error: {e}")

        #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