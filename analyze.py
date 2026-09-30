import sqlite3
import pandas as pd

conn = sqlite3.connect("jobs.db")
df = pd.read_sql("SELECT * FROM jobs", conn)
conn.close()

print(df.shape)
print(df.info())
print(df.head())

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

clean_titles = df["title"].str.lower()
top_titles = clean_titles.value_counts().head(10)

top_companies = df["company"].value_counts().head(10)

plt.figure(figsize=(8, 5))
sns.barplot(x=top_companies.values, y=top_companies.index, color="steelblue")
plt.title("Top 10 Companies by Number of Job Postings")
plt.xlabel("Number of postings")
plt.ylabel("Company")
plt.tight_layout()
plt.savefig("chart_top_companies.png")
plt.show()

top_10_states = df["state"].value_counts().head(10)

plt.figure(figsize=(8, 5))

top_titles.index = top_titles.index.str.title()

sns.barplot(x=top_10_states.values, y=top_10_states.index, color="skyblue")
plt.title("Top 10 states by Number of job postings")
plt.xlabel("Number of postings")
plt.ylabel("State")
plt.tight_layout()
plt.savefig("chart_top_states.png")
plt.show()

# Step 1: filter out rows with no salary
salary_df = df[df["salary_min"].notna()]

# Step 2: group by search_query and calculate the average
avg_salary = salary_df.groupby("search_query")["salary_min"].mean().sort_values(ascending=False)

# Step 3: plot it (same barplot pattern as before)
plt.figure(figsize=(8, 5))
sns.barplot(x=avg_salary.values, y=avg_salary.index, color="mediumseagreen")
plt.title("Average Minimum Salary by Job Role")
plt.xlabel("Average minimum salary")
plt.ylabel("Job role")
plt.tight_layout()
plt.savefig("chart_avg_salary.png")
plt.show()

postings_by_date = df.groupby("posted_date").size()

plt.figure(figsize=(10, 5))
postings_by_date.plot(kind="line", marker="o", color="darkorange")
plt.title("Job Postings Over Time")
plt.xlabel("Date")
plt.ylabel("Number of postings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart_postings_over_time.png")
plt.show()

top_titles = clean_titles.value_counts().head(10)
top_titles.index = top_titles.index.str.title()

plt.figure(figsize=(8, 5))
sns.barplot(x=top_titles.values, y=top_titles.index, color="mediumpurple")
plt.title("Top 10 Job Titles by Number of Postings")
plt.xlabel("Number of postings")
plt.ylabel("Job title")
plt.tight_layout()
plt.savefig("chart_top_titles.png")
plt.show()