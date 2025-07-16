from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os

endpoint = os.environ.get("FORM_RECOGNIZER_ENDPOINT")
key = os.environ.get("FORM_RECOGNIZER_KEY")

if not endpoint or not key:
    raise ValueError("❌ FORM_RECOGNIZER_ENDPOINT and FORM_RECOGNIZER_KEY must be set in environment variables.")

client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
