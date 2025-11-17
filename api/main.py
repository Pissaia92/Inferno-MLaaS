import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from pathlib import Path

# --- Pydantic Models ---
class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: str

# --- Model Loading Logic (WITH ENHANCED DEBUGGING) ---
ROOT_DIR = Path(__file__).parent.parent
MODEL_PATH = ROOT_DIR / "model.pkl"
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    print("\n--- STARTING LIFESPAN ---")
    print(f"Looking for model at: {MODEL_PATH}")
    
    try:
        # Try to load the model
        model = joblib.load(MODEL_PATH)
        print(">>> SUCCESS: Model loaded successfully.")
    
    except FileNotFoundError:
        print(">>> ERROR (FileNotFoundError):")
        print(f"The script did not find ANY file at this path: {MODEL_PATH}")
        print("Please confirm the 'model.pkl' file is in the project's root folder.")
        model = None
    
    except Exception as e:
        # Catch ALL other errors
        print(f">>> ERROR (Unexpected): {type(e).__name__} <<<")
        print(f"Error Message: {e}")
        print("This usually means the file exists, but:")
        print("1. It is corrupted (try regenerating it)")
        print("2. The script does not have read PERMISSIONS.")
        model = None
    
    print("--- LIFESPAN: 'yield' (App is running) ---")
    yield
    # Cleaning up
    model = None
    print("--- LIFESPAN: Shutdown ---")

app = FastAPI(lifespan=lifespan)

# --- Endpoints ---

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=SentimentResponse)
def predict(request: SentimentRequest):
    if model is None:
        # If the model failed to load, return a clear error
        raise HTTPException(status_code=503, detail="Model is not loaded or failed to load. Check server logs.")
    
    # Run prediction (assuming model returns an array)
    prediction = model.predict([request.text])[0]
    
    return SentimentResponse(text=request.text, sentiment=str(prediction))