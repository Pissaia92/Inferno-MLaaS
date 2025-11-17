import io
import joblib
import boto3
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Generator


class SentimentRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    text: str
    sentiment: str


# Global variable to store the model
model = None


def load_model() -> None:
    """Load the trained model from S3."""
    global model
    bucket_name = os.getenv("MODEL_BUCKET_NAME")
    if not bucket_name:
        raise RuntimeError("MODEL_BUCKET_NAME environment variable not set")
    
    s3_client = boto3.client('s3')
    
    try:
        # Download model from S3 to temporary location
        response = s3_client.get_object(Bucket=bucket_name, Key='model.pkl')
        model_data = response['Body'].read()
        
        # Load model directly from bytes
        model = joblib.load(io.BytesIO(model_data))
    except Exception as e:
        raise RuntimeError(f"Failed to load model from S3: {str(e)}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator:
    """Lifespan context manager to load model on startup."""
    load_model()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/predict", response_model=SentimentResponse)
async def predict_sentiment(request: SentimentRequest):
    """Predict sentiment for the given text."""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Make prediction
    prediction = model.predict([request.text])[0]
    sentiment = "positive" if prediction == 1 else "negative"
    
    return SentimentResponse(text=request.text, sentiment=sentiment)