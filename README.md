#  AyurSutra

**The Smart Management Platform for Panchakarma Wellness**

---

A lightweight SaaS-style web application prototype to digitize and streamline Panchakarma therapy management for Ayurvedic centres. AyurSutra bridges traditional Ayurvedic practice and modern clinic management with role-based access, session tracking, visual analytics and digital patient records.

## Table of contents

* [Demo](#demo)
* [Overview](#overview)
* [Key Features](#key-features)
* [Tech Stack](#tech-stack)
* [Installation & Setup](#installation--setup)
  * [Prerequisites](#prerequisites)
  * [Local setup](#local-setup)
* [Usage](#usage)
* [Login Credentials (Prototype)](#login-credentials-prototype)
* [Project Structure](#project-structure)
* [Future Scope](#future-scope)
* [License](#license)
* [Team](#team)

---

## Demo

**Live demo:** *[AyurSutra](https://ayursutra-hackops.vercel.app/)*

---

## Overview

Many Ayurvedic centres still operate with manual, paper-based Panchakarma workflows. AyurSutra is a high-fidelity prototype web app designed for the SIH 2025 demo. It automates the therapy lifecycle with role-based authentication, simulated booking flows, and interactive wellness analytics.

This repository contains a prototype built for speed and reliability at demo time using mocked data (no production DB included in this prototype).

Note: This repository is optimized for Vercel Serverless deployments. It uses a Mock Data Engine to ensure 100% stability during live demos without the overhead of a production database.

---

## Key Features

### For Practitioners & Doctors

* **Smart Dashboard** — visual analytics of patient flow and therapy statuses (Chart.js)
* **Therapy Management** — track ongoing Panchakarma sessions in real-time
* **Patient Records** — digital history of treatments, notes and prescriptions

### For Patients

* **Seamless Booking** — simple appointment scheduling interface
* **Treatment Tracking** — view progress for ongoing therapies
* **Health History** — access past prescriptions and wellness reports

### Security & Access (Prototype)

* Role-based authentication (Patient vs Doctor)
* Session management via `Flask-Session`
* Mocked/dummy data for stable demo deployments (no production DB included)

---

## Tech Stack

| Component  | Technologies / Notes                  |
| ---------- | ------------------------------------- |
| Frontend   | HTML, CSS, JavaScript, Chart.js       |
| Backend    | Python 3.8+, Flask                    |
| Data       | Mocked JSON / Python dict (prototype) |
| Deployment | Vercel (serverless entrypoint)        |

---

## Installation & Setup

These instructions are for local development/testing only (prototype). The project uses mocked data to ensure stable demos without database dependencies.

### Prerequisites

* Python 3.8+
* Git

### Local setup

```bash
# 1. Clone the repository
git clone https://github.com/The-HackOps/AyurSutra.git
cd AyurSutra

# 2. Create a virtual environment
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python run.py
```

After launching, open your browser to `http://127.0.0.1:5001` (default for this prototype).

---

## Usage

* Switch Roles: Use the toggle buttons on the Sign-In page to switch between Patient and Doctor interfaces.
* Book & Approve: Book a therapy as a Patient and see it appear for approval in the Doctor's Manage Schedule tab.
* Analyze: Check the "Patient Feedback" and "Progress" tabs to see visual health trends.

---

## Login Credentials (Prototype)

For the SIH 2025 demo the app ships with mocked users so deployments remain stable without a SQL backend.

* **Patient**

  * Email: `patient@test.com`
  * Password: `123`

* **Doctor / Practitioner**

  * Email: `doctor@test.com`
  * Password: `123`

---

## Project Structure

```
AyurSutra/
├── api/                  # Vercel serverless entry point
├── app/
│   ├── static/           # CSS, JS, Images
│   ├── templates/        # HTML Files
│   ├── auth.py           # Authentication logic (Mock Data)
│   ├── main.py           # Main routing logic
│   ├── forms.py          # WTForms definitions
│   └── __init__.py       # App Factory
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel deployment config
└── run.py                # Local development entry point
```

*Note:* The current prototype uses mocked data for reliable demos. If you want DB-backed deployments, add a secure database (Postgres / MySQL) and update the configuration and `auth.py` accordingly.

---

## Future Scope

* **AI Integration:** Analyze patient `Prakriti` (body type) using ML models and provide decision support for personalized Panchakarma protocols.
* **IoT Integration:** Connect wearables to stream real-time vitals during therapy sessions.
* **Telemedicine:** Integrated video consultation feature for remote follow-ups and consultations.
* **Persistent DB:** Migrate from mocked data to a secure, audited database with role-based data encryption and backups.
* **Audit & Compliance:** Add logging, audit trails and role-based data access for practical clinic use.

---

## License

This project is released under the **MIT License**. See `LICENSE` for details.

---

## Team HackOps

* Backend / Database — [Anurag](https://github.com/anuragkumar88), [Dev](https://github.com/DevKumar005), [Uday](https://github.com/singhuday1)
* UI/UX Designer — [Krishna](https://github.com/krishnajais001), [Nishant](https://github.com/maninishant), [Taniya](https://github.com/Taniyarawat)
* Full Stack — [Dev](https://github.com/DevKumar005)
* Presenter, QA & Testing — [Taniya](https://github.com/Taniyarawat)

**Made with ❤️ by Team HackOps for SIH 2025**

---

## Contact

For questions about the project or to request contributions, contact the team lead or open an issue in this repository.
