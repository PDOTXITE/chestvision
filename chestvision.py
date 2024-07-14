import streamlit as st
from pages import prediction, about_us

# Set the page layout to wide
st.set_page_config(layout="wide")

PAGES = {
    "Prediction": prediction,
    "About Us": about_us
}

def main():
    st.title("Welcome to Chest-Vision")

    st.subheader('Multi-label Classification of 14 Common Thorax Diseases from Chest X-ray Images Using Transfer Learning Technique')
    st.write("Activated by Princess Chulaborn Science High School Satun")

    st.write("""
    **Introduction to Our Platform**

    Chest diseases are a significant health issue and a leading cause of death worldwide. They encompass various medical conditions such as chronic obstructive pulmonary disease, chronic bronchitis, pulmonary fibrosis, and pneumonia. Early diagnosis of chest diseases is crucial for effective treatment and reducing the risk of mortality.
    Currently, chest X-ray (CXR) imaging is a widely used method for diagnosing chest diseases, but the accuracy of diagnosis heavily depends on the expertise of radiologists. In many community hospitals, there is a shortage of specialized radiologists, leading to potential delays in diagnosis.

    **Our Project Capabilities**

    Our platform is capable of classifying 14 different types of chest diseases using advanced transfer learning techniques. These diseases include:
    - Cardiomegaly
    - Hernia
    - Infiltration
    - Nodule
    - Emphysema
    - Effusion
    - Atelectasis
    - Pleural Thickening
    - Pneumothorax
    - Mass
    - Fibrosis
    - Consolidation
    - Edema
    - Pneumonia
    """)

if __name__ == "__main__":
    main()

