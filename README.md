🔬 Bragg Angle Calculator

📖 Overview

The Bragg Angle Calculator is a web application built using Streamlit to compute theoretical and experimental Bragg angles in X-ray diffraction (XRD) studies. It allows users to input X-ray energy and lattice parameters to compute Bragg angles and visualize diffraction data interactively.

🛠 Features

Compute theoretical Bragg angles based on X-ray energy and lattice parameters.

Predict experimental Bragg angles from measured reflections.

Visualize diffraction data with tabular and graphical representations.

Download computed results in CSV format for further analysis.

🚀 Installation

Prerequisites

Ensure you have Python 3.8+ installed on your system.

Setup Instructions

Clone the repository:

git clone https://github.com/abd-zak/braggcalculator.git
cd braggcalculator

Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

Install dependencies:

pip install -r requirements.txt

Run the Streamlit app:

streamlit run streamlit_app.py

📜 How to Use

Enter the energy (keV) and lattice parameter (Å).

Click "Calculate Theoretical Bragg Angles" to compute results.

For experimental Bragg angles:

Provide measured Bragg angle (θ).

Click "Predict Bragg Angles".

View results in tabular and graphical formats.

Download results as CSV for further analysis.

📂 Project Structure

braggcalculator/
│── fonts/                  # Font files (if applicable)
│── streamlit_app.py        # Main Streamlit app
│── requirements.txt        # Dependencies
│── README.md               # Documentation
└── .gitignore              # Ignore unnecessary files

🌍 Deployment

The app is deployed on Streamlit Cloud:
🔗 Bragg Angle Calculator

To deploy manually:

Push your latest code to GitHub.

Link the repository on Streamlit Cloud.

Set up the Python version and dependencies.

🛠 Troubleshooting

If Symbola font is missing, ensure it is stored inside the fonts/ directory.

Run pip install -r requirements.txt if missing dependencies.

Restart the Streamlit app if you encounter issues.

📜 License

This project is open-source under the MIT License.

🤝 Contributing

Fork the repository.

Create a feature branch: git checkout -b feature-name

Commit changes: git commit -m "Added feature"

Push to GitHub: git push origin feature-name

Open a pull request.

📧 Contact

For questions or suggestions:

GitHub: abd_zak

Email: aboudi.zak00@gmail.com

🚀 Happy Computing! 🔬

