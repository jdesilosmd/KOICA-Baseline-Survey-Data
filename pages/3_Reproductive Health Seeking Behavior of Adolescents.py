import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("C:/Users/ASUS/OneDrive/Documents/Data Science/KOICA/KOICA_SURVEY_4.xlsx")
df3 = df.iloc[:, [3, 8, 9, 10] + list(range(26, 74))]

# Dictionary for renaming columns
column_rename_dict = {
    'A2_City': 'City',
    'B2_Age_as_of_last_birthday': 'Age',
    'B3_Sex_assigned_at_birth': 'Sex Assigned At Birth',
    'B4_Level_of_Education': 'Level Of Education',
    'Do_you_seek_consulta_your_health_concerns': 'Seeks Health Consultation',
    'What_was_the_reason_for_the_consultation': 'Consultation Reason',
    'What_is_the_name_of_sought_consultation': 'Consultation Facility Name',
    'Type_of_Facility_of_e_mentioned_facility': 'Facility Type',
    'Structure_of_Facility': 'Facility Structure',
    'Locality_of_Facility': 'Facility Locality',
    'How_many_days_per_we_this_health_facility': 'Facility Days Per Week',
    'How_many_days_per_we_this_health_facility_001': 'Facility Days Per Week Alternate',
    'Are_the_hours_this_f_n_convenient_for_you': 'Convenient Facility Hours',
    'How_did_you_hear_about_this_facility': 'Source Of Facility Information',
    'How_did_you_hear_about_this_facility/radio': 'Heard From Radio',
    'How_did_you_hear_about_this_facility/television': 'Heard From Television',
    'How_did_you_hear_about_this_facility/newspaper': 'Heard From Newspaper',
    'How_did_you_hear_about_this_facility/friend': 'Heard From Friend',
    'How_did_you_hear_about_this_facility/relative': 'Heard From Relative',
    'How_did_you_hear_about_this_facility/posters': 'Heard From Posters',
    'How_did_you_hear_about_this_facility/pamphlet_brochure': 'Heard From Pamphlet Or Brochure',
    'How_did_you_hear_about_this_facility/social_media': 'Heard From Social Media',
    'How_did_you_hear_about_this_facility/other': 'Heard From Other Sources',
    'How_did_you_hear_abo_facility_If_Others': 'Other Source Details',
    'Did_the_health_servi_ou_during_your_visit': 'Received Health Services During Visit',
    'Were_you_given_assur_ntiality_and_consent': 'Confidentiality And Consent Given',
    'Did_the_service_prov_ate_examination_room': 'Private Examination Room Provided',
    'Did_the_service_prov_s_of_the_health_exam': 'Received Health Exam Details',
    'Did_you_receive_or_d_rial_to_read_at_home': 'Received Material For Home',
    'What_subject_s_is_a_red_in_this_material': 'Material Subjects',
    'What_subject_s_is_a_red_in_this_material/maternal_health': 'Material Subject - Maternal Health',
    'What_subject_s_is_a_red_in_this_material/contraception': 'Material Subject - Contraception',
    'What_subject_s_is_a_red_in_this_material/sti': 'Material Subject - STI',
    'What_subject_s_is_a_red_in_this_material/hiv_aids': 'Material Subject - HIV/AIDS',
    'What_subject_s_is_a_red_in_this_material/drugs_alcohol': 'Material Subject - Drugs And Alcohol',
    'What_subject_s_is_a_red_in_this_material/others': 'Material Subject - Other Topics',
    'Did_any_service_prov_rn_for_another_visit': 'Referred For Another Visit',
    'Did_you_pay_for_the_ices_rendered_to_you': 'Paid For Services Rendered',
    'If_yes_in_Q8_how_mu_e_following_services': 'Service Costs',
    'If_yes_in_Q8_how_mu_ces_Pregnancy_Test': 'Cost Of Pregnancy Test',
    'If_yes_in_Q8_how_mu_rvices_Anemia_Test': 'Cost Of Anemia Test',
    'If_yes_in_Q8_how_mu_ty_Delivery_Services': 'Cost Of Delivery Services',
    'If_yes_in_Q8_how_mu_eening_and_treatment': 'Cost Of Screening And Treatment',
    'If_yes_in_Q8_how_mu_s_HIV_AIDS_Testing': 'Cost Of HIV/AIDS Testing',
    'If_yes_in_Q8_how_mu_raception_Counseling': 'Cost Of Contraception Counseling',
    'If_yes_in_Q8_how_mu_Reduction_Counseling': 'Cost Of Risk Reduction Counseling',
    'If_yes_in_Q8_how_mu_rtility_Consultation': 'Cost Of Fertility Consultation',
    'If_yes_in_Q8_how_mu_Gynecological_Exams': 'Cost Of Gynecological Exams',
    'If_yes_in_Q8_how_mu_stfeeding_Counseling': 'Cost Of Breastfeeding Counseling',
    'If_yes_in_Q8_how_mu_Nutrition_Counseling': 'Cost Of Nutrition Counseling',
    'If_yes_in_Q8_how_mu_Parenting_Classes': 'Cost Of Parenting Classes',
    'If_yes_in_Q8_how_mu_ng_services_Others': 'Cost Of Other Services'
}

