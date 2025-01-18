from pathlib import Path

class Config:
    # Rutas del proyecto
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    
    # Rutas alternativas para el modelo
    MODEL_PATHS = [
        PROJECT_ROOT / "models" / "trained_model",          # Ruta principal
        Path("/mount/src/phishing-mail-detection/models/trained_model"),  # Streamlit Cloud
        Path("models/trained_model"),                       # Ruta relativa
    ]
    
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
    
    # Columnas del dataset
    TEXT_COLUMN = "Email Text"
    LABEL_COLUMN = "Email Type"
    COLUMNS_TO_KEEP = [TEXT_COLUMN, LABEL_COLUMN] 
    
    # Configuración de la interfaz
    INTERFACE = {
        'THEME': 'light',
        'PRIMARY_COLOR': '#FF4B4B',
        'SECONDARY_COLOR': '#0083B8',
        'BACKGROUND_COLOR': '#FFFFFF'
    }
    
    # Umbrales de confianza
    CONFIDENCE_THRESHOLDS = {
        'HIGH': 0.9,
        'MEDIUM': 0.7,
        'LOW': 0.5
    }
    
    # Palabras clave para análisis
    SUSPICIOUS_KEYWORDS = {
        'URGENCY': ['urgent', 'immediately', 'now', 'quick'],
        'SENSITIVE': ['password', 'credit card', 'bank', 'account'],
        'OFFERS': ['won', 'prize', 'lottery', 'free']
    } 