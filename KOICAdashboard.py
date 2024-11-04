import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# Load data
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQL2JLmFxlnDQyRrUq8FzKBnMf5yWtULvcmwwSOLCBmkvBuyTTE2RtcResYiHe3cg/pub?output=xlsx"
# df = pd.read_excel("C:/Users/ASUS/OneDrive/Documents/Data Science/KOICA/KOICA_SURVEY_4.xlsx")
df = pd.read_excel(url)

# Data assignment

df2 = df.iloc[:, [3, 8, 9, ]+list(range(8, 26))]
df3 = df.iloc[:, [3]+list(range(26, 74))]
df4 = df.iloc[:, [3]+list(range(74, 111))]
df5 = df.iloc[:, [3]+list(range(111, 144))]
df6 = df.iloc[:, [3]+list(range(144, 154))]
df7 = df.iloc[:, [3]+list(range(154, 196))]
df8 = df.iloc[:, [3]+list(range(196, 430))]
df9 = df.iloc[:, [3]+list(range(430, 460))]
df10 = df.iloc[:, [3]+list(range(460, 601))]
df11 = df.iloc[:, [3]+list(range(601, 645))]
df12 = df.iloc[:, [3]+list(range(645, 746))]

st.write(df)
