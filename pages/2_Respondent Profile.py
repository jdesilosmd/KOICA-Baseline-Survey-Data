import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
# url = "https://onedrive.live.com/download?resid=8452D606ADDC0A0F!142073&ithint=file%2cxlsx&authkey=!ALoiLKebKzNyaSk&wdo=2&cid=8452d606addc0a0f"
url = "https://onedrive.live.com/download?id=8452D606ADDC0A0F!168524&resid=8452D606ADDC0A0F!168524&ithint=file%2cxlsx&authkey=!AGclL-FtAeSoR0U&wdo=2&cid=8452d606addc0a0f"
df = pd.read_excel(url)

df2 = df.iloc[:, [3] + list(range(8, 26))]

# Column renaming
column_renaming = {
    df2.columns[0]: "City",
    df2.columns[1]: "Age",
    df2.columns[2]: "Sex Assigned at Birth",
    df2.columns[3]: "Level of Education",
    df2.columns[4]: "School Status",
    df2.columns[5]: "Marital Status",
    df2.columns[6]: "Residence",
    df2.columns[7]: "Risk Status",
    df2.columns[8]: "Work Status",
    df2.columns[9]: "Religious Denomination",
    df2.columns[10]: "Household Income",
    df2.columns[11]: "Gender Identity",
    df2.columns[12]: "Sexual Preference",
    df2.columns[13]: "Primary Caregiver",
    df2.columns[14]: "Other Caregiver",
    df2.columns[15]: "Close Friends",
    df2.columns[16]: "Number of Close Friends",
    df2.columns[17]: "Regular Contact with Close Friends",
    df2.columns[18]: "Parents were Teenage Parents"
}

# Apply column renaming
df2.rename(columns=column_renaming, inplace=True)

# Modify specific values in Religious Denomination
religion_mapping = {
    "catholic": "Catholic",
    "other christian": "Non-Catholic Christian",
    "others none": "Others"
}
df2["Religious Denomination"] = df2["Religious Denomination"].replace(religion_mapping)

# Define site groups
samar_sites = ['Marabut', 'Calbiga', 'Basey', 'Paranas', 'Santa Rita', 'San Jose De Buan', 'Calbayog City', 'Villareal', 'San Sebastian', 'Catbalogan']
southern_leyte_sites = ['Maasin City', 'Liloan', 'Padre Burgos', 'Limasawa', 'Libagon', 'Tomas Oppus', 'Sogod', 'Malitbog', 'Macrohon', 'Bontoc']
all_sites = df2['City'].unique().tolist()

# Sidebar Expander for Filters
with st.sidebar:
    st.write("**Filters**")
    with st.expander("Filter Options"):
        # Data Mode Selection
        data_mode = st.radio("Display Mode:", ["Raw Data", "Percent"], index=0, key="global_display_mode")

        # KOICA Site Selection using Radio Buttons
        site_mode = st.radio("KOICA Site Selection:", ["All", "Samar", "Southern Leyte", "Manually Select"], index=0)
        if site_mode == "All":
            selected_sites = all_sites
        elif site_mode == "Samar":
            selected_sites = samar_sites
        elif site_mode == "Southern Leyte":
            selected_sites = southern_leyte_sites
        else:
            selected_sites = st.multiselect("Select KOICA Site(s):", options=all_sites)

        # Gender Selection
        selected_gender = st.multiselect("Select Gender:", options=["male", "female"], default=["male", "female"])

        # Age Group Selection with "All Age Groups" option
        age_group = st.radio("Select Age Group:", ["All Age Groups", "10-14 years", "15-19 years"], index=0)

# Apply Filters
filtered_df = df2[(df2['City'].isin(selected_sites)) & (df2['Sex Assigned at Birth'].isin(selected_gender))]

if age_group == "10-14 years":
    filtered_df = filtered_df[filtered_df['Age'].between(10, 14)]
elif age_group == "15-19 years":
    filtered_df = filtered_df[filtered_df['Age'].between(15, 19)]
# No age filter is applied if "All Age Groups" is selected

# Helper function for creating bar graphs and tables
def create_bar_graph_and_table(df, column_name, display_mode):
    counts = df[column_name].value_counts(normalize=(display_mode == "Percent")).reset_index()
    counts.columns = [column_name, "Percent" if display_mode == "Percent" else "Count"]
    if display_mode == "Percent":
        counts['Percent'] = (counts['Percent'] * 100).round(0).astype(int).astype(str) + '%'
    fig = px.bar(counts, x="Percent" if display_mode == "Percent" else "Count", y=column_name, orientation='h',
                 title=f"{column_name} of Respondents", text="Percent" if display_mode == "Percent" else "Count",
                 template="seaborn")
    fig.update_traces(marker_line_color="black", marker_line_width=1, texttemplate='%{text}')
    fig.update_layout(xaxis_title="% of Respondents" if display_mode == "Percent" else "# of Respondents", 
                      yaxis_title=column_name)
    counts.index = counts.index + 1
    return fig, counts

# ----------- Location Analysis -----------
with st.container():
    with st.expander("Location Analysis"):
        fig_age = px.histogram(filtered_df, x="Age", nbins=filtered_df["Age"].nunique(), template="seaborn")
        fig_age.update_traces(marker=dict(color="lightblue", line=dict(color="black", width=1)), texttemplate='%{y}')
        fig_age.update_layout(xaxis_title="Age in Years", yaxis_title="# of Respondents", bargap=0.2)
        st.plotly_chart(fig_age, use_container_width=True)

        st.subheader("Age Distribution Table")
        age_counts = filtered_df['Age'].value_counts().reset_index().rename(columns={'index': 'Age', 'Age': 'Count'})
        age_counts.index = age_counts.index + 1
        st.dataframe(age_counts, height=300)

