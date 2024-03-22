import streamlit as st
from honeybee_energy.simulation.control import SimulationControl
from honeybee_energy.simulation.output import SimulationOutput
from honeybee_energy.simulation.parameter import SimulationParameter
from honeybee_energy.simulation.output import SimulationOutput  # Assuming similar functions exist for these
from honeybee_energy.simulation.control import SimulationControl
from honeybee_energy.simulation.runperiod import RunPeriod
from honeybee_energy.simulation.shadowcalculation import ShadowCalculation
from honeybee_energy.simulation.sizing import SizingParameter
from honeybee_energy.simulation.runperiod import RunPeriod
from honeybee_energy.simulation.shadowcalculation import ShadowCalculation
from honeybee_energy.simulation.sizing import SizingParameter
import pandas as pd
from honeybee_energy.simulation.runperiod import RunPeriod
from datetime import datetime

def create_simulation_control():
    # Streamlit interface for SimulationControl inputs
    do_zone_sizing = st.checkbox("Zone Sizing Calculation", value=True, help="Whether the zone sizing calculation should be run.")
    do_system_sizing = st.checkbox("System Sizing Calculation", value=True, help="Whether the system sizing calculation should be run.")
    do_plant_sizing = st.checkbox("Plant Sizing Calculation", value=True, help="Whether the plant sizing calculation should be run.")
    run_for_sizing_periods = st.checkbox("Run for Sizing Periods", value=False, help="Whether the simulation should be run for the sizing periods.")
    run_for_run_periods = st.checkbox("Run for Run Periods", value=True, help="Whether the simulation should be run for the run periods.")

    # Create SimulationControl object with user inputs
    simulation_control = SimulationControl(
        do_zone_sizing=do_zone_sizing,
        do_system_sizing=do_system_sizing,
        do_plant_sizing=do_plant_sizing,
        run_for_sizing_periods=run_for_sizing_periods,
        run_for_run_periods=run_for_run_periods
    )
    
    return simulation_control

def create_simulation_output():
    # Streamlit interface for SimulationOutput inputs
    
    # Let users input a list of outputs. Here, a simple text area is used for simplicity,
    # but it could be enhanced to offer a selection from a predefined list or multiple text inputs.
    outputs_input = st.text_area("Outputs",
                                 help="List of EnergyPlus output names as strings, separated by commas. Leave blank for none.")
    outputs = [output.strip() for output in outputs_input.split(',')] if outputs_input else None
    
    # Reporting frequency
    reporting_frequency = st.selectbox("Reporting Frequency",
                                       options=SimulationOutput.REPORTING_FREQUENCIES,
                                       index=SimulationOutput.REPORTING_FREQUENCIES.index('Hourly'),
                                       help="Frequency at which the outputs are reported.")
    
    # Include SQLite
    include_sqlite = st.checkbox("Include SQLite Report", value=True,
                                 help="Whether a SQLite report should be generated from the simulation.")
    
    # Include HTML
    include_html = st.checkbox("Include HTML Report", value=True,
                               help="Whether an HTML report should be generated from the simulation.")
    
    # Summary reports input
    summary_reports_input = st.text_area("Summary Reports",
                                         help="List of EnergyPlus summary report names as strings, separated by commas. Use 'AllSummary' for all reports.")
    summary_reports = [report.strip() for report in summary_reports_input.split(',')] if summary_reports_input else ('AllSummary',)
    
    # Unmet setpoint tolerance
    unmet_setpoint_tolerance = st.number_input("Unmet Setpoint Tolerance", value=1.11, min_value=0.0, format="%.2f",
                                               help="Tolerance in degrees Celsius for unmet setpoint calculation.")
    
    # Create SimulationOutput object with user inputs
    simulation_output = SimulationOutput(
        outputs=outputs,
        reporting_frequency=reporting_frequency,
        include_sqlite=include_sqlite,
        include_html=include_html,
        summary_reports=summary_reports,
        unmet_setpoint_tolerance=unmet_setpoint_tolerance
    )
    
    return simulation_output

