import time
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles # Import StaticFiles
from fastapi.responses import FileResponse   # Import FileResponse
from app.schemas import WineInput, PredictionOut
from app.core import load_model_artifacts, logger

ml_models = {}
QUALITY_MAP = {0: 'Bad (Score <= 6)', 1: 'Good (Score >= 7)'}

@asynccontextmanager
async def lifespan(app: FastAPI):
    resources = load_model_artifacts()
    if resources:
        ml_models["model"] = resources["model"]
        ml_models["scaler"] = resources["scaler"]
    yield
    ml_models.clear()

app = FastAPI(title="Wine Quality API", lifespan=lifespan)

# --- NEW: SERVE STATIC FILES ---
# This line maps the /static URL to your physical folder
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def get_index():
    """Serves the frontend homepage."""
    return FileResponse("app/static/index.html")

# --- KEEP YOUR API ROUTES ---

@app.post("/predict", response_model=PredictionOut)
def predict(data: WineInput):
    start_time = time.time()
    model, scaler = ml_models.get("model"), ml_models.get("scaler")

    if not model:
        raise HTTPException(status_code=503, detail="Model missing")

    features = [data.volatile_acidity, data.chlorides, data.density, data.pH, data.alcohol]
    features_arr = np.array(features).reshape(1, -1)
    scaled = scaler.transform(features_arr)
    
    prediction = model.predict(scaled)
    label = QUALITY_MAP.get(int(prediction[0]), "Unknown")
    
    duration = (time.time() - start_time) * 1000
    return {"quality_label": label, "latency_ms": round(duration, 2)}