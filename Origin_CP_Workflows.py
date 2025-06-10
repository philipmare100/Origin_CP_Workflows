import streamlit as st
from coffee.client import JsonApiClient
import sys
sys.path.append('/opt/anaconda3/envs/myenvtest/lib/python3.10/site-packages')
from coffee.workflows import ConstantPropertyWorkflow
import tempfile

st.title("Constant Property Workflow - Bulk Create")

st.header("Step 1: Upload a CSV file")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    st.write("Uploaded file:", uploaded_file.name)

    if st.button("Process File"):
        try:
            # Write the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            # Use the temporary file path
            with JsonApiClient() as client:
                cp_workflow = ConstantPropertyWorkflow(client)
                cp_workflow.bulk_create_constant_property(temp_file_path)

            st.success("File processed successfully!")
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")
