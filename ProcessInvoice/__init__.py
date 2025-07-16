import azure.functions as func
import logging
from form_config import client
from azure.core.exceptions import AzureError

def main(myblob: func.InputStream):
    logging.info("🔔 ProcessInvoice triggered")
    
    try:
        logging.info(f"📄 Blob path: {myblob.name} | Size: {myblob.length} bytes")
        pdf_bytes = myblob.read()

        logging.info("📦 Read blob into memory, calling Form Recognizer")

        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice",
            document=pdf_bytes,
            content_type="application/pdf"
        )
        result = poller.result()

        logging.info("📥 Form Recognizer response received")

        for idx, doc in enumerate(result.documents):
            fields = doc.fields
            vendor_name = fields.get("VendorName").value if fields.get("VendorName") else "N/A"
            invoice_id = fields.get("InvoiceId").value if fields.get("InvoiceId") else "N/A"
            invoice_date = fields.get("InvoiceDate").value if fields.get("InvoiceDate") else "N/A"
            total_amount = fields.get("InvoiceTotal").value if fields.get("InvoiceTotal") else "N/A"

            logging.info(f"🧾 Invoice #{idx + 1}")
            logging.info(f"   Vendor     : {vendor_name}")
            logging.info(f"   Invoice ID : {invoice_id}")
            logging.info(f"   Date       : {invoice_date}")
            logging.info(f"   Total      : {total_amount}")

    except AzureError as azerr:
        logging.error("🛑 Azure Form Recognizer client error:")
        logging.exception(azerr)
        raise

    except Exception as e:
        logging.error("❌ General exception during invoice processing")
        logging.exception(e)
        raise
