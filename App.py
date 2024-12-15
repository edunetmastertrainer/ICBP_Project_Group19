import pickle
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
from PIL import Image

 
# loading the saved models
 
mentalHealth = pickle.load(open('models/MentalHealth.pkl', 'rb'))
liver = pickle.load(open('models/Liver.pkl','rb'))
def calculate_bmi(weight, height):
    bmi = weight / (height / 100) ** 2
    return bmi
def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal Weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def protein_calculator(weight_kg, activity_level='sedentary'):
    """
    Estimate the daily protein requirement based on weight and activity level.

    Parameters:
    weight_kg (float): Weight of the person in kilograms.
    activity_level (str): The activity level of the individual (default is 'sedentary').
                          Options: 'sedentary', 'active', 'very_active'.

    Returns:
    float: The estimated daily protein requirement in grams.
    """
    # Default protein needs per kilogram based on activity level
    if activity_level == 'sedentary':
        protein_per_kg = 0.8
    elif activity_level == 'active':
        protein_per_kg = 1.2
    elif activity_level == 'very_active':
        protein_per_kg = 1.5
    else:
        raise ValueError("Invalid activity level. Choose from 'sedentary', 'active', or 'very_active'.")
    
    # Calculate protein requirement
    protein_needed = weight_kg * protein_per_kg
    return protein_needed

import math

def body_fat_calculator(sex, waist, neck, height, hip=None):
    """
    Calculate body fat percentage using the US Navy formula.
    
    Parameters:
    sex (str): 'male' or 'female' indicating gender.
    waist (float): Waist circumference in inches.
    neck (float): Neck circumference in inches.
    height (float): Height in inches.
    hip (float, optional): Hip circumference in inches (only needed for females).
    
    Returns:
    float: Estimated body fat percentage.
    """
    if sex == 'Male':
        # For men, use the formula without hip measurement
        body_fat_percentage = 86.010 * math.log10(waist - neck) - 70.041 * math.log10(height) + 36.76
    elif sex == 'Female':
        if hip is None:
            raise ValueError("Hip measurement is required for females.")
        # For women, use the formula with hip measurement
        body_fat_percentage = 163.205 * math.log10(waist + hip - neck) - 97.684 * math.log10(height) - 78.387
    else:
        raise ValueError("Sex must be either 'male' or 'female'.")
    
    return body_fat_percentage



