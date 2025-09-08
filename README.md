# Vaccination Data Analysis Project

## 📌 Project Overview
This project focuses on analyzing global vaccination data using **Python, SQL, and Power BI**.  
The goal is to design a clean, normalized database, perform data analysis, and present insights through interactive dashboards.

---

## 🎯 Objectives
- Extract and clean raw vaccination datasets using Python.
- Store structured data in a relational SQL database.
- Apply **database normalization** and enforce **primary/foreign key constraints**.
- Build insightful **Power BI dashboards** to visualize vaccination coverage, incidence, and reported cases.
- Document the process, challenges, and solutions.

---

## 🛠️ Tech Stack
- **Python** – Data extraction & cleaning  
- **MySQL** – Database design & management  
- **Power BI** – Data visualization & reporting  
- **GitHub** – Version control & project hosting  



---

## 🗄️ Database Design
- **Tables Created**
  - `coverage`
  - `incidence`
  - `reported_cases`
  - `vaccine_introduction`
  - `vaccine_schedule`

- **Keys & Constraints**
  - Primary keys on unique identifiers (country code, year, antigen/disease).
  - Foreign keys to maintain referential integrity between tables.
  - Example: `coverage.code` → `vaccine_schedule.iso_3_code`

---

## 📊 Power BI Reports
The following insights were generated:
- **Vaccination Coverage Trends** – Coverage percentage across years.  
- **Incidence & Reported Cases** – Relationship between coverage and disease reduction.  
- **Vaccine Introductions** – Timeline of new vaccine rollouts.  


---

## 📖 Process
1. **Data Extraction & Cleaning** – Removed duplicates, standardized codes, fixed missing values.  
2. **Database Creation** – Designed normalized schema in MySQL with proper constraints.  
3. **Data Loading** – Populated tables with cleaned datasets.  
4. **Visualization** – Built Power BI dashboards for insights.  
5. **Documentation** – Challenges and solutions recorded for reproducibility.  

---


