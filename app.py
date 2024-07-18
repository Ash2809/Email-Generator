from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st
import smtplib, ssl
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(google_api_key = GOOGLE_API_KEY,model = "gemini-pro",temperature = 0.5)

template = """You are an expert in writing an email.
You have to write a grammatically correct email on "{subject}" and 
write this in a {tone} way in {words} words.receipient name is{rec_name},Sender name is {sen_name}"""

prompt = PromptTemplate(template = template,input_variables=["reciepient","tone","words","subject","rec_name","sen_name"])

st.set_page_config(page_title="EMAIL GENERATION",
                   layout="centered",
                   initial_sidebar_state="collapsed")

subject  = st.text_input("Write the Subject")
tone = st.selectbox("What should be the tone of E-Mail?",
                    ("Professional", "Apologetic", "Simple","enthusiastic","confident"))

st.write("You selected: ",tone)

words = st.slider("Select no of Words", 0, 500)
rec_name = st.text_input("Enter Reciepient name")
sen_name = st.text_input("Enter sender name")

prompt = prompt.format(subject = subject,
              tone = tone,
              words = words,
              rec_name = rec_name,
              sen_name = sen_name)


submit = st.button("SUBMIT")

if submit:
    response = llm.invoke(prompt).content
    st.write(response)

# send = st.button("Click if want to mail this")
# if send:
    load_dotenv()
    smtp_server = "smtp.gmail.com"
    port = 587 
    sender_email = st.text_input("Enter Your EMAIL ID")
    password =  os.getenv("APP_PASS") # First turn on 2 step Verfication & Use the app-specific password here

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context) 
        server.login(sender_email, password)
        
        # TODO: Send email here
        recipient_email = st.text_input("Enter receipients EMAIL ID")
        subject = subject
        body = response

        message = f"Subject: {subject}\n\n{body}"
        
        server.sendmail(sender_email, recipient_email, message)
        st.balloons()
        st.write("Email sent successfully")

    except Exception as e:
        st.write(e)
    finally:
        server.quit()
