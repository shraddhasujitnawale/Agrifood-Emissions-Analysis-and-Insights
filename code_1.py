import streamlit as st
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

# Load the machine learning model
dt = pickle.load(open("final.pkl", "rb"))

# Set Page Configuration
st.set_page_config(page_title=" Agrifood Emissions Analysis ", layout="wide",initial_sidebar_state="expanded")

# Title and Introduction
st.title("🌾 Agrifood Emissions Analysis and Insights")
st.markdown(
    """
    Welcome to the **Agrifood Emissions Analysis Tool**! This application enables you to:
    - **Predict CO₂ emissions** based on agricultural practices.
    - Analyze key factors like population, crop residue, and temperature.
    - Visualize and interpret the impact of rice cultivation, fertilizers, and agro-waste on emissions.
    """
)
# Initialize session state variables if not already initialized
if "average_temp" not in st.session_state:
    st.session_state.average_temp = 25  # default value
if "crop_residue" not in st.session_state:
    st.session_state.crop_residue = 30  # default value
if "forest_fires" not in st.session_state:
    st.session_state.forest_fires = 20  # default value
if "rural_population" not in st.session_state:
    st.session_state.rural_population = 50  # default value
if "rice_cultivation" not in st.session_state:
    st.session_state.rice_cultivation = 40  # default value
if "fertilizers_manufacturing" not in st.session_state:
    st.session_state.fertilizers_manufacturing = 80  # default value
if "pesticides_manufacturing" not in st.session_state:
    st.session_state.pesticides_manufacturing = 50  # default value
if "on_farm_energy_use" not in st.session_state:
    st.session_state.on_farm_energy_use = 20  # default value
if "on_farm_electricity" not in st.session_state:
    st.session_state.on_farm_electricity = 50  # default value
    # Initialize session state variables
if "total_emission" not in st.session_state:
    st.session_state.total_emission = 50  # Default value
    
fertilizers_manufacturing=0
input_data=0
# Sidebar Inputs
st.sidebar.title("🔍 Explore Parameters")
tabs = ["Population", "Emissions", "Food", "Fertilizer", "Employment", "CO₂ Analysis","Energy and Manufacturing"]
selected_tab = st.sidebar.radio("Navigate to:", tabs)

# Function to display metrics aesthetically
def display_metrics(label, value, delta=None, help_text=None):
    st.metric(label=label, value=value, delta=delta, help=help_text)
# 1️⃣ Population Parameters
if selected_tab == "Population":
    st.header("🏘️ Population Parameters")
    st.write("Specify population-related data below:")
    with st.form(key="rural_population_form"):  
        rural_population = st.slider(
            "Rural Population (millions)", 1, 100, 50, help="Specify the size of the rural population."
        )
        # Submit Button
        rural_form_submitted = st.form_submit_button("Submit Rural Parameters")

    if rural_form_submitted:
        # Dynamic Calculations for Rural Population
        rice_cultivation = rural_population * 0.8  # Example: 80% of rural population involved in rice cultivation
        on_farm_energy_use = rural_population * 0.1  # Example: 10 GWh per million rural residents
        agrofood_systems_waste_disposal = rural_population * 0.6  # Example: 60 tons per million rural residents

        # Output Analysis
        st.subheader("Rural Impact Analysis")
        st.write(f"- **Rural Population**: {rural_population} million")
        st.write(f"  - Estimated Rice Cultivation: **{rice_cultivation:.2f}%**")
        st.write(f"  - Estimated On-Farm Energy Use: **{on_farm_energy_use:.2f} GWh**")
        st.write(f"  - Estimated Agrofood System Waste Disposal: **{agrofood_systems_waste_disposal:.2f} tons**")

    
# 2️⃣ Emissions Parameters
elif selected_tab == "Emissions":
    st.header("🌡️ Emissions Parameters")
    st.write("Specify factors contributing to emissions below:")
    with st.form(key='total_emission_form'):
        average_temp = st.slider("Average Temperature (°C)", 0, 100, 25, help="Enter the average temperature.")
        crop_residue = st.slider("Crop Residue Burning (%)", 0, 100, 30, help="Enter the percentage of crop residue burned.")
        forest_fires = st.slider("Forest Fires (hectares)", 0, 100, 20, help="Enter the area affected by forest fires.")
        rice_cultivation = st.slider("Rice Cultivation (%)", 0, 100, 40, help="Enter the percentage of rice cultivation.")
        
        emission_submit_button= st.form_submit_button(label='Analyze Emission')
    
    if emission_submit_button:
        crop_residue= rice_cultivation*0.3
        forest_fires= average_temp*5
        st.write(f"  Average temperature:{average_temp:.2f}")
        st.write(f"  Crop Residue: {crop_residue:.2f}")
        st.write(f"  Forest Fires: {forest_fires:.2f}")
        st.write(f"  Rice Cultivation:{rice_cultivation:.2f}")

