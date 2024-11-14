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

# Define specific ordering for selected expanders
yes_no_idk_order = ["Yes", "No", "I Don't Know"]
yes_no_order = ["Yes", "No"]

# 1. Stack columns 5-10: "What are the ways you know to prevent pregnancy?"
df_methods = filtered_df7.iloc[:, list(range(5, 11))]
df_methods.rename(columns=lambda x: x.split('/')[-1], inplace=True)  # Use only the part after '/' in the name
df_methods_stack = df_methods.stack().reset_index().rename(columns={'level_1': 'Method', 0: 'Answer'})
df_methods_stack = df_methods_stack[df_methods_stack['Answer'] == 1.0]
df_methods_grp = df_methods_stack.groupby('Method', as_index=False).size().rename(columns={'size': 'Respondents'}).sort_values('Respondents')

with st.expander("What are the ways you know to prevent pregnancy?"):
    fig = px.bar(
        df_methods_grp,
        x='Respondents',
        y='Method',
        orientation='h',
        text='Respondents',
        template='seaborn'
    )
    fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
    fig.update_layout(
        title="Ways to Prevent Pregnancy",
        xaxis_title="Count",
        yaxis_title="Prevention Method"
    )
    st.plotly_chart(fig)
    st.dataframe(df_methods_grp.rename(columns={'Method': 'Prevention Method', 'Respondents': 'Count'}))

# 2. Individual expanders for columns 11, 12, 26, and 33 with text transformations and ordering adjustments
expander_info = {
    11: {"order": yes_no_idk_order, "title": "As far as you know, are there any diseases that can be transmitted through sexual intercourse?"},
    12: {"order": yes_no_idk_order, "title": "Have you heard of HIV/AIDS?"},
    26: {"order": yes_no_order, "title": "Do you know any ways you can protect yourself from STIs including HIV/AIDS?"},
    33: {"order": None, "title": None}  # No specific order, follows the natural order
}

for col_idx, info in expander_info.items():
    col_name = filtered_df7.columns[col_idx]
    col_data = filtered_df7[col_name].dropna().apply(lambda x: x.replace('_', ' ').title().replace("Don T Know", "I Don't Know"))
    col_counts = col_data.value_counts().reset_index()
    col_counts.columns = ['Response', 'Count']
    
    if info["title"]:
        expander_title = info["title"]
    else:
        expander_title = col_name

    # Sort data by specified order if provided, else sort by count ascending
    if info["order"]:
        fig = px.bar(
            col_counts,
            x='Count',
            y='Response',
            orientation='h',
            text='Count',
            template='seaborn',
            category_orders={'Response': info["order"]}
        )
    else:
        col_counts = col_counts.sort_values('Count')
        fig = px.bar(
            col_counts,
            x='Count',
            y='Response',
            orientation='h',
            text='Count',
            template='seaborn'
        )

    fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
    fig.update_layout(
        title=expander_title,
        xaxis_title="Count",
        yaxis_title="Response"
    )
    with st.expander(expander_title):
        st.plotly_chart(fig)
        st.dataframe(col_counts)

# 3. Stack columns 14-25: "Signs and symptoms of sexually transmitted infections"
df_sti_symptoms = filtered_df7.iloc[:, list(range(14, 26))]
df_sti_symptoms.rename(columns=lambda x: x.split('/')[-1], inplace=True)
df_sti_symptoms_stack = df_sti_symptoms.stack().reset_index().rename(columns={'level_1': 'Symptom', 0: 'Answer'})
df_sti_symptoms_stack = df_sti_symptoms_stack[df_sti_symptoms_stack['Answer'] == 1.0]
df_sti_symptoms_grp = df_sti_symptoms_stack.groupby('Symptom', as_index=False).size().rename(columns={'size': 'Respondents'}).sort_values('Respondents')

with st.expander("From what you’ve heard or read, what are some common signs and symptoms of sexually transmitted infections?"):
    fig = px.bar(
        df_sti_symptoms_grp,
        x='Respondents',
        y='Symptom',
        orientation='h',
        text='Respondents',
        template='seaborn'
    )
    fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
    fig.update_layout(
        title="Common Signs and Symptoms of STIs",
        xaxis_title="Count",
        yaxis_title="Symptom"
    )
    st.plotly_chart(fig)
    st.dataframe(df_sti_symptoms_grp.rename(columns={'Symptom': 'STI Symptom', 'Respondents': 'Count'}))

# 4. Stack columns 28-32: "Ways to get HIV/AIDS"
df_hiv_ways = filtered_df7.iloc[:, list(range(28, 33))]
df_hiv_ways.rename(columns=lambda x: x.split('/')[-1], inplace=True)
df_hiv_ways_stack = df_hiv_ways.stack().reset_index().rename(columns={'level_1': 'Way', 0: 'Answer'})
df_hiv_ways_stack = df_hiv_ways_stack[df_hiv_ways_stack['Answer'] == 1.0]
df_hiv_ways_grp = df_hiv_ways_stack.groupby('Way', as_index=False).size().rename(columns={'size': 'Respondents'}).sort_values('Respondents')

with st.expander("As far as you know, what are the ways to get HIV/AIDS"):
    fig = px.bar(
        df_hiv_ways_grp,
        x='Respondents',
        y='Way',
        orientation='h',
        text='Respondents',
        template='seaborn'
    )
    fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
    fig.update_layout(
        title="Ways to Get HIV/AIDS",
        xaxis_title="Count",
        yaxis_title="Way"
    )
    st.plotly_chart(fig)
    st.dataframe(df_hiv_ways_grp.rename(columns={'Way': 'Way to Get HIV/AIDS', 'Respondents': 'Count'}))

# 5. Stack columns 35-45: "Ways of protecting from STIs"
df_sti_protection = filtered_df7.iloc[:, list(range(35, 46))]
df_sti_protection.rename(columns=lambda x: x.split('/')[-1], inplace=True)  # Use only the part after '/' in the name
df_sti_protection_stack = df_sti_protection.stack().reset_index().rename(columns={'level_1': 'Protection Method', 0: 'Answer'})
df_sti_protection_stack = df_sti_protection_stack[df_sti_protection_stack['Answer'] == 1.0]
df_sti_protection_grp = df_sti_protection_stack.groupby('Protection Method', as_index=False).size().rename(columns={'size': 'Respondents'}).sort_values('Respondents')

with st.expander("If yes, what are the ways of protecting yourself from STIs?"):
    fig = px.bar(
        df_sti_protection_grp,
        x='Respondents',
        y='Protection Method',
        orientation='h',
        text='Respondents',
        template='seaborn'
    )
    fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
    fig.update_layout(
        title="Ways of Protecting from STIs",
        xaxis_title="Count",
        yaxis_title="Protection Method"
    )
    st.plotly_chart(fig)
    st.dataframe(df_sti_protection_grp.rename(columns={'Protection Method': 'Protection Method', 'Respondents': 'Count'}))
