import streamlit as st
import os
from app import MedicalInteractionApp
import time

# Set page configuration
st.set_page_config(
    page_title="MedInteract",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a more fun interface
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .big-font {
        font-size: 24px !important;
    }
    .med-font {
        font-size: 18px !important;
    }
    .highlight {
        padding: 20px;
        border-radius: 10px;
        background-color: #e6f3ff;
        margin-bottom: 20px;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        background-color: white;
    }
    .emoji-heading {
        font-size: 28px;
    }
    .stButton button {
        border-radius: 20px;
        font-weight: bold;
        padding: 10px 25px;
    }
    .sources {
        font-size: 12px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'app' not in st.session_state:
    st.session_state.app = MedicalInteractionApp()
if 'current_meds' not in st.session_state:
    st.session_state.current_meds = []
if 'allergies' not in st.session_state:
    st.session_state.allergies = []
if 'conditions' not in st.session_state:
    st.session_state.conditions = []
if 'new_meds' not in st.session_state:
    st.session_state.new_meds = []
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'result' not in st.session_state:
    st.session_state.result = None

# Helper functions for dynamic form elements
def add_current_med():
    st.session_state.current_meds.append({"name": "", "dosage": ""})

def remove_current_med(index):
    st.session_state.current_meds.pop(index)

def add_allergy():
    st.session_state.allergies.append({"name": "", "reaction": ""})

def remove_allergy(index):
    st.session_state.allergies.pop(index)

def add_condition():
    st.session_state.conditions.append("")

def remove_condition(index):
    st.session_state.conditions.pop(index)

def add_new_med():
    st.session_state.new_meds.append({"name": "", "dosage": ""})

def remove_new_med(index):
    st.session_state.new_meds.pop(index)

def clear_form():
    """Clear all form fields."""
    st.session_state.current_meds = []
    st.session_state.allergies = []
    st.session_state.conditions = []
    st.session_state.new_meds = []
    if 'age' in st.session_state:
        st.session_state.age = ""
    if 'gender' in st.session_state:
        st.session_state.gender = ""
    if 'bp' in st.session_state:
        st.session_state.bp = ""
    if 'additional_info' in st.session_state:
        st.session_state.additional_info = ""
    st.session_state.analysis_done = False
    st.session_state.result = None

def run_analysis():
    """Run the interaction analysis."""
    # Check if we have at least one new medication
    if not st.session_state.new_meds or not any(med["name"] for med in st.session_state.new_meds):
        st.warning("⚠️ Please add at least one new medication to check for interactions")
        return
        
    # Filter out empty entries
    filtered_current_meds = [med for med in st.session_state.current_meds if med["name"]]
    filtered_allergies = [allergy for allergy in st.session_state.allergies if allergy["name"]]
    filtered_conditions = [condition for condition in st.session_state.conditions if condition]
    filtered_new_meds = [med for med in st.session_state.new_meds if med["name"]]
    
    # Collect patient info
    patient_info = {
        "age": st.session_state.age if 'age' in st.session_state else "",
        "gender": st.session_state.gender if 'gender' in st.session_state else "",
        "bp": st.session_state.bp if 'bp' in st.session_state else ""
    }
    
    # Get additional info
    additional_info = st.session_state.additional_info if 'additional_info' in st.session_state else ""
    
    with st.spinner("🔍 Analyzing potential interactions..."):
        # Run analysis
        result = st.session_state.app.analyze_interactions(
            filtered_current_meds, 
            filtered_allergies, 
            filtered_conditions, 
            filtered_new_meds,
            patient_info,
            additional_info
        )
        
        # Store result in session state
        st.session_state.result = result
        st.session_state.analysis_done = True

# Main UI
st.title("💊 MedInteract: Drug Interaction Checker")

# Check data directory
data_dir = "data"
if not os.path.exists(data_dir) or not [f for f in os.listdir(data_dir) if f.endswith('.pdf')]:
    st.warning("⚠️ No medical data found! Please add PDF files to the 'data' folder.")

# Display main interface with animated tabs
tab1, tab2 = st.tabs(["📝 Enter Information", "📊 View Analysis"])

# Tab 1: Input Form
with tab1:
    st.markdown('<p class="big-font">Enter Patient & Medication Details</p>', unsafe_allow_html=True)
    
    # Basic patient info
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="emoji-heading">👤 Patient Information</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.text_input("Age", key="age", placeholder="e.g., 45")
    with col2:
        gender = st.selectbox("Gender", ["", "Male", "Female", "Other"], key="gender")
    with col3:
        bp = st.text_input("Blood Pressure", key="bp", placeholder="e.g., 120/80")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Current Medications
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="emoji-heading">💊 Current Medications</p>', unsafe_allow_html=True)
    
    if not st.session_state.current_meds:
        st.info("No current medications added yet")
    
    for i, med in enumerate(st.session_state.current_meds):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.session_state.current_meds[i]["name"] = st.text_input(
                f"Medication Name #{i+1}", 
                value=med["name"],
                key=f"current_med_name_{i}",
                placeholder="e.g., Lisinopril"
            )
        with col2:
            st.session_state.current_meds[i]["dosage"] = st.text_input(
                f"Dosage #{i+1}", 
                value=med["dosage"],
                key=f"current_med_dosage_{i}",
                placeholder="e.g., 10mg daily"
            )
        with col3:
            st.button("❌", key=f"remove_current_med_{i}", on_click=remove_current_med, args=(i,))
    
    st.button("➕ Add Current Medication", on_click=add_current_med, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Allergies
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="emoji-heading">🚫 Allergies</p>', unsafe_allow_html=True)
    
    if not st.session_state.allergies:
        st.info("No allergies added yet")
    
    for i, allergy in enumerate(st.session_state.allergies):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.session_state.allergies[i]["name"] = st.text_input(
                f"Allergy #{i+1}", 
                value=allergy["name"],
                key=f"allergy_name_{i}",
                placeholder="e.g., Penicillin"
            )
        with col2:
            st.session_state.allergies[i]["reaction"] = st.text_input(
                f"Reaction #{i+1}", 
                value=allergy["reaction"],
                key=f"allergy_reaction_{i}",
                placeholder="e.g., Rash"
            )
        with col3:
            st.button("❌", key=f"remove_allergy_{i}", on_click=remove_allergy, args=(i,))
    
    st.button("➕ Add Allergy", on_click=add_allergy, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Medical Conditions
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="emoji-heading">🏥 Medical Conditions</p>', unsafe_allow_html=True)
    
    if not st.session_state.conditions:
        st.info("No medical conditions added yet")
    
    for i, condition in enumerate(st.session_state.conditions):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.session_state.conditions[i] = st.text_input(
                f"Condition #{i+1}", 
                value=condition,
                key=f"condition_{i}",
                placeholder="e.g., Diabetes, Hypertension, Asthma"
            )
        with col2:
            st.button("❌", key=f"remove_condition_{i}", on_click=remove_condition, args=(i,))
    
    st.button("➕ Add Medical Condition", on_click=add_condition, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # New medications (the ones being checked)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="emoji-heading">🆕 New Medications</p>', unsafe_allow_html=True)
    st.write("Add medications you want to check for potential interactions:")
    
    if not st.session_state.new_meds:
        st.info("No new medications added yet")
    
    for i, med in enumerate(st.session_state.new_meds):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.session_state.new_meds[i]["name"] = st.text_input(
                f"New Medication #{i+1}", 
                value=med["name"],
                key=f"new_med_name_{i}",
                placeholder="e.g., Metoprolol"
            )
        with col2:
            st.session_state.new_meds[i]["dosage"] = st.text_input(
                f"Dosage #{i+1}", 
                value=med["dosage"],
                key=f"new_med_dosage_{i}",
                placeholder="e.g., 25mg twice daily"
            )
        with col3:
            st.button("❌", key=f"remove_new_med_{i}", on_click=remove_new_med, args=(i,))
    
    st.button("➕ Add New Medication", on_click=add_new_med, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional information
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="emoji-heading">📝 Additional Information</p>', unsafe_allow_html=True)
    additional_info = st.text_area(
        "Any other relevant details (optional)",
        key="additional_info",
        height=100,
        placeholder="Enter any additional medical details or specific concerns"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        analyze_button = st.button("🔍 Analyze Interactions", type="primary", use_container_width=True, on_click=run_analysis)
    with col2:
        clear_button = st.button("🗑️ Clear Form", use_container_width=True, on_click=clear_form)

# Tab 2: Analysis Results
with tab2:
    if st.session_state.analysis_done and st.session_state.result:
        st.markdown('<p class="big-font">Analysis Results</p>', unsafe_allow_html=True)
        
        result = st.session_state.result
        
        if "error" in result:
            st.error(result["error"])
        else:
            st.markdown('<div class="card highlight">', unsafe_allow_html=True)
            st.markdown(result["analysis"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display sources
            if result.get("sources"):
                with st.expander("📚 View Source References"):
                    for i, source in enumerate(result["sources"]):
                        st.markdown(f"**Source {i+1}:** {source['source']} (Page: {source['page']})")
                        st.markdown(f"<div class='sources'>*Excerpt:* {source['content']}</div>", unsafe_allow_html=True)
                        st.markdown("---")
    else:
        if st.session_state.app.is_initialized:
            st.info("👈 Enter patient information and click 'Analyze Interactions' to see results here")
        else:
            # Simulate initialization automatically when page is loaded
            if 'auto_init' not in st.session_state:
                st.session_state.auto_init = True
                with st.spinner("🔄 Initializing system... Please wait..."):
                    success, message = st.session_state.app.initialize()
                    if success:
                        st.success("✅ System initialized successfully!")
                        time.sleep(1)
                        st.info("👈 Enter patient information and click 'Analyze Interactions' to see results here")
                    else:
                        st.error(f"❌ Initialization failed: {message}")
            else:
                st.info("👈 Enter patient information and click 'Analyze Interactions' to see results here")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 12px;'>"
    "⚠️ This tool is for educational purposes only. Always consult a healthcare professional for medical advice.</div>", 
    unsafe_allow_html=True
)