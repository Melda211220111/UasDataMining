import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
def load_data():
    file_path = 'Classification.csv'
    return pd.read_csv(file_path)

data = load_data()

# Streamlit app configuration
st.set_page_config(page_title="Drug Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Header
st.title("🌟 Drug Analysis Dashboard")
st.markdown(
    """<style>
    .title {
        font-family: 'Arial', sans-serif;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
st.sidebar.markdown("Refine the dataset by using the filters below.")

# Custom styled range slider for age
st.sidebar.markdown("**Select Age Range**")
age_filter = st.sidebar.slider(
    label="",
    min_value=int(data['Age'].min()),
    max_value=int(data['Age'].max()),
    value=(20, 60),
    help="Slide to select the age range of patients."
)

# Gender filter with emojis for Male/Female
st.sidebar.markdown("**Select Gender**")
sex_filter = st.sidebar.multiselect(
    label="",
    options=data['Sex'].unique(),
    default=data['Sex'].unique(),
    format_func=lambda x: "👩 Female" if x == "F" else "👨 Male",
    help="Select one or more genders."
)

# Blood Pressure filter
st.sidebar.markdown("**Select Blood Pressure Levels**")
bp_filter = st.sidebar.multiselect(
    label="",
    options=data['BP'].unique(),
    default=data['BP'].unique(),
    help="Choose blood pressure levels to include."
)

# Cholesterol filter
st.sidebar.markdown("**Select Cholesterol Levels**")
cholesterol_filter = st.sidebar.multiselect(
    label="",
    options=data['Cholesterol'].unique(),
    default=data['Cholesterol'].unique(),
    format_func=lambda x: "🔴 High" if x == "HIGH" else "🟢 Normal",
    help="Choose cholesterol levels to include."
)

# Filter dataset
data_filtered = data[(data['Age'] >= age_filter[0]) & (data['Age'] <= age_filter[1])]
data_filtered = data_filtered[data_filtered['Sex'].isin(sex_filter)]
data_filtered = data_filtered[data_filtered['BP'].isin(bp_filter)]
data_filtered = data_filtered[data_filtered['Cholesterol'].isin(cholesterol_filter)]

# Layout
col1, col2, col3 = st.columns(3)

# Card 1: Age Statistics
with col1:
    st.markdown("### 📊 Age Statistics")
    st.metric(label="Average Age", value=round(data_filtered['Age'].mean(), 1))
    st.metric(label="Minimum Age", value=data_filtered['Age'].min())
    st.metric(label="Maximum Age", value=data_filtered['Age'].max())

# Card 2: Gender Distribution
with col2:
    st.markdown("### 👥 Gender Distribution")
    gender_count = data_filtered['Sex'].value_counts()
    fig, ax = plt.subplots()
    gender_count.plot(kind='pie', autopct="%1.1f%%", ax=ax, colors=['#ff9999', '#66b3ff'])
    ax.set_ylabel("")
    st.pyplot(fig)

# Card 3: Drug Distribution
with col3:
    st.markdown("### 💊 Drug Distribution")
    drug_count = data_filtered['Drug'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=drug_count.index, y=drug_count.values, ax=ax, hue="viridis")
    ax.set_title("Drug Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Drug Type", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.bar_label(ax.containers[0])
    st.pyplot(fig)

# Row for Detailed Visualizations
st.markdown("---")
st.markdown("### 📈 Detailed Visualizations")

col4, col5 = st.columns(2)

with col4:
    st.markdown("#### Na_to_K vs Age")
    fig, ax = plt.subplots()
    sns.scatterplot(
        x='Age', y='Na_to_K', hue='Drug', data=data_filtered,
        palette='husl', ax=ax, s=100, edgecolor='w', alpha=0.8
    )
    ax.set_title("Na_to_K vs Age", fontsize=14, fontweight='bold')
    ax.set_xlabel("Age", fontsize=12)
    ax.set_ylabel("Na_to_K", fontsize=12)
    ax.legend(title="Drug", fontsize=10, title_fontsize=12, loc='best')
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

with col5:
    st.markdown("#### Blood Pressure and Cholesterol Levels")
    fig, ax = plt.subplots()
    sns.countplot(
        x='BP', hue='Cholesterol', data=data_filtered,
        palette='muted', ax=ax, edgecolor='black'
    )
    ax.set_title("BP and Cholesterol Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Blood Pressure Levels", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.legend(title="Cholesterol", fontsize=10, title_fontsize=12, loc='best')
    ax.grid(visible=True, which='major', linestyle='--', alpha=0.6)
    st.pyplot(fig)

# Footer Insights
st.markdown("---")
st.markdown(
    """<div style="text-align: center;">
    <h3>📌 Insights</h3>
    <ul style="list-style: none;">
        <li>🔹 Analyze the impact of age and Na_to_K ratio on drug prescriptions.</li>
        <li>🔹 Explore the relationship between blood pressure, cholesterol levels, and drug recommendations.</li>
    </ul>
    </div>""",
    unsafe_allow_html=True
)
