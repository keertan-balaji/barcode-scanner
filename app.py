import pandas as pd
import streamlit as st

# Sample DataFrame to keep track of items and quantities

# Initialize the session state DataFrame
if 'df' not in st.session_state:
    st.session_state.df = None

# Function to update quantity or remove item from DataFrame
def update_quantity(df, scanned_item):
    scanned_item = scanned_item.strip()
    if scanned_item in df['Material'].values:
        idx = df[df['Material'] == scanned_item].index[0]
        df.loc[idx, 'Source target qty'] -= 1
        if df.loc[idx, 'Source target qty'] <= 0:
            df = df.drop(idx)
    return df

# Callback function to handle input and reset the field
def process_input():
    scanned_item = st.session_state.barcode_input
    st.session_state.df = update_quantity(st.session_state.df, scanned_item)
    st.session_state.barcode_input = ''  # Clear input field after processing

# Streamlit app UI and logic
st.title("Inventory Tracker")
reference_file = st.file_uploader("Choose reference file", accept_multiple_files=False)
if reference_file:
    if st.session_state.df is None:
        reference_df = pd.read_excel(reference_file)
        st.write(f"Reference file: {reference_file.name}")
        st.session_state.df = reference_df[["Transfer Order Number","Transfer order item","Material","Source target qty"]]

    # Text input for scanning item (simulated as barcode input)
    st.text_input("Scan the item's barcode (type and press Enter):", 
                key="barcode_input", 
                on_change=process_input)

    # Display the updated DataFrame
    st.write("Current Inventory:")
    st.dataframe(st.session_state.df)

    # Stop if all items are scanned
    if st.session_state.df.empty:
        st.success("All items scanned! Inventory complete.")

    # Button to reset the DataFrame
    if st.button("Reset Inventory"):
        st.session_state.df = pd.read_excel(reference_file)

    # Inject JavaScript to focus on the input element automatically
    st.components.v1.html("""
        <script>
            document.getElementById("barcode_input").focus();
        </script>
        """, height=0)
