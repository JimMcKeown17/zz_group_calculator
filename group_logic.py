import streamlit as st
import pandas as pd

# Title of the web app
st.title("Zazi iZandi Group Calculator")
st.text("Add each of your children's EGRA scores. Double check that the number you've entered is correct. Click 'Process Data' to get your children's group numbers.")

# Initialize session state to hold the input data
if "data" not in st.session_state:
    st.session_state.data = {"Name": [], "Surname": [], "Score": []}

# Form for data entry
with st.form(key="data_entry_form"):
    cols = st.columns(3)
    # Input fields
    name = cols[0].text_input("Name")
    surname = cols[1].text_input("Surname")
    score = cols[2].number_input("Score", min_value=0, max_value=100, value=0, step=1)

    # Add record button
    add_record = st.form_submit_button(label="Add Record")

    # If the form is submitted, append the data to the session state
    if add_record:
        st.session_state.data["Name"].append(name)
        st.session_state.data["Surname"].append(surname)
        st.session_state.data["Score"].append(score)

# Create a DataFrame from the session state data
if st.session_state.data["Name"]:
    df = pd.DataFrame(st.session_state.data)
    df.index = df.index + 1
    st.markdown(f'##### The number of children scores entered is: {len(df)}')
    st.markdown('---')
    st.text('The following shows the children and scores that you have entered so far')
    st.write(df)
else:
    st.write("No data entered yet.")


# Function to assign groups
def assign_groups(df, group_size=7):
    df = df.sort_values(by='Score').reset_index(drop=True)
    df.index = df.index + 1
    df['group'] = (df.index-1) // group_size + 1

    # Check the number of records in the last group
    last_group = df['group'].max()
    last_group_count = df[df['group'] == last_group].shape[0]

    if last_group_count == 1 and last_group > 1:
        df.loc[df['group'] == last_group, 'group'] = last_group - 1
    elif last_group_count == 2 and last_group > 1:
        # Change the group number of the first record in the second-to-last group to the third-to-last group
        second_to_last_group_first_index = df[df['group'] == (last_group - 1)].index[0]
        df.loc[second_to_last_group_first_index, 'group'] = last_group - 2

        # Change the group number of all records in the last group to the second-to-last group
        df.loc[df['group'] == last_group, 'group'] = last_group - 1
    elif last_group_count == 3 and last_group > 1:
        # Change the group number of the last two indices of the 2nd to last group and put them into the last group
        second_to_last_group_7th_index = df[df['group'] == (last_group - 1)].index[6]
        second_to_last_group_6th_index = df[df['group'] == (last_group - 1)].index[5]
        df.loc[second_to_last_group_7th_index, 'group'] = last_group
        df.loc[second_to_last_group_6th_index, 'group'] = last_group
    elif last_group_count == 4 and last_group > 1:
        # Change the group number of the last two indices of the 2nd to last group and put them into the last group
        second_to_last_group_7th_index = df[df['group'] == (last_group - 1)].index[6]
        df.loc[second_to_last_group_7th_index, 'group'] = last_group
    return df


# Layout for buttons
col1, col2 = st.columns(2)

with col1:
    process_data = st.button("Calculate Groups")

with col2:
    clear_data = st.button("Start Over")

# Process data button logic
if process_data:
    if st.session_state.data["Name"]:
        df = pd.DataFrame(st.session_state.data)
        df = assign_groups(df)
        st.markdown("#### Please find your child groups below:")
        st.dataframe(df)
        groups_df = df.groupby('group')['Name'].count()
        st.markdown("#### The number of children in each of your groups is: ")
        st.dataframe(groups_df)
    else:
        st.write("No data to process.")

# Clear data button logic
if clear_data:
    st.session_state.data = {"Name": [], "Surname": [], "Score": []}
    st.write("Data has been cleared. You can start over.")
