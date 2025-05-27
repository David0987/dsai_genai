#!/bin/bash

# Create a new conda environment
conda create -n genai python=3.11 -y

# Activate the environment
source activate genai

# Install required packages
pip install google-generativeai>=0.3.0
pip install langchain>=0.1.0
pip install langchain-google-genai>=0.0.5
pip install faiss-cpu>=1.7.4
pip install PyPDF2>=3.0.0
pip install python-docx>=0.8.11
pip install jupyter
pip install ipykernel

# Add the environment to Jupyter
python -m ipykernel install --user --name genai --display-name "Python (genai)"

echo "Environment setup complete! You can now start Jupyter with: jupyter notebook" 