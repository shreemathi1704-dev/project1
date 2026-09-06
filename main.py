import os
import io

import numpy as np
import tensorflow as tf

from PIL import Image

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, Prediction
from disease_info import get_disease_info


# ==================================================
# CREATE FASTAPI APP
# ==================================================

app = FastAPI(
    title="AgriGuard AI",
    description="AI Based Crop Disease Detection System",
    version="1.0.0"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==================================================
# PROJECT PATH
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "agriguard_model.keras"
)


CLASS_PATH = os.path.join(
    BASE_DIR,
    "model",
    "class_names.txt"
)


# ==================================================
# CHECK MODEL
# ==================================================

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )


if not os.path.exists(CLASS_PATH):

    raise FileNotFoundError(
        f"Class names not found: {CLASS_PATH}"
    )


# ==================================================
# LOAD MODEL
# ==================================================

model = tf.keras.models.load_model(
    MODEL_PATH
)


# ==================================================
# LOAD CLASS NAMES
# ==================================================

with open(
    CLASS_PATH,
    "r",
    encoding="utf-8"
) as file:

    class_names = [
        line.strip()
        for line in file
        if line.strip()
    ]


print("Loaded classes:")
print(class_names)


# ==================================================
# HOME API
# ==================================================

@app.get("/")
def home():

    return {
        "success": True,
        "message": "AgriGuard AI Backend is Running",
        "classes": class_names
    }


# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
def health():

    return {
        "status": "online"
    }


# ==================================================
# PREDICT
# ==================================================

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    # ----------------------------------------------
    # CHECK FILE
    # ----------------------------------------------

    if not file.filename:

        return {
            "success": False,
            "message": "No image selected"
        }


    # ----------------------------------------------
    # READ IMAGE
    # ----------------------------------------------

    image_bytes = await file.read()


    # ----------------------------------------------
    # OPEN IMAGE
    # ----------------------------------------------

    try:

        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

    except Exception:

        return {
            "success": False,
            "message": "Invalid image file"
        }


    # ----------------------------------------------
    # RESIZE
    # ----------------------------------------------

    image = image.resize(
        (224, 224)
    )


    # ----------------------------------------------
    # NUMPY
    # ----------------------------------------------

    image_array = np.array(
        image,
        dtype=np.float32
    )


    # Add batch dimension

    image_array = np.expand_dims(
        image_array,
        axis=0
    )


    # ----------------------------------------------
    # PREDICTION
    # ----------------------------------------------

    predictions = model.predict(
        image_array,
        verbose=0
    )


    predicted_index = int(
        np.argmax(predictions[0])
    )


    confidence = float(
        np.max(predictions[0])
    ) * 100


    predicted_class = class_names[
        predicted_index
    ]


    # ----------------------------------------------
    # DISEASE INFORMATION
    # ----------------------------------------------

    info = get_disease_info(
        predicted_class
    )


    # ----------------------------------------------
    # DATABASE
    # ----------------------------------------------

    db = SessionLocal()

    try:

        record = Prediction(

            filename=file.filename,

            prediction=predicted_class,

            confidence=confidence

        )

        db.add(record)

        db.commit()

    finally:

        db.close()


    # ----------------------------------------------
    # RETURN RESULT
    # ----------------------------------------------

    return {

        "success": True,

        "prediction":
            predicted_class,

        "confidence":
            round(confidence, 2),

        "disease":
            info["disease"],

        "severity":
            info["severity"],

        "cause":
            info["cause"],

        "solution":
            info["solution"]

    }


# ==================================================
# HISTORY
# ==================================================

@app.get("/history")
def history():

    db = SessionLocal()

    try:

        records = (
            db.query(Prediction)
            .order_by(Prediction.id.desc())
            .limit(20)
            .all()
        )


        result = []


        for record in records:

            result.append({

                "id":
                    record.id,

                "filename":
                    record.filename,

                "prediction":
                    record.prediction,

                "confidence":
                    round(
                        record.confidence,
                        2
                    )

            })


        return result

    finally:

        db.close()