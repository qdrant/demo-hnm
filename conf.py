import os


MODEL_NAME = "resnet18"
VECTOR_SIZE = 512
BATCH_SIZE = 100

QDRANT_HOST = os.environ.get("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.environ.get("QDRANT_PORT", "6333"))
COLLECTION_NAME = "articles"
DISTANCE_FUNCTION = "Cosine"

NUM_RESULTS = 20
NUM_RESULTS_PER_ROW = 4

DATA_DIR = os.environ.get("DATA_DIR", "./data")
IMAGES_DIR = f"{DATA_DIR}/images"
EXAMPLES_DIR = f"{DATA_DIR}/examples"
