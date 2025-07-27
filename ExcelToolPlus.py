import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Multi Excel Filter Tool", layout="wide")
st.title("📊 Multi Excel File Upload and Filter Tool")

# Upload multiple Excel files
uploaded_files = st.file_uploader("Upload up to 10 Excel files", type=["xlsx", "xls"], accept_multiple_files=True)

if uploaded_files:
    combined_df = pd.DataFrame()

    for file in uploaded_files:
        try:
            df = pd.read_excel(file)
            df['Source File'] = file.name  # Add a column to identify the source
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            st.error(f"Failed to read {file.name}: {e}")

    if not combined_df.empty:
        st.success(f"{len(uploaded_files)} files combined successfully!")

        # Let user select which columns to display
        st.subheader("🔍 Select Columns to Display")
        all_columns = combined_df.columns.tolist()
        selected_columns = st.multiselect("Choose columns to show", all_columns, default=all_columns[:5])

        # Optional filter: e.g., Case Type
        if "Case Type" in combined_df.columns:
            case_type_filter = st.radio("Filter by Case Type", ["All", "Domestic", "International"])
            if case_type_filter != "All":
                combined_df = combined_df[combined_df["Case Type"].str.lower() == case_type_filter.lower()]

        # Show filtered data
        st.dataframe(combined_df[selected_columns])

        # Download filtered data
        output = BytesIO()
        combined_df[selected_columns].to_excel(output, index=False)
        st.download_button("📥 Download Filtered Data", output.getvalue(), file_name="filtered_combined_data.xlsx")
    else:
        st.warning("No valid data found in uploaded files.")
else:
    st.info("Please upload up to 10 Excel files to get started.")
