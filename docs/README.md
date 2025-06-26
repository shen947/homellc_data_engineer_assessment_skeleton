# Data Engineering Assessment

Welcome! This exercise is designed to evaluate your core skills in **data engineering**:

- **SQL databases**: Data modeling, normalization, and scripting
- **Python and ETL**: Data cleaning, transformation, and loading workflows

---

## 📚 How This Document Works

Each section is structured with:

- **Problem:** Background and context for the task
- **Task:** What you are required to do (including any bonus “extra” tasks)
- **Solution:** Where you must document your approach, decisions, and provide instructions for reviewers

> **Tech Stack:**  
> Please use only Python (for ETL/data processing) and SQL/MySQL (for database).  
> Only use extra libraries if they do not replace core logic, and clearly explain your choices in your solution.

---

## 0. Setup

1. **Fork and clone this repository:**
    ```bash
    git clone https://github.com/<your-username>/homellc_data_engineer_assessment_skeleton.git
    ```
2. **Start the MySQL database in Docker:**
    ```bash
    docker-compose -f docker-compose.initial.yml up --build -d
    ```
    - Database is available on `localhost:3306`
    - Credentials/configuration are in the Docker Compose file
    - **Do not change** database name or credentials

3. For MySQL Docker image reference:  
   [MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

### Problem

You are provided with property-related data in a CSV file.
- Each row relates to a property.
- There are multiple Columns related to this property.
- The database is not normalized and lacks relational structure.


### Task

- **Normalize the data:**
  - Develop a Python ETL script to read, clean, transform, and load   data into your normalized MySQL tables.
  - Refer the field config document for the relation of business logic
  - Use primary keys and foreign keys to properly capture relationships

- **Deliverable:**
  - Write necessary python and sql scripts
  - Place the scripts inside the `sql/` directory)
  - The scripts should take the initial csv to your final, normalized schema when executed
  - Clearly document how to run your script, dependencies, and how it integrates with your database.

**Tech Stack:**  
- Python (include a `requirements.txt`)
Use **MySQL** and SQL for all database work  
- You may use any CLI or GUI for development, but the final changes must be submitted as python/ SQL scripts 
- **Do not** use ORM migrations—write all SQL by hand

### Solution

**Document your database design and solution here:**  
**The raw CSV file was flattened and lacked relational structure. I designed a normalized schema consisting of four main tables:**

- addresses - stores street, city, state, zip, country.

- financials - includes list price, taxes, net yield, and IRR.

- properties - connects each property to its address and financial info, with a purchase date and title.

- features - describes the number of bedrooms, bathrooms, square footage, and basement presence per property.

- All tables use integer primary keys and appropriate foreign key constraints to preserve referential integrity.


**Document your ETL logic here:**  
**How to Run the Project:**

**Start Docker**:
- docker compose up -d

**Load the schema into MySQL:**
- docker exec -i homellc-mysql mysql -u root -p6equj5_root < sql/schema.sql

**Install Python dependencies:**
- pip install -r requirements.txt

**Run the ETL script:**
- python scripts/etl.py --csv sql/fake_data.csv --config sql/"Field Config.xlsx"

**Verify the load:**
- Use MySQL to check row counts in each table.

**The script reads the raw data using pandas, normalizes it by creating deduplicated reference tables, assigns surrogate keys, merges foreign keys back into the main data, and finally loads each table into MySQL using mysql-connector-python.**

All logic is kept lightweight, readable, and reproducible.

---

## Submission Guidelines

- Edit this README with your solutions and instructions for each section
- Place all scripts/code in their respective folders (`sql/`, `scripts/`, etc.)
- Ensure all steps are fully **reproducible** using your documentation

---

**Good luck! We look forward to your submission.**
