import streamlit as st
import pandas as pd
import plotly.express as px

# Page Title
st.title("1. KOICA Site Profile")

# Load data

url = "https://onedrive.live.com/download?id=8452D606ADDC0A0F!168524&resid=8452D606ADDC0A0F!168524&ithint=file%2cxlsx&authkey=!AGclL-FtAeSoR0U&wdo=2&cid=8452d606addc0a0f"
df = pd.read_excel(url)

df1 = df.iloc[:, [3, 5, 6]]

# Define a mapping of sites to provinces
site_to_province = {
    'Maasin City': 'Southern Leyte',
    'Catbalogan': 'Samar',
    'Calbayog City': 'Samar',
    'Santa Rita': 'Samar',
    'Malitbog': 'Southern Leyte',
    'Macrohon': 'Southern Leyte',
    'Padre Burgos': 'Southern Leyte',
    'Sogod': 'Southern Leyte',
    'Basey': 'Samar',
    'Villareal': 'Samar',
    'Paranas': 'Samar',
    'Bontoc': 'Southern Leyte',
    'Liloan': 'Southern Leyte',
    'Tomas Oppus': 'Southern Leyte',
    'Calbiga': 'Samar',
    'Marabut': 'Samar',
    'San Sebastian': 'Samar',
    'Libagon': 'Southern Leyte',
    'San Jose De Buan': 'Samar',
    'Limasawa': 'Southern Leyte'
}

# Sidebar Filters
st.sidebar.header("Filters")
with st.sidebar.expander("Filter Options"):
    display_mode = st.radio("Display Mode:", ["Raw Data", "Percent"], index=0)
    
    # Select KOICA Site(s)
    koica_sites = ["All"] + list(df1.iloc[:, 0].unique())
    selected_sites = st.multiselect("Select KOICA Site(s):", options=koica_sites, default="All")
    
    # Select Gender
    genders = ["male", "female"]
    selected_genders = st.multiselect("Select Gender:", options=genders, default=genders)
    
    # Select Age Group
    age_groups = ["10-14 years", "15-19 years", "All"]
    selected_age_group = st.radio("Select Age Group:", age_groups, index=2)

# Filter data based on sidebar selections
# Note: Add logic here to filter `df1` based on `selected_sites`, `selected_genders`, and `selected_age_group` as needed

# Add Province mapping to `df1`
df1['Province'] = df1.iloc[:, 0].map(site_to_province)

# Create two aggregated DataFrames: one by Site and one by Province
df_sites = df1.iloc[:, 0].value_counts(sort=True).reset_index()
df_sites.columns = ['Site', 'Respondents']
df_sites['Percentage'] = (df_sites['Respondents'] / df_sites['Respondents'].sum() * 100).round()

df_provinces = df1['Province'].value_counts(sort=True).reset_index()
df_provinces.columns = ['Province', 'Respondents']
df_provinces['Percentage'] = (df_provinces['Respondents'] / df_provinces['Respondents'].sum() * 100).round()

# Adjust index to start from 1
df_sites.index += 1
df_provinces.index += 1

# Function to generate a bar chart
def generate_chart(data, y_column, x_column, color_column=None, is_percentage=False):
    if is_percentage:
        fig = px.bar(data, y=y_column, x=x_column, color=color_column, orientation='h', text=data[x_column].apply(lambda x: f"{x}%"))
    else:
        fig = px.bar(data, y=y_column, x=x_column, color=color_column, orientation='h', text=x_column)
    
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        showlegend=False,
        template='seaborn'
    )
    fig.update_traces(textposition='outside')
    return fig

# Display the plot and table based on the selection
with st.container():
    if display_mode == "Raw Data":
        fig = generate_chart(df_sites, y_column='Site', x_column='Respondents', color_column='Site')
        st.plotly_chart(fig)
        st.subheader("Table: Number of Respondents per KOICA Site")
        st.dataframe(df_sites[['Site', 'Respondents']], use_container_width=True)
    else:
        fig = generate_chart(df_sites, y_column='Site', x_column='Percentage', color_column='Site', is_percentage=True)
        st.plotly_chart(fig)
        st.subheader("Table: Percentage of Respondents per KOICA Site")
        st.dataframe(df_sites[['Site', 'Percentage']], use_container_width=True)