# sidebar for navigation
def main():
    with st.sidebar:
        image = Image.open('images/navbar.png')
        st.image(image,width =200)
        selected = option_menu('Disease Diagnosis and Recommendation System',
                             
                              ['Mental Health','Liver Disorders','BMI CALCULATOR','Protein Calculator','Body Fat Calculator'],
                              icons=['liver','brain','hearts','star','diamond'],
                              default_index=0,styles={"container":{"background-color":"#9ce3c3"},})
 
    if (selected == 'Mental Health'):
       
        # page title
        st.title('Mental Health')
       
       
        # getting the input data from the user
        col1, col2, col3,col4= st.columns(4)
       
        with col1:
            sex_options = ['Male','Female']
            sex = st.selectbox('Gender',sex_options)
           
        with col2:
             age = st.text_input('Age')
       
        with col3:
            working_or_student_options = ['Working',"Student"]
            working_or_student = st.selectbox('working_or_student',working_or_student_options)
       
        with col1:
            academic_pressure_options =["Not Student","No Pressure","Below Average","Average","Above Avegrage","High"]
            academic_pressure = st.selectbox('Academic Pressure',academic_pressure_options)
       
        with col2:
            work_pressure_options = ["I am Student","No Pressure","Below Average","Average","Above Avegrage","High"]
            work_pressure = st.selectbox("Work Pressure",work_pressure_options)
       
        with col3:
            CGPA_options = ["I am Working",">=9","9-8","8-7","7-6","6-5","5-4","4-3","<3"]
            CGPA = st.selectbox("CGPA",CGPA_options)
       
       
        with col1:
            study_satisfaction_options = ["I am Working","No","Below Average","Average","Above Avegrage","High"]
            study_satisfaction = st.selectbox("Study Satisfaction",study_satisfaction_options)
       
        with col2:
            job_satisfaction_options = ["I am Student","No","Below Average","Average","Above Avegrage","High"]
            job_satisfaction = st.selectbox("Job Satisfaction",job_satisfaction_options)

        with col3:
            sleep_duration_options = ["1-3 Hours","3-4 Hours","5-6 Hours","6-7 Hours","7-8 Hours","More than 8 Hours"]
            sleep_duration = st.selectbox("Sleep Duration",sleep_duration_options)
        
        with col1:
            dietary_habits_options = ["Healthy", "Moderate", "Unhealthy"]
            dietary_habits = st.selectbox("Dietary Habits",dietary_habits_options)
        
        with col3:
            suicide_ideation_options = ['Yes','No']
            suicide_ideation = st.selectbox('Have you ever had suicidal thoughts',suicide_ideation_options)
        with col2:
            Work_Study_Hours = st.text_input("Work/Study Hours")

        with col1:
            financial_stress_options = ["No","Mild","Moderate"," High","Severe"]
            financial_stress = st.selectbox("Financial Stress",financial_stress_options)
        
        with col2:
            family_history_options = ["Yes","No"]
            family_history = st.selectbox("Family History of Mental Illness",family_history_options) 
        with col4:
            image = Image.open('images/mental.png')
            st.image(image,width = 400)  
        with col4:
            image = Image.open('images/mental2.png')
            st.image(image,width = 400) 
 
        # code for Prediction
        diab_diagnosis = ''
       
        # creating a button for Prediction
       
        if st.button('Mental Test Result'):
            sex_mapping = {'Male':0,'Female':1}
            working_or_student_mapping = {'Working':1,"Student":0}
            academic_pressure_mapping ={"Not Student":0,"No Pressure":1,"Below Average":2,"Average":3,"Above Avegrage":4,"High":5}
            work_pressure_mapping = {"I am Student":0,"No Pressure":1,"Below Average":2,"Average":3,"Above Avegrage":4,"High":5}
            CGPA_mapping = {"I am Working":0,">=9":5,"9-8":4,"8-7":3.5,"7-6":3,"6-5":2.5,"5-4":2,"4-3":1.5,"<3":1}
            study_satisfaction_mapping = {"I am Working":0,"No":1,"Below Average":2,"Average":3,"Above Avegrage":4,"High":5}
            job_satisfaction_mapping = {"I am Student":0,"No":1,"Below Average":2,"Average":3,"Above Avegrage":4,"High":5}
            sleep_duration_mapping = {"1-3 Hours":1,"3-4 Hours":2,"5-6 Hours":3,"6-7 Hours":4,"7-8 Hours":5,"More than 8 Hours":6}
            dietary_habits_mapping = {"Healthy":2, "Moderate":1, "Unhealthy":0}
            suicide_ideation_mapping = {'Yes':1,'No':0}
            financial_stress_mapping = {"No":1,"Mild":2,"Moderate":3," High":4,"Severe":5}
            family_history_mapping = {"Yes":1,"No":0}

            mental_prediction = mentalHealth.predict([[sex_mapping[sex],float(age),working_or_student_mapping[working_or_student],academic_pressure_mapping[academic_pressure],work_pressure_mapping[work_pressure],CGPA_mapping[CGPA],study_satisfaction_mapping[study_satisfaction],job_satisfaction_mapping[job_satisfaction],sleep_duration_mapping[sleep_duration],dietary_habits_mapping[dietary_habits],suicide_ideation_mapping[suicide_ideation],float(Work_Study_Hours),financial_stress_mapping[financial_stress],family_history_mapping[family_history]]])
            
           
            if (mental_prediction[0] == 1):
              st.success('The person is suffering from depression')
            else:
              st.success('The person is Mentaly fit')
       
    if(selected == 'Liver Disorders'):
        # page title
        st.title('Healthy Liver Prediction')
       
        col1, col2, col3 ,col4= st.columns(4)
       
        with col1:
            age = st.text_input('Age')

        with col2:
            gender = st.selectbox("Gender",['Male','Female'])
        with col3:
            total_Bilirubin = st.text_input("Total Bilirubin")
        
        with col1:
            direct_Bilirubin = st.text_input("Direct Bilirubin")
        with col2:
            alkaline_phosphatase = st.text_input("Alkaline Phosphatase")
        with col3:
            sgpt  = st.text_input("SGPT")
        with col1:
            sgot = st.text_input("SGOT")
        with col2:
            total_proteins = st.text_input("Total Proteins")
        with col3:
             albumin = st.text_input("Albumin")
        with col1:
            A_G_Ratio = st.text_input("A/G Ratio")
        with col4:
            image = Image.open('images/liver.jpg')
            st.image(image,width =350)
        with col4:
            image = Image.open('images/liver2.png')
            st.image(image,width =350)
        
        # creating a button for Prediction
       
        if st.button('Liver Disease Test Result'):
            liver_pred = liver.predict([[float(age),{'Male':0,"Female":1}[gender],float(total_Bilirubin),float(direct_Bilirubin),float(alkaline_phosphatase),float(sgpt),float(sgot),float(total_proteins),float(albumin),float(A_G_Ratio)]])
            
            if liver_pred[0] == 1:
                st.success('The person liver is Healthy')
            elif liver_pred[0]==2:
                st.success('The person liver is UnHealthy (Moderate)')
            else:
                st.success('The person liver is in UnHealthy (High)')


        st.markdown("<p>The normal range for some liver function tests are:<br> Total bilirubin: 0.1–1.2 milligrams per deciliter (mg/dL)<br> Direct bilirubin: 0.0–0.3 mg/dL<br> ALT (SGPT): 5–40 IU/L <br>AST (SGOT): 5–40 IU/L<br> Alkaline phosphatase: 30–115 U/L <br> Albumin: 3.5–5.0 grams per deciliter (g/dL) <br> Total protein: 6.3–7.9 g/dL </p>",unsafe_allow_html=True)
        #st.success(diab_diagnosis)
       
    if(selected == 'BMI CALCULATOR'):
       
        st.title("BMI CALCULATOR")
 
        st.write("Body Mass Index (BMI) is a measure of body fat based on height and weight.")
        st.write("Use this calculator to find out your BMI category.")
        col1,col2 = st.columns([2,1])
        with col1:
            weight = st.text_input("Enter your weight (in kilograms)")
            height = st.text_input("Enter your height (in centimeters)")
       
            if st.button("Calculate BMI"):
               
                weight = float(weight)
                height = float(height)
                bmi = calculate_bmi(weight, height)
                category = interpret_bmi(bmi)
       
                st.write("### Results")
                st.write(f"Your BMI: {bmi:.2f}")
                st.write(f"Category: {category}")
        with col2:
            image = Image.open('images/bmi.png')
            st.image(image,width =350)  
 
    if(selected == 'Protein Calculator'):
        st.title("Protein Calculator")
        st.write("Estimate the daily protein requirement based on weight and activity level")
        st.write("Use this calculator to find out your daily protein requirement.")
        col1,col2 = st.columns([2,1])
        with col1:
            weight_kg = st.text_input('Enter your weight (in kilograms)')
            activity_level = st.selectbox('activity level',['sedentary','active','very_active'])
            if st.button("Calculate Protein"):
                weight = float(weight_kg)
                protein_intake = protein_calculator(weight, activity_level)
                st.success(f'Daily protein requirement: {protein_intake} grams')

    if(selected == 'Body Fat Calculator'):
        st.title("Body Fat Calculator")
        st.write("Calculate body fat percentage using the US Navy formula")
        st.write("Use this calculator to find out body fat")
        col1,col2 = st.columns([2,1])
        with col1:
            sex = st.selectbox('Gender',['Male','Female'])
            waist = st.text_input('Waist circumference in inches')
            neck = st.text_input('Neck circumference in inches.')
            height = st.text_input('Height in inches')
            hip = st.text_input('Hip circumference in inches only for Female')
            if st.button("Body Fat Calculator"):
                waist = float(waist)
                neck = float(neck)
                height = float(height)
                hip = float(hip)
                body_fat = body_fat_calculator(sex, waist, neck, height, hip)
                if(sex=='Male'):
                    if(body_fat>=25):
                        result = "Obese"
                    elif(body_fat<24 and body_fat>=18):
                        result = "Average"
                    elif(body_fat<17):
                        result = "Good: Fit"
                else:
                    if(body_fat>=32):
                        result = "Obese"
                    elif(body_fat<31 and body_fat>=25):
                        result = "Average"
                    elif(body_fat<24):
                        result = "Good: Fit"
                st.success(f"Body Fat Percentage: {body_fat:.2f}%. \n You are in - {result} Category")

if __name__ == "__main__":
    main()
 
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.markdown("<p style = 'color:grey;'>This is a prediction web app for informational purposes only.\n It is not a substitute for professional medical advice.\nPlease consult a doctor or visit a hospital for proper diagnosis and treatment.</p>",unsafe_allow_html=True)
st.write("\n")
st.write("\n")
st.markdown('<p style="font-size:12px; color:#808080;">©2024</p>', unsafe_allow_html=True)
 
 
 
 