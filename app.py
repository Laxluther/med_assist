from model import MedicalInteractionModel
from data_loader import MedicalDataLoader

class MedicalInteractionApp:
    """Main application class for the Medical Interaction Checker system."""
    
    def __init__(self, model_name="llama3", data_dir="data"):
        self.model = MedicalInteractionModel(model_name=model_name)
        self.data_loader = MedicalDataLoader(data_dir=data_dir)
        self.is_initialized = False
        
    def initialize(self):
        """Initialize the system by loading documents and setting up the model."""
        try:
            # Load and split documents
            chunks = self.data_loader.load_and_split()
            
            if not chunks:
                return False, "No document chunks available. Please add PDF files to the data directory."
            
            # Initialize the model with the chunks
            self.model.initialize(chunks)
            self.is_initialized = True
            
            return True, "System initialized successfully!"
        except Exception as e:
            return False, f"Error initializing system: {str(e)}"
            
    def analyze_interactions(self, current_meds, allergies, conditions, new_meds, patient_info, additional_info=""):
        """Analyze potential drug interactions."""
        if not self.is_initialized:
            self.initialize()
            
        return self.model.analyze_interactions(
            current_meds, allergies, conditions, new_meds, patient_info, additional_info
        )