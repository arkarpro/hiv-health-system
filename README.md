# 🏥 HIV Health Information System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B.svg)
![Google Sheets](https://img.shields.io/badge/Database-Google%20Sheets-109618.svg)

A centralized web application built with **Streamlit** and **Google Sheets API** to manage HIV patient records, testing histories, treatment plans, and facility information. 

## ✨ Features

* **👥 Patient Management:** Register and maintain demographic data of patients.
* **🔬 HIV Testing:** Record testing dates and results (Positive/Negative).
* **💊 Treatment Tracking:** Monitor ART (Antiretroviral Therapy) and pregnancy status.
* **🏥 Facilities:** Manage clinical facilities across different townships and states.
* **📊 Dashboard:** Real-time data visualization of tested patients, positive cases, and ART statuses.

## 🛠️ Tech Stack

* **Frontend & Backend:** [Streamlit](https://streamlit.io/) (Python)
* **Data Manipulation:** Pandas
* **Database:** Google Sheets
* **Authentication:** Google Service Account (`gspread`, `google-auth`)

## 📂 Project Structure

```text
hiv-health-system/
│
├── .streamlit/
│   └── secrets.toml         # ⚠️ Must be created locally (DO NOT upload to GitHub)
├── pages/
│   ├── 1_HIV_Testing.py     # Testing records form
│   ├── 2_Treatment.py       # ART and treatment tracking
│   ├── 3_Reports.py         # Analytics dashboard
│   ├── 4_Settings.py        # Facilities management
│   └── 5_Patient.py         # Patient registration
│
├── app.py                   # Main entry point of the app
├── connection.py            # Centralized Google Sheets connection setup
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
