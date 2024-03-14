
"""Streamlit application for creating and visualizing Room Properties.

This module defines the main application interface and logic for the Streamlit 
application. The application allows users to set parameters for a building's 
geometry, generates the corresponding building model, and provides an option 
to visualize the model.
"""

# Import necessary libraries and modules
import streamlit as st
from pathlib import Path
import tempfile
import json


# Import local modules for handling inputs and web visualization
from inputs import (initialize,upload_hbjson_file,upload_design_weather_file,
                    upload_weather_file)
import web as web

# Set the page configuration for Streamlit, defining the title
st.set_page_config(page_title="Simulation App")

def main():
    """Main function for the Room Properties Streamlit App.
    
    This function orchestrates the user interface and interactions for the 
    Streamlit application. It initializes session state variables, displays 
    input sliders for users to set building parameters, generates the building 
    model based on those parameters, and provides an option to visualize the 
    model in 3D.
    """
   
    # Initialize session state variables and settings for the application
    initialize()

    # Allow user to upload a Honeybee json file
    st.title("Simulation Files Uploader")
    upload_hbjson_file()
    upload_design_weather_file()
    upload_weather_file()

    if st.session_state.hb_model and st.session_state.epw_data and st.session_state.ddy_data:
        if st.button("Load files"):
            st.success("Files loaded successfuly")
            tab1, tab2, = st.tabs(["Simulation Settings", "Results"])
            with tab1:
                st.header("Simulation")
            
            with tab2:
                st.header("Results")
            
            st.text("Download simulation Results")
            # To download the model results, if a run was successful
            json_string = json.dumps(st.session_state.hb_model.to_dict())
            st.download_button(label="Download results (.csv)",data=json_string,file_name="Rsults.csv",mime="text/csv")
    else:
        # Use a placeholder to show a disabled-like button
        st.button("Load files", disabled=True)     

if __name__ == "__main__":
    # Run the main function if this module is executed as the main script
    main()
