# Medical Interaction Checker
A system for analyzing potential interactions between medications, conditions, and patient factors using Retrieval-Augmented Generation with Ollama local models.
![localhost_8501-MedInteract(1)](https://github.com/user-attachments/assets/bdd80c94-46f3-41e4-87c0-76aeaf3436e8)
![localhost_8501-MedInteract(2)](https://github.com/user-attachments/assets/4a7a3d69-4b30-43f2-9738-074b430d6483)
![localhost_8501-MedInteract(3)](https://github.com/user-attachments/assets/2ee171bf-ce5e-45b1-abd3-b0c72355e295)
## Setup Instructions
### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Ollama
1. Download and install Ollama from the official website: [https://ollama.com/download](https://ollama.com/download)
2. Pull the desired Llama model:
```bash
ollama pull llama3
```

### 3. Prepare Medical Reference Data
1. Create a `data` directory in the project root
2. Place your medical PDFs (like "KD-Tripathi-Pharmacology-Book.pdf") in this directory

### 4. Project Structure
```
medical-interaction-checker/
├── app.py                 # Core application logic
├── data_loader.py         # PDF loading and processing
├── model.py               # RAG and LLM management with Ollama
├── streamlit_app.py       # User interface
├── data/                  # Directory for your medical PDFs
│   └── KD-Tripathi-Pharmacology-Book.pdf
└── chroma_db/             # Vector database storage (created automatically)
```

### 5. Run the Application
```bash
streamlit run streamlit_app.py
```

## Usage Instructions
1. **Start Ollama**: Ensure Ollama is running in the background
2. **Initialize the System**: Click the "Initialize System" button in the sidebar when you first run the application
3. **Input Patient Data**: Fill out the form with patient information, medications, and conditions
4. **Analyze Interactions**: Click "Analyze Interactions" to get a detailed analysis
5. **Review Results**: The system will highlight potential interactions based on your medical PDFs

## Ollama Configuration
In your `model.py`, you'll need to modify if u want to change the model:

```python
import ollama

def initialize_model():
    # Use Ollama's local model
    client = ollama.Client()
    model = client.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': 'Hello'}]
    )
    return model
```

## Important Notes
- Ensure Ollama is running before starting the application
- The quality of analysis depends on the content of your reference PDFs
- For best performance, use a system with sufficient RAM

## Troubleshooting
### Ollama Issues
- Verify Ollama is installed and running: `ollama list`
- Check that the Llama3 model is pulled: `ollama pull llama3.1`
- Restart Ollama if you encounter connection issues

### PDF Processing Issues
- Verify PDFs are text-based and readable
- Convert scanned PDFs to searchable PDFs if needed


## Disclaimer
This tool is intended as a reference only and should not replace clinical judgment. Always consult official prescribing information and guidelines.

## Contributing
Contributions are welcome! Please submit pull requests or open issues on the project repository.


