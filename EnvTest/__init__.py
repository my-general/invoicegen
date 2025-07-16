import azure.functions as func
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(f"""
        ✅ AzureWebJobsStorage: {os.environ.get("AzureWebJobsStorage")}
        ✅ FORM_RECOGNIZER_ENDPOINT: {os.environ.get("FORM_RECOGNIZER_ENDPOINT")}
        ✅ FUNCTIONS_WORKER_RUNTIME: {os.environ.get("FUNCTIONS_WORKER_RUNTIME")}
    """, mimetype="text/plain")
