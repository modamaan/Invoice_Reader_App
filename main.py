# from dotenv import load_dotenv
# load_dotenv() ## for load all environments

# import streamlit as st
# import os
# from  PIL import Image
# import google.generativeai as genai

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ## as function to load Gemini pro vision

# model = genai.GenerativeModel("gemini-1.5-flash")

# def get_gemini_response(input,image,prompt):
#     response = model.generate_content([input,image[0],prompt])
#     # response = get_gemini_response(input, image_data, input)
#     return response.text

# def input_image_details(uploaded_file):
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()

#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# ## intialize our streamlit app

# st.set_page_config(page_title="MultiLanguage Invoice Extractor")
# st.header("Invoice Reader Application")
# input = st.text_input("Input Prompt: ",key="input")
# uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg","jpeg","png"])
# image = ""
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image", use_column_width=True)

# submit = st.button("Tell me about the invoice")

# input_prompt="""
# your an expert in understanding invoices. we will upload a image as invoice
# and you will have to answer any question based on the uploaded image
# """

# ## if submit button is clicked

# if submit:
#     if uploaded_file is not None:  # Check if an image is uploaded
#         image_data = input_image_details(uploaded_file)
#         response = get_gemini_response(input_prompt, image_data, input)
#         st.subheader("The Response is")
#         st.write(response)
#     else:
#         st.error("Please upload an Invoice image before submitting.")


import cv2
import pytesseract
import numpy as np
import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

# Initialize Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the Generative Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to extract text using OCR
def extract_text_from_image(image):
    # Convert the image to grayscale for better OCR performance
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(gray_image)
    # Get bounding boxes of text
    boxes = pytesseract.image_to_boxes(gray_image)
    extracted_text = []
    
    # Process each detected character's bounding box
    for box in boxes.splitlines():
        b = box.split()
        extracted_text.append({
            "char": b[0],
            "left": int(b[1]),
            "top": int(b[2]),
            "right": int(b[3]),
            "bottom": int(b[4]),
        })
    return extracted_text

# Function to highlight the text in the image
def highlight_text_in_image(image, extracted_text):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    for box in extracted_text:
        # Draw bounding boxes around detected text
        cv2.rectangle(img, (box['left'], box['top']), (box['right'], box['bottom']), (255, 0, 0), 2)
    
    # Convert back to PIL format and return
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Function to get a response from Gemini
def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to input image details
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI setup
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("Invoice Reader Application")

input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image = ""

# Show uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the invoice")

# Input prompt for AI model
input_prompt = """
You are an expert in understanding invoices. We will upload an image as an invoice,
and you will have to answer any question based on the uploaded image.
"""

# When the user clicks "Submit"
if submit:
    if uploaded_file is not None:  # Ensure an image is uploaded
        # Extract text from the uploaded image
        extracted_text = extract_text_from_image(image)

        # Highlight text in the image
        highlighted_image = highlight_text_in_image(image, extracted_text)
        st.image(highlighted_image, caption="Highlighted Text in Image")

        # Prepare image data for API call
        image_data = input_image_details(uploaded_file)
        
        # Get response from Gemini
        response = get_gemini_response(input_prompt, image_data, input)
        
        # Show the response
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.error("Please upload an Invoice image before submitting.")








