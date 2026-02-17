from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.logging_config import get_logger
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.auth.router import router as auth_router
from fastapi.responses import HTMLResponse

# Setup logging
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting...")
    yield
    print("App shutting down...")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# def main():
#     logger.warning("Hello From Invitation Project")
#     return "Hello From Invitation Project"


@app.get("/", response_class=HTMLResponse)
def scanner_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>QR Scanner</title>
        <script src="https://unpkg.com/html5-qrcode"></script>
    </head>
    <body>
        <h2>Scan Invitation QR</h2>
        <div id="reader" style="width:300px;"></div>

        <script>
            function onScanSuccess(decodedText) {
                fetch("/checkin", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ code: decodedText })
                })
                .then(response => response.json())
                .then(data => alert(data.message));
            }

            let html5QrcodeScanner = new Html5QrcodeScanner(
                "reader", { fps: 10, qrbox: 250 });
            html5QrcodeScanner.render(onScanSuccess);
        </script>
    </body>
    </html>
    """


@app.post("/checkin")
def checkin(data: dict):
    code = data.get("code")
    print("Scanned:", code)

    # # Example validation
    # if code == "INV-123":
    #     return {"message": "✅ Welcome!"}
    return {"message": "❌ Invalid invitation"}


app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)
