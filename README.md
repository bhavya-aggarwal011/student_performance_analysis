# Student Performance Analysis Dashboard

An end-to-end data analysis project on a 10,000-student dataset to discover what factors drive exam scores and placement outcomes. Includes data cleaning, exploratory data analysis, statistical analysis, data visualisation, insight extraction, and a fully interactive live dashboard with real-time filters.

---

## Project Structure

```
CHECK/
│
├── app.py                               # Interactive Dash dashboard
├── requirements.txt                     # Python dependencies
│
├── charts/
│     ├── chart_01_histograms.png
│     ├── chart_02_boxplots.png
│     ├── chart_03_placement_pie.png
│     ├── chart_04_scatter_plots.png
│     ├── chart_05_study_vs_score_detail.png
│     ├── chart_06_correlation_heatmap.png
│     ├── chart_07_placed_vs_notplaced.png
│     ├── correlation_bar_chart.png
│     └── exam_score_distribution.png
│
├── data/
│     ├── student_dataset.csv            # Original raw dataset
│     └── student_dataset_cleaned.csv   # Cleaned version
│
├── insights/
│     ├── insight_01_study_hours.png
│     ├── insight_02_attendance.png
│     ├── insight_03_internet_usage.png
│     ├── insight_04_assignments.png
│     └── insight_05_student_profiles.png
│
└── notebook/
      └── dash.ipynb                     # Full analysis notebook
```

---

## Dataset

| Property | Value |
|---|---|
| Total rows | 10,000 students |
| Total columns | 8 |
| Missing values | None |
| Target variables | `exam_score`, `placement_status` |

### Columns

| Column | Description |
|---|---|
| `study_hours` | Daily study hours (1–11) |
| `attendance` | Class attendance percentage (40–100%) |
| `sleep_hours` | Average sleep hours per night |
| `internet_usage` | Daily internet usage in hours |
| `assignments_completed` | Number of assignments submitted |
| `previous_score` | Score in previous exam |
| `exam_score` | Final exam score |
| `placement_status` | Placed / Not Placed |

---

## Analysis Steps

### Step 1 — Data Loading
- Loaded 10,000 rows from CSV
- Verified all 8 columns and data structure

### Step 2 — Data Cleaning
- Zero missing values
- Zero duplicate rows
- All data types verified correct
- All value ranges validated
- Column names standardised

### Step 3 — Descriptive Statistics
- Mean, median, mode, standard deviation for all columns
- Skewness and quartile analysis
- Statistics split by placement group

### Step 4 — Visual Analysis
- 7 histograms — univariate distribution of each variable
- 7 box plots — Placed vs Not Placed comparison
- 6 scatter plots — each feature vs exam score
- Correlation heatmap — all variables vs all variables
- Grouped bar chart — placement group comparison

### Step 5 — Insight Extraction
- 5 data-backed insights with supporting charts
- Each insight includes exact numbers and recommended actions

---

## Key Findings

| # | Insight | Key Number |
|---|---|---|
| 1 | Study hours is the strongest predictor of exam score | r = +0.563 |
| 2 | High attendance students place 17% more than low attendance | 91.7% vs 74.8% |
| 3 | Internet usage is the only negative predictor | r = −0.152 |
| 4 | Assignment completion shows the biggest placement gap | 95.6% vs 68.6% |
| 5 | Students with all good habits achieve 100% placement rate | 444 students |

---

## Dashboard Features

The interactive dashboard built with Plotly Dash includes:

**Live Filters — all charts update instantly when changed:**
- Placement Status dropdown — All / Placed Only / Not Placed Only
- Study Hours range slider — 1 to 11 hrs/day
- Attendance range slider — 40% to 100%
- Exam Score range slider — 0 to 100

**Charts:**
- 4 KPI cards — total students, placement rate, avg score, avg study hours
- Pie and bar chart — placement breakdown
- Scatter plot — study hours vs exam score
- Histogram grid — distribution of all 7 variables
- Box plots — Placed vs Not Placed
- Grouped bar chart — all metrics compared
- Correlation heatmap

---

## How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/bhavya-aggarwal011/student-performance-analysis.git
cd student-performance-analysis
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the dashboard**
```bash
python app.py
```

**4. Open in browser**
```
http://127.0.0.1:8050
```

---

## Live Dashboard

👉 **[Click here to view the live dashboard](https://YOUR-RENDER-URL.onrender.com)**

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Data Analysis | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Dashboard | Plotly Dash |
| Deployment | Render |

---

## Results Summary

```
Dataset Overview
Total students : 10,000
Placed         : 8,356  (83.6%)
Not Placed     : 1,644  (16.4%)
Avg exam score : 86.70

Correlations with Exam Score
study_hours           r = +0.563  Strong
assignments_completed r = +0.388  Moderate
previous_score        r = +0.319  Moderate
attendance            r = +0.223  Weak
sleep_hours           r = +0.145  Weak
internet_usage        r = -0.152  Weak negative

Star Student Profile
(study >= 8hrs, attendance >= 80%, internet <= 4hrs)
Students  : 444
Placed    : 100.0%
Avg score : 98.64
```

---

## Author

**Bhavya Aggarwal**
Aspiring Data Analyst | Python Enthusiast | Exploring Data Through Insights and Visualization 🚀