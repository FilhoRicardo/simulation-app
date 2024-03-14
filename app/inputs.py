
import streamlit as st
import json
import web as web
import tempfile
from pathlib import Path
from honeybee.model import Model,Room


def initialize():
    if "epw_data" not in st.session_state: 
        st.session_state.epw_data = None
    if "hb_model" not in st.session_state: 
        st.session_state.hb_model = None
    if "temp_folder" not in st.session_state: 
        st.session_state.temp_folder = Path(tempfile.mkdtemp()) #not going to generate a local file, just creates a temporary file in memory
    if "hb_json_path" not in st.session_state: 
        st.session_state.hb_json_path = None
    if "ddy_data" not in st.session_state:
        st.session_state.ddy_data = None

def display_model_geometry():
       
    st.session_state.hb_json_path = st.session_state.temp_folder.joinpath(f"{st.session_state.hb_model.identifier}.hbjson")
    st.session_state.hb_json_path.write_text(json.dumps(st.session_state.hb_model.to_dict()))
    web.show_model(st.session_state.hb_json_path)

def upload_hbjson_file():
        
    # Upload Honeybee JSON file
    uploaded_file = st.file_uploader("Upload a Honeybee JSON (*.hbjson) file", type=["json"])
    
    if uploaded_file is not None:
        # Read and parse the JSON file
        try:
            hbjson_data = json.load(uploaded_file)
        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid *.json file.")
            return
        
        # Check if the JSON file contains a Honeybee model
        if "type" in hbjson_data and hbjson_data["type"] == "Model":
            st.success("Honeybee JSON file successfully loaded.")
            
            # Create a Honeybee model object from the deserialized data
            st.session_state.hb_model = Model.from_dict(hbjson_data)
            
            # Visualize the 3D model using Polination Streamlit Viewer
            display_model_geometry()
        else:
            st.error("The uploaded JSON file does not contain a valid Honeybee model.")

import streamlit as st

def upload_design_weather_file():
        
    # Upload .DDY design weather file
    uploaded_file = st.file_uploader("Upload a Design Weather (.DDY) file", type=["ddy"])
    
    if uploaded_file is not None:
        # Attempt to read the .DDY file
        try:
            # Assuming the .DDY file is text, we read it as such
            content = uploaded_file.getvalue().decode("utf-8")
        except Exception as e:
            st.error(f"Failed to read the .DDY file. Error: {e}")
            return None      
       
        # If the file passes the basic checks, we consider it a valid .DDY file
        st.success(".DDY file successfully uploaded.")
        
        # Convert the file content into a Python object
        # For this example, we'll simply use the file's text content
        ddy_data = content
        
        # Here you would typically process the ddy_data
        # For demonstration, we'll just store it in the session state
        st.session_state.ddy_data = ddy_data

def upload_weather_file():
        
    # Upload EPW weather file
    uploaded_file = st.file_uploader("Upload an EnergyPlus Weather (EPW) file", type=["epw"])
    
    if uploaded_file is not None:
        # Attempt to read the EPW file
        try:
            # Assuming the EPW file is text, we read it line by line
            lines = uploaded_file.getvalue().decode("utf-8").splitlines()
        except Exception as e:
            st.error(f"Failed to read the EPW file. Error: {e}")
            return None
        
        # Basic validation of the EPW file structure
        if len(lines) < 8:
            st.error("Invalid EPW file. The file seems to be too short.")
            return None
        
        if not lines[0].startswith("LOCATION"):
            st.error("Invalid EPW file. The file does not start with a LOCATION line.")
            return None
        
        # If the file passes the checks, we consider it a valid EPW file
        st.success("EPW file successfully uploaded.")
        
        # Convert the lines into a Python object (for demonstration purposes, this will just be a list of lines)
        epw_data = lines
        
        # Here you would typically convert epw_data into a more specific object
        # For demonstration, we'll just store it in the session state
        st.session_state.epw_data = epw_data