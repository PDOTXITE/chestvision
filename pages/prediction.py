import streamlit as st
from torchvision import models
import torch
import torch.nn as nn
from torchvision.transforms import transforms
from PIL import Image
import numpy as np
from fpdf import FPDF
import base64
import os

# List of classes
all_classes = ["Cardiomegaly", "Hernia", "Infiltration", "Nodule", "Emphysema", "Effusion", "Atelectasis",
               "Pleural_Thickening", "Pneumothorax", "Mass", "Fibrosis", "Consolidation",
               "Edema", "Pneumonia"]

sample_images = {
    "None": "../",
    "sample1": "sample/sample1.png",
    "sample2": "sample/sample2.png",
    "sample3": "sample/sample3.png"
}

@st.cache_resource
def load_model():
    try:
        # Load the state dictionary separately
        state_dict = torch.load('models/densenet121v001model.pth', map_location=torch.device('cpu'))
        
        # Create the DenseNet121 model
        model = models.densenet121(pretrained=False)
        num_features = model.classifier.in_features
        model.classifier = nn.Linear(num_features, len(all_classes))
        
        # Load the state dictionary into the model
        model.load_state_dict(state_dict)
        model.eval()
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def preprocess_image(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def predict_image(image, model):
    with torch.no_grad():
        output = model(image)
        threshold = 0.1
        predicted_labels = (output > threshold).squeeze().int()
        return predicted_labels
def create_pdf(fullname, age, height_cm, weight_kg, gender, view_position, allergies, pred_labels, image_path):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 20, txt="Collected Data:", ln=True, align='L')
    
    pdf.cell(200, 10, txt=f"Fullname: {fullname}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Height (cm): {height_cm}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Weight (kg): {weight_kg}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"View Position: {view_position}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"History of Allergies/Congenital Diseases: {allergies}", ln=True, align='L')
    
    pdf.cell(200, 10, txt="Predicted Labels:", ln=True, align='L')
    if pred_labels.sum() == 0:
        pdf.cell(200, 10, txt="No Finding", ln=True, align='L')
    else:
        for idx, label in enumerate(all_classes):
            if pred_labels[idx] == 1:
                pdf.cell(200, 10, txt=f"- {label}", ln=True, align='L')
    
    pdf.ln(10)  # Add some space before the image
    pdf.cell(200, 10, txt="Uploaded Image:", ln=True, align='L')
    pdf.ln(10)  # Add some space before the image
    pdf.image(image_path, x=10, y=pdf.get_y(), w=100)

    pdf_output = os.path.join(os.getcwd(), "collected_data.pdf")
    pdf.output(pdf_output)
    return pdf_output

def main():
    st.title("X-Ray Image Classification")
    
    st.markdown("<h2 style='color: yellow;'>Step 1: </h2>", unsafe_allow_html=True)
    st.subheader("Enter Patient Details")
    
    with st.form("patient_details_form"):
        fullname = st.text_input("Fullname")
        age = st.slider("Age", 0, 110, 30)
        height_cm = st.number_input("Height in centimeters", 0, 300, 170)
        weight_kg = st.number_input("Weight in kilograms", 0, 200, 70)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        view_position = st.selectbox("View position", ["AP", "PA"])
        allergies = st.text_area("History of Allergies/Congenital Diseases")
        
        submitted = st.form_submit_button("Save and Continue to Step 2")
        if submitted:
            st.success("Patient details saved. Please proceed to Step 2.")
    
    st.markdown("<h2 style='color: yellow;'>Step 2: </h2>", unsafe_allow_html=True)
    st.subheader("Upload X-Ray Image")
    model = load_model()
    if model is None:
        return

    image = None
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png"], key="file_uploader_1")

    with st.expander("Or choose from sample here..."):
        sample = st.selectbox(label="Select here", options=list(sample_images.keys()), label_visibility="hidden")

    image_path = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        image_path = os.path.join(os.getcwd(), uploaded_file.name)
        image.save(image_path)
    elif sample != "None":
        image = Image.open(sample_images[sample])
        st.image(image, caption=f'Selected Sample: {sample}', use_column_width=True)
        image_path = os.path.join(os.getcwd(), f"{sample}.png")
        image.save(image_path)

    if image is not None:
        image_tensor = preprocess_image(image)
        
        # Validate model input
        try:
            predicted_labels = predict_image(image_tensor, model)
        except Exception as e:
            st.error(f"Prediction error: {e}")
            return

        st.subheader("Predicted labels:")
        if predicted_labels.sum() == 0:
            st.write("No Finding")
        else:
            for idx, label in enumerate(all_classes):
                if predicted_labels[idx] == 1:
                    st.write(f"- {label}")

        pdf_output = create_pdf(fullname, age, height_cm, weight_kg, gender, view_position, allergies, predicted_labels, image_path)

        with open(pdf_output, "rb") as f:
            pdf_base64 = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/octet-stream;base64,{pdf_base64}" download="collected_data.pdf">Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
