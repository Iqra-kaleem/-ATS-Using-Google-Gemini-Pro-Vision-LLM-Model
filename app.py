from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from groq import Groq
from PIL import Image
import pdf2image
import fitz  # PyMuPDF

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_groq_response(input,pdf_content,prompt):
    final_prompt = f"""
    Job Description
    {input}
    
    Resume
    {pdf_content}

    {prompt}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )

    return chat_completion.choices[0].message.content

def input_pdf_setup(uploaded_file):
     text = ""

     pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

     for page in pdf:
        text += str(page.get_text())

     return text
    
## Streamlit app 
st.set_page_config(page_title="ATS Resume Expert") 
st.header("ATS Tracking ")  
input_text=st.text_area("Job Description: ", key="input")
uploaded_file=st.file_uploader("Upload your resume in (Pdf)", type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

    submit1 = st.button("Tell Me About the Resume")
    submit2 = st.button("How Can I Improve my skills")
    submit3 = st.button("Percentage Match")

    input_prompt1 = """
    You are an experienced HR  with Tech Experinece in the field of any one job role from Data Science, Full Stack
    web developement, Big Data, DEVOPS , AI engineering, your task is to review
    the provided resume against the job description for these profiles.
    Please share your strengths and weakness of the applicant in relation 
    to the specifiedjob description, Highlight the strengths and weaknesses of the applicant
    to the specified job description, and provide actionable feedback on how to improve the
    resume to better align with the job requirements.
    """

    input_prompt2 = """
    You are an experienced career coach and technical mentor with expertise in roles such as 
    Data Science, Full Stack Development, Web Development, Big Data, DevOps, and AI Engineering.

    Your task is to analyze the provided resume and job description, then identify the skills 
    the candidate is currently lacking or needs to improve for the target role.

    Provide:
    1. A list of important missing technical skills.
    2. A list of missing soft skills or professional skills.
    3. Recommended tools, technologies, frameworks, or concepts to learn.
    4. A step-by-step improvement roadmap for the candidate.
    5. Suggested projects or certifications that can strengthen the profile.
    6. Interview preparation tips relevant to the job role.
    7. Final career advice to improve the chances of getting selected.

    Keep the response clear, structured, practical, and beginner-friendly.
    """

    input_prompt3 = """
    You are an skilled ATS(Applicant Tracking System) scanner with a deep understanding of any one job role from
    Data Science, Full Stack ,web developement, Big Data, DEVOPS , AI engineering and deep ATS functionality
    your task is to evaluate the resume against the job description, give me the percentage of match if the 
    resume matches the job description . First the output should come as percentage
    and then keywords missing and last final thought.
    """

    if submit1:
       if uploaded_file is not None:
           pdf_content=input_pdf_setup(uploaded_file)
           response= get_groq_response(input_prompt1, pdf_content,input_text)
           st.subheader("The Response is ")
           st.write(response)
       else:
           st.write("Please upload a PDF file to proceed.") 

    elif submit2:
        if uploaded_file is not None:
           pdf_content=input_pdf_setup(uploaded_file)
           response= get_groq_response(input_prompt2, pdf_content,input_text)
           st.subheader("The Response is ")
           st.write(response)
        else:
           st.write("Please upload a PDF file to proceed.")         

    elif submit3:
        if uploaded_file is not None:
           pdf_content=input_pdf_setup(uploaded_file)
           response= get_groq_response(input_prompt3, pdf_content,input_text)
           st.subheader("The Response is ")
           st.write(response)
        else:
           st.write("Please upload a PDF file to proceed.")          
           
