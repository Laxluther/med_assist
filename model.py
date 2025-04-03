import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama

class MedicalInteractionModel:
    """Manages the RAG model and interactions with the vector database."""
    
    def __init__(self, 
                model_name="llama3.1", 
                embedding_model="pritamdeka/S-PubMedBert-MS-MARCO",
                persist_dir="./chroma_db"):
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.persist_dir = persist_dir
        self.llm = None
        self.vectorstore = None
        self.qa_chain = None
    
    def initialize(self, chunks):
        """Initialize the entire model in one step."""
        # Create embeddings
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        
        # Create or load vector store
        if os.path.exists(self.persist_dir) and os.listdir(self.persist_dir):
            vectorstore = Chroma(persist_directory=self.persist_dir, embedding_function=embeddings)
            
            # Add new chunks if provided
            if chunks:
                vectorstore.add_documents(chunks)
                vectorstore.persist()
        else:
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=self.persist_dir
            )
            vectorstore.persist()
        
        self.vectorstore = vectorstore
        
        # Initialize LLM
        self.llm = Ollama(
            model=self.model_name,
            temperature=0.1,
            num_predict=2048,
            keep_alive="5m",
            base_url="http://10.145.138.115:11434" 
        )
        
        # Configure retriever
        retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 5,
                "fetch_k": 15,
                "lambda_mult": 0.7
            }
        )
        
        # Create custom prompt template
        prompt_template = """
        You are a friendly medical assistant focusing on drug interactions and safety concerns.
        
        Context information from medical literature:
        {context}
        
        Based on the context information and your knowledge, answer the following query:
        {question}
        
        Focus on identifying potential negative interactions, side effects, or concerns.
        Don't provide treatment suggestions or next steps.
        Be conversational and explain in simple terms, but be comprehensive.
        Include a disclaimer that you are NOT a doctor and this is for informational purposes only.
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question"]
        )
        
        # Create the QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        return True
    
    def format_medical_query(self, current_meds, allergies, conditions, new_meds, patient_info, additional_info=""):
        """Format structured medical data into a query for the LLM."""
        query = """
        You are a friendly medical assistant. Please analyze the following patient information and identify any potential 
        negative interactions or concerns in a conversational, easy-to-understand way.
        
        Patient Information:
        """
        
        if patient_info.get("age") or patient_info.get("gender") or patient_info.get("bp"):
            query += "\nBasic Information:\n"
            if patient_info.get("age"):
                query += f"- Age: {patient_info['age']}\n"
            if patient_info.get("gender"):
                query += f"- Gender: {patient_info['gender']}\n"
            if patient_info.get("bp"):
                query += f"- Blood Pressure: {patient_info['bp']}\n"
        
        # Format current medications
        if current_meds:
            query += "\nCurrent Medications:\n"
            for med in current_meds:
                if med['name'] and med['dosage']:
                    query += f"- {med['name']} ({med['dosage']})\n"
        
        # Format allergies
        if allergies:
            query += "\nAllergies:\n"
            for allergy in allergies:
                if allergy['name']:
                    reaction = f" (Reaction: {allergy['reaction']})" if allergy['reaction'] else ""
                    query += f"- {allergy['name']}{reaction}\n"
        
        # Format conditions
        if conditions:
            query += "\nMedical Conditions:\n"
            for condition in conditions:
                if condition:
                    query += f"- {condition}\n"
        
        # Format new medications
        if new_meds:
            query += "\nNewly Prescribed Medications:\n"
            for med in new_meds:
                if med['name'] and med['dosage']:
                    query += f"- {med['name']} ({med['dosage']})\n"
        
        # Add additional information if provided
        if additional_info:
            query += f"\nAdditional Information:\n{additional_info}\n"
        
        # Add specific instructions for the analysis
        query += """
        Please analyze for potential interactions and concerns, considering:
        1. Drug-drug interactions between current and new medications
        2. Allergy concerns with any medications
        3. Drug-condition interactions
        4. Age, gender, or blood pressure related concerns
        
        Be conversational and educational in your response. Organize your answer in clear sections but don't use 
        numbering or bullet points unless necessary. Explain any medical terms you use.
        
        End with a disclaimer that you are NOT a doctor and this analysis is for informational purposes only.
        """
        
        return query
    
    def analyze_interactions(self, current_meds, allergies, conditions, new_meds, patient_info, additional_info=""):
        """Analyze potential drug interactions based on patient information."""
        if not self.qa_chain:
            return {"error": "System not initialized. Please initialize the system first."}
        
        try:
            # Format query
            query = self.format_medical_query(
                current_meds, allergies, conditions, new_meds, patient_info, additional_info
            )
            
            # Get response
            result = self.qa_chain({"query": query})
            
            # Format response with sources
            response = {
                "analysis": result["result"],
                "sources": [
                    {
                        "source": doc.metadata.get("source", "Unknown"),
                        "page": doc.metadata.get("page", "Unknown"),
                        "content": doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                    }
                    for doc in result.get("source_documents", [])
                ]
            }
            
            return response
            
        except Exception as e:
            return {"error": f"Error analyzing interactions: {str(e)}"}