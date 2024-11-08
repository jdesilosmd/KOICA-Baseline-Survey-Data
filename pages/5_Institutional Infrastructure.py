import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
url = "https://onedrive.live.com/download?id=8452D606ADDC0A0F!168524&resid=8452D606ADDC0A0F!168524&ithint=file%2cxlsx&authkey=!AGclL-FtAeSoR0U&wdo=2&cid=8452d606addc0a0f"
df = pd.read_excel(url)


# Rename columns by removing the letter-number code at the start
df.columns = df.columns.str.replace(r'^[A-Z0-9]+\.\s+', '', regex=True)

# Selecting relevant columns
df5 = df.iloc[:, [3, 8, 9, 10] + list(range(111, 144))]

# Title
st. title("5. Institutional Infrastructure")

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
filtered_df5 = df5[df5['City'].isin(selected_sites)] if selected_sites else df5
filtered_df5 = filtered_df5[filtered_df5['Sex assigned at birth'].isin(selected_gender)]

if age_group == "10-14":
    filtered_df5 = filtered_df5[(filtered_df5['Age as of last birthday'] >= 10) & (filtered_df5['Age as of last birthday'] <= 14)]
elif age_group == "15-19":
    filtered_df5 = filtered_df5[(filtered_df5['Age as of last birthday'] >= 15) & (filtered_df5['Age as of last birthday'] <= 19)]

# Function to create bar graphs and tables for columns
def create_bar_graph_and_table(filtered_df, column_name):
    df_stack = filtered_df[[column_name]].stack().reset_index().rename(columns={'level_1': 'Response', 0: 'Answer'})
    df_stack = df_stack.loc[:, ['Response', 'Answer']]
    df_stack = df_stack.fillna(0)
    df_grp = df_stack.groupby(['Answer'], as_index=False).size().rename(columns={'size': 'Respondents'})

    total_responses = df_grp['Respondents'].sum()
    if display_type == "Percent":
        df_grp['Percent'] = (df_grp['Respondents'] / total_responses * 100).round(0).astype(int)
        fig = px.bar(
            df_grp,
            x='Percent',
            y='Answer',
            orientation='h',
            text=df_grp['Percent'].apply(lambda x: f"{x}%"),
            template='seaborn'
        )
        table_data = df_grp[['Answer', 'Percent']].rename(columns={'Answer': 'Response'})
    else:
        fig = px.bar(
            df_grp,
            x='Respondents',
            y='Answer',
            orientation='h',
            text=df_grp['Respondents'],
            template='seaborn'
        )
        table_data = df_grp[['Answer', 'Respondents']].rename(columns={'Answer': 'Response', 'Respondents': 'Count'})

    fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
    fig.update_layout(
        title=f"{column_name}",
        xaxis_title="Percentage" if display_type == "Percent" else "Count",
        yaxis_title="Response"
    )

    st.plotly_chart(fig)
    st.dataframe(table_data)

# Create expanders for all columns, replacing the content for the specific expander
for column in df5.columns[4:]:  # Skipping demographic columns, focusing on survey questions
    if column == "As far as you know, what types of services are provided at this facility for youth clients?":
        df_services = df5.iloc[:, 22:35]
        df_services_stack = df_services.stack().reset_index().rename(columns={'level_1': 'Service', 0: 'Answer'})
        df_services_stack = df_services_stack.loc[:, ['Service', 'Answer']]
        df_services_stack = df_services_stack.fillna(0)
        df_services_grp = df_services_stack.groupby(['Service'], as_index=False).value_counts().rename(columns={'count': 'Respondents'})

        # Filter where Answer is 1.0 and sort by Respondents
        df_services_grp_1 = df_services_grp.loc[df_services_grp['Answer'] == 1.0, ['Service', 'Answer', 'Respondents']]
        df_services_grp_1 = df_services_grp_1.sort_values('Respondents', ascending=False)

        # Plotting
        title = "As far as you know, what types of services are provided at this facility for youth clients?"
        fig = px.bar(
            df_services_grp_1,
            x='Respondents',
            y='Service',
            orientation='h',
            text='Respondents',
            title=title,
            template='seaborn'
        )
        fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
        fig.update_layout(
            xaxis_title="Number of Respondents",
            yaxis_title="Service"
        )

        with st.container():
            with st.expander(title, expanded=True):
                st.plotly_chart(fig)
                st.dataframe(df_services_grp_1[['Service', 'Respondents']])

    else:
        with st.container():
            with st.expander(f"{column}", expanded=False):
                create_bar_graph_and_table(filtered_df5, column)
for column in df5.columns[4:]:  # Skipping demographic columns, focusing on survey questions
    if column not in df5.columns[22:35]:  # Skip columns already used in the custom expander
        with st.container():
            with st.expander(f"{column}", expanded=False):
                create_bar_graph_and_table(filtered_df5, column)