# ----------- Gender Analysis -----------
with st.container():
    with st.expander("Gender Analysis"):
        fig_sex_at_birth, sex_at_birth_counts = create_bar_graph_and_table(filtered_df, "Sex Assigned at Birth", data_mode)
        st.plotly_chart(fig_sex_at_birth, use_container_width=True)
        st.subheader("Sex Assigned at Birth Table")
        st.dataframe(sex_at_birth_counts, height=300)
        
        fig_gender_identity, gender_identity_counts = create_bar_graph_and_table(filtered_df, "Gender Identity", data_mode)
        st.plotly_chart(fig_gender_identity, use_container_width=True)
        st.subheader("Gender Identity Table")
        st.dataframe(gender_identity_counts, height=300)

        fig_sexual_preference, sexual_preference_counts = create_bar_graph_and_table(filtered_df, "Sexual Preference", data_mode)
        st.plotly_chart(fig_sexual_preference, use_container_width=True)
        st.subheader("Sexual Preference Table")
        st.dataframe(sexual_preference_counts, height=300)

# ----------- Household Income -----------
with st.container():
    with st.expander("Household Income"):
        fig_income = px.histogram(filtered_df, x="Household Income", template="seaborn")
        fig_income.update_traces(marker=dict(color="#FFA500", line=dict(color="black", width=1)), texttemplate='%{y}')
        fig_income.update_layout(xaxis_title="Household Income (Pesos)", yaxis_title="# of Respondents", bargap=0.2)
        st.plotly_chart(fig_income, use_container_width=True)

        st.subheader("Household Income Table")
        income_counts = filtered_df['Household Income'].value_counts().reset_index().rename(columns={'index': 'Household Income (Pesos)', 'Household Income': 'Count'})
        income_counts.index = income_counts.index + 1
        st.dataframe(income_counts, height=300)

# ----------- Educational Background -----------
with st.container():
    with st.expander("Educational Background"):
        fig_level, level_counts = create_bar_graph_and_table(filtered_df, "Level of Education", data_mode)
        st.plotly_chart(fig_level, use_container_width=True)
        st.subheader("Level of Education Table")
        st.dataframe(level_counts, height=300)

        fig_status, status_counts = create_bar_graph_and_table(filtered_df, "School Status", data_mode)
        st.plotly_chart(fig_status, use_container_width=True)
        st.subheader("School Status Table")
        st.dataframe(status_counts, height=300)

# ----------- Primary Caregiver Analysis -----------
with st.container():
    with st.expander("Primary Caregiver"):
        fig_primary_caregiver, primary_caregiver_counts = create_bar_graph_and_table(filtered_df, "Primary Caregiver", data_mode)
        st.plotly_chart(fig_primary_caregiver, use_container_width=True)
        st.subheader("Primary Caregiver Table")
        st.dataframe(primary_caregiver_counts, height=300)

        fig_other_caregiver, other_caregiver_counts = create_bar_graph_and_table(filtered_df, "Other Caregiver", data_mode)
        st.plotly_chart(fig_other_caregiver, use_container_width=True)
        st.subheader("Other Caregiver Table")
        st.dataframe(other_caregiver_counts, height=300)

# Additional Sections: Marital Status, Residence, Risk Status, Work Status, Religion
for section in ["Marital Status", "Residence", "Risk Status", "Work Status", "Religious Denomination"]:
    with st.container():
        with st.expander(section):
            fig, counts = create_bar_graph_and_table(filtered_df, section, data_mode)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader(f"{section} Table")
            st.dataframe(counts, height=300)

# ----------- Presence, Number of, and Regular Contact with Close Friends -----------
with st.container():
    with st.expander("Presence, Number of, and Regular Contact with Close Friends"):
        fig_close_friends, close_friends_counts = create_bar_graph_and_table(filtered_df, "Close Friends", data_mode)
        st.plotly_chart(fig_close_friends, use_container_width=True)
        st.subheader("Close Friends Table")
        st.dataframe(close_friends_counts, height=300)

        fig_number_close_friends = px.histogram(filtered_df, x="Number of Close Friends", nbins=10, template="seaborn")
        fig_number_close_friends.update_traces(marker=dict(color="lightgreen", line=dict(color="black", width=1)), texttemplate='%{y}')
        fig_number_close_friends.update_layout(xaxis_title="Number of Close Friends", yaxis_title="# of Respondents", bargap=0.2)
        st.plotly_chart(fig_number_close_friends, use_container_width=True)
        
        number_close_friends_counts = filtered_df["Number of Close Friends"].value_counts().reset_index().rename(columns={'index': 'Number of Close Friends', 'Number of Close Friends': 'Count'})
        number_close_friends_counts.index = number_close_friends_counts.index + 1
        st.subheader("Number of Close Friends Table")
        st.dataframe(number_close_friends_counts, height=300)

        fig_regular_contact_close_friends, regular_contact_close_friends_counts = create_bar_graph_and_table(filtered_df, "Regular Contact with Close Friends", data_mode)
        st.plotly_chart(fig_regular_contact_close_friends, use_container_width=True)
        st.subheader("Regular Contact with Close Friends Table")
        st.dataframe(regular_contact_close_friends_counts, height=300)

# ----------- Parents were Teenage Parents -----------
with st.container():
    with st.expander("Parents were Teenage Parents"):
        fig_parents_teen, parents_teen_counts = create_bar_graph_and_table(filtered_df, "Parents were Teenage Parents", data_mode)
        st.plotly_chart(fig_parents_teen, use_container_width=True)
        st.subheader("Parents were Teenage Parents Table")
        st.dataframe(parents_teen_counts, height=300)