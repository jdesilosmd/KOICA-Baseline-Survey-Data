import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
url = "https://onedrive.live.com/download?id=8452D606ADDC0A0F!168524&resid=8452D606ADDC0A0F!168524&ithint=file%2cxlsx&authkey=!AGclL-FtAeSoR0U&wdo=2&cid=8452d606addc0a0f"
df = pd.read_excel(url)



# Clean column names
df.columns = df.columns.str.replace(r'^[A-Z0-9]+\.\s+', '', regex=True)


# Select relevant columns
df3 = df.iloc[:, [3, 8, 9, 10] + list(range(26, 74))]

# Remove duplicate columns and any with unwanted suffixes
df3 = df3.loc[:, ~df3.columns.duplicated()]
df3 = df3[[col for col in df3.columns if not any(col.endswith(f".{num}") for num in range(1, 10))]]

# Normalize values: Replace underscores and capitalize strings
df3 = df3.applymap(lambda x: x.replace('_', ' ').capitalize() if isinstance(x, str) else x)

# Sidebar filter options
st.sidebar.title("Filter Options")

# Add unique keys to all widgets
display_type = st.sidebar.radio(
    "Display Data As", options=["Raw", "Percent"], index=0, key="unique_display_type"
)
site_selection = st.sidebar.radio(
    "Select Sites",
    options=["All Sites", "Samar Sites", "Southern Leyte Sites", "Manually Select"],
    key="unique_site_selection"
)

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
    selected_sites = st.sidebar.multiselect(
        "Select Sites", options=samar_sites + southern_leyte_sites, key="unique_manual_site_selection"
    )
else:
    selected_sites = []

# Additional filters
selected_gender = st.sidebar.multiselect(
    "Select Gender", options=["male", "female"], default=["male", "female"], key="unique_gender_multiselect"
)
age_group = st.sidebar.radio(
    "Select Age Group", options=["All Age Groups", "10-14", "15-19"], key="unique_age_group_radio"
)

# Apply filters
filtered_df3 = df3.copy()
filtered_df3['City'] = filtered_df3['City'].str.strip().str.title()
if selected_sites:
    filtered_df3 = filtered_df3[filtered_df3['City'].isin(selected_sites)]
if selected_gender:
    filtered_df3 = filtered_df3[filtered_df3['Sex assigned at birth'].str.lower().isin(selected_gender)]

if age_group == "10-14":
    filtered_df3 = filtered_df3[
        (filtered_df3['Age as of last birthday'] >= 10) & (filtered_df3['Age as of last birthday'] <= 14)
    ]
elif age_group == "15-19":
    filtered_df3 = filtered_df3[
        (filtered_df3['Age as of last birthday'] >= 15) & (filtered_df3['Age as of last birthday'] <= 19)
    ]

# Display title
st.title("3. Reproductive Health Seeking Behavior of Adolescents")

# Function to create expanders from column indices and titles
def create_expanders_from_info(expander_info, df, display_type):
    for col_idx, info in expander_info.items():
        col_name = df.columns[col_idx]
        col_data = df[col_name].dropna().apply(
            lambda x: x.replace('_', ' ').title().replace("Don t know", "I Don't Know") if isinstance(x, str) else x
        )
        col_counts = col_data.value_counts().reset_index()
        col_counts.columns = ['Response', 'Count']

        if display_type == "Percent":
            col_counts['Percent'] = (col_counts['Count'] / col_counts['Count'].sum()) * 100
            col_counts['Percent'] = col_counts['Percent'].round(2)

        # Sort data by Count or Percent in descending order
        col_counts = col_counts.sort_values(by='Count' if display_type == "Raw" else 'Percent', ascending=False)

        if col_counts.empty:
            continue

        y_axis = 'Percent' if display_type == "Percent" else 'Count'
        fig = px.bar(
            col_counts,
            x=y_axis,
            y='Response',
            orientation='h',
            text=y_axis,
            template='plotly_white',
            category_orders={"Response": col_counts["Response"].tolist()}  # Ensure bar order matches table order
        )
        fig.update_traces(
            marker_line_color='black',
            marker_line_width=1,
            texttemplate='%{text:.2f}%' if display_type == "Percent" else '%{text}',
            textposition='outside'
        )
        fig.update_layout(
            title=info["title"],
            xaxis_title=y_axis,
            yaxis_title="Response"
        )

        with st.expander(info["title"]):
            st.plotly_chart(fig)
            st.dataframe(col_counts if display_type == "Raw" else col_counts[['Response', 'Percent']])