def create_simulation_parameter():
    # Assuming you have similar Streamlit interfaces for the complex objects
    output = create_simulation_output()
    run_period = create_run_period()
    timestep = st.slider("Timesteps per hour", 1, 60, 6)
    simulation_control = create_simulation_control()
    shadow_calculation = create_shadow_calculation()
    sizing_parameter = create_sizing_parameter()
    north_angle = st.slider("North Angle", -360, 360, 0)
    terrain_type = st.selectbox("Terrain Type", ['Ocean', 'Country', 'Suburbs', 'Urban', 'City'], index=4)

    simulation_parameter = SimulationParameter(
        output=output,
        run_period=run_period,
        timestep=timestep,
        simulation_control=simulation_control,
        shadow_calculation=shadow_calculation,
        sizing_parameter=sizing_parameter,
        north_angle=north_angle,
        terrain_type=terrain_type
    )
    
    return simulation_parameter

def create_run_period():
    # Streamlit interface for RunPeriod inputs
    start_date = st.date_input("Start Date", value=datetime(2023, 1, 1))
    end_date = st.date_input("End Date", value=datetime(2023, 12, 31))
    
    start_day_of_week = st.selectbox("Start Day of the Week", 
                                     options=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 
                                     index=0)
    
    # For simplicity, we're not handling holidays and daylight saving time here
    # This example assumes no holidays and no daylight saving time adjustments
    
    # Convert start and end dates to Honeybee's expected format
    # Note: Honeybee and Ladybug use a 'month/day' format for dates.
    start_date_str = start_date.strftime("%m/%d")
    end_date_str = end_date.strftime("%m/%d")

    # Create RunPeriod object
    run_period = RunPeriod(
        start_date=start_date_str, 
        end_date=end_date_str, 
        start_day_of_week=start_day_of_week
    )
    
    return run_period

def create_shadow_calculation():
    # Streamlit interface for ShadowCalculation inputs
    solar_distribution = st.selectbox(
        "Solar Distribution",
        options=[
            'MinimalShadowing', 
            'FullExterior', 
            'FullInteriorAndExterior', 
            'FullExteriorWithReflections', 
            'FullInteriorAndExteriorWithReflections'
        ], 
        index=3,  # Default to 'FullExteriorWithReflections'
        help="Describes how EnergyPlus treats beam solar radiation and reflections from surfaces."
    )
    
    calculation_method = st.selectbox(
        "Calculation Method",
        options=['PolygonClipping', 'PixelCounting'],
        index=0,  # Default to 'PolygonClipping'
        help="CPU-based polygon clipping or GPU-based pixel counting method."
    )
    
    calculation_update_method = st.selectbox(
        "Calculation Update Method",
        options=['Periodic', 'Timestep'],
        index=0,  # Default to 'Periodic'
        help="Describes how often solar and shading calculations are updated."
    )
    
    calculation_frequency = st.slider(
        "Calculation Frequency",
        min_value=1,
        max_value=365,
        value=30,  # Default
        help="Number of days in each period for a unique shadow calculation, used if Periodic method is selected."
    )
    
    maximum_figures = st.number_input(
        "Maximum Figures",
        min_value=1000,
        max_value=30000,
        value=15000,  # Default
        step=1000,
        help="Number of figures used in shadow overlaps."
    )
    
    # Create ShadowCalculation object
    shadow_calculation = ShadowCalculation(
        solar_distribution=solar_distribution,
        calculation_method=calculation_method,
        calculation_update_method=calculation_update_method,
        calculation_frequency=calculation_frequency,
        maximum_figures=maximum_figures
    )
    
    return shadow_calculation

def create_sizing_parameter():
    # Streamlit interface for SizingParameter inputs
    heating_factor = st.number_input("Heating Factor", value=1.25, min_value=0.0, help="Multiplier for peak heating load.")
    cooling_factor = st.number_input("Cooling Factor", value=1.15, min_value=0.0, help="Multiplier for peak cooling load.")
    
    efficiency_standard = st.selectbox(
        "Efficiency Standard",
        options=[None, 'DOE_Ref_Pre_1980', 'DOE_Ref_1980_2004', 'ASHRAE_2004', 'ASHRAE_2007', 'ASHRAE_2010', 'ASHRAE_2013', 'ASHRAE_2016', 'ASHRAE_2019'],
        index=0,  # Default to None
        help="Efficiency standard for setting HVAC equipment efficiencies."
    )
    
    climate_zone = st.selectbox(
        "Climate Zone",
        options=[None] + ['0A', '1A', '2A', '3A', '4A', '5A', '6A', '0B', '1B', '2B', '3B', '4B', '5B', '6B', '3C', '4C', '5C', '7', '8'],
        index=0,  # Default to None
        help="ASHRAE climate zone for the efficiency standard."
    )
    
    building_type = st.selectbox(
        "Building Type",
        options=[None, 'NonResidential', 'Residential', 'MidriseApartment', 'HighriseApartment', 'LargeOffice', 'MediumOffice', 'SmallOffice', 'Retail', 'StripMall', 'PrimarySchool', 'SecondarySchool', 'SmallHotel', 'LargeHotel', 'Hospital', 'Outpatient', 'Warehouse', 'SuperMarket', 'FullServiceRestaurant', 'QuickServiceRestaurant', 'Laboratory', 'Courthouse'],
        index=0,  # Default to None
        help="Building type for the efficiency standard."
    )
    
    bypass_efficiency_sizing = st.checkbox("Bypass Efficiency Sizing", value=False, help="Whether to bypass the efficiency sizing run.")
    
    # Create SizingParameter object
    sizing_parameter = SizingParameter(
        design_days=None,  # Assuming design days are set elsewhere or not needed for this example
        heating_factor=heating_factor,
        cooling_factor=cooling_factor,
        efficiency_standard=efficiency_standard,
        climate_zone=climate_zone,
        building_type=building_type,
        bypass_efficiency_sizing=bypass_efficiency_sizing
    )
    
    return sizing_parameter



def run_simulation(simulation_parameters):
    # Assuming `model` is your energy model already created and setup
    # and you've created your simulation settings with the functions provided earlier
    # Apply simulation parameters to the model
    st.session_state.hb_model.simulation_parameter = simulation_parameters
    #TODO - write code to serialize the HB Json file and return the path
    # Step 3: Run the simulation
    # Define the folder where the simulation will be run and where the results will be saved
    output_folder = 'path/to/output_folder'
    # Define the path to the EnergyPlus executable
    energyplus_path = 'path/to/energyplus'

    import subprocess

    # Define paths
    hbjson_path = 'path/to/your/model.hbjson'
    output_folder = 'path/to/output/folder'
    energyplus_path = 'path/to/energyplus'  # Optional if EnergyPlus is in PATH

    # Construct the command
    command = [
        'honeybee-energy', 'run', hbjson_path,
        '--folder', output_folder
    ]

    # Add the EnergyPlus path if it's not in the system PATH
    if energyplus_path:
        command.extend(['--energyplus-path', energyplus_path])

    # Run the command
    subprocess.run(command, check=True)

### for next week ###
    
import os
from honeybee.model import Model

def save_model_to_hbjson(hb_model, file_path):
    """
    Serialize a Honeybee model to an HBJSON file.

    Args:
        hb_model: A Honeybee model object.
        file_path: The file path where the HBJSON will be saved.
    
    Returns:
        The path to the saved HBJSON file.
    """
    # Serialize the model to a dictionary
    model_dict = hb_model.to_dict()
    
    # Serialize the dictionary to a JSON string
    # Note: We're using the json module, but you can use any method you prefer for serialization
    import json
    model_json = json.dumps(model_dict)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save the JSON string to a file
    with open(file_path, 'w') as fp:
        fp.write(model_json)
    
    return file_path

# Example usage
if __name__ == "__main__":
    # Assume `model` is your Honeybee Model object
    model = Model(...)  # Replace this with your model creation or loading logic

    # Define the path where you want to save the HBJSON
    hbjson_path = 'path/to/your/model.hbjson'

    # Save the model to an HBJSON file
    saved_path = save_model_to_hbjson(model, hbjson_path)
    print(f"Model saved to: {saved_path}")
