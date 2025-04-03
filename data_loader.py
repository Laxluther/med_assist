import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class MedicalDataLoader:
    """Handles loading and processing of medical PDF documents."""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        
    def load_and_split(self, chunk_size=1000, chunk_overlap=200):
        """Load and split documents in one step."""
        if not os.path.exists(self.data_dir):
            print(f"Creating data directory '{self.data_dir}'")
            os.makedirs(self.data_dir)
            return []
            
        pdf_files = [f for f in os.listdir(self.data_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in '{self.data_dir}'. Please add some medical PDFs.")
            return []
            
        documents = []
        
        print(f"Loading {len(pdf_files)} PDF files from {self.data_dir}...")
        for pdf_file in pdf_files:
            file_path = os.path.join(self.data_dir, pdf_file)
            try:
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
                print(f"✓ Loaded {pdf_file}")
            except Exception as e:
                print(f"✗ Error loading {pdf_file}: {str(e)}")
                
        if not documents:
            return []
        
        print(f"Splitting {len(documents)} documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks for processing")
        
        return chunks