# 3️⃣ Food Parameters
# Initialize the variable outside the conditional block

elif selected_tab == "Food":
    st.header("🍚 Food Parameters")
    st.write("Adjust food-related parameters below:")
    with st.form("food_parameters_form"):
        rice_cultivation = st.slider("Rice Cultivation (%)", 0, 100, 40, help="Specify the percentage of rice cultivation.")
        food_retail = st.slider("Food Retail",0,100,30) 
        food_processing = st.slider("Food Processing",0,100,50)
        waste_disposal = rice_cultivation * 2  
        
        food_form_submit_button = st.form_submit_button(label="Food Data Submit")
        
        food_form_submit_button= st.success("Food parameters updated successfully!")

    if food_form_submit_button:
        st.subheader("Food Parameters Impact Analysis")
        st.write(f"### Based on **Rice Cultivation: {rice_cultivation}%**:")
        st.write(f"- **Food Retail**: Energy use is estimated at **{food_retail:.2f} GWh**, proportional to rice cultivation.")
        st.write(f"- **Food Processing**: Energy use is estimated at **{food_processing:.2f} GWh**, increasing with rice cultivation.")
        st.write(f"- **Agrifood Waste Disposal**: Waste is estimated at **{waste_disposal:.2f} tons**, impacted directly by cultivation levels.")

    st.info(
        f"**Insights:**\n"
        f"- Higher rice cultivation levels lead to increased energy consumption in food retail and processing.\n"
        f"- Waste disposal also rises proportionally, requiring enhanced waste management systems."
    )
# 4️⃣ Energy and Manufacturing Parameters
elif selected_tab == "Energy and Manufacturing":
    st.header("Energy and Manufacturing")
    st.write("Adjust energy and manufacturing related parameters below:")

    with st.form(key='energy_and_manufacturing_form'):  # Form context starts here
        # Energy Use and Manufacturing Parameters
        on_farm_energy_use = st.slider("On-farm Energy Use (GWh)", 0, 100, 20, help="Energy used on farms.")
        on_farm_electricity = st.slider("On-farm Electricity Use (GWh)", 0, 100, 50, help="Electricity used on farms.")
        fertilizers_manufacturing = st.slider("Fertilizers Manufacturing (tons)", 0, 100, 80, help="Fertilizer production.")
        pesticides_manufacturing = st.slider("Pesticides Manufacturing (tons)", 0, 100, 50, help="Pesticide production.")

        # Form submit button inside the form context
        energy_and_manufacturing_submit_button = st.form_submit_button("Analyze energy and manufacturing")
    
    if energy_and_manufacturing_submit_button:
        st.write(f'***On Farm Energy Use: {on_farm_energy_use}')
        st.write(f'***On Farm Electricity Use: {on_farm_electricity}')
        st.write(f'***Fertilizers Manufacturing: {fertilizers_manufacturing}')
        st.write(f'***Pesticides Manufacturing: {pesticides_manufacturing}')

        
elif selected_tab == "Fertilizer":
    # Insight Message on Waste Disposal and Fertilizer
    st.info(
        f"Agrofood system waste disposal is done on farms, helping to **fertilize soil** naturally and **reduce fertilizer use**. "
        f"This not only improves soil quality but also decreases reliance on synthetic fertilizers, supporting sustainability."
    )
    # Initialize session state for fertilizer form if not already done
    if "show_fertilizer_form" not in st.session_state:
        st.session_state.show_fertilizer_form = False
    # Prompt to analyze fertilizer impact
    st.write("### Proceed to Analyze Fertilizer Impact")
    if st.button("Analyze Fertilizer Impact"):
        st.session_state.show_fertilizer_form = True  # Update session state to show the next form
    # Separate Fertilizer Impact Form
    if st.session_state.show_fertilizer_form:
        st.subheader("Fertilizer Impact Analysis")
        # Input for Increase in Agrofood Waste Disposal
        waste_increase = st.slider("Increase in Agrofood System Waste Disposal (tons)", 0, 100, 10, help="Specify how much the agrofood waste disposal increases.")
        # Dynamic Calculation of Fertilizer Reduction
        fertilizer_reduction = waste_increase * 0.3  # Example: 30% of waste directly reduces fertilizer demand
        impact_on_fertilizer_manufacturing = fertilizer_reduction * 0.2  # Example: 20% less production required
        # Fertilizer Impact Results
        st.write(f"- **Increase in Agrofood Waste Disposal**: {waste_increase} tons")
        st.write(f"- **Reduction in Fertilizer Use**: **{fertilizer_reduction:.2f} tons**")
        st.write(f"- **Impact on Fertilizer Manufacturing**: **{impact_on_fertilizer_manufacturing:.2f}% decrease**")
        # Final Message
        st.info(
            "Increasing agrofood system waste disposal on farms directly decreases the dependency on synthetic fertilizers. "
            "This reduces production demand in fertilizer manufacturing, promoting environmental sustainability."
        )
