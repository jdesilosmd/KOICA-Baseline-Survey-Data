import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
url = "https://onedrive.live.com/download?id=8452D606ADDC0A0F!168524&resid=8452D606ADDC0A0F!168524&ithint=file%2cxlsx&authkey=!AGclL-FtAeSoR0U&wdo=2&cid=8452d606addc0a0f"
df = pd.read_excel(url)


# Clean column names
df.columns = df.columns.str.replace(r'^[A-Z0-9]+\.\s+', '', regex=True)

# Select relevant columns
df10 = df.iloc[:, [3, 8, 9, 10] + list(range(406, 547))]

# Remove duplicate columns and any with unwanted suffixes
df10 = df10[[col for col in df10.columns if not any(col.endswith(f".{num}") for num in range(1, 10))]]

# Normalize values: Replace underscores and capitalize strings
df10 = df10.applymap(lambda x: x.replace('_', ' ').capitalize() if isinstance(x, str) else x)

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
filtered_df10 = df10.copy()
filtered_df10['City'] = filtered_df10['City'].str.strip().str.title()
if selected_sites:
    filtered_df10 = filtered_df10[filtered_df10['City'].isin(selected_sites)]
if selected_gender:
    filtered_df10 = filtered_df10[filtered_df10['Sex assigned at birth'].str.lower().isin(selected_gender)]

if age_group == "10-14":
    filtered_df10 = filtered_df10[
        (filtered_df10['Age as of last birthday'] >= 10) & (filtered_df10['Age as of last birthday'] <= 14)
    ]
elif age_group == "15-19":
    filtered_df10 = filtered_df10[
        (filtered_df10['Age as of last birthday'] >= 15) & (filtered_df10['Age as of last birthday'] <= 19)
    ]

# Display title
st.title("10. Attitudes, Beliefs and Values towards ASRH and Adolescent Pregnancy")

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

# Define specific columns for expanders
expander_info = {
    4: {"title": filtered_df10.columns[4]},
    5: {"title": filtered_df10.columns[5]},
    73: {"title": filtered_df10.columns[73]},
    98: {"title": filtered_df10.columns[98]},
    108: {"title": filtered_df10.columns[108]},
    111: {"title": filtered_df10.columns[111]},
    120: {"title": filtered_df10.columns[120]},
    121: {"title": filtered_df10.columns[121]},
    122: {"title": filtered_df10.columns[122]},
    123: {"title": filtered_df10.columns[123]},
    124: {"title": filtered_df10.columns[124]},
    125: {"title": filtered_df10.columns[125]},
    126: {"title": filtered_df10.columns[126]},

    
}

# Call the function for specific expanders
create_expanders_from_info(expander_info, filtered_df10)

# Helper function to create expanders and graphs for given column ranges
def create_expander_and_graph(start_col, end_col, expander_title, graph_title):
    df_subset = filtered_df10.iloc[:, list(range(start_col, end_col + 1))]
    df_subset.rename(columns=lambda x: x.split('/')[-1] if '/' in x else x, inplace=True)

    # Convert "Yes" to 1 and "No" to 0 if they appear in the responses
    df_subset = df_subset.replace({"Yes": 1, "No": 0})

    # Stack the columns and filter for answers marked as 1.0 (indicating a positive response)
    df_stack = df_subset.stack().reset_index().rename(columns={'level_1': 'Category', 0: 'Answer'})
    df_stack = df_stack[df_stack['Answer'] == 1.0]

    # Group by category and count respondents
    df_grouped = (
        df_stack.groupby('Category', as_index=False)
        .size()
        .rename(columns={'size': 'Respondents'})
        .sort_values('Respondents', ascending=False)
        .reset_index(drop=True)
    )

    # Display results in an expander
    with st.expander(expander_title):
        fig = px.bar(
            df_grouped,
            x='Respondents',
            y='Category',
            orientation='h',
            text='Respondents',
            template='plotly_white'
        )
        fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
        fig.update_layout(
            title=graph_title,
            xaxis_title="Count",
            yaxis_title="Category"
        )
        st.plotly_chart(fig)
        st.dataframe(df_grouped.rename(columns={'Category': 'Source', 'Respondents': 'Count'}))

# Create additional expanders for the specified ranges
create_expander_and_graph(9, 16, "What are the advantages to using condoms?", "What are the advantages to using condoms?")
create_expander_and_graph(20, 27, "What are the disadvantages to using condoms?", "What are the disadvantages to using condoms?")
create_expander_and_graph(31, 36, "What important steps do you know on how to use a condom?", "What important steps do you know on how to use a condom?")
create_expander_and_graph(42, 51, "When do you think you would use a condom?", "When do you think you would use a condom?")
create_expander_and_graph(55, 64, "When do you think most girls your age would use condoms?", "When do you think most girls your age would use condoms?")
create_expander_and_graph(68, 72, "What are the ways to prevent pregnancy in case a woman had unplanned, unprotected intercourse or sexual assault?", "What are the ways to prevent pregnancy in case a woman had unplanned, unprotected intercourse or sexual assault?")
create_expander_and_graph(76, 85, "Are there any good things about having a child while you are a teenager?", "Are there any good things about having a child while you are a teenager?")
create_expander_and_graph(90, 97, "Are there any reasons why pregnancy/childbirth should be avoided when you are a teenager?", "Are there any reasons why pregnancy/childbirth should be avoided when you are a teenager?")
create_expander_and_graph(100, 107, "Why are you not ready to become pregnant?", "Why are you not ready to become pregnant?")
create_expander_and_graph(114, 119, "Why is it difficult for unmarried girls to obtain contraceptive methods?", "Why is it difficult for unmarried girls to obtain contraceptive methods?")
create_expander_and_graph(128, 145, "Other ASRH Beliefs", "Other ASRH Beliefs")