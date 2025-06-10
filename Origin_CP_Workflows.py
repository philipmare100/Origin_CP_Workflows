import streamlit as st
from coffee.client import JsonApiClient
import sys
sys.path.append('/opt/anaconda3/envs/myenvtest/lib/python3.10/site-packages')
from coffee.workflows import ConstantPropertyWorkflow
import tempfile
import pandas as pd

st.title("Constant Property Workflow – Create and Link in One Step")

# Upload CSV
uploaded_file = st.file_uploader("Upload a full Constant Property definition CSV", type=["csv"])

if uploaded_file is not None:
    st.write("Uploaded file:", uploaded_file.name)

    if st.button("Process File"):
        try:
            # Save full file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
                temp_file.write(uploaded_file.read())
                full_file_path = temp_file.name

            # Read original CSV into a DataFrame
            df_full = pd.read_csv(full_file_path)

            # Validate required columns
            required_columns = {"name", "component_type"}
            if not required_columns.issubset(df_full.columns.str.lower()):
                st.error("CSV must include at least 'name' and 'component_type' columns.")
            else:
                with JsonApiClient() as client:
                    cp_workflow = ConstantPropertyWorkflow(client)

                    # Step 1: Create constant properties
                    cp_workflow.bulk_create_constant_property(full_file_path)
                    st.success("Step 1: Constant properties created successfully.")

                    # Step 2: Strip to linking columns only and save
                    df_link = df_full[["name", "component_type"]]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as link_file:
                        df_link.to_csv(link_file.name, index=False)
                        link_file_path = link_file.name

                    # Step 3: Link to component types
                    cp_workflow.bulk_link_constant_property_to_component_type(link_file_path)
                    st.success("Step 2: Properties linked to component types successfully.")

        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
