from flask import Flask, request, jsonify, render_template_string
from vanna.remote import VannaDefault
import pandas as pd
import os
import pickle
from sqlalchemy import create_engine
import plotly.express as px

app = Flask(__name__)

# --- Vanna AI Configuration ---
api_key = os.getenv("VANNA_API_KEY")
model_name = os.getenv("VANNA_MODEL_NAME", "advwork")

if not api_key:
    raise ValueError("VANNA_API_KEY environment variable not set")

vn = VannaDefault(model=model_name, api_key=api_key)

# --- SQL Server Configuration ---
conn_str = (
    "mssql+pyodbc://localhost/AdventureWorks2019"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)
engine = create_engine(conn_str)

# --- Load or Extract Schema ---
schema_file = 'schema_context.pkl'

def load_schema():
    if os.path.exists(schema_file):
        with open(schema_file, 'rb') as f:
            return pickle.load(f)
    else:
        query = "SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS"
        df = pd.read_sql(query, engine)
        schema = {}
        for _, row in df.iterrows():
            key = f"{row['TABLE_SCHEMA']}.{row['TABLE_NAME']}"
            schema.setdefault(key, []).append(row['COLUMN_NAME'])
        with open(schema_file, 'wb') as f:
            pickle.dump(schema, f)
        return schema

schema_dict = load_schema()

def build_schema_context():
    return "\n".join([
        f"Table: {tbl} | Columns: {', '.join(cols)}"
        for tbl, cols in list(schema_dict.items())[:30]
    ])

# --- UI Route ---
@app.route("/", methods=["GET", "POST"])
def ui():
    error_html = sql_html = table_html = chart_html = ""
    question = ""

    if request.method == "POST":
        question = request.form.get("question", "")
        schema = build_schema_context()
        prompt = f"""
You are querying the AdventureWorks2019 SQL Server database.
Here is the database schema:
{schema}
Question: {question}
Write SQL Server query for this.
"""
        try:
            sql = vn.generate_sql(prompt)
            df = pd.read_sql(sql, engine)
            sql_html = f"<h5 style='color:white;'>Generated SQL:</h5><pre style='color:white;'>{sql}</pre>"
            table_html = f"<h5 style='color:white;'>Results:</h5>{df.to_html(index=False, classes='table table-dark table-striped')}"
            if df.shape[1] >= 2:
                numeric_cols = df.select_dtypes(include="number").columns
                if len(numeric_cols):
                    fig = px.bar(df, x=df.columns[0], y=numeric_cols[0],
                                 title=f"{numeric_cols[0]} by {df.columns[0]}",
                                 template="plotly_dark")
                    chart_html = f"<h5 style='color:white;'>Chart:</h5>{fig.to_html(full_html=False)}"
        except Exception as e:
            error_html = f"<div class='alert alert-danger'>Error: {str(e)}</div>"

    return render_template_string(open("templates/ui.html").read(),
                                  error_html=error_html,
                                  sql_html=sql_html,
                                  table_html=table_html,
                                  chart_html=chart_html,
                                  question=question)

if __name__ == '__main__':
    app.run(debug=True)
