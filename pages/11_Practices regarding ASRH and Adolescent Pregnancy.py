import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
url = "https://onedrive.live.com/download?id=8452D606ADDC0A0F!168524&resid=8452D606ADDC0A0F!168524&ithint=file%2cxlsx&authkey=!AGclL-FtAeSoR0U&wdo=2&cid=8452d606addc0a0f"
df = pd.read_excel(url)


# Clean column names
df.columns = df.columns.str.replace(r'^[A-Z0-9]+\.\s+', '', regex=True)

# Select relevant columns
df11 = df.iloc[:, [3, 8, 9, 10] + list(range(547, 591))]

# Remove duplicate columns and any with unwanted suffixes
df11 = df11[[col for col in df11.columns if not any(col.endswith(f".{num}") for num in range(1, 10))]]

# Normalize values: Replace underscores and capitalize strings
df11 = df11.applymap(lambda x: x.replace('_', ' ').capitalize() if isinstance(x, str) else x)

# Sidebar filter options
st.sidebar.title("Filter Options")
display_type = st.sidebar.radio("Display Data As", options=["Raw", "Percent"], index=0)
site_selection = st.sidebar.radio("Select Sites", options=["All Sites", "Samar Sites", "Southern Leyte Sites", "Manually Select"])

# Define actual sites
samar_sites = [
    "Calbayog City", "Catbalogan", "Santa Rita", "Basey",
    "Villareal", "Paranas", "Calbiga", "Marabut",
    "San Sebastian", "San Jose de Buan"
]
southern_leyte_sites = [
    "Maasin City", "Macrohon", "Padre Burgos", "Sogod",
    "Malitbog", "Bontoc", "Liloan", "Tomas Oppus",
    "Libagon", "Limasawa"
]

# Determine selected sites
if site_selection == "All Sites":
    selected_sites = samar_sites + southern_leyte_sites
elif site_selection == "Samar Sites":
    selected_sites = samar_sites
elif site_selection == "Southern Leyte Sites":
    selected_sites = southern_leyte_sites
elif site_selection == "Manually Select":
    selected_sites = st.sidebar.multiselect("Select Sites", options=samar_sites + southern_leyte_sites)
else:
    selected_sites = []

# Additional filters
selected_gender = st.sidebar.multiselect("Select Gender", options=["male", "female"], default=["male", "female"])
age_group = st.sidebar.radio("Select Age Group", options=["All Age Groups", "10-14", "15-19"])

# Apply filters
filtered_df11 = df11.copy()
filtered_df11['City'] = filtered_df11['City'].str.strip().str.title()
if selected_sites:
    filtered_df11 = filtered_df11[filtered_df11['City'].isin(selected_sites)]
if selected_gender:
    filtered_df11 = filtered_df11[filtered_df11['Sex assigned at birth'].str.lower().isin(selected_gender)]

if age_group == "10-14":
    filtered_df11 = filtered_df11[
        (filtered_df11['Age as of last birthday'] >= 10) & (filtered_df11['Age as of last birthday'] <= 14)
    ]
elif age_group == "15-19":
    filtered_df11 = filtered_df11[
        (filtered_df11['Age as of last birthday'] >= 15) & (filtered_df11['Age as of last birthday'] <= 19)
    ]

# Display title
st.title("11. Practices regarding ASRH and Adolescent Pregnancy")

# Function to create expanders from column indices and titles
def create_expanders_from_info(expander_info, df):
    """
    Create expanders and bar charts for specific column indices.

    Parameters:
    - expander_info (dict): A dictionary with column indices and titles.
    - df (DataFrame): The filtered DataFrame to process.
    """
    for col_idx, info in expander_info.items():
        col_name = df.columns[col_idx]
        col_data = df[col_name].dropna().apply(
            lambda x: x.replace('_', ' ').title().replace("Don t know", "I Don't Know") if isinstance(x, str) else x
        )
        col_counts = col_data.value_counts().reset_index()
        col_counts.columns = ['Response', 'Count']

        # Skip empty columns
        if col_counts.empty:
            continue

        # Create a bar chart for the column
        fig = px.bar(
            col_counts,
            x='Count',
            y='Response',
            orientation='h',
            text='Count',
            template='plotly_white'
        )
        fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
        fig.update_layout(
            title=info["title"],
            xaxis_title="Count",
            yaxis_title="Response"
        )

        # Display the chart and data in an expander
        with st.expander(info["title"]):
            st.plotly_chart(fig)
            st.dataframe(col_counts)

st.write(filtered_df11.columns)