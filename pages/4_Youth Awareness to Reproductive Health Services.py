import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
url = "https://onedrive.live.com/download?resid=8452D606ADDC0A0F!142073&ithint=file%2cxlsx&authkey=!ALoiLKebKzNyaSk&wdo=2&cid=8452d606addc0a0f"
df = pd.read_excel(url)

# Selecting columns
df4 = df.iloc[:, [3, 8, 9, 10] + list(range(74, 111))]

# Title
st.title("4. Youth Awareness to Reproductive Health Services")

# Full column renaming
column_renaming = {
    df4.columns[0]: "City",
    df4.columns[1]: "Age",
    df4.columns[2]: "Sex Assigned At Birth",
    df4.columns[3]: "Level of Education",
    df4.columns[4]: "Do You Know Any Service Organizations For Victims Of Sexual Abuse",
    df4.columns[5]: "Do You Know Any Youth Organizations In Your Area",
    df4.columns[6]: "Do You Know If Schools Provide Reproductive Health Information",
    df4.columns[7]: "Do You Know If Health Facility Has Contraception Commodities",
    df4.columns[8]: "Types Of Contraception Available In Facility",
    df4.columns[9]: "Available Contraception/Combined Pills",
    df4.columns[10]: "Available Contraception/Progesterone-Only Pill",
    df4.columns[11]: "Available Contraception/Condom",
    df4.columns[12]: "Available Contraception/Spermicide",
    df4.columns[13]: "Available Contraception/IUD",
    df4.columns[14]: "Available Contraception/Injectables",
    df4.columns[15]: "Available Contraception/Diaphragm",
    df4.columns[16]: "Available Contraception/Emergency Contraception",
    df4.columns[17]: "Services At Facility",
    df4.columns[18]: "Services At Facility/Pregnancy Test",
    df4.columns[19]: "Services At Facility/Anemia Test",
    df4.columns[20]: "Services At Facility/Maternity Delivery Services",
    df4.columns[21]: "Services At Facility/STI Screening And Treatment",
    df4.columns[22]: "Services At Facility/HIV AIDS Testing",
    df4.columns[23]: "Services At Facility/Contraception Counseling",
    df4.columns[24]: "Services At Facility/Risk Reduction Counseling",
    df4.columns[25]: "Services At Facility/Infertility Consultation",
    df4.columns[26]: "Services At Facility/Gynecological Exams",
    df4.columns[27]: "Services At Facility/Breastfeeding Counseling",
    df4.columns[28]: "Services At Facility/Nutrition Counseling",
    df4.columns[29]: "Services At Facility/Parenting Classes",
    df4.columns[30]: "Are There Any STI Tests Available",
    df4.columns[31]: "Tests Available For STIs/Syphilis",
    df4.columns[32]: "Tests Available For STIs/Gonorrhea",
    df4.columns[33]: "Tests Available For STIs/Chlamydia",
    df4.columns[34]: "Tests Available For STIs/Candida",
    df4.columns[35]: "Tests Available For Cervical Cancer",
    df4.columns[36]: "Are You Aware Of Services For Unplanned Pregnancy",
    df4.columns[37]: "Are You Aware Of Services For Unwanted Pregnancy",
    df4.columns[38]: "Services For Unplanned Pregnancy",
    df4.columns[39]: "Considered Any Services For Unplanned Pregnancy",
    df4.columns[40]: "Availed Services For Unplanned Pregnancy"
}

# Apply renaming
df4 = df4.rename(columns=column_renaming)

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

# Sidebar filter options
with st.sidebar.expander("Filter Options", expanded=True):
    display_type = st.radio("Display Data As", options=["Raw", "Percent"], index=0, key="display_type_radio")
    site_selection = st.radio("Select Sites", options=["All Sites", "Samar Sites", "Southern Leyte Sites", "Manually Select"], index=0, key="site_selection_radio")
    
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
filtered_df4 = df4[df4['City'].isin(selected_sites)] if selected_sites else df4
filtered_df4 = filtered_df4[filtered_df4['Sex Assigned At Birth'].isin(selected_gender)]

if age_group == "10-14":
    filtered_df4 = filtered_df4[(filtered_df4['Age'] >= 10) & (filtered_df4['Age'] <= 14)]
elif age_group == "15-19":
    filtered_df4 = filtered_df4[(filtered_df4['Age'] >= 15) & (filtered_df4['Age'] <= 19)]

