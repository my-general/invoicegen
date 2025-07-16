import logging
import os
import azure.functions as func
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["FORM_RECOGNIZER_ENDPOINT"]
key = os.environ["FORM_RECOGNIZER_KEY"]

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

def main(blob: func.InputStream):
    logging.info(f"Blob trigger function processed blob \n"
                 f"Name: {blob.name} \n"
                 f"Blob Size: {blob.length} bytes")

    try:
        poller = document_analysis_client.begin_analyze_document(
            model_id="prebuilt-invoice",
            document=blob.read()
        )
        result = poller.result()

        for doc in result.documents:
            vendor = doc.fields.get("VendorName")
            total = doc.fields.get("InvoiceTotal")
            invoice_id = doc.fields.get("InvoiceId")

            logging.info(f"✅ Vendor: {vendor.value if vendor else 'N/A'}")
            logging.info(f"💰 Total Amount: {total.value if total else 'N/A'}")
            logging.info(f"🧾 Invoice ID: {invoice_id.value if invoice_id else 'N/A'}")

    except Exception as e:
        logging.error(f"❌ Failed to process invoice: {e}")
