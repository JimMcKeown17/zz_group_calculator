import streamlit as st
import pandas as pd

# Title of the web app
st.title("Data Entry App")

# Initialize session state to hold the input data
if "data" not in st.session_state:
    st.session_state.data = []

# Function to add a new record
def add_record():
    st.session_state.data.append({"Name": "", "Surname": "", "Score": 0})

# Function to remove a record
def remove_record(index):
    del st.session_state.data[index]

# Button to add a new row
st.button("Add Record", on_click=add_record)

# Display the input fields for each record
for i, record in enumerate(st.session_state.data):
    cols = st.columns(3)
    cols[0].text_input("Name", value=record["Name"], key=f"name_{i}", on_change=lambda i=i: update_record(i, "Name", cols[0].text_input))
    cols[1].text_input("Surname", value=record["Surname"], key=f"surname_{i}", on_change=lambda i=i: update_record(i, "Surname", cols[1].text_input))
    cols[2].number_input("Score", value=record["Score"], key=f"score_{i}", on_change=lambda i=i: update_record(i, "Score", cols[2].number_input))
    st.button("Remove", key=f"remove_{i}", on_click=lambda i=i: remove_record(i))

# Function to update a record
def update_record(index, field, value):
    st.session_state.data[index][field] = value

# Convert the session state data to a DataFrame
df = pd.DataFrame(st.session_state.data)
st.write(df)

# Button to process the data (you can add your processing logic here)
if st.button("Process Data"):
    st.write("Processing data...")
    # Add your data processing logic here
