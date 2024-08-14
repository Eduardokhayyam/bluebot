import os
import sympy as sp
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as ggi

load_dotenv(".venv")

#function to perform calculations
def calculate(expression):
    try:
        result = sp.sympify(expression)
        return result
    except sp.SympifyError:
        return "Rephrase the question to be clearer and concise."
    
#Function to processe user input
def process_user_input(user_input):
     """
    Processes the user's input and attempts to evaluate it as a mathematical expression.

    Args:
        user_input (str): The user's input.

    Returns:
        str or sympy.Expr: The result of the evaluation, or a message indicating that the question should be rephrased.
    """
     expression = user_input.strip()
     result = calculate(expression)
     return result

# Function to display the feedback form
def display_feedback_form():
    """
    Displays a feedback form that allows users to provide feedback on the accuracy of the responses.
    """
    st.header("Feedback Form")
    st.write("Please take a moment to provide feedback on the accuracy of the response you received.")
    with st.form("feedback_form"):
        st.text_input("Question:", key="question")
        st.text_input("Response:", key="response")
        st.selectbox("Rating:", options=["Very Accurate", "Somewhat Accurate", "Inaccurate"], key="rating")
        st.text_area("Comment:", key="comment")
        st.form_submit_button("Submit")

# Function to collect and store feedback
def collect_feedback(feedback):
    """
    Collects and stores feedback from the user.

    Args:
        feedback (dict): A dictionary containing the user's feedback.
    """
    # Store the feedback in a database or spreadsheet
    pass

# Function to update the model
def update_model(feedback):
    """
    Updates the model based on the feedback provided by the user.

    Args:
        feedback (dict): A dictionary containing the user's feedback.
    """
    # Fine-tune the model on the feedback data or incorporate the feedback into the training process
    pass

#Configure page layout
st.set_page_config(
    page_title= "Chat with Bluebot a Gemini-Pro language model!",
    page_icon=":robot_face:",
    layout= "centered",
    initial_sidebar_state= "auto"
)
#Displaying the chatbot's tittle on the page
st.title(" 🔷 Chat with me, I'll answer your questions!")


google_api_key = os.getenv("google_api_key")

#Set up Google Gemini-Pro Model
ggi.configure(api_key = google_api_key)
model = ggi.GenerativeModel('gemini-pro')

#Function to translate roles between Geimini_Pro and Streamlit
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    
#start chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

#Displaying the chat history for when user input a new message
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)


#Function to obtain calculations from Gemini
def obtain_answer(prompt):
    response = ggi.generate_text(
        prompt=prompt,
        max_output_tokens= 150,
        temperature= 0.7
    )
    return response['text']

#chatbot interface
def chatbot():
    print("Welcome to Bluebot!")
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["quit", "exit"]:
            print("Bluebot: Until later!")
            break
        if "calculate" in user_message.lower():
            expression = user_message.split("calculate")[-1].strip()
            answer = calculate(expression)
        else:
            answer = obtain_answer(user_message)
            print("Funbot: {}".format(answer))

#input field for user's message
user_prompt = st.chat_input("Ask Bluebot (Phrase the question to be clear and concise)...")
if user_prompt:
    #add user's message to chat an display
    st.chat_message("user").markdown(user_prompt)

    #Send user's message to Gmini-Pro and get response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    #Display Gemini response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)