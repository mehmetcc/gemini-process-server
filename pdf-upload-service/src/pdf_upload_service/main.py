from fastapi import FastAPI
from pdf_upload_service.routes.post_pdf import router as api_router

app = FastAPI(
    title="PDF Upload Service",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

# For development purposes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("pdf_upload_service.main:app",
                host="0.0.0.0", port=8000, reload=True)
