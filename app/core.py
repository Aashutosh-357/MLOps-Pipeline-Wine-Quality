import joblib
import os
import logging

# Configure logging (Best Practice: Don't use print() in production)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model_artifacts(artifact_dir: str = "artifacts"):
    """
    Loads model and scaler safely.
    Returns: dict or None
    """
    model_path = os.path.join(artifact_dir, "Tuned_RandomForest.pkl")
    scaler_path = os.path.join(artifact_dir, "StandardScaler.pkl")

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        logger.error(f"Artifacts missing in {artifact_dir}")
        return None

    try:
        logger.info("Loading ML artifacts into memory...")
        return {
            "model": joblib.load(model_path),
            "scaler": joblib.load(scaler_path)
        }
    except Exception as e:
        logger.critical(f"Failed to load models: {e}")
        return None