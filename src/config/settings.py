import os

from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

NUM_MESSAGES: int = int(os.getenv("NUM_MESSAGES", "1"))
WAIT_TIME_SECONDS: int = int(os.getenv("WAIT_TIME_SECONDS", "10"))
SQS_PREDICT_QUEUE_NAME: str = os.getenv("SQS_PREDICT_QUEUE_NAME", "mairror-predict")
MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE: str = os.getenv("MONGO_DATABASE", "mairror")
MONGO_COLLECTION_PREDICT: str = os.getenv("MONGO_COLLECTION_PREDICT", "predict")
MONGO_COLLECTION_FACES: str = os.getenv("MONGO_COLLECTION_FACES", "faces")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
