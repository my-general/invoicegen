import azure.functions as func
import logging
from form_config import client  # Ensure this client is correctly initialized in form_config.py

def main(myblob: func.InputStream):
    logging.info("✅ Blob trigger activated")
    logging.info(f"📄 File: {myblob.name}, Size: {myblob.length} bytes")

    try:
        # Read PDF content from the blob
        pdf_bytes = myblob.read()

        # Begin invoice analysis using Azure Form Recognizer
        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice",
            document=pdf_bytes,
            content_type="application/pdf"
        )
        result = poller.result()

        logging.info("📥 Invoice details extracted:")

        for idx, doc in enumerate(result.documents):
            fields = doc.fields

            vendor_name = fields.get("VendorName").value if fields.get("VendorName") else "N/A"
            invoice_id = fields.get("InvoiceId").value if fields.get("InvoiceId") else "N/A"
            invoice_date = fields.get("InvoiceDate").value if fields.get("InvoiceDate") else "N/A"
            total_amount = fields.get("InvoiceTotal").value if fields.get("InvoiceTotal") else "N/A"

            logging.info(f"🧾 Invoice #{idx + 1}:")
            logging.info(f"   Vendor      : {vendor_name}")
            logging.info(f"   Invoice ID  : {invoice_id}")
            logging.info(f"   Date        : {invoice_date}")
            logging.info(f"   Total       : {total_amount}")

    except Exception as e:
        logging.exception(f"❌ Error during invoice analysis: {e}")
        raise  # This rethrows the error to allow Azure to handle retries
