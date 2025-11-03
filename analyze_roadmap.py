import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load Data
df = pd.read_csv("all_courses_roadmap.csv")
print("✅ Data loaded successfully!\n")
print(df.head())

# Step 2: Basic Info
print("\n📈 Dataset Overview:")
print(df.info())
print("\nUnique Courses:", df['Course'].nunique())

# Step 3: Summary Statistics
avg_duration = df.groupby('Course')['Duration_Weeks'].mean().sort_values()
print("\n⏱️ Average Duration per Course:\n", avg_duration)

# Step 4: Visualization - Average Duration
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_duration.index, y=avg_duration.values, palette="coolwarm")
plt.xticks(rotation=45)
plt.title("Average Duration (Weeks) per Course")
plt.xlabel("Course")
plt.ylabel("Average Duration (Weeks)")
plt.tight_layout()
plt.show()

# Step 5: Skill Level Distribution
plt.figure(figsize=(6,4))
sns.countplot(x='Level', data=df, order=['Beginner','Intermediate','Advanced','Expert'])
plt.title("Distribution of Skill Levels Across All Courses")
plt.show()

# Step 6: Most Common Tools
tools = df['Tools'].str.split(',').explode().str.strip()
tool_counts = tools.value_counts().head(10)

plt.figure(figsize=(8,5))
sns.barplot(x=tool_counts.values, y=tool_counts.index, palette="viridis")
plt.title("Top 10 Most Common Tools in Roadmaps")
plt.xlabel("Count")
plt.ylabel("Tool")
plt.show()
