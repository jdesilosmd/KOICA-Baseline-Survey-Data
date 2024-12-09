import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
url = "https://onedrive.live.com/download?id=8452D606ADDC0A0F!168524&resid=8452D606ADDC0A0F!168524&ithint=file%2cxlsx&authkey=!AGclL-FtAeSoR0U&wdo=2&cid=8452d606addc0a0f"
df = pd.read_excel(url)


# Rename columns by removing the letter-number code at the start
df.columns = df.columns.str.replace(r'^[A-Z0-9]+\.\s+', '', regex=True)

# Selecting relevant columns
df7 = df.iloc[:, [3, 8, 9, 10] + list(range(154, 196))]

# Remove duplicate columns and any column with '.1', '.2', etc., in its name
df7 = df7.loc[:, ~df7.columns.duplicated()]
df7 = df7[[col for col in df7.columns if not any(char.isdigit() and col.endswith(f".{char}") for char in "123456789")]]

# Title
st.title("7. Self-rating of Knowledge about ASRH")

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
filtered_df7 = df7[df7['City'].isin(selected_sites)].copy() if selected_sites else df7.copy()
filtered_df7 = filtered_df7[filtered_df7['Sex assigned at birth'].isin(selected_gender)]

if age_group == "10-14":
    filtered_df7 = filtered_df7[(filtered_df7['Age as of last birthday'] >= 10) & (filtered_df7['Age as of last birthday'] <= 14)]
elif age_group == "15-19":
    filtered_df7 = filtered_df7[(filtered_df7['Age as of last birthday'] >= 15) & (filtered_df7['Age as of last birthday'] <= 19)]

# Function to calculate percentages
def calculate_percent(df, group_col, count_col):
    group_total = df[count_col].sum()
    df['Percentage'] = (df[count_col] / group_total * 100).round(2).apply(lambda x: f"{x}%") if group_total > 0 else 0
    return df

# Helper function to plot data
def plot_data(df, group_col, count_col, title):
    fig = px.bar(
        df,
        x='Percentage' if display_type == "Percent" else count_col,
        y=group_col,
        orientation='h',
        text='Percentage' if display_type == "Percent" else count_col,
        template='seaborn'
    )
    fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
    fig.update_layout(
        title=title,
        xaxis_title="Percentage" if display_type == "Percent" else "Count",
        yaxis_title=group_col
    )
    return fig

# Section 1: "Ways to Prevent Pregnancy"
df_methods = filtered_df7.iloc[:, list(range(5, 11))]
df_methods.rename(columns=lambda x: x.split('/')[-1], inplace=True)
df_methods_stack = df_methods.stack().reset_index().rename(columns={'level_1': 'Method', 0: 'Answer'})
df_methods_stack = df_methods_stack[df_methods_stack['Answer'] == 1.0]
df_methods_grp = df_methods_stack.groupby('Method', as_index=False).size().rename(columns={'size': 'Respondents'}).sort_values('Respondents')

if display_type == "Percent":
    df_methods_grp = calculate_percent(df_methods_grp, 'Method', 'Respondents')

with st.expander("What are the ways you know to prevent pregnancy?"):
    st.plotly_chart(plot_data(df_methods_grp, 'Method', 'Respondents', "Ways to Prevent Pregnancy"))
    st.dataframe(df_methods_grp.rename(columns={'Method': 'Prevention Method', 'Respondents': 'Count', 'Percentage': 'Percent'}))

# Section 2: Expanders for individual questions
expander_info = {
    11: {"order": ["Yes", "No", "I Don't Know"], "title": "Are there any diseases that can be transmitted through sexual intercourse?"},
    12: {"order": ["Yes", "No", "I Don't Know"], "title": "Have you heard of HIV/AIDS?"},
    26: {"order": ["Yes", "No"], "title": "Do you know any ways you can protect yourself from STIs including HIV/AIDS?"}
}

for col_idx, info in expander_info.items():
    col_name = filtered_df7.columns[col_idx]
    col_data = filtered_df7[col_name].dropna().apply(lambda x: x.replace('_', ' ').title().replace("Don T Know", "I Don't Know"))
    col_counts = col_data.value_counts().reset_index()
    col_counts.columns = ['Response', 'Count']

    if display_type == "Percent":
        col_counts = calculate_percent(col_counts, 'Response', 'Count')

    with st.expander(info["title"]):
        st.plotly_chart(plot_data(col_counts, 'Response', 'Count', info["title"]))
        st.dataframe(col_counts.rename(columns={'Response': 'Answer', 'Count': 'Count', 'Percentage': 'Percent'}))

# Section 3: STI Symptoms
df_sti_symptoms = filtered_df7.iloc[:, list(range(14, 26))]
df_sti_symptoms.rename(columns=lambda x: x.split('/')[-1], inplace=True)
df_sti_symptoms_stack = df_sti_symptoms.stack().reset_index().rename(columns={'level_1': 'Symptom', 0: 'Answer'})
df_sti_symptoms_stack = df_sti_symptoms_stack[df_sti_symptoms_stack['Answer'] == 1.0]
df_sti_symptoms_grp = df_sti_symptoms_stack.groupby('Symptom', as_index=False).size().rename(columns={'size': 'Respondents'}).sort_values('Respondents')

if display_type == "Percent":
    df_sti_symptoms_grp = calculate_percent(df_sti_symptoms_grp, 'Symptom', 'Respondents')

with st.expander("Common signs and symptoms of STIs"):
    st.plotly_chart(plot_data(df_sti_symptoms_grp, 'Symptom', 'Respondents', "Common STI Symptoms"))
    st.dataframe(df_sti_symptoms_grp.rename(columns={'Symptom': 'STI Symptom', 'Respondents': 'Count', 'Percentage': 'Percent'}))

# Section 4: Ways to Get HIV/AIDS
df_hiv_ways = filtered_df7.iloc[:, list(range(28, 33))]
df_hiv_ways.rename(columns=lambda x: x.split('/')[-1], inplace=True)
df_hiv_ways_stack = df_hiv_ways.stack().reset_index().rename(columns={'level_1': 'Way', 0: 'Answer'})
df_hiv_ways_stack = df_hiv_ways_stack[df_hiv_ways_stack['Answer'] == 1.0]
df_hiv_ways_grp = df_hiv_ways_stack.groupby('Way', as_index=False).size().rename(columns={'size': 'Respondents'}).sort_values('Respondents')

if display_type == "Percent":
    df_hiv_ways_grp = calculate_percent(df_hiv_ways_grp, 'Way', 'Respondents')

with st.expander("Ways to Get HIV/AIDS"):
    st.plotly_chart(plot_data(df_hiv_ways_grp, 'Way', 'Respondents', "Ways to Get HIV/AIDS"))
    st.dataframe(df_hiv_ways_grp.rename(columns={'Way': 'HIV/AIDS Way', 'Respondents': 'Count', 'Percentage': 'Percent'}))

# Repeat similar logic for other sections (if applicable)
