import pandas as pd
import streamlit as st

# Sample DataFrame to keep track of items and quantities

# Initialize the session state DataFrame
if 'df' not in st.session_state:
    st.session_state.df = None

if 'scanned_item_count' not in st.session_state:
    st.session_state.scanned_item_count = None

if 'not_scanned_item_count' not in st.session_state:
    st.session_state.not_scanned_item_count = None

if 'selected_rows' not in st.session_state and st.session_state.df is not None:
    st.session_state.selected_rows = [False] * len(st.session_state.df)

# Function to update quantity or remove item from DataFrame
def update_quantity(df, scanned_item):
    scanned_item = scanned_item.strip()
    if scanned_item in df['Material'].values:
        idx = df[df['Material'] == scanned_item].index[0]
        df.loc[idx, 'Source target qty'] -= 1
        st.success(f"Item scanned: {scanned_item} | Remaining Quantity: {df.loc[idx, 'Source target qty']}")
        if df.loc[idx, 'Source target qty'] <= 0:
            df = df.drop(idx)
        st.session_state.scanned_item_count += 1
        st.session_state.not_scanned_item_count -= 1
    else:
        st.error(f"Item not found: {scanned_item}")
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
        reference_df = reference_df[["Material","Source target qty"]]
        st.write(f"Reference file: {reference_file.name}")
        st.session_state.df = reference_df.groupby('Material', as_index=False).sum()

    # Text input for scanning item (simulated as barcode input)
    st.text_input("Scan the item's barcode (type and press Enter):", 
                key="barcode_input", 
                on_change=process_input)

    if st.session_state.not_scanned_item_count is None:
        st.session_state.not_scanned_item_count = sum(st.session_state.df['Source target qty'])
    if st.session_state.scanned_item_count is None:
        st.session_state.scanned_item_count = 0
    st.write(f"Scanned items: {st.session_state.scanned_item_count}")
    st.write(f"Not scanned items: {st.session_state.not_scanned_item_count}")
    # Display the updated DataFrame
    st.write("Current Inventory:")
    selected_rows = st.dataframe(st.session_state.df,on_select="rerun",height = 35*len(st.session_state.df),use_container_width=True)
    # print(selected_rows)
    # Stop if all items are scanned
    if st.session_state.df.empty:
        st.success("All items scanned! Inventory complete.")


    # Inject JavaScript to focus on the input element automatically
    st.components.v1.html("""
        <script>
            document.getElementById("barcode_input").focus();
        </script>
        """, height=0)

