import streamlit as st  # type:ignore
import numpy_financial as npf  # type:ignore
import base64
import speech_recognition as sr
import re
from word2number import w2n

def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def recognize_speech_and_set(key):
    spoken = recognize_speech()
    if key in ["p", "r", "t"]:
        try:
            st.session_state[key] = float(spoken)
        except:
            st.warning("Please speak a valid number.")
    else:
        st.session_state[key] = spoken

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak now.")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except Exception as e:
        st.error(f"Could not recognize speech: {e}")
        return ""

set_bg("Buddy.png")
# Centered, extra large, bold, and stylish title using a Google Fonts import for a modern look
st.markdown('''
<link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
<h1 style="text-align:center; color:black; font-size: 4.5rem; font-weight: bold; font-family: 'Pacifico', cursive; letter-spacing: 0.08em; margin-bottom: 0.5em;">Finance Buddy</h1>
''', unsafe_allow_html=True)

# Use columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # Name input and output in main column
    st.markdown('<div style="font-size:1.3rem; font-weight:bold; margin-bottom:0.2em; color:black;">Enter Your Name</div>', unsafe_allow_html=True)
    name = st.text_input("", value=st.session_state.get("name", ""), key="name")
    st.button("Speak Name", on_click=recognize_speech_and_set, args=("name",))
    if st.session_state.get("name", ""):
        st.write(f"Hello , {st.session_state['name']}!Welcome to My Web Server.")
    # Principal input
    st.markdown('<div style="font-size:1.3rem; font-weight:bold; margin-bottom:0.2em; color:black;">Principal Amount</div>', unsafe_allow_html=True)
    def set_principal():
        spoken = recognize_speech()
        try:
            st.session_state["p"] = float(spoken)
        except:
            st.warning("Please speak a valid number.")
    p = st.number_input("", value=st.session_state.get("p", 0.0), key="p")
    st.button("Speak Principal Amount", on_click=set_principal)
    if st.session_state.get("p", 0.0):
        st.write(f"Your ,Principal amount is ₹ {st.session_state['p']}.")
    # Rate input
    st.markdown('<div style="font-size:1.3rem; font-weight:bold; margin-bottom:0.2em; color:black;">Rate of Interest</div>', unsafe_allow_html=True)
    def set_rate():
        spoken = recognize_speech()
        try:
            st.session_state["r"] = float(spoken)
        except:
            st.warning("Please speak a valid number.")
    r = st.number_input("", value=st.session_state.get("r", 0.0), key="r")
    st.button("Speak Rate of Interest", on_click=set_rate)
    if st.session_state.get("r", 0.0):
        st.write(f"Your , Rate of Interest is this {st.session_state['r']}%.")
    # Tenure input
    st.markdown('<div style="font-size:1.3rem; font-weight:bold; margin-bottom:0.2em; color:black;">Tenure of Loan</div>', unsafe_allow_html=True)
    def set_tenure():
        spoken = recognize_speech()
        # Try to extract a number from the spoken text (handle words like 'ten', 'twenty', etc.)
        try:
            # Try direct conversion first
            st.session_state["t"] = float(spoken)
        except:
            # Try to extract digits from spoken text
            numbers = re.findall(r"\d+\.?\d*", spoken)
            if numbers:
                st.session_state["t"] = float(numbers[0])
            else:
                # Try to convert number words to digits (e.g., 'ten' -> 10)
                try:
                    st.session_state["t"] = float(w2n.word_to_num(spoken))
                except:
                    st.warning("Please speak a valid number.")
    t = st.number_input("", value=st.session_state.get("t", 0.0), key="t")
    st.button("Speak Tenure", on_click=set_tenure)
    if st.session_state.get("t", 0.0):
        st.write(f"Tenure of Your Loan Amount(in Years) is {st.session_state['t']} years.")
    if st.button("Calculate"):
        st.subheader("Results")
        st.title("Simple Interest")
        # Simple Interest
        SI = st.session_state.get("p", 0.0) * st.session_state.get("r", 0.0) * st.session_state.get("t", 0.0) / 100
        st.write(f"Simple Interest is:{SI}")
        # Compound Interest
        st.title("Compound Interest")
        CI = st.session_state.get("p", 0.0) * ((1 + st.session_state.get("r", 0.0) / 100) ** st.session_state.get("t", 0.0)) - st.session_state.get("p", 0.0)
        st.write(f"Compound Interest is:{CI}")
        # EMI
        st.title("EMI")
        monthly_rate = st.session_state.get("r", 0.0) / (12 * 100)
        months = int(st.session_state.get("t", 0.0) * 12)
        EMI = npf.pmt(monthly_rate, months, -st.session_state.get("p", 0.0))
        st.write(f"Monthly EMI:₹{EMI}")

with col2:
    st.write("")  # Empty or for future use





    