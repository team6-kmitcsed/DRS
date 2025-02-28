import streamlit as st
import openai  
st.set_page_config(page_title="🩺 Health Advice Chatbot", layout="centered")
st.markdown(
    """
    <style>
        .stTextArea textarea { font-size: 16px; }
        .stButton button { background-color: #4CAF50; color: white; font-size: 16px; padding: 10px 20px; }
        .stSelectbox div { font-size: 16px; }
        .stSlider div { font-size: 16px; }
        .response-box {
            border-left: 5px solid #4CAF50;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            line-height: 1.6;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🩺 Health Advice Chatbot")
st.markdown("### 🤖 Your AI Health Consultant")
st.info("Get preliminary health advice based on your queries. **Note:** This is not a substitute for professional medical advice.")

# Fetch API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Query type selection
query_type = st.selectbox("📌 **Select Query Type**", 
                          ["Symptom Checker", "Preventive Measures", "General Health Advice", "Medical Terms", "First Aid"])

# User input with character limit
user_input = st.text_area("✍️ **Enter your query here:**", max_chars=300, help="Keep your query brief (max 300 characters).")

# Token limit selection
max_tokens = st.slider("🔢 **Max Response Length (Tokens)**", min_value=50, max_value=300, value=150)

# Submit button
if st.button("🚀 **Get Advice**"):
    if not user_input:
        st.warning("⚠️ **Please enter a query before submitting.**")
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

        # OpenAI API client
        client = openai.OpenAI(api_key=api_key)

        # Display loading indicator
        with st.spinner("⏳ **Fetching response...**"):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a highly knowledgeable and empathetic health assistant dedicated to providing accurate, reliable, and easy-to-understand health and diet advice. Your primary role is to assist users with health-related inquiries, including symptoms, preventive care, nutrition, fitness, mental well-being, and first aid.When answering, carefully analyze the user’s query, ensuring that you fully understand their concern before responding. Provide clear, concise, and practical advice that is easy for anyone to comprehend, regardless of their medical knowledge. If necessary, offer step-by-step guidance, helpful precautions, and actionable tips to ensure users can apply the information effectively in real life.You must strictly limit your responses to health and diet-related topics. If a user asks a question unrelated to health, wellness, or nutrition, politely inform them that you are only trained to provide health-related advice and cannot assist with other topics.Ensure that all information you provide is based on well-established medical knowledge and best practices. However, always include a disclaimer that your advice should not replace professional medical consultation, diagnosis, or treatment. Encourage users to seek a healthcare professional when necessary.Your goal is to be a friendly, trustworthy, and helpful health assistant that empowers users to make informed decisions about their well-being."},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=max_tokens
                )

                # Extract response
                advice = response.choices[0].message.content.strip()

                # Display response in a better format
                st.success("✅ **Response Received**")
                st.markdown(f'<div class="response-box">{advice}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ **Unexpected Error:** {e}")
