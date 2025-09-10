"""
Streamlit Dashboard for Revenue Leakage Detection System
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
import json
import sys
import tempfile

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Now we can import from app module
IMPORT_SUCCESS = True
IMPORT_ERRORS = []

try:
    from app.utils.data_generator import DataGenerator
except ImportError as e:
    IMPORT_ERRORS.append(f"DataGenerator: {e}")
    IMPORT_SUCCESS = False

try:
    from app.utils.ocr_reader import OCRReader
except ImportError as e:
    IMPORT_ERRORS.append(f"OCRReader: {e}")
    IMPORT_SUCCESS = False

# Additional imports that might be needed
try:
    import cv2
except ImportError as e:
    IMPORT_ERRORS.append(f"OpenCV (cv2): {e}")
    IMPORT_SUCCESS = False

# Set page configuration
st.set_page_config(
    page_title="Revenue Leakage Detection System",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e0e0e0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_files' not in st.session_state:
    st.session_state.generated_files = []

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Incidents", "Detection", "Data Generator", "Settings"])

# Mock data generation functions
def generate_mock_incidents():
    """Generate mock incident data"""
    incident_types = ["missing_charge", "incorrect_rate", "usage_mismatch", "duplicate_entry"]
    severities = ["low", "medium", "high", "critical"]
    statuses = ["detected", "investigating", "resolved", "closed"]
    
    incidents = []
    for i in range(50):
        incident = {
            "ID": f"INC-{1000+i}",
            "Type": np.random.choice(incident_types),
            "Severity": np.random.choice(severities),
            "Status": np.random.choice(statuses),
            "Description": f"Sample incident description for {np.random.choice(incident_types).replace('_', ' ')}",
            "Financial Impact ($)": round(np.random.uniform(10, 1000), 2),
            "Detected At": datetime.now() - timedelta(days=np.random.randint(0, 30)),
            "Related Entities": f"CUST-{np.random.randint(100, 999)}",
        }
        incidents.append(incident)
    
    return pd.DataFrame(incidents)

def generate_mock_financial_data():
    """Generate mock financial impact data"""
    dates = pd.date_range(datetime.now() - timedelta(days=90), datetime.now(), freq='D')
    data = []
    for date in dates:
        data.append({
            "Date": date,
            "Financial Impact ($)": round(np.random.uniform(100, 2000), 2),
            "Incident Count": np.random.randint(1, 10)
        })
    return pd.DataFrame(data)

def generate_mock_root_cause_data():
    """Generate mock root cause distribution data"""
    causes = ["System Integration Error", "Manual Entry Error", "Contract Misinterpretation", 
              "Rate Configuration Issue", "Billing Process Failure", "Data Synchronization Issue"]
    values = [35, 25, 20, 10, 7, 3]
    return pd.DataFrame({"Root Cause": causes, "Count": values})

# Dashboard page
if page == "Dashboard":
    st.title("💰 Revenue Leakage Detection Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Incidents", "138", "+12%")
    
    with col2:
        st.metric("Financial Impact", "$12,450", "+8%")
    
    with col3:
        st.metric("Avg. Resolution Time", "3.2 days", "-0.5 days")
    
    with col4:
        st.metric("Detection Rate", "94%", "+2%")
    
    # Financial impact trend
    st.subheader("Financial Impact Trend")
    financial_data = generate_mock_financial_data()
    
    fig_financial = px.line(financial_data, x="Date", y="Financial Impact ($)", 
                           title="Daily Financial Impact Trend")
    fig_financial.update_layout(height=400)
    st.plotly_chart(fig_financial, use_container_width=True)
    
    # Incident distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Incident Type Distribution")
        incident_data = generate_mock_incidents()
        type_counts = incident_data["Type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]
        
        fig_types = px.pie(type_counts, values="Count", names="Type", 
                          title="Incident Types Distribution")
        st.plotly_chart(fig_types, use_container_width=True)
    
    with col2:
        st.subheader("Root Cause Analysis")
        root_cause_data = generate_mock_root_cause_data()
        
        fig_causes = px.bar(root_cause_data, x="Count", y="Root Cause", 
                           orientation='h', title="Root Cause Distribution")
        fig_causes.update_layout(height=400)
        st.plotly_chart(fig_causes, use_container_width=True)

# Incidents page
elif page == "Incidents":
    st.title("📋 Incident Management")
    
    # Generate mock data
    df = generate_mock_incidents()
    
    # Filters
    st.sidebar.subheader("Filters")
    
    incident_type = st.sidebar.multiselect(
        "Incident Type",
        options=df["Type"].unique(),
        default=df["Type"].unique()
    )
    
    severity = st.sidebar.multiselect(
        "Severity",
        options=df["Severity"].unique(),
        default=df["Severity"].unique()
    )
    
    status = st.sidebar.multiselect(
        "Status",
        options=df["Status"].unique(),
        default=df["Status"].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df["Type"].isin(incident_type)) &
        (df["Severity"].isin(severity)) &
        (df["Status"].isin(status))
    ]
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Filtered Incidents", len(filtered_df))
    
    with col2:
        total_impact = filtered_df["Financial Impact ($)"].sum()
        st.metric("Total Financial Impact", f"${total_impact:,.2f}")
    
    with col3:
        avg_impact = filtered_df["Financial Impact ($)"].mean()
        st.metric("Average Impact per Incident", f"${avg_impact:,.2f}")
    
    # Incident table
    st.subheader("Incident List")
    
    # Format the dataframe for display
    display_df = filtered_df.copy()
    display_df["Detected At"] = display_df["Detected At"].dt.strftime("%Y-%m-%d %H:%M")
    
    st.dataframe(
        display_df,
        column_config={
            "ID": st.column_config.TextColumn("ID"),
            "Type": st.column_config.TextColumn("Type"),
            "Severity": st.column_config.TextColumn("Severity"),
            "Status": st.column_config.TextColumn("Status"),
            "Description": st.column_config.TextColumn("Description"),
            "Financial Impact ($)": st.column_config.NumberColumn("Financial Impact ($)", format="$%.2f"),
            "Detected At": st.column_config.TextColumn("Detected At"),
            "Related Entities": st.column_config.TextColumn("Related Entities"),
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Incident details
    st.subheader("Incident Details")
    selected_incident = st.selectbox("Select an incident to view details", 
                                    options=filtered_df["ID"].tolist())
    
    if selected_incident:
        incident_details = filtered_df[filtered_df["ID"] == selected_incident].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Incident Information**")
            st.write(f"**ID:** {incident_details['ID']}")
            st.write(f"**Type:** {incident_details['Type'].replace('_', ' ')}")
            st.write(f"**Severity:** {incident_details['Severity']}")
            st.write(f"**Status:** {incident_details['Status']}")
            st.write(f"**Detected At:** {incident_details['Detected At']}")
            st.write(f"**Financial Impact:** ${incident_details['Financial Impact ($)']}")
        
        with col2:
            st.write("**Description**")
            st.write(incident_details['Description'])
            
            st.write("**Related Entities**")
            st.write(incident_details['Related Entities'])
            
            st.write("**Evidence**")
            st.write("- Provisioning Record: PROV-789")
            st.write("- Billing Record: BILL-456")
            st.write("- Usage Log: USAGE-123")

# Detection page
elif page == "Detection":
    st.title("🔍 Revenue Leakage Detection")
    
    st.subheader("Run Detection")
    
    # Detection parameters
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=7))
        incident_types = st.multiselect(
            "Detection Types",
            ["Missing Charges", "Incorrect Rates", "Usage Mismatches", "Duplicate Entries"],
            ["Missing Charges", "Incorrect Rates"]
        )
    
    with col2:
        end_date = st.date_input("End Date", datetime.now())
        sensitivity = st.slider("Detection Sensitivity", 0, 100, 75)
    
    # Run detection button
    if st.button("🚀 Run Detection", type="primary"):
        st.info("Running detection... This may take a few moments.")
        
        # Simulate detection process
        import time
        with st.spinner("Analyzing data..."):
            time.sleep(2)
            
            # Generate mock results
            new_incidents = np.random.randint(1, 10)
            financial_impact = round(np.random.uniform(100, 1000), 2)
            
            st.success(f"Detection complete! Found {new_incidents} new incidents with a potential financial impact of ${financial_impact}.")
            
            # Show results
            st.subheader("Detection Results")
            results_df = generate_mock_incidents().head(new_incidents)
            st.dataframe(results_df)
    
    st.subheader("Detection Rules Configuration")
    
    # Rule configuration
    rules = [
        {"name": "Missing Charge Detection", "description": "Detect services provisioned but not billed", "enabled": True},
        {"name": "Incorrect Rate Detection", "description": "Detect billing records with wrong rates", "enabled": True},
        {"name": "Usage Mismatch Detection", "description": "Detect discrepancies between usage and billing", "enabled": True},
        {"name": "Duplicate Entry Detection", "description": "Detect duplicate billing entries", "enabled": True},
    ]
    
    for i, rule in enumerate(rules):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{rule['name']}**")
            st.write(rule['description'])
        with col2:
            st.checkbox("Enabled", value=rule['enabled'], key=f"rule_{i}")

# Data Generator page
elif page == "Data Generator":
    st.title("📂 Data Generator & File Upload")
    
    if not IMPORT_SUCCESS:
        st.error("Data generator modules not available. Please check your installation.")
        if IMPORT_ERRORS:
            st.write("Specific errors:")
            for error in IMPORT_ERRORS:
                st.write(f"- {error}")
        st.stop()
    
    # Initialize data generator
    try:
        generator = DataGenerator()
        ocr_reader = OCRReader()
    except Exception as e:
        st.error(f"Error initializing data generator: {e}")
        st.stop()
    
    # Tabs for different functionalities
    tab1, tab2 = st.tabs(["Generate Sample Data", "Upload Your Data"])
    
    with tab1:
        st.subheader("Generate Sample Data Files")
        st.write("Create sample PDF, CSV, and JSON files with realistic billing, provisioning, and contract data.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**PDF Billing Data**")
            pdf_records = st.number_input("Number of billing records", min_value=5, max_value=100, value=20, key="pdf_records")
            if st.button("Generate PDF"):
                with st.spinner("Generating PDF..."):
                    try:
                        pdf_path, pdf_data = generator.generate_pdf_billing_file(num_records=pdf_records)
                        st.session_state.generated_files.append(pdf_path)
                        st.success(f"Generated PDF: {os.path.basename(pdf_path)}")
                        st.download_button(
                            label="Download PDF",
                            data=open(pdf_path, "rb").read(),
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Error generating PDF: {e}")
        
        with col2:
            st.write("**CSV Provisioning Data**")
            csv_records = st.number_input("Number of provisioning records", min_value=5, max_value=100, value=20, key="csv_records")
            if st.button("Generate CSV"):
                with st.spinner("Generating CSV..."):
                    try:
                        csv_path, csv_data = generator.generate_csv_provisioning_file(num_records=csv_records)
                        st.session_state.generated_files.append(csv_path)
                        st.success(f"Generated CSV: {os.path.basename(csv_path)}")
                        st.download_button(
                            label="Download CSV",
                            data=open(csv_path, "rb").read(),
                            file_name=os.path.basename(csv_path),
                            mime="text/csv"
                        )
                    except Exception as e:
                        st.error(f"Error generating CSV: {e}")
        
        with col3:
            st.write("**JSON Contract Data**")
            json_records = st.number_input("Number of contract records", min_value=1, max_value=50, value=10, key="json_records")
            if st.button("Generate JSON"):
                with st.spinner("Generating JSON..."):
                    try:
                        json_path, json_data = generator.generate_json_contract_file(num_records=json_records)
                        st.session_state.generated_files.append(json_path)
                        st.success(f"Generated JSON: {os.path.basename(json_path)}")
                        st.download_button(
                            label="Download JSON",
                            data=open(json_path, "rb").read(),
                            file_name=os.path.basename(json_path),
                            mime="application/json"
                        )
                    except Exception as e:
                        st.error(f"Error generating JSON: {e}")
        
        # Display generated files
        if st.session_state.generated_files:
            st.subheader("Generated Files")
            for file_path in st.session_state.generated_files:
                st.write(f"- {os.path.basename(file_path)}")
    
    with tab2:
        st.subheader("Upload Your Data Files")
        st.write("Upload your own PDF, CSV, or JSON files for processing.")
        
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "csv", "json"])
        
        if uploaded_file is not None:
            # Create a temporary file to save the uploaded file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Process based on file type
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_extension == ".pdf":
                st.subheader("PDF Content (OCR)")
                with st.spinner("Processing PDF with OCR..."):
                    # For demo purposes, we'll just show file info
                    # In a real implementation, you would use OCR to extract text
                    st.info("In a full implementation, this would use OCR to extract text from the PDF.")
                    st.write(f"File size: {len(uploaded_file.getvalue())} bytes")
                    st.write(f"File name: {uploaded_file.name}")
                    
            elif file_extension == ".csv":
                st.subheader("CSV Data")
                try:
                    # Read CSV file
                    df = pd.read_csv(tmp_file_path)
                    st.write(f"Rows: {len(df)}, Columns: {len(df.columns)}")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
                    
            elif file_extension == ".json":
                st.subheader("JSON Data")
                try:
                    # Read JSON file
                    data = json.load(open(tmp_file_path, 'r'))
                    st.write(f"Data records: {len(data) if isinstance(data, list) else 'N/A'}")
                    st.json(data)
                except Exception as e:
                    st.error(f"Error reading JSON: {e}")
            
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except:
                pass

# Settings page
elif page == "Settings":
    st.title("⚙️ System Settings")
    
    st.subheader("Qdrant Configuration")
    qdrant_host = st.text_input("Qdrant Host", "localhost")
    qdrant_port = st.number_input("Qdrant Port", 6333)
    
    st.subheader("Gemini Configuration")
    gemini_api_key = st.text_input("Gemini API Key", type="password")
    
    st.subheader("Data Sources")
    st.checkbox("Enable Billing Data Source", True)
    st.checkbox("Enable Provisioning Data Source", True)
    st.checkbox("Enable Usage Data Source", True)
    st.checkbox("Enable Contract Data Source", True)
    
    st.subheader("Alerting")
    st.checkbox("Enable Email Alerts", True)
    st.checkbox("Enable Slack Notifications", False)
    email_recipients = st.text_input("Email Recipients", "team@example.com")
    
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Revenue Leakage Detection System v1.0")