# New Section: CO₂ Emission Analysis
elif selected_tab == "CO₂ Analysis":
    st.subheader("CO₂ Emission Analysis")
    forest_fires = locals().get("forest_fires", 43)
    crop_residue = locals().get("crop_residue", 0)
    average_temp = locals().get("average_temp", 25) 
    fires_in_organic_soils = locals().get("fires_in_organic_soils",20)
    total_emission = locals().get("total Emission",25)

    with st.form(key='co2_analysis_form'):
        total_emission= forest_fires+fires_in_organic_soils
        forest_fires= st.selectbox('Area of Forest',['Dense Forest','Less Forest','No Forest'])
        crop_residue= st.slider('Crop Residue', 0, 100, 20)
        average_temp = st.selectbox('Average Temperature',['High','Low','Very High'])
        fires_in_organic_soils = st.slider('Fires in Organic Soils',0,50,10)
        co2_analysis_form_submit_button= st.form_submit_button(label='Predict Co2 Emitted')
        
    if co2_analysis_form_submit_button:
         st.write(f"- **Total Emission**: Overall CO2 emitted is **{total_emission:.2f}**%")

# 4️⃣ Employment Parameters
elif selected_tab == "Employment":
    st.subheader("🏢 Employment in Urban Areas")
    st.write("Analyze the impact of urban population growth on employment in various sectors:")

    # Input for Urban Population Growth
    urban_population_growth = st.slider(
        "Projected Increase in Urban Population (millions)", 0, 50, 10, help="Specify the projected increase in urban population.")
    pesticides_manufacturing= st.slider(
        "Pesticides Manufacturing",0,100,30 )
    fertilizers_manufacturing = st.slider(
        "Fertilizer Manufacturing",0,100,30
    )
    # Employment Estimation Logic
    fertilizer_employment_per_million = 10  # Jobs per ton per million urban population
    pesticide_employment_per_million = 20  # Jobs per ton per million urban population

    try:
        # Calculate employment based on inputs
        fertilizer_employment = urban_population_growth * fertilizers_manufacturing * fertilizer_employment_per_million 
        pesticide_employment = urban_population_growth * pesticides_manufacturing * pesticide_employment_per_million 

        total_employment = fertilizer_employment + pesticide_employment

        # Display Employment Results
        st.write(f"### Employment Impact")
        st.write(f"- **Fertilizers Manufacturing Sector**: {fertilizer_employment:.0f} new jobs")
        st.write(f"- **Pesticides Manufacturing Sector**: {pesticide_employment:.0f} new jobs")
        st.write(f"- **Total Estimated Employment**: {total_employment:.0f} new jobs")
    except Exception as e:
        st.error(f"Error in calculating employment: {e}")

        
# Submit Button
if st.sidebar.button("Submit Input"):
    # Prepare the input data from session state and inputs
    input_data = pd.DataFrame({
        "Average Temperature (°C)": [st.session_state.average_temp],
        "Crop Residue Burning (%)": [st.session_state.crop_residue],
        "Urban Population": [st.session_state.rural_population],  
        "Forest Fires": [st.session_state.forest_fires],
        "Rice Cultivation (%)": [st.session_state.rice_cultivation],
        "Pesticides Manufacturing": [st.session_state.pesticides_manufacturing],
        "Food Retail (energy use, GWh)": [st.session_state.rice_cultivation * 5], 
        "Food Processing (energy use, GWh)": [st.session_state.rice_cultivation * 7.5],
        "On-farm Electricity Use (GWh)": [st.session_state.on_farm_electricity],
        "Fertilizers Manufacturing (tons)": [st.session_state.fertilizers_manufacturing],
        "Fires in Organic Soils (hectares)": [st.session_state.forest_fires * 0.001],
        "On-farm Energy Use (GWh)": [st.session_state.on_farm_energy_use],
        "Rural Population": [st.session_state.rural_population],
        "Total Emission": [st.session_state.total_emission]  # Ensure total_emission is updated before
    })
    

