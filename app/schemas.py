from pydantic import BaseModel, Field

class WineInput(BaseModel):
    # Field descriptions appear in Swagger UI
    volatile_acidity: float = Field(..., gt=0, description="Volatile Acidity (0.1 - 2.0)")
    chlorides: float = Field(..., gt=0, description="Chlorides level")
    density: float = Field(..., gt=0, description="Density (approx 0.99 - 1.0)")
    pH: float = Field(..., gt=0, lt=14, description="pH Level (2.0 - 4.0)")
    alcohol: float = Field(..., gt=0, description="Alcohol percentage")

    class Config:
        json_schema_extra = {
            "example": {
                "volatile_acidity": 0.7,
                "chlorides": 0.045,
                "density": 0.99,
                "pH": 3.2,
                "alcohol": 10.5
            }
        }

class PredictionOut(BaseModel):
    quality_label: str
    latency_ms: float = Field(..., description="Inference time in milliseconds")