# Function to plot bar graph and table for a given column
def plot_graph_and_table(filtered_df, column_name):
    value_counts = filtered_df[column_name].value_counts()
    total_responses = value_counts.sum()

    if display_type == "Percent":
        percent_counts = (value_counts / total_responses * 100).round(0).astype(int)  # Convert to percent, round off, remove decimals
        fig = px.bar(
            percent_counts,
            orientation='h',
            text=percent_counts.apply(lambda x: f"{x}%"),  # Display percent values at bar tips
            template='seaborn'
        )
        table_data = percent_counts.reset_index()
        table_data.columns = ['Response', 'Percent']  # Explicitly rename columns
    else:
        fig = px.bar(
            value_counts,
            orientation='h',
            text=value_counts,  # Display raw counts at bar tips
            template='seaborn'
        )
        table_data = value_counts.reset_index()
        table_data.columns = ['Response', 'Count']  # Explicitly rename columns

    # Customize graph appearance
    fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
    fig.update_layout(
        title=f"{column_name}",
        xaxis_title="Percentage" if display_type == "Percent" else "Count",
        yaxis_title="Response"
    )

    # Display bar graph and table
    st.plotly_chart(fig)
    st.dataframe(table_data)

# Create expanders for each specific column
with st.container():
    with st.expander("Knowledge of Organizations Present in the Area", expanded=True):
        plot_graph_and_table(filtered_df4, 'Do You Know Any Service Organizations For Victims Of Sexual Abuse')
        plot_graph_and_table(filtered_df4, 'Do You Know Any Youth Organizations In Your Area')

    with st.expander("Reproductive Health Information in Schools", expanded=True):
        plot_graph_and_table(filtered_df4, 'Do You Know If Schools Provide Reproductive Health Information')

    with st.expander("Contraception Commodities in Health Facilities", expanded=True):
        plot_graph_and_table(filtered_df4, 'Do You Know If Health Facility Has Contraception Commodities')


# Create a new expander for the "Types Of Contraception Available In Facility"
with st.container():
    with st.expander("Types Of Contraception Available In Facility", expanded=True):
        # Extract columns for the "Types Of Contraception Available In Facility"
        df_contraception = filtered_df4.iloc[:, 9:17]

        # Rename the columns for clarity
        df_contraception.rename(columns={
            df_contraception.columns[0]: 'Combined Pills',
            df_contraception.columns[1]: 'Progesterone-Only Pill',
            df_contraception.columns[2]: 'Condom',
            df_contraception.columns[3]: 'Spermicide',
            df_contraception.columns[4]: 'IUD',
            df_contraception.columns[5]: 'Injectables',
            df_contraception.columns[6]: 'Diaphragm',
            df_contraception.columns[7]: 'Emergency Contraception'
        }, inplace=True)

        # Stack the data
        df_contraception_stack = df_contraception.stack().reset_index().rename(columns={'level_1': 'Type of Contraception', 0: 'Answer'})
        df_contraception_stack = df_contraception_stack.loc[:, ['Type of Contraception', 'Answer']]

        # Fill missing values with 0 (assuming only valid answers are 1)
        df_contraception_stack = df_contraception_stack.fillna(0)

        # Group by 'Type of Contraception' and count only responses where Answer is 1
        df_contraception_grp = df_contraception_stack.groupby(['Type of Contraception'], as_index=False).value_counts().rename(columns={'count': 'Respondents'})

        # Filter to include only rows where the Answer is 1 (indicating 'Yes' or positive response)
        df_contraception_grp_1 = df_contraception_grp.loc[df_contraception_grp['Answer'] == 1.0, ['Type of Contraception', 'Respondents']]
        df_contraception_grp_1 = df_contraception_grp_1.sort_values('Respondents', ascending=False)

        # Check if the display type is "Percent" and adjust the data accordingly
        total_responses = df_contraception_grp_1['Respondents'].sum()
        if display_type == "Percent":
            df_contraception_grp_1['Percent'] = (df_contraception_grp_1['Respondents'] / total_responses * 100).round(0).astype(int)
            fig = px.bar(
                df_contraception_grp_1,
                x='Percent',
                y='Type of Contraception',
                orientation='h',
                text=df_contraception_grp_1['Percent'].apply(lambda x: f"{x}%"),  # Display percent values at bar tips
                template='seaborn'
            )
            table_data = df_contraception_grp_1[['Type of Contraception', 'Percent']]
        else:
            fig = px.bar(
                df_contraception_grp_1,
                x='Respondents',
                y='Type of Contraception',
                orientation='h',
                text=df_contraception_grp_1['Respondents'],  # Display raw counts at bar tips
                template='seaborn'
            )
            table_data = df_contraception_grp_1[['Type of Contraception', 'Respondents']].rename(columns={'Respondents': 'Count'})

        # Customize graph appearance
        fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
        fig.update_layout(
            title="Types Of Contraception Available In Facility",
            xaxis_title="Percentage" if display_type == "Percent" else "Count",
            yaxis_title="Type of Contraception"
        )

        # Display bar graph and table
        st.plotly_chart(fig)
        st.dataframe(table_data)