st.title("3. Reproductive Health Seeking Behavior of Adolescents")

# Apply renaming
df3.rename(columns=column_rename_dict, inplace=True)

# Remove underscores in data (not column names)
df3 = df3.replace('_', ' ', regex=True)

# Define actual sites based on your provided list
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

# Expander for filter options
with st.sidebar.expander("Filter Options", expanded=True):

    # Display type filter (Raw or Percent) with unique key
    display_type = st.radio("Display Data As", options=["Raw", "Percent"], index=0, key="display_type_radio")

    # Site selection with radio buttons and unique key
    site_selection = st.radio(
        "Select Sites",
        options=["All Sites", "Samar Sites", "Southern Leyte Sites", "Manually Select"],
        index=0,
        key="site_selection_radio"
    )
    
    # Multiselect for manual site selection, only visible if "Manually Select" is chosen
    selected_sites = []
    if site_selection == "All Sites":
        selected_sites = samar_sites + southern_leyte_sites
    elif site_selection == "Samar Sites":
        selected_sites = samar_sites
    elif site_selection == "Southern Leyte Sites":
        selected_sites = southern_leyte_sites
    elif site_selection == "Manually Select":
        selected_sites = st.multiselect("Select Sites", options=samar_sites + southern_leyte_sites, key="manual_site_select")

    # Gender filter with unique key
    selected_gender = st.multiselect("Select Gender", options=["male", "female"], default=["male", "female"], key="gender_multiselect")

    # Age filter with unique key
    age_group = st.radio("Select Age Group", options=["All Age Groups", "10-14", "15-19"], key="age_group_radio")

# Apply site filtering
filtered_df3 = df3[df3['City'].isin(selected_sites)] if selected_sites else df3

# Apply gender filtering
filtered_df3 = filtered_df3[filtered_df3['Sex Assigned At Birth'].isin(selected_gender)]

# Apply age filtering only if a specific age group is selected
if age_group == "10-14":
    filtered_df3 = filtered_df3[(filtered_df3['Age'] >= 10) & (filtered_df3['Age'] <= 14)]
elif age_group == "15-19":
    filtered_df3 = filtered_df3[(filtered_df3['Age'] >= 15) & (filtered_df3['Age'] <= 19)]

# Seeks Health Consultation and related attributes
consultation_counts = filtered_df3["Seeks Health Consultation"].value_counts(normalize=(display_type == "Percent")).reset_index()
consultation_counts.columns = ["Seeks Health Consultation", "Count"]
consultation_counts = consultation_counts.sort_values(by="Count", ascending=True)
if display_type == "Percent":
    consultation_counts["Count"] = (consultation_counts["Count"] * 100).round(0).astype(int).astype(str) + "%"
consultation_counts.index = range(1, len(consultation_counts) + 1)

reason_counts = filtered_df3["Consultation Reason"].value_counts(normalize=(display_type == "Percent")).reset_index()
reason_counts.columns = ["Consultation Reason", "Count"]
reason_counts = reason_counts.sort_values(by="Count", ascending=True)
if display_type == "Percent":
    reason_counts["Count"] = (reason_counts["Count"] * 100).round(0).astype(int).astype(str) + "%"
reason_counts.index = range(1, len(reason_counts) + 1)

facility_counts = filtered_df3["Consultation Facility Name"].value_counts(normalize=(display_type == "Percent")).reset_index()
facility_counts.columns = ["Consultation Facility Name", "Count"]
facility_counts = facility_counts.sort_values(by="Count", ascending=True)
if display_type == "Percent":
    facility_counts["Count"] = (facility_counts["Count"] * 100).round(0).astype(int).astype(str) + "%"
facility_counts.index = range(1, len(facility_counts) + 1)