def create_expander_and_graph(start_col, end_col, expander_title, graph_title, display_type):
    df_subset = filtered_df3.iloc[:, list(range(start_col, end_col + 1))]
    df_subset.rename(columns=lambda x: x.split('/')[-1] if '/' in x else x, inplace=True)
    df_subset = df_subset.replace({"Yes": 1, "No": 0})

    df_stack = df_subset.stack().reset_index().rename(columns={'level_1': 'Category', 0: 'Answer'})
    df_stack = df_stack[df_stack['Answer'] == 1.0]

    df_grouped = (
        df_stack.groupby('Category', as_index=False)
        .size()
        .rename(columns={'size': 'Respondents'})
        .sort_values('Respondents', ascending=False)
        .reset_index(drop=True)
    )

    if display_type == "Percent":
        df_grouped['Percent'] = (df_grouped['Respondents'] / df_grouped['Respondents'].sum()) * 100
        df_grouped['Percent'] = df_grouped['Percent'].round(2)

    y_axis = 'Percent' if display_type == "Percent" else 'Respondents'
    with st.expander(expander_title):
        fig = px.bar(
            df_grouped,
            x=y_axis,
            y='Category',
            orientation='h',
            text=y_axis,
            template='plotly_white',
            category_orders={"Category": df_grouped["Category"].tolist()}  # Ensure bar order matches table order
        )
        fig.update_traces(
            marker_line_color='black',
            marker_line_width=1,
            texttemplate='%{text:.2f}%' if display_type == "Percent" else '%{text}',
            textposition='outside'
        )
        fig.update_layout(
            title=graph_title,
            xaxis_title=y_axis,
            yaxis_title="Category"
        )
        st.plotly_chart(fig)
        st.dataframe(df_grouped if display_type == "Raw" else df_grouped[['Category', 'Percent']].rename(columns={'Category': 'Source'}))


# Define specific columns for expanders
expander_info = {
    4: {"title": filtered_df3.columns[4]},
    5: {"title": filtered_df3.columns[5]},
    6: {"title": filtered_df3.columns[6]},
    7: {"title": filtered_df3.columns[7]},
    8: {"title": filtered_df3.columns[8]},
    9: {"title": filtered_df3.columns[9]},
    10: {"title": filtered_df3.columns[10]},
    11: {"title": filtered_df3.columns[11]},
    12: {"title": filtered_df3.columns[12]},
    23: {"title": filtered_df3.columns[23]},
    24: {"title": filtered_df3.columns[24]},
    25: {"title": filtered_df3.columns[25]},
    26: {"title": filtered_df3.columns[26]},
    27: {"title": filtered_df3.columns[27]},
    28: {"title": filtered_df3.columns[28]},
    36: {"title": filtered_df3.columns[36]},
    37: {"title": filtered_df3.columns[37]},


}

# Create additional expanders for the specified ranges
create_expanders_from_info(expander_info, filtered_df3, display_type)
create_expander_and_graph(12, 22, "How did you hear about this facility?", "How did you hear about this facility?", display_type)
create_expander_and_graph(28, 34, "What subject(s) is/are covered in this material?", "What subject(s) is/are covered in this material?", display_type)
# create_expander_and_graph(37, 49, "How much did you pay for the following services", "How much did you pay for the following services", display_type)
