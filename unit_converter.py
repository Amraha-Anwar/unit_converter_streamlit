import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# Initialize session state for conversion history
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []

# Set page config and theme
st.set_page_config(page_title="🌠Advanced Unit Converter", layout="wide", page_icon="🛠")


st.markdown("""
    <style>
    /* Interactive gradient background */
    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(270deg, #1A1E2E, #2B2B3D, #1A1E2E);
        background-size: 300% 300%;
        animation: gradientAnimation 10s ease infinite;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
    }
    
    /* Custom container styling */
    .conversion-container {
        background: linear-gradient(to bottom right, rgba(255,255,255,0.05), rgba(255,255,255,0.1));
        border-radius: 15px;
        padding: 25px;
        margin: 10px 0;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .conversion-container:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(to right, #2E7D32, #43A047);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        font-size: 1.1em;
    }
    
    /* Input fields styling */
    .stNumberInput, .stSelectbox {
        background: rgba(255,255,255,0.1);
        color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.2);
        padding: 8px;
    }

    .stNumberInput:focus, .stSelectbox:focus {
        border-color: #6C5CE7;
        box-shadow: 0 0 8px rgba(108, 92, 231, 0.6);
    }

    /* Label text styling */
    .stSelectbox label, .stNumberInput label {
        color: #FFFFFF !important;
        font-size: 1em;
        font-weight: bold;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(to right, #6C5CE7, #8E7CFF);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1em;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(to right, #8E7CFF, #A89BFF);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.4);
    }

    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(to right, #00C853, #64DD17);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1em;
        transition: all 0.3s ease;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(to right, #64DD17, #76FF03);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 200, 83, 0.4);
    }

    /* Expander and other text elements */
    .streamlit-expanderHeader, .stMarkdown, h1, h2, h3 {
        color: #FFFFFF !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
    }

    ::-webkit-scrollbar-thumb {
        background: #6C5CE7;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #8E7CFF;
    }

    /* Animation for title */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .title-animation {
        animation: fadeIn 1.5s ease-out;
    }

    /* Form section styling */
    .form-section {
        margin-bottom: 20px;
    }

    .form-section label {
        color: #FFFFFF !important;
        font-size: 1.1em;
        font-weight: bold;
    }

    /* Personalized touch */
    .personalized-touch {
        text-align: center;
        margin-top: 20px;
        font-size: 0.9em;
        color: rgba(255,255,255,0.8);
    }
    </style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="title-animation">🌠 Advanced Unit Converter</h1>', unsafe_allow_html=True)
st.markdown("_Convert units with style and precision_")

# Conversion factors dictionary
CONVERSION_FACTORS = {
    "Length": {
        "Meters": {"Kilometers": 0.001, "Feet": 3.28084, "Miles": 0.000621371},
        "Kilometers": {"Meters": 1000, "Feet": 3280.84, "Miles": 0.621371},
        "Feet": {"Meters": 0.3048, "Kilometers": 0.0003048, "Miles": 0.000189394},
        "Miles": {"Meters": 1609.34, "Kilometers": 1.60934, "Feet": 5280}
    },
    "Weight": {
        "Kilograms": {"Grams": 1000, "Pounds": 2.20462, "Ounces": 35.274},
        "Grams": {"Kilograms": 0.001, "Pounds": 0.00220462, "Ounces": 0.035274},
        "Pounds": {"Kilograms": 0.453592, "Grams": 453.592, "Ounces": 16},
        "Ounces": {"Kilograms": 0.0283495, "Grams": 28.3495, "Pounds": 0.0625}
    }
}

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    conversions = {
        "Celsius": {
            "Fahrenheit": lambda x: (x * 9/5) + 32,
            "Kelvin": lambda x: x + 273.15
        },
        "Fahrenheit": {
            "Celsius": lambda x: (x - 32) * 5/9,
            "Kelvin": lambda x: (x - 32) * 5/9 + 273.15
        },
        "Kelvin": {
            "Celsius": lambda x: x - 273.15,
            "Fahrenheit": lambda x: (x - 273.15) * 9/5 + 32
        }
    }
    return conversions[from_unit][to_unit](value)

# main layout
col1, col2 = st.columns([2, 1])

with col1:
    with st.container():
        st.markdown('<div class="conversion-container">', unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        unit_type = st.selectbox(
            "Choose the type of unit to convert:",
            ["Length", "Weight", "Temperature"],
            help="Select the type of conversion you want to perform"
        )

        # Get appropriate units based on unit type
        units = {
            "Length": ["Meters", "Kilometers", "Feet", "Miles"],
            "Weight": ["Kilograms", "Grams", "Pounds", "Ounces"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"]
        }[unit_type]

        from_unit = st.selectbox("From", units)
        to_unit = st.selectbox("To", units)

        # Add a slider for value input (optional)
        value = st.slider(
            "Enter value to convert:",
            min_value=0.0 if unit_type != "Temperature" else -100.0,
            max_value=1000.0,
            value=10.0,
            step=0.1,
            help="Use the slider or manually enter the value"
        )

        if st.button("Convert", use_container_width=True):
            # Perform conversion
            if unit_type == "Temperature":
                result = convert_temperature(value, from_unit, to_unit)
            else:
                if from_unit == to_unit:
                    result = value
                else:
                    result = value * CONVERSION_FACTORS[unit_type][from_unit][to_unit]

            # Store conversion in history
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.conversion_history.append({
                'timestamp': timestamp,
                'from_value': value,
                'from_unit': from_unit,
                'to_value': result,
                'to_unit': to_unit,
                'unit_type': unit_type
            })

            # Show result with comparisons
            st.success(f"🎯 Converted value: {result:.4f} {to_unit}")
            
            # Show relative comparison
            if unit_type == "Length" and to_unit in ["Meters", "Kilometers"]:
                comparison = result / 1.7
                st.info(f"📏 This is approximately {comparison:.1f} times the height of an average person!")
            elif unit_type == "Weight" and to_unit in ["Kilograms", "Pounds"]:
                comparison = result / 70
                st.info(f"⚖️ This is approximately {comparison:.1f} times the weight of an average person!")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Conversion history
    st.subheader("📜 Recent Conversions")
    if st.session_state.conversion_history:
        for conv in reversed(st.session_state.conversion_history[-5:]):
            st.write(f"**{conv['timestamp']}**: {conv['from_value']} {conv['from_unit']} → "
                    f"{conv['to_value']:.4f} {conv['to_unit']}")
        
        # Clear history button
        if st.button("Clear History"):
            st.session_state.conversion_history = []
    else:
        st.info("No conversion history yet")

    # Add visualization of conversion
    if st.session_state.conversion_history:
        st.subheader("📊 Conversion Trend")
        latest_conversions = st.session_state.conversion_history[-10:]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[conv['timestamp'] for conv in latest_conversions],
            y=[conv['to_value'] for conv in latest_conversions],
            mode='lines+markers',
            name='Converted Values',
            line=dict(color='#6C5CE7', width=2),
            marker=dict(color='#8E7CFF', size=8)
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="Time",
            yaxis_title="Converted Value",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF')
        )
        st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
with st.expander("ℹ️ Help & Tips"):
    st.markdown("""
    - Use the dropdown menus to select your units
    - Enter the value you want to convert
    - Click the Convert button to see the result
    - View your conversion history on the right
    - The graph shows your recent conversion trends
    - For temperature conversions, negative values are allowed
    """)


if st.session_state.conversion_history:
    import pandas as pd
    history_df = pd.DataFrame(st.session_state.conversion_history)
    csv = history_df.to_csv(index=False)
    st.markdown('<div class="stDownloadButton">', unsafe_allow_html=True)
    st.download_button(
        label="📥 Download Conversion History",
        data=csv,
        file_name="conversion_history.csv",
        mime="text/csv"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="personalized-touch">Made with ❤️ by Amraha Anwar</div>', unsafe_allow_html=True)