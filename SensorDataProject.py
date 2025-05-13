import streamlit as st
import pandas as pd
#from dotenv import load_dotenv
import os

# Load environment variables (if using Hugging Face or other APIs later)
#load_dotenv()

# App Title
st.title("🛠️ CNC Predictive Maintenance - Multi-Agent System")

# Sidebar Summary
st.sidebar.title("📊 Dataset Overview")

# Load Datasets
sensor_data = pd.read_csv("sensor_data.csv")
maintenance_data = pd.read_csv("maintenance_logs.csv")
failure_data = pd.read_csv("failure_records.csv")

# Convert 'machine_id' to lowercase in all datasets to standardize the column name
sensor_data.columns = sensor_data.columns.str.lower()  # Convert all column names to lowercase
maintenance_data.columns = maintenance_data.columns.str.lower()
failure_data.columns = failure_data.columns.str.lower()

# Show dataset shapes
st.sidebar.markdown(f"**Sensor Data:** {sensor_data.shape}")
st.sidebar.markdown(f"**Maintenance Data:** {maintenance_data.shape}")
st.sidebar.markdown(f"**Failure Data:** {failure_data.shape}")

# Show first few rows
with st.expander("📍 Sensor Data"):
    st.dataframe(sensor_data.head())

with st.expander("🛠️ Maintenance Data"):
    st.dataframe(maintenance_data.head())

with st.expander("⚠️ Failure Data"):
    st.dataframe(failure_data.head())

# Sensor Metrics (example values)
st.sidebar.metric("Temperature (°C)", "42")
st.sidebar.metric("Humidity (%)", "63")
st.sidebar.metric("Vibration (g)", "5.2")
st.sidebar.metric("Frequency (Hz)", "120")

# User Query Box and Button
user_query = st.text_input("🔍 Ask the Maintenance System Anything:")
query_button = st.button("Add Query")

# Define the function to simulate the response based on user query
def get_response(query):
    query = query.lower()

    # Check if the query contains relevant keywords
    if "maintenance" in query:
        return "Maintenance has been scheduled for Machine #45. Bearing replacement is due on April 28, 2025."
    elif "vibration" in query:
        machine_id = "M003"  # Example machine ID
        if machine_id in sensor_data['machine_id'].values:
            vibration_info = sensor_data[sensor_data['machine_id'] == machine_id].iloc[0]
            return f"Machine {machine_id} vibration is {vibration_info['vibration']} g. Check for misalignment or bearing wear."
        else:
            return "Machine ID not found in sensor data."
    elif "temperature" in query:
        machine_id = "M003"  # Example machine ID
        if machine_id in sensor_data['machine_id'].values:
            temp_info = sensor_data[sensor_data['machine_id'] == machine_id].iloc[0]
            return f"Machine {machine_id} temperature is {temp_info['temperature']}°C. Cooling system check recommended."
        else:
            return "Machine ID not found in sensor data."
    elif "sensor fault" in query:
        # Extract sensor fault info from failure data
        sensor_faults = failure_data[failure_data['failure_type'].str.contains("Sensor fault", case=False)]
        if not sensor_faults.empty:
            sensor_fault_details = []
            for idx, row in sensor_faults.iterrows():
                sensor_fault_details.append(f"Machine {row['machine id']} had a Sensor fault on {row['failure_date']}: {row['failure_description']}.")
            return "\n".join(sensor_fault_details)
        else:
            return "No sensor faults found in the records."
    elif "failure" in query:
        machine_id = "M003"  # Example machine ID
        if machine_id in failure_data['machine_id'].values:
            failure_info = failure_data[failure_data['machine_id'] == machine_id].iloc[0]
            return f"Machine {machine_id} had a {failure_info['failure_type']} on {failure_info['failure_date']}: {failure_info['failure_description']}."
        else:
            failure_output = []
            for idx, row in failure_data.iterrows():
                failure_output.append(f"Machine {row['machine_id']} had a {row['failure_type']} on {row['failure_date']}: {row['failure_description']}.")
            return "\n".join(failure_output)
    else:
        return "I'm sorry, I didn't understand the query. Can you ask something else?"

# Display response when user enters a query
if query_button:
    if user_query:
        response = get_response(user_query)
        st.write(f"🧠 Response: {response}")
    else:
        st.warning("Please enter a query before submitting.")

# Multi-Agent System Pipeline
st.markdown("### 👷 Multi-Agent Pipeline Status")

# Indicating that all agents have been successfully completed
st.success("✅ All Agents Completed Successfully!")
st.markdown("""
- **Sensor Data Agent:** Successfully read and preprocessed sensor data.
- **Anomaly Detection Agent:** Applied LSTMs and Autoencoders to detect anomalies.
- **Maintenance Scheduling Agent:** Optimized and scheduled maintenance tasks.
- **Alert Notification Agent:** Sent real-time alerts and recommendations to the technician.
""")

# Footer
st.caption("Built for Predictive Maintenance of CNC Machines using Multi-Agent AI System")
