import streamlit as st
from main import predict_disease, symptom_index
from streamlit_lottie import st_lottie
import requests

# Load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie animations
lottie_health = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_ks1irfoc.json")
lottie_doctor = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_uhg5v4.json")

# Page config
st.set_page_config(page_title="my_medi_buddy", page_icon="💊", layout="centered")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Home", "Predict Disease", "About Us"])

# HOME PAGE
if page == "Home":
    st.markdown("""
        <h1 style='text-align: center; color: #2E8B57;'>my_medi_buddy</h1>
    """, unsafe_allow_html=True)

    if lottie_health:
        st_lottie(lottie_health, height=250)

    st.markdown("""
    <div style='background-color: #E8F5E9; padding: 15px; border-radius: 10px;'>
        <h3>💡 Why is it important to stay healthy?</h3>
        <ul>
            <li><b>Workouts</b> improve heart health, boost your mood, and build strength.</li>
            <li><b>Eating healthy</b> supports your immune system and gives you lasting energy.</li>
            <li>Keeping your body active helps reduce stress and chronic illness.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# PREDICT DISEASE PAGE
elif page == "Predict Disease":
    st.markdown("""
        <h2 style='color: #2E8B57;'>🧠 Enter Your Symptoms</h2>
    """, unsafe_allow_html=True)

    st.info("Enter at least 3 valid symptoms. Suggestions will appear as you type.")

    all_symptoms = sorted(symptom_index.keys())
    selected_symptoms = st.multiselect("Select your symptoms:", options=all_symptoms)

    if st.button("Predict Disease"):
        if len(selected_symptoms) < 3:
            st.warning("Please enter at least 3 symptoms for accurate prediction.")
        else:
            result = predict_disease(selected_symptoms)
            st.success(f"Predicted Disease: {result['disease']}")
            st.markdown(f"**Description:** {result['description']}")
            st.markdown("**Precautions:**")
            for precaution in result['precautions']:
                st.write(f"- {precaution}")

            if lottie_doctor:
                st_lottie(lottie_doctor, height=200)

            st.markdown("""
                <div style='background-color: #FFF3CD; padding: 15px; border-radius: 10px; margin-top: 20px;'>
                    <b>Note:</b> This disease prediction is based on data analysis. If symptoms worsen or persist, please consult a certified medical professional immediately.
                </div>
            """, unsafe_allow_html=True)

# ABOUT US PAGE
elif page == "About Us":
    st.markdown("""
        <h2 style='color: #2E8B57;'>About my_medi_buddy</h2>
        <p><b>Developer:</b> Aniket Gaikwad</p>
        <p><b>Project Purpose:</b> This application is designed to help users predict possible diseases based on their symptoms using a machine learning model. It also offers precautionary measures and health advice.</p>
        <p><b>Technology Used:</b> Python, Streamlit, Random Forest Classifier, and health-related datasets from Kaggle.</p>
        <p>Thank you for using <b>my_medi_buddy</b>. Stay healthy, stay informed. 💚</p>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr style='border: 1px solid #ccc;'/>
    <div style='text-align:right; color:gray;'>Created by <b>Aniket</b></div>
""", unsafe_allow_html=True)
