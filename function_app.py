import azure.functions as func
import logging
from form_config import client  # Make sure this correctly initializes Azure Form Recognizer client

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="invoices/pending/{name}",
                  connection="AzureWebJobsStorage")  # <-- Fixed here
def ProcessInvoice(myblob: func.InputStream):
    logging.info("✅ Blob trigger activated")
    logging.info(f"📄 File: {myblob.name}, Size: {myblob.length} bytes")

    try:
        # Call Azure Form Recognizer on PDF blob
        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice",
            document=myblob  # Direct stream from blob
        )

        result = poller.result()

        logging.info("📥 Invoice details extracted:")

        for idx, doc in enumerate(result.documents):
            fields = doc.fields
            vendor_name = fields.get("VendorName").value if fields.get("VendorName") else None
            invoice_id = fields.get("InvoiceId").value if fields.get("InvoiceId") else None
            invoice_date = fields.get("InvoiceDate").value if fields.get("InvoiceDate") else None
            total_amount = fields.get("InvoiceTotal").value if fields.get("InvoiceTotal") else None

            logging.info(f"🧾 Invoice #{idx+1}:")
            logging.info(f"   Vendor: {vendor_name}")
            logging.info(f"   Invoice ID: {invoice_id}")
            logging.info(f"   Date: {invoice_date}")
            logging.info(f"   Total: {total_amount}")

    except Exception as e:
        logging.error(f"❌ Error during invoice analysis: {e}")
