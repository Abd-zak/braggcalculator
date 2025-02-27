


import streamlit as st
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import logging
import datetime
#######################################################################
########################### font l0oading #############################
#######################################################################
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# Use the font from the repository
symbola_font_path = os.path.join(os.path.dirname(__file__), "fonts", "Symbola.ttf")

# Ensure the font file exists before loading
if os.path.exists(symbola_font_path):
    prop = fm.FontProperties(fname=symbola_font_path)
    plt.rcParams["font.family"] = prop.get_name()
    print(f"✅ Loaded font: {prop.get_name()} from {symbola_font_path}")
else:
    print("⚠️ Warning: Symbola font not found, using default font.")


#######################################################################
#######################################################################


# Define font download links for missing fonts
FONT_DOWNLOAD_LINKS = {
    "Symbola": "https://fontlibrary.org/en/font/symbola",
    "Noto Color Emoji": "https://fonts.google.com/noto/specimen/Noto+Color+Emoji"
}
LOG_FILE = "font_errors.log"

pd.set_option('future.no_silent_downcasting', True)

# Enable wide layout
st.set_page_config(page_title="Bragg Angle Calculator", layout="wide", initial_sidebar_state="collapsed")

col1, col2 ,col3 = st.columns([1,3, 1])  # Adjust proportions as needed
with col2:
    st.markdown("""
        ## 📖 Introduction: Understanding Bragg’s Law and X-ray Diffraction
        **Bragg’s Law** is a fundamental principle in X-ray crystallography, describing how X-rays are diffracted by a crystal lattice:

        \[
        λ= 2d sin θ
        \]

        where:λ
        - **n** is the order of reflection (typically 1 for most measurements),
        - **λ** is the wavelength of the incident X-ray beam,
        - **d** is the spacing between atomic planes in the crystal lattice,
        - **θ** is the Bragg angle.

        ### 🔬 Why is Bragg’s Law Important?
        - **Crystal Structure Determination:** Used to determine atomic arrangements in materials.
        - **Material Characterization:** Helps analyze crystalline phases, strain, and defects.
        - **Nanotechnology & Semiconductors:** Essential in studying thin films and advanced materials.

        ### 🔢 How This App Works
        - **Calculate theoretical Bragg angles** for given energy and lattice parameter.
        - **Predict experimental Bragg angles** from measured reflections.
        - **Visualize diffraction data** with plots.
        - **Download computed results** for further study.

        ---
    """, unsafe_allow_html=True)




st.markdown("""
    <style>
        .stMarkdown { margin-bottom: -10px !important; }
        .stButton { margin-top: -10px !important; }
        .stNumberInput { margin-bottom: -10px !important; }
        .stTextInput { margin-bottom: -10px !important; }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
        .stTable { margin: auto; text-align: center; }
    </style>
""", unsafe_allow_html=True)


# ✅ Initialize session state variables (to persist results)
if "bragg_data" not in st.session_state:
    st.session_state.bragg_data = {}
    st.session_state.bragg_df = pd.DataFrame()
if "predicted_data" not in st.session_state:
    st.session_state.predicted_data = {}
    st.session_state.predicted_df = pd.DataFrame()


#######################################################################
##################### functions #######################################
#######################################################################
# ✅ Function to Compute Lattice Parameter from Experimental Data
def compute_lattice_param(energy_keV, hkl, exp_theta):
    """Computes lattice parameter based on an experimental Bragg angle and reflection."""
    energy_eV = energy_keV * 1e3
    h = 4.135667696e-15  # Planck's constant (eV⋅s)
    c = 299792458  # Speed of light (m/s)
    wavelength = h * c / energy_eV  

    h, k, l = map(int, hkl.strip("()").split(","))
    theta_rad = np.radians(exp_theta)
    lattice_param = (wavelength / (2 * np.sin(theta_rad))) * np.sqrt(h**2 + k**2 + l**2)
    
    return lattice_param * 1e10  # Convert to Å