# Create bar graphs for Seeks Health Consultation data
fig_consultation = px.bar(
    consultation_counts,
    y="Seeks Health Consultation",
    x="Count",
    title="Seeks Health Consultation Responses",
    template="seaborn",
    orientation='h'
)
fig_consultation.update_traces(marker=dict(color="steelblue", line=dict(color="black", width=1)))
fig_consultation.update_traces(text=consultation_counts["Count"], textposition="outside")

fig_reason = px.bar(
    reason_counts,
    y="Consultation Reason",
    x="Count",
    title="Consultation Reason Responses",
    template="seaborn",
    orientation='h'
)
fig_reason.update_traces(marker=dict(color="steelblue", line=dict(color="black", width=1)))
fig_reason.update_traces(text=reason_counts["Count"], textposition="outside")

fig_facility = px.bar(
    facility_counts,
    y="Consultation Facility Name",
    x="Count",
    title="Consultation Facility Name Responses",
    template="seaborn",
    orientation='h'
)
fig_facility.update_traces(marker=dict(color="steelblue", line=dict(color="black", width=1)))
fig_facility.update_traces(text=facility_counts["Count"], textposition="outside")

# Health Facility Attributes - Counts and Plots
facility_columns = [
    "Facility Type", "Facility Structure", "Facility Locality",
    "Facility Days Per Week", "Facility Days Per Week Alternate", "Convenient Facility Hours"
]
facility_counts_dict = {}

for col in facility_columns:
    counts = filtered_df3[col].value_counts(normalize=(display_type == "Percent")).reset_index()
    counts.columns = [col, "Count"]
    counts = counts.sort_values(by="Count", ascending=True)
    if display_type == "Percent":
        counts["Count"] = (counts["Count"] * 100).round(0).astype(int).astype(str) + "%"
    counts.index = range(1, len(counts) + 1)
    facility_counts_dict[col] = counts

# Source of Facility Information - Columns 14 to 22 (filtered data)
df_infosource = filtered_df3.iloc[:, list(range(14, 23))]
df_infosource.rename(columns={
    df_infosource.columns[0]: 'Radio',
    df_infosource.columns[1]: 'TV',
    df_infosource.columns[2]: 'Newspaper',
    df_infosource.columns[3]: 'Friend',
    df_infosource.columns[4]: 'Relative',
    df_infosource.columns[5]: 'Posters',
    df_infosource.columns[6]: 'Pamphlet/Brochure',
    df_infosource.columns[7]: 'Social Media',
    df_infosource.columns[8]: 'Other'
}, inplace=True)

# Stack the data to create a 'Source' column and an 'Answer' column
df_infosource_stack = df_infosource.stack().reset_index().rename(columns={'level_1': 'Source', 0: 'Answer'})

# Filter for rows where the answer indicates usage (assuming 1 means "Yes")
df_infosource_stack = df_infosource_stack.fillna(0)
df_infosource_grp = df_infosource_stack.groupby(['Source', 'Answer']).size().reset_index(name='Respondents')
df_infosource_grp_1 = df_infosource_grp[df_infosource_grp['Answer'] == 1.0][['Source', 'Respondents']]
df_infosource_grp_1 = df_infosource_grp_1.sort_values('Respondents', ascending=True)  # Sorted for the bar graph
df_infosource_grp_1.index = range(1, len(df_infosource_grp_1) + 1)  # Set table index to start from 1

# Create the bar graph for Source of Facility Information
fig_source_info = px.bar(
    df_infosource_grp_1,
    y="Source",
    x="Respondents",
    title="Source of Facility Information",
    template="seaborn",
    orientation='h'
)
fig_source_info.update_traces(marker=dict(color="steelblue", line=dict(color="black", width=1)))
fig_source_info.update_traces(text=df_infosource_grp_1["Respondents"], textposition="outside")

# Other Source Details - Assuming it's in a specific column, filter and count values
other_source_details = filtered_df3['Other Source Details'].dropna()  # Adjust this column name as necessary
other_source_counts = other_source_details.value_counts().reset_index()
other_source_counts.columns = ['Other Source Details', 'Count']
other_source_counts.index = range(1, len(other_source_counts) + 1)  # Set index to start from 1

# Create bar graph for Other Source Details
fig_other_source_details = px.bar(
    other_source_counts,
    y="Other Source Details",
    x="Count",
    title="Other Source Details",
    template="seaborn",
    orientation='h'
)
fig_other_source_details.update_traces(marker=dict(color="steelblue", line=dict(color="black", width=1)))
fig_other_source_details.update_traces(text=other_source_counts["Count"], textposition="outside")

