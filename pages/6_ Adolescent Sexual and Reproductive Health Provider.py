import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
url = "https://onedrive.live.com/download?id=8452D606ADDC0A0F!168524&resid=8452D606ADDC0A0F!168524&ithint=file%2cxlsx&authkey=!AGclL-FtAeSoR0U&wdo=2&cid=8452d606addc0a0f"
df = pd.read_excel(url)

# Rename columns by removing the letter-number code at the start
df.columns = df.columns.str.replace(r'^[A-Z0-9]+\.\s+', '', regex=True)

# Selecting relevant columns
df6 = df.iloc[:, [3, 8, 9, 10]+list(range(144, 154))]

# Remove duplicate columns and any column with '.1', '.2', etc., in its name
df6 = df6.loc[:, ~df6.columns.duplicated()]
df6 = df6[[col for col in df6.columns if not any(char.isdigit() and col.endswith(f".{char}") for char in "123456789")]]

# Title
st.title("6. Adolescent Sexual and Reproductive Health Provider")

# Sidebar filter options
with st.sidebar.expander("Filter Options", expanded=True):
    display_type = st.radio("Display Data As", options=["Raw", "Percent"], index=0, key="display_type_radio")
    site_selection = st.radio("Select Sites", options=["All Sites", "Samar Sites", "Southern Leyte Sites", "Manually Select"], index=0, key="site_selection_radio")

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

    selected_sites = []
    if site_selection == "All Sites":
        selected_sites = samar_sites + southern_leyte_sites
    elif site_selection == "Samar Sites":
        selected_sites = samar_sites
    elif site_selection == "Southern Leyte Sites":
        selected_sites = southern_leyte_sites
    elif site_selection == "Manually Select":
        selected_sites = st.multiselect("Select Sites", options=samar_sites + southern_leyte_sites, key="manual_site_select")

    selected_gender = st.multiselect("Select Gender", options=["male", "female"], default=["male", "female"], key="gender_multiselect")
    age_group = st.radio("Select Age Group", options=["All Age Groups", "10-14", "15-19"], key="age_group_radio")

# Apply filters to the DataFrame
filtered_df6 = df6[df6['City'].isin(selected_sites)].copy() if selected_sites else df6.copy()
filtered_df6 = filtered_df6[filtered_df6['Sex assigned at birth'].isin(selected_gender)]

if age_group == "10-14":
    filtered_df6 = filtered_df6[(filtered_df6['Age as of last birthday'] >= 10) & (filtered_df6['Age as of last birthday'] <= 14)]
elif age_group == "15-19":
    filtered_df6 = filtered_df6[(filtered_df6['Age as of last birthday'] >= 15) & (filtered_df6['Age as of last birthday'] <= 19)]

# Start visualization after "Level of Education" column
start_column = filtered_df6.columns.get_loc("Level of Education") + 1  # Start from the next column after "Level of Education"
for column in filtered_df6.columns[start_column:]:  # Start from the column after "Level of Education"
    with st.expander(column):  # Removed "Overview" from expander title
        with st.container():
            # Stack and standardize answers to capitalize "Yes" and "No"
            df6_stack = filtered_df6[[column]].stack().reset_index().rename(columns={'level_1': 'Response', 0: 'Answer'})
            df6_stack['Answer'] = df6_stack['Answer'].replace({'yes': 'Yes', 'no': 'No'})  # Capitalize Yes/No responses
            df6_stack = df6_stack.loc[:, ['Response', 'Answer']]
            df6_stack = df6_stack.fillna(0)
            df6_grp = df6_stack.groupby(['Answer'], as_index=False).size().rename(columns={'size': 'Respondents'})

            total_responses = df6_grp['Respondents'].sum()
            if display_type == "Percent":
                df6_grp['Percent'] = (df6_grp['Respondents'] / total_responses * 100).round(0).astype(int)
                fig = px.bar(
                    df6_grp,
                    x='Percent',
                    y='Answer',
                    orientation='h',
                    text=df6_grp['Percent'].apply(lambda x: f"{x}%"),
                    template='seaborn'
                )
                table_data = df6_grp[['Answer', 'Percent']].rename(columns={'Answer': 'Response'})
            else:
                fig = px.bar(
                    df6_grp,
                    x='Respondents',
                    y='Answer',
                    orientation='h',
                    text=df6_grp['Respondents'],
                    template='seaborn'
                )
                table_data = df6_grp[['Answer', 'Respondents']].rename(columns={'Answer': 'Response', 'Respondents': 'Count'})

            fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
            fig.update_layout(
                title=column,
                xaxis_title="Percentage" if display_type == "Percent" else "Count",
                yaxis_title="Response"
            )

            st.plotly_chart(fig)
            st.dataframe(table_data)
