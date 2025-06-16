import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load datasets
df_main = pd.read_csv("dataset.csv")
df_precaution = pd.read_csv("symptom_precaution.csv")
df_description = pd.read_csv("symptom_Description.csv")

# Fill missing symptoms with 'None'
df_main.fillna('None', inplace=True)

# All symptom columns
symptom_columns = [col for col in df_main.columns if col.startswith("Symptom_")]

# Unique symptoms from all rows
# Extract all unique symptoms from the dataset (excluding 'None')
all_symptoms = sorted(set(symptom for symptom in df_main[symptom_columns].values.flatten() if symptom != 'None'))

symptom_index = {symptom: idx for idx, symptom in enumerate(all_symptoms)}

# One-hot encode symptoms
def encode_symptoms(row):
    encoded = [0] * len(symptom_index)
    for symptom in row[symptom_columns]:
        if symptom != 'None' and symptom in symptom_index:
            encoded[symptom_index[symptom]] = 1
    return encoded

X = np.array(df_main.apply(encode_symptoms, axis=1).tolist())
le = LabelEncoder()
y = le.fit_transform(df_main["Disease"])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=le.classes_))

def predict_disease(symptom_list):
    # Create a zero vector and set 1 where symptom exists
    input_vector = [0] * len(symptom_index)
    for symptom in symptom_list:
        if symptom in symptom_index:
            input_vector[symptom_index[symptom]] = 1

    # Predict
    prediction = model.predict([input_vector])[0]
    disease_name = le.inverse_transform([prediction])[0]

    # Get precaution
    precaution_row = df_precaution[df_precaution["Disease"] == disease_name]
    precautions = precaution_row.iloc[0, 1:].dropna().tolist() if not precaution_row.empty else ["No data"]

    # Get description
    desc_row = df_description[df_description["Disease"] == disease_name]
    description = desc_row.iloc[0]["Description"] if not desc_row.empty else "No description available."

    return {
        "disease": disease_name,
        "precautions": precautions,
        "description": description
    }

# 🔍 Example usage
example_symptoms = ["itching", "skin_rash", "nodal_skin_eruptions"]
result = predict_disease(example_symptoms)
print("Predicted Disease:", result["disease"])
print("Precautions:", result["precautions"])
print("Description:", result["description"])