# Health Service Experience Attributes
experience_columns = [
    "Received Health Services During Visit", "Confidentiality And Consent Given",
    "Private Examination Room Provided", "Received Health Exam Details", "Received Material For Home"
]
experience_counts_dict = {}

for col in experience_columns:
    counts = filtered_df3[col].value_counts(normalize=(display_type == "Percent")).reset_index()
    counts.columns = [col, "Count"]
    counts = counts.sort_values(by="Count", ascending=True)
    if display_type == "Percent":
        counts["Count"] = (counts["Count"] * 100).round(0).astype(int).astype(str) + "%"
    counts.index = range(1, len(counts) + 1)
    experience_counts_dict[col] = counts

# Subjects Covered - Columns for Material Subjects
subject_columns = [
    "Material Subject - Maternal Health", "Material Subject - Contraception", 
    "Material Subject - STI", "Material Subject - HIV/AIDS", 
    "Material Subject - Drugs And Alcohol", "Material Subject - Other Topics"
]

# Stack the data to create a 'Subject' column and an 'Answer' column
df_subjects = filtered_df3[subject_columns].stack().reset_index().rename(columns={'level_1': 'Subject', 0: 'Answer'})

# Filter for rows where the answer indicates coverage (assuming 1 means "Yes")
df_subjects = df_subjects.fillna(0)
df_subjects_grp = df_subjects.groupby(['Subject', 'Answer']).size().reset_index(name='Respondents')
df_subjects_grp_1 = df_subjects_grp[df_subjects_grp['Answer'] == 1.0][['Subject', 'Respondents']]
df_subjects_grp_1 = df_subjects_grp_1.sort_values('Respondents', ascending=True)  # Sorted for the bar graph
df_subjects_grp_1.index = range(1, len(df_subjects_grp_1) + 1)  # Set table index to start from 1

# Create the bar graph for Subjects Covered
fig_subjects = px.bar(
    df_subjects_grp_1,
    y="Subject",
    x="Respondents",
    title="Subjects Covered",
    template="seaborn",
    orientation='h'
)
fig_subjects.update_traces(marker=dict(color="steelblue", line=dict(color="black", width=1)))
fig_subjects.update_traces(text=df_subjects_grp_1["Respondents"], textposition="outside")

# Referred For Another Visit - Advised when to return to the facility
referred_counts = filtered_df3["Referred For Another Visit"].value_counts(normalize=(display_type == "Percent")).reset_index()
referred_counts.columns = ["Referred For Another Visit", "Count"]
referred_counts = referred_counts.sort_values(by="Count", ascending=True)
if display_type == "Percent":
    referred_counts["Count"] = (referred_counts["Count"] * 100).round(0).astype(int).astype(str) + "%"
referred_counts.index = range(1, len(referred_counts) + 1)

# Create bar graph for Referred For Another Visit
fig_referred = px.bar(
    referred_counts,
    y="Referred For Another Visit",
    x="Count",
    title="Advised when to return to the facility",
    template="seaborn",
    orientation='h'
)
fig_referred.update_traces(marker=dict(color="steelblue", line=dict(color="black", width=1)))
fig_referred.update_traces(text=referred_counts["Count"], textposition="outside")

# Paid For Services Rendered - Paid for reproductive health services
paid_counts = filtered_df3["Paid For Services Rendered"].value_counts(normalize=(display_type == "Percent")).reset_index()
paid_counts.columns = ["Paid For Services Rendered", "Count"]
paid_counts = paid_counts.sort_values(by="Count", ascending=True)
if display_type == "Percent":
    paid_counts["Count"] = (paid_counts["Count"] * 100).round(0).astype(int).astype(str) + "%"
paid_counts.index = range(1, len(paid_counts) + 1)

# Create bar graph for Paid For Services Rendered
fig_paid = px.bar(
    paid_counts,
    y="Paid For Services Rendered",
    x="Count",
    title="Paid for the reproductive health services",
    template="seaborn",
    orientation='h'
)
fig_paid.update_traces(marker=dict(color="steelblue", line=dict(color="black", width=1)))
fig_paid.update_traces(text=paid_counts["Count"], textposition="outside")