# ✅ Function to Calculate Bragg Angles
def calculate_bragg_angles(energy_keV, lattice_param, num_reflections, miller_indices=None):
    """Calculate Bragg angles and return data including d-spacing, sin²(θ), λ/2d, and Intensity."""
    energy_eV = energy_keV * 1e3
    h = 4.135667696e-15  # Planck's constant (eV⋅s)
    c = 299792458  # Speed of light (m/s)
    wavelength = h * c / energy_eV  # Compute wavelength

    if miller_indices is None:
        miller_indices = [
            (1, 1, 1), (2, 0, 0), (2, 2, 0), (3, 1, 1), (2, 2, 2), 
            (4, 0, 0), (3, 3, 1), (4, 2, 0), (4, 2, 2), (5, 1, 1), 
            (4, 4, 0), (5, 3, 1), (6, 2, 0), (5, 3, 3), (7, 1, 1)
        ]

    d_spacing = {
        f"({h}{k}{l})": lattice_param * 1e-10 / np.sqrt(h**2 + k**2 + l**2)
        for h, k, l in miller_indices[:num_reflections]
    }

    reflections = list(d_spacing.keys())
    d_values = list(d_spacing.values())
    theta = [
        round(np.degrees(np.arcsin(wavelength / (2 * d))), 2) if wavelength / (2 * d) <= 1 else None
        for d in d_values
    ]
    two_theta = [round(2 * t, 2) if t else None for t in theta]
    sin_sq_theta = [round(np.sin(np.radians(t))**2, 4) if t else None for t in theta]
    lambda_by_2d = [round(wavelength / (2 * d), 4) if d else None for d in d_values]

    return {
    "Miller Indices (hkl)": reflections,
    "d-spacing (Å)": [round(d * 1e10, 4) for d in d_values],  
    "θ (°)": theta,  
    "2θ (°)": two_theta,  
    "sin²(θ)": sin_sq_theta,
    "λ / 2d": lambda_by_2d}