# Create a new expander for the "Services at Facility"
with st.container():
    with st.expander("Services at Facility", expanded=True):
        # Extract columns related to services at the facility
        df_services = filtered_df4.iloc[:, 18:30]

        # Rename the columns for clarity
        df_services.rename(columns={
            df_services.columns[0]: 'Pregnancy Test',
            df_services.columns[1]: 'Anemia Test',
            df_services.columns[2]: 'Maternity/Delivery Services',
            df_services.columns[3]: 'STI Screening and Treatment',
            df_services.columns[4]: 'HIV/AIDS Testing',
            df_services.columns[5]: 'Contraception Counseling',
            df_services.columns[6]: 'Risk Reduction Counseling',
            df_services.columns[7]: 'Infertility Consultation',
            df_services.columns[8]: 'Gynecological Exams',
            df_services.columns[9]: 'Breastfeeding Counseling',
            df_services.columns[10]: 'Nutrition Counseling',
            df_services.columns[11]: 'Parenting Classes'
        }, inplace=True)

        # Stack the data
        df_services_stack = df_services.stack().reset_index().rename(columns={'level_1': 'Service', 0: 'Answer'})
        df_services_stack = df_services_stack.loc[:, ['Service', 'Answer']]

        # Fill missing values with 0 (assuming only valid answers are 1)
        df_services_stack = df_services_stack.fillna(0)

        # Group by 'Service' and count only responses where Answer is 1
        df_services_grp = df_services_stack.groupby(['Service'], as_index=False).value_counts().rename(columns={'count': 'Respondents'})

        # Filter to include only rows where the Answer is 1 (indicating 'Yes' or positive response)
        df_services_grp_1 = df_services_grp.loc[df_services_grp['Answer'] == 1.0, ['Service', 'Respondents']]
        df_services_grp_1 = df_services_grp_1.sort_values('Respondents', ascending=False)

        # Check if the display type is "Percent" and adjust the data accordingly
        total_responses = df_services_grp_1['Respondents'].sum()
        if display_type == "Percent":
            df_services_grp_1['Percent'] = (df_services_grp_1['Respondents'] / total_responses * 100).round(0).astype(int)
            fig = px.bar(
                df_services_grp_1,
                x='Percent',
                y='Service',
                orientation='h',
                text=df_services_grp_1['Percent'].apply(lambda x: f"{x}%"),  # Display percent values at bar tips
                template='seaborn'
            )
            table_data = df_services_grp_1[['Service', 'Percent']]
        else:
            fig = px.bar(
                df_services_grp_1,
                x='Respondents',
                y='Service',
                orientation='h',
                text=df_services_grp_1['Respondents'],  # Display raw counts at bar tips
                template='seaborn'
            )
            table_data = df_services_grp_1[['Service', 'Respondents']].rename(columns={'Respondents': 'Count'})

        # Customize graph appearance
        fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
        fig.update_layout(
            title="Services Available at Facility",
            xaxis_title="Percentage" if display_type == "Percent" else "Count",
            yaxis_title="Service"
        )

        # Display bar graph and table
        st.plotly_chart(fig)
        st.dataframe(table_data)


