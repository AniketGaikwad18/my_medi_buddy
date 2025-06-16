import streamlit as st
from main import predict_disease, symptom_index
from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Set page config
st.set_page_config(page_title="my_medi_buddy", page_icon="💊", layout="wide")

# Navigation
page = st.sidebar.selectbox("Navigate", ["Home", "About Us"])

if page == "Home":
    st.markdown("<h1 style='text-align: center; color: green;'>my_medi_buddy</h1>", unsafe_allow_html=True)

    st.markdown(
        '''
        <div style="background-color:#e8f5e9; padding: 20px; border-radius: 10px">
            <h3 style="color:#2e7d32;">💡 Why is it important to stay healthy?</h3>
            <ul style="color:#1b5e20;">
                <li><b>Workouts</b> improve heart health, boost your mood, and build strength.</li>
                <li><b>Eating healthy</b> supports your immune system and gives you lasting energy.</li>
                <li><b>Keeping your body active</b> helps reduce stress and chronic illness.</li>
            </ul>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown("---")

    symptoms_input = st.text_input("Enter your symptoms (comma-separated, e.g. headache, fever, cough):")
    st.markdown("*Please enter at least 3 symptoms to get accurate results.*")

    if st.button("Predict"):
        input_symptoms = [s.strip() for s in symptoms_input.split(",") if s.strip() in symptom_index]
        if len(input_symptoms) < 3:
            st.warning("⚠️ Please enter at least 3 valid symptoms from the dataset.")
        else:
            prediction = predict_disease(input_symptoms)
            st.success(f"**Predicted Disease:** {prediction}")

            # Animation
            lottie_url = "https://assets4.lottiefiles.com/packages/lf20_jcikwtux.json"
            lottie_json = load_lottieurl(lottie_url)
            if lottie_json:
                st_lottie(lottie_json, height=300)

            # Note
            st.info("🩺 This prediction is based on data and is for informational purposes only. "
                    "In case of emergency or worsening symptoms, please consult a medical professional.")

    st.markdown("<div style='text-align: right;'>Created by <b>Aniket</b></div>", unsafe_allow_html=True)

elif page == "About Us":
    st.markdown("<h1 style='color: green;'>About My Medi Buddy</h1>", unsafe_allow_html=True)
    st.markdown("""
**Creator:** Aniket Gaikwad  
**Project:** Machine Learning Based Disease Prediction System  
**Description:**  
This web application uses a Random Forest Classifier trained on symptoms data to predict the likely disease.  
It provides basic healthcare tips and encourages a healthy lifestyle.  

📢 Please note: This tool is meant to guide and inform, but it is not a substitute for professional medical advice.  

🙏 Thank you for using **my_medi_buddy**! Stay healthy and safe 💚
    """)