# ✅ Function to Display Tables Horizontally
def display_horizontal_table(data):
    """Display a fully styled horizontal table using st.table()."""
    df = pd.DataFrame(data).T  # ✅ Transpose DataFrame for horizontal layout

    # ✅ Set the first row as headers and remove it from data
    df.columns = df.iloc[0]  
    df = df[1:]  

    # ✅ Convert missing values safely
    df = df.fillna("N/A").astype(str)

    # ✅ Apply styling using Markdown for background colors
    st.markdown(
        """
        <style>
            table {
                width: 100%;
                font-size: 20px;
                color: white !important;  /* White text for readability */
                background-color: #222 !important;  /* Dark grey background */
                text-align: center !important;
            }
            th {
                background-color: #8B0000 !important;  /* Dark Red Headers */
                color: white !important;
                padding: 10px;
            }
            td {
                padding: 8px;
                border-bottom: 1px solid #444 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ✅ Display the table with Streamlit's built-in `st.table()`
    st.markdown("### 📜 Bragg Angle Table", unsafe_allow_html=True)
    st.table(df)

def plot_bragg_angles(df, title, color):
    """Plots Bragg angles vs. reflections while handling Unicode Theta symbols."""
    expected_col_names = ["Miller Indices (hkl)", "2\u03B8 (°)", "\u03B8 (°)"]  # Using Unicode θ
    df.columns = [col.strip() for col in df.columns]  # Clean column names

    if "2\u03B8 (°)" not in df.columns or "Miller Indices (hkl)" not in df.columns:
        st.error("🚨 Error: Missing required columns for plotting.")
        st.write("Columns found:", df.columns)  # Debugging info
        return

    # ✅ Generate the plot
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(df["Miller Indices (hkl)"], df["2\u03B8 (°)"], color="red", marker="o", label="Bragg Angles")
    ax.plot(df["Miller Indices (hkl)"], df["2\u03B8 (°)"], linestyle="--", color="red", alpha=0.6)
    ax.set_xlabel("Miller Indices (hkl)")
    ax.set_ylabel("2θ (°)")
    ax.set_title(title)
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)




#######################################################################
#######################################################################
######################### CSS STYLING #################################
#######################################################################

# 🎨 CENTRALIZED UI SETTINGS
UI_SETTINGS = {
    "background": "#121212",
    "text_color": "white",
    "highlight": "#ffcc00",
    "button_color": "#e63946",
    "button_hover": "#d62828",
    "font_size": "30px",
    "table_font_size": "30px",
}



# 🔧 APPLY CSS STYLING
st.markdown(f"""
    <style>
        body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {{
            background-color: {UI_SETTINGS["background"]};
            color: {UI_SETTINGS["text_color"]} !important;
            font-size: {UI_SETTINGS["font_size"]} !important;
        }}
        .stButton>button {{
            background-color: {UI_SETTINGS["button_color"]} !important;
            color: white !important;
            font-size: 30px !important;
            font-weight: bold;
            padding: 12px 20px;
        }}
        .stButton>button:hover {{
            background-color: {UI_SETTINGS["button_hover"]} !important;
        }}
        .stDownloadButton>button {{
            background-color: {UI_SETTINGS["button_color"]} !important;
            color: white !important;
            font-size: 30px !important;
            border-radius: 6px;
            padding: 12px 20px;
        }}
        .stDownloadButton>button:hover {{
            background-color: {UI_SETTINGS["button_hover"]} !important;
        }}
        table {{
            font-size: {UI_SETTINGS["table_font_size"]} !important;
        }}

        /* Fixed number input styling */
        .stNumberInput label {{
            font-size: 20px !important;
            color: {UI_SETTINGS["text_color"]} !important;
        }}
        .stNumberInput input {{
            font-size: 18px !important;
            padding: 8px 12px !important;
        }}
        .stTextInput label {{
            font-size: 20px !important;
            color: white !important;
        }}
        .stTextInput input {{
            font-size: 18px !important;
            padding: 8px 12px !important;
            background-color: #333333 !important;
            color: white !important;
            border-radius: 5px !important;
        }}
    </style>
""", unsafe_allow_html=True)




#######################################################################
########################### CSS STYLING ###############################
#######################################################################

st.markdown(f"<h1 style='color: #ffcc00; text-align: center;'>🔬 Bragg Angle Calculator</h1>", unsafe_allow_html=True)

#######################################################################
####################### THEORETICAL BRAGG ANGLES ######################
#######################################################################

st.markdown("## 📡 Theoretical Bragg Angles")

col1, col2 = st.columns(2)
with col1:
    energy_keV = st.number_input("🔋 Enter the energy in keV:", min_value=1.0, value=10.0)
    num_reflections = st.number_input("📡 Number of reflections:", min_value=1, value=6, step=1)
with col2:
    lattice_param = st.number_input("🧪 Enter the lattice parameter in Å:", min_value=1.0, value=3.923)

if st.button("🔬 Calculate Theoretical Bragg Angles"):
    st.session_state.bragg_data = calculate_bragg_angles(energy_keV, lattice_param, num_reflections)
    st.session_state.bragg_df = pd.DataFrame(st.session_state.bragg_data)

if st.session_state.bragg_data:
    col1, col2 = st.columns([2, 1])
    with col1:
        display_horizontal_table(st.session_state.bragg_data)
    with col2:
        plot_bragg_angles(st.session_state.bragg_df, "📊 Theoretical Bragg Reflection Plot", "red")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Theoretical CSV filename
    theoretical_filename = f"bragg_angles_{energy_keV}keV_{lattice_param}A_{timestamp}.csv"

    csv = st.session_state.bragg_df.to_csv(index=False).encode('utf-8')
    download_success = st.download_button(label="📥 Download CSV", data=csv, file_name=theoretical_filename, mime="text/csv")

    if download_success:
        st.success(f"✅ **Theoretical data downloaded as:** `{theoretical_filename}`")

#######################################################################
##################### EXPERIMENTAL BRAGG ANGLE ########################
#######################################################################

st.markdown("## 📏 Experimental Bragg Angle Prediction")

col1, col2 = st.columns(2)
with col1:
    exp_hkl = st.text_input("📡 Enter the known reflection (e.g., (111)):", value="(1,1,1)")
    num_reflections_exp = st.number_input("📡 Number of reflections for prediction:", min_value=1, value=6, step=1)
with col2:
    exp_theta = st.number_input("📏 Enter measured Bragg angle (°):", min_value=0.0, value=30.0)

if st.button("🔬 Predict Bragg Angles"):
    computed_lattice_param = compute_lattice_param(energy_keV, exp_hkl, exp_theta)
    st.success(f"✅ Computed d spacing: **{computed_lattice_param:.3f} Å**")

    st.session_state.predicted_data = calculate_bragg_angles(energy_keV, computed_lattice_param, num_reflections_exp)
    st.session_state.predicted_df = pd.DataFrame(st.session_state.predicted_data)

if st.session_state.predicted_data:
    col1, col2 = st.columns([2, 1])
    with col1:
        display_horizontal_table(st.session_state.predicted_data)
    with col2:
        plot_bragg_angles(st.session_state.predicted_df, "📊 Predicted Bragg Reflection Plot", "blue")
    # Generate timestamp for unique filenames
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Experimental CSV filename
    experimental_filename = f"predicted_bragg_{energy_keV}keV_{exp_hkl}_{timestamp}.csv"


    csv = st.session_state.predicted_df.to_csv(index=False).encode('utf-8')
    download_success = st.download_button(label="📥 Download CSV", data=csv, file_name=experimental_filename, mime="text/csv")

    if download_success:
        st.success(f"✅ **Experimental data downloaded as:** `{experimental_filename}`")