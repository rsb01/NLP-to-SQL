# 🧠 NLP-to-SQL App with Flask & SQL Server

This is a Flask-based web application that uses natural language processing to convert user questions into SQL queries. It connects to the **AdventureWorks2019** SQL Server database and displays both the generated SQL and query results.

## 🌟 Features

- Converts natural language questions to SQL queries
- Displays query results as HTML tables and charts (Plotly)
- Clean Bootstrap-based UI with background image
- Can use either Vanna AI or LLaMA 3 via LangChain (optional setup)

---

## 🚀 Setup Instructions

### 1. Clone This Repository

```bash 
git clone https://github.com/YOUR_USERNAME/nlp-to-sql.git
cd nlp-to-sql
```

### 2. Install Python Requirements

```bash
pip install -r requirements.txt
```

### 3. Setup the SQL Server

- Install SQL Server (Developer Edition).
- Restore the `AdventureWorks2019.bak` database using SQL Server Management Studio (SSMS).
- Ensure you have **ODBC Driver 17 for SQL Server** installed.

### 4. Run the Web App

```bash
python app.py
```

Then go to `http://localhost:5000/` in your browser.

---

## 📁 Project Structure

```
nlp-to-sql/
├── app.py
├── schema_context.pkl
├── static/
│   └── background.jpg
├── templates/
│   └── ui.html
├── requirements.txt
├── .gitignore
├── README.md
└── AdventureWorks2019.bak (optional, not pushed to GitHub)
```
---

## 📸 UI Preview

The app uses a stylish Bootstrap 5 dark theme and a background image from `/static/background.jpg`.

---

## 🔐 Notes

- Do not upload `.bak` and `.pkl` files to GitHub.
- You can expand this project using LangChain or Hugging Face Transformers.

---

**Made with ❤️ by Raam Sai Bharadwaj**


