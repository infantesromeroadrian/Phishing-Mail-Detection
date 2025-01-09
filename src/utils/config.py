from pathlib import Path

class Config:
    # Rutas del proyecto
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    MODELS_DIR = PROJECT_ROOT
    
    # Configuración del modelo
    MODEL_NAME = "bert-base-uncased"
    MAX_LENGTH = 128
    NUM_LABELS = 2
    
    # Parámetros de entrenamiento
    TRAIN_BATCH_SIZE = 16
    EVAL_BATCH_SIZE = 32
    LEARNING_RATE = 2e-5
    NUM_EPOCHS = 3
    
    # Nombres de archivos
    RAW_DATA_FILE = "Phishing_Email.csv"
    CLEANED_DATA_FILE = "cleaned_phishing_email.csv"
    TOKENIZED_DATA_DIR = "tokenized_phishing_email"
    MODEL_PATH = "trained_model"
    
    # Columnas del dataset
    TEXT_COLUMN = "Email Text"
    LABEL_COLUMN = "Email Type"
    COLUMNS_TO_KEEP = [TEXT_COLUMN, LABEL_COLUMN] 