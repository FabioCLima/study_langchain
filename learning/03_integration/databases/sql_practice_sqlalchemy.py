import pandas as pd
from sqlalchemy import create_engine

# conecta ao banco PostgreSQL
db_engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/sql_course")

# executa a query e carrega em DataFrame
df_emails = pd.read_sql("SELECT email FROM sales.customers", db_engine)

print(df_emails.head())  # exibe as 5 primeiras linhas

