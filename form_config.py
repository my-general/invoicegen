from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os

# Set your Form Recognizer endpoint and key
FORM_RECOGNIZER_ENDPOINT = os.getenv("FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("FORM_RECOGNIZER_KEY")

# Check if keys are loaded correctly
if not FORM_RECOGNIZER_ENDPOINT or not FORM_RECOGNIZER_KEY:
    raise ValueError("❌ FORM_RECOGNIZER_ENDPOINT and FORM_RECOGNIZER_KEY must be set in environment variables.")

client = DocumentAnalysisClient(
    endpoint=FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(FORM_RECOGNIZER_KEY)
)