# Create a new expander for the "Tests Available For STIs and Cervical Cancer"
with st.container():
    with st.expander("Tests Available For STIs and Cervical Cancer", expanded=True):
        # Extract columns related to tests available for STIs and Cervical Cancer
        df_tests = filtered_df4.iloc[:, 31:36]

        # Rename the columns for clarity
        df_tests.rename(columns={
            df_tests.columns[0]: 'Syphilis',
            df_tests.columns[1]: 'Gonorrhea',
            df_tests.columns[2]: 'Chlamydia',
            df_tests.columns[3]: 'Candida',
            df_tests.columns[4]: 'Cervical Cancer'
        }, inplace=True)

        # Stack the data
        df_tests_stack = df_tests.stack().reset_index().rename(columns={'level_1': 'Test', 0: 'Answer'})
        df_tests_stack = df_tests_stack.loc[:, ['Test', 'Answer']]

        # Fill missing values with 0
        df_tests_stack = df_tests_stack.fillna(0)

        # Group by 'Test' and 'Answer' and count the occurrences
        df_tests_grp = df_tests_stack.groupby(['Test', 'Answer'], as_index=False).size().rename(columns={'size': 'Respondents'})

        # Sort values by the number of respondents for better visualization
        df_tests_grp = df_tests_grp.sort_values('Respondents', ascending=False)

        # Check if the display type is "Percent" and adjust the data accordingly
        total_responses = df_tests_grp['Respondents'].sum()
        if display_type == "Percent":
            df_tests_grp['Percent'] = (df_tests_grp['Respondents'] / total_responses * 100).round(0).astype(int)
            fig = px.bar(
                df_tests_grp,
                x='Percent',
                y='Test',
                color='Answer',
                barmode='group',
                orientation='h',
                text=df_tests_grp['Percent'].apply(lambda x: f"{x}%"),  # Display percent values at bar tips
                template='seaborn'
            )
            table_data = df_tests_grp[['Test', 'Answer', 'Percent']]
        else:
            fig = px.bar(
                df_tests_grp,
                x='Respondents',
                y='Test',
                color='Answer',
                barmode='group',
                orientation='h',
                text=df_tests_grp['Respondents'],  # Display raw counts at bar tips
                template='seaborn'
            )
            table_data = df_tests_grp[['Test', 'Answer', 'Respondents']].rename(columns={'Respondents': 'Count'})

        # Customize graph appearance
        fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
        fig.update_layout(
            title="Tests Available For STIs and Cervical Cancer",
            xaxis_title="Percentage" if display_type == "Percent" else "Count",
            yaxis_title="Test"
        )

        # Display bar graph and tableAfter this, create bar graphs and tables for the remaining columns in their own individual expanders.
        st.plotly_chart(fig)
        st.dataframe(table_data)


#####

# Create bar graphs and tables for the last 5 columns in their own expanders
last_columns = filtered_df4.columns[-5:]

# Iterate over each column and create an expander with a bar graph and table
for column in last_columns:
    with st.container():
        with st.expander(f"{column}", expanded=True):
            # Stack the data for the specific column
            df_col_stack = filtered_df4[[column]].stack().reset_index().rename(columns={'level_1': 'Response', 0: 'Answer'})
            df_col_stack = df_col_stack.loc[:, ['Response', 'Answer']]

            # Fill missing values with 0
            df_col_stack = df_col_stack.fillna(0)

            # Group by 'Answer' and count the occurrences
            df_col_grp = df_col_stack.groupby(['Answer'], as_index=False).size().rename(columns={'size': 'Respondents'})

            # Sort values by the number of respondents for better visualization
            df_col_grp = df_col_grp.sort_values('Respondents', ascending=False)

            # Check if the display type is "Percent" and adjust the data accordingly
            total_responses = df_col_grp['Respondents'].sum()
            if display_type == "Percent":
                df_col_grp['Percent'] = (df_col_grp['Respondents'] / total_responses * 100).round(0).astype(int)
                fig = px.bar(
                    df_col_grp,
                    x='Percent',
                    y='Answer',
                    orientation='h',
                    text=df_col_grp['Percent'].apply(lambda x: f"{x}%"),  # Display percent values at bar tips
                    template='seaborn'
                )
                table_data = df_col_grp[['Answer', 'Percent']]
                table_data.columns = ['Response', 'Percent']  # Rename columns for clarity
            else:
                fig = px.bar(
                    df_col_grp,
                    x='Respondents',
                    y='Answer',
                    orientation='h',
                    text=df_col_grp['Respondents'],  # Display raw counts at bar tips
                    template='seaborn'
                )
                table_data = df_col_grp[['Answer', 'Respondents']].rename(columns={'Respondents': 'Count'})
                table_data.columns = ['Response', 'Count']  # Rename columns for clarity

            # Customize graph appearance
            fig.update_traces(marker_line_color='black', marker_line_width=1, textposition='outside')
            fig.update_layout(
                title=f"{column}",
                xaxis_title="Percentage" if display_type == "Percent" else "Count",
                yaxis_title="Response"
            )

            # Display bar graph and table
            st.plotly_chart(fig)
            st.dataframe(table_data)
