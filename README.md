# 🚀 High-End Employee Management & Payroll System

A premium, glassmorphism-inspired Personnel Management and Financial Orchestration platform. Built with **Python Flask** and **Modern Frontend Architectures**, this system provides a seamless experience for HR specialists, Administrators, and Employees.

![Premium UI Experience](https://img.shields.io/badge/UI-Glassmorphism-indigo?style=for-the-badge)
![Backend](https://img.shields.io/badge/Backend-Flask-black?style=for-the-badge)
![Database](https://img.shields.io/badge/Database-PostgreSQL/SQLite-blue?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-JWT_Auth-emerald?style=for-the-badge)

---

## 🌟 Key Features

### 👤 Advanced Personnel Onboarding
- **Role-Based Provisioning**: Seamlessly onboard standard Employees or HR Specialists.
- **Temporary Access Management**: Set one-time temporary passwords with mandatory reset on first login.
- **Smart Designation System**: Standardized role selection with automated departmental mapping.

### 💰 Automated Payroll Intelligence
- **One-Click Generation**: Generate precise monthly payroll records for the entire organization.
- **Comprehensive Deductions**: Automated calculation of base salary, allowances, bonuses, and tax/PF deductions.
- **Financial History**: Maintain full dossiers of all past payouts and financial audits.

### 📅 Attendance & Shift Orchestration
- **Mission Assignment**: Assign specific daily tasks and shifts to personnel.
- **Smart Logging**: Real-time attendance tracking with anomaly detection.
- **Status Monitoring**: At-a-glance visualization of personnel availability (Present, On Leave, Late).

### 📈 Performance Auditing
- **Strategic Reviews**: HR and Admins can conduct performance audits for any personnel.
- **Rating Matrix**: 5-star rating system with detailed textual feedback cycles.
- **Bio-Dossiers**: Full historical view of an employee's journey (Performance, Attendance, Payroll).

### 🎨 State-of-the-Art Interface
- **Glassmorphism Design**: A futuristic, translucent UI with smooth transitions and high visibility.
- **Responsive Navigation**: Optimized for a 3-column strategic dashboard layout.
- **Dynamic Interactions**: Micro-animations and real-time data syncing for a premium feel.

---

## 🛠️ Tech Stack

- **Core**: Python 3.x, Flask
- **Security**: JWT (JSON Web Tokens), Bcrypt Hashing
- **Database**: SQLAlchemy ORM (PostgreSQL/SQLite)
- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (Modern Flexbox/Grid)
- **Styling**: Custom Glassmorphism Framework, TailwindCSS (for utility structures)

---

## 🚀 Quick Setup

### 1. Prerequisite Configuration
Ensure you have Python 3.10+ installed.

### 2. Environment Setup
Clone the repository and initialize the virtual environment:
```bash
git clone https://github.com/harshith1432/Employee-management-and-payroll-system.git
cd Employee-management-and-payroll-system
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Initialization
Create your local environment and initialize the schema:
```bash
python init_db.py
python create_admin.py  # Create your first Admin account
```

### 5. Launch the Matrix
```bash
python run.py
```
Access the strategic dashboard at `http://localhost:5000`.

---

## 📂 Project Structure

```text
├── app/
│   ├── models/          # Data Models (User, Employee, Attendance, etc.)
│   ├── routes/          # API Endpoints (Auth, Employee, Payroll, etc.)
│   ├── templates/       # Glassmorphism HTML views
│   ├── static/          # Assets and standard CSS
│   ├── utils/           # Helper scripts (Emails, Decorators)
│   └── extensions.py    # Flask extension initialization
├── config.py            # Global Configuration settings
├── run.py               # Main Application entry point
└── requirements.txt     # Dependency matrix
```

---

## 🛡️ Security Protocols

- **JWT Authentication**: All API requests require a valid Bearer token.
- **Password Safety**: Mandatory change for temporary passwords ensure account integrity.
- **Role Guards**: Strict HR/Admin decorators protect strategic data endpoints.

---

## 🤝 Contribution Strategy

1. **Fork** the repository.
2. **Implement** your feature or fix.
3. **Commit** with meaningful strategic messages.
4. **Push** to your origin and create a **Pull Request**.

---

Developed with ❤️ by [Harshith](https://github.com/harshith1432)
