import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to load data with caching
@st.cache_data
def load_data(file, option):
    if option == "csv":
        df = pd.read_csv(file)
    elif option == "excel":
        df = pd.read_excel(file)
    return df

# Function to filter DataFrame based on selected values
def filter_dataframe(df, selected_filters):
    for column in df.columns:
        if df[column].dtype == 'object':
            if column not in selected_filters:
                selected_filters[column] = sorted(df[column].astype(str).unique())

            selected_values = st.sidebar.multiselect(f"Select {column}", selected_filters[column])

            if selected_values:
                df = df[df[column].astype(str).isin(selected_values)]
    return df

# Function to display distribution chart
# Function to display distribution chart with error handling
def display_distribution_chart(df, selected_column_chart):
    st.subheader(f"{selected_column_chart} Distribution")

    # Check if the selected column contains numerical values
    try:
        num_bins = 10
        hist, bin_edges = np.histogram(df[selected_column_chart], bins=num_bins)
        st.bar_chart(hist, use_container_width=True)
    except (TypeError, ValueError) as e:
        st.error("Error: Choose a column with numerical values for the distribution chart.")

# Function to display bar chart for value counts of a categorical or object column
def display_categorical_value_counts_chart(df, selected_column_chart):
    st.subheader(f"Value Counts for {selected_column_chart}")

    # Check if the selected column is categorical or object
    if pd.api.types.is_object_dtype(df[selected_column_chart]):
        value_counts = df[selected_column_chart].value_counts()
        st.bar_chart(value_counts, use_container_width=True)
    else:
        st.error(f"Choose a categorical or object column for the value counts chart.")


# Function to display scatter plot with customizable size
def display_scatter_plot(df, scatter_1, scatter_2, plot_size=(4, 4)):
    st.subheader(f"Scatter Plot: {scatter_1} vs {scatter_2}")
    fig, ax = plt.subplots(figsize=plot_size)
    ax.scatter(df[scatter_1], df[scatter_2], c="purple")
    ax.set_xlabel(scatter_1)
    ax.set_ylabel(scatter_2)
    st.pyplot(fig)

# Main Streamlit app
st.set_page_config(page_title="Dashboard", page_icon="bar_chart", layout="wide")

option = st.sidebar.selectbox('Choose file type:', ('Choose one...', 'csv', 'excel'))
file = st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx"])

if file is not None:
    df = load_data(file, option)

    check_box = st.sidebar.checkbox(label="Display dataset")

    selected_filters = {}
    df = filter_dataframe(df, selected_filters)


    if check_box:
        st.subheader("Dataset")
        st.write(df)

    # Distribution Chart
    selected_distribution_chart = st.selectbox("Select Column for Distribution Chart", df.columns)
    display_distribution_chart(df, selected_distribution_chart)
    selected_values_chart=st.selectbox("Select Column for Chart",df.columns)
    display_categorical_value_counts_chart(df,selected_values_chart)

    # Scatter Plot
    st.subheader("Select Columns for Scatter Plot")
    scatter_1 = st.selectbox("Select First Column", df.columns)
    scatter_2 = st.selectbox("Select Second Column", df.columns)
    display_scatter_plot(df, scatter_1, scatter_2)

else:
    st.info("Please upload a file.")
