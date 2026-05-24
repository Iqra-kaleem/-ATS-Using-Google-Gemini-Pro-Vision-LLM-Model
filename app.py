from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert PDF to images
        images= pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
        {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode() # encode to base64
        }
        ]

        return pdf_parts
    else:
      raise FileNotFoundError("No file uploaded")
    
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
           response= get_gemini_response(input_prompt1, pdf_content,input_text)
           st.subheader("The Response is ")
           st.write(response)
       else:
           st.write("Please upload a PDF file to proceed.")   

    elif submit3:
        if uploaded_file is not None:
           pdf_content=input_pdf_setup(uploaded_file)
           response= get_gemini_response(input_prompt3, pdf_content,input_text)
           st.subheader("The Response is ")
           st.write(response)
        else:
           st.write("Please upload a PDF file to proceed.")          
           
