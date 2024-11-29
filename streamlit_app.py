import streamlit as st
from pptx import Presentation
from pptx.util import Inches
from pdf2image import convert_from_bytes
import io

# Set the page configuration
st.set_page_config(
    page_title='Conversão PDF para PPT - SERCOM',
    layout='wide',
    page_icon="https://media.licdn.com/dms/image/C4D0BAQHXylmAyGyD3A/company-logo_200_200/0/1630570245289?e=2147483647&v=beta&t=Dxas2us5gteu0P_9mdkQBwJEyg2aoc215Vrk2phu7Bs",
    initial_sidebar_state='auto'
)

# Function to convert PDF to PowerPoint with each page as an image
def convert_pdf_to_ppt_with_images(pdf_file):
    # Convert PDF pages to images
    images = convert_from_bytes(pdf_file.read())
    # Create a PowerPoint presentation
    presentation = Presentation()
    
    for image in images:
        # Add a blank slide
        slide = presentation.slides.add_slide(presentation.slide_layouts[5])  # Blank layout
        # Save the image to a BytesIO stream
        image_stream = io.BytesIO()
        image.save(image_stream, format='PNG')
        image_stream.seek(0)
        # Add the image to the slide
        slide.shapes.add_picture(image_stream, Inches(0), Inches(0), width=Inches(10), height=Inches(7.5))
    
    return presentation

# Streamlit app layout
st.title('Conversão de PDF para PPT')
pdf_file = st.file_uploader("Faça o upload do arquivo em formato PDF", type=['pdf'])

if pdf_file is not None:
    if st.button('Converter para PPT'):
        with st.spinner('Convertendo...'):
            try:
                # Convert PDF to PPT with images
                presentation = convert_pdf_to_ppt_with_images(pdf_file)
                # Save the presentation to a BytesIO stream
                ppt_io = io.BytesIO()
                presentation.save(ppt_io)
                ppt_io.seek(0)
                st.success("Conversão concluída 🥳")
                st.download_button(
                    label="Baixar PPT",
                    data=ppt_io,
                    file_name="converted_presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
            except Exception as e:
                st.error(f"Error during conversion: {e}")