# Display Seeks Health Consultation section
with st.container():
    with st.expander("Seeks Health Consultation"):
        # Seeks Health Consultation Graph and Table
        st.plotly_chart(fig_consultation, use_container_width=True)
        st.write("Counts of Seeks Health Consultation")
        st.dataframe(consultation_counts.reset_index(drop=True), height=300)
        
        # Consultation Reason Graph and Table
        st.plotly_chart(fig_reason, use_container_width=True)
        st.write("Counts of Consultation Reason")
        st.dataframe(reason_counts.reset_index(drop=True), height=300)
        
        # Consultation Facility Name Graph and Table
        st.plotly_chart(fig_facility, use_container_width=True)
        st.write("Counts of Consultation Facility Name")
        st.dataframe(facility_counts.reset_index(drop=True), height=300)

# Display Health Facility section
with st.container():
    with st.expander("Health Facility"):
        for col, counts in facility_counts_dict.items():
            fig = px.bar(
                counts,
                y=col,
                x="Count",
                title=f"{col} Responses",
                template="seaborn",
                orientation='h'
            )
            fig.update_traces(marker=dict(color="steelblue", line=dict(color="black", width=1)))
            fig.update_traces(text=counts["Count"], textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
            st.write(f"Counts of {col}")
            st.dataframe(counts.reset_index(drop=True), height=300)

# Display Source of Facility Information section with Other Source Details
with st.container():
    with st.expander("Source of Facility Information"):
        st.plotly_chart(fig_source_info, use_container_width=True)
        st.write("Counts of Source of Facility Information")
        st.dataframe(df_infosource_grp_1.reset_index(drop=True), height=300)
        
        # Other Source Details graph and table
        st.plotly_chart(fig_other_source_details, use_container_width=True)
        st.write("Counts of Other Source Details")
        st.dataframe(other_source_counts, height=300)

# Display Health Service Experience section
with st.container():
    with st.expander("Health Service Experience"):
        for col, counts in experience_counts_dict.items():
            fig = px.bar(
                counts,
                y=col,
                x="Count",
                title=f"{col} Responses",
                template="seaborn",
                orientation='h'
            )
            fig.update_traces(marker=dict(color="steelblue", line=dict(color="black", width=1)))
            fig.update_traces(text=counts["Count"], textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
            st.write(f"Counts of {col}")
            st.dataframe(counts.reset_index(drop=True), height=300)

# Display Subjects Covered section
with st.container():
    with st.expander("Subjects Covered"):
        st.plotly_chart(fig_subjects, use_container_width=True)
        st.write("Counts of Subjects Covered")
        st.dataframe(df_subjects_grp_1, height=300)

# Display Advised when to return to the facility section
with st.container():
    with st.expander("Advised when to return to the facility"):
        st.plotly_chart(fig_referred, use_container_width=True)
        st.write("Counts of Advised when to return to the facility")
        st.dataframe(referred_counts, height=300)

# Display Paid for the reproductive health services section
with st.container():
    with st.expander("Paid for the reproductive health services"):
        st.plotly_chart(fig_paid, use_container_width=True)
        st.write("Counts of Paid for the reproductive health services")
        st.dataframe(paid_counts, height=300)

# Display Cost of Availed Services section
with st.container():
    with st.expander("Cost of Availed Services"):

        # Define the columns for Cost of Services
        cost_columns = [
            "Cost Of Pregnancy Test", "Cost Of Anemia Test", "Cost Of Delivery Services",
            "Cost Of Screening And Treatment", "Cost Of HIV/AIDS Testing", 
            "Cost Of Contraception Counseling", "Cost Of Risk Reduction Counseling",
            "Cost Of Fertility Consultation", "Cost Of Gynecological Exams", 
            "Cost Of Breastfeeding Counseling", "Cost Of Nutrition Counseling", 
            "Cost Of Parenting Classes", "Cost Of Other Services"
        ]
        
        # Create a selectbox for choosing which cost column to display
        selected_cost_column = st.selectbox("Select Service to Display Cost", options=cost_columns)

        # Replace NaN values with zero, filter out values greater than 1000, and get value counts
        selected_cost_data = filtered_df3[selected_cost_column].fillna(0)
        selected_cost_data = selected_cost_data[selected_cost_data <= 1000].value_counts().reset_index()
        selected_cost_data.columns = ["Cost (PHP)", "Number of Responses"]

        # Format the cost values in Philippine Pesos
        selected_cost_data["Cost (PHP)"] = selected_cost_data["Cost (PHP)"].apply(lambda x: f"₱{int(x):,}")

        # Display the table
        st.write(f"Cost Distribution for {selected_cost_column.replace('Cost Of ', '').replace('_', ' ')}")
        st.dataframe(selected_cost_data.reset_index(drop=True), height=300)
