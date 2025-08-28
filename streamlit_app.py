import pandas as pd
import joblib
import os
import io
import pickle
from io import BytesIO
import streamlit as st
import sys
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #00325B;
        textColor = #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def load_model():
    model = joblib.load('./logistic_regression_model.pkl')
    return model

def prediction(text, model):
    # Assuming the model expects a list of texts for prediction
    prediction = model.predict(text)
    return prediction

def main():

    st.header("C2P Prediction App")
    st.write("Python version:", sys.version)
    st.subheader("Assessing alerts relevant for our products or business")
    st.write("Upload a Excel file for prediction:")
    file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
    
    if file is not None:
        try:
            df = pd.read_excel(file)
                                  
            df = df[['Name','Summary']]
            
            df.rename(columns={'Name':'C2P Alerts_mod'},inplace=True)
            
            st.write("Excel File Contents:")
            pd.set_option('display.max_colwidth', None)
            st.write(df)
            
            model =load_model()
            
            # Combine the two inputs
            predictions = prediction(df[['C2P Alerts_mod','Summary']], model)

            # Add predictions to DataFrame
            
            df['Predictions'] = predictions
            
            dataset = pd.DataFrame({})
            
            dataset = df
            pd.set_option('display.max_colwidth', None)
            
            st.write("Prediction Results:")
            
            styled_df = df.style.map(lambda x: f"background-color: {'green' if x == 'YES' else 'red'}", subset='Predictions')
            #styled_df = dataset.style.background_gradient(cmap='viridis')
            #html = styled_df.to_html()

# Display the HTML in Streamlit
            st.dataframe(styled_df, use_container_width=True)
            
                          
        except Exception as e:
            st.error(f"An error occurred: {e}")
        

if __name__ == '__main__':
    main()

