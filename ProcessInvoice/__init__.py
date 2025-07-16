import azure.functions as func
import logging
from form_config import client
import json
import traceback

def main(myblob: func.InputStream):
    logging.info("✅ Blob trigger activated")
    logging.info(f"📄 Blob Name: {myblob.name}")
    logging.info(f"📦 Blob Size: {myblob.length} bytes")
    logging.info(f"🕓 Blob Timestamp: {myblob.uri}")

    try:
        # Step 1: Read the blob content
        pdf_bytes = myblob.read()
        if not pdf_bytes:
            raise ValueError("🚫 Blob is empty or unreadable")

        logging.info("📥 Successfully read PDF from blob")

        # Step 2: Begin invoice analysis
        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice",
            document=pdf_bytes,
            content_type="application/pdf"
        )

        logging.info("🔍 Form Recognizer poller started... waiting for result")

        result = poller.result()

        if not result or not result.documents:
            raise ValueError("❗No invoice documents returned from Form Recognizer")

        logging.info("✅ Form Recognizer analysis completed")

        # Step 3: Log each extracted invoice
        for idx, doc in enumerate(result.documents):
            fields = doc.fields if hasattr(doc, "fields") else {}
            invoice_data = {
                "VendorName": fields.get("VendorName").value if fields.get("VendorName") else "N/A",
                "InvoiceId": fields.get("InvoiceId").value if fields.get("InvoiceId") else "N/A",
                "InvoiceDate": fields.get("InvoiceDate").value if fields.get("InvoiceDate") else "N/A",
                "InvoiceTotal": fields.get("InvoiceTotal").value if fields.get("InvoiceTotal") else "N/A"
            }

            logging.info(f"🧾 Invoice #{idx + 1}:")
            for key, val in invoice_data.items():
                logging.info(f"   {key}: {val}")

    except Exception as e:
        logging.error("❌ Exception occurred during invoice processing.")
        logging.error(f"🛑 Error Type: {type(e).__name__}")
        logging.error(f"📝 Error Message: {e}")
        logging.error(f"🔍 Full Traceback:\n{traceback.format_exc()}")
        raise
