import os
from transformers import BertTokenizer
from utils.config import Config
from data.preprocessor import DataPreprocessor
from data.dataset import DatasetProcessor
from models.trainer import ModelTrainer
from models.predictor import PhishingPredictor
from utils.metrics import print_metrics

def main():
    # Crear directorios necesarios
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    os.makedirs(Config.MODELS_DIR, exist_ok=True)

    # 1. Preprocesamiento de datos
    print("\n=== Iniciando Preprocesamiento ===")
    preprocessor = DataPreprocessor(
        file_path=Config.DATA_DIR / Config.RAW_DATA_FILE,
        columns_to_keep=Config.COLUMNS_TO_KEEP
    )
    preprocessor.preprocess()
    cleaned_dataset = preprocessor.get_dataset()

    # Guardar dataset preprocesado
    cleaned_dataset.to_csv(Config.DATA_DIR / Config.CLEANED_DATA_FILE, index=False)

    # 2. Preparación del dataset
    print("\n=== Preparando Dataset ===")
    tokenizer = BertTokenizer.from_pretrained(Config.MODEL_NAME)
    processor = DatasetProcessor(
        dataframe=cleaned_dataset,
        tokenizer=tokenizer,
        max_length=Config.MAX_LENGTH
    )
    processor.split_dataset()
    processor.tokenize()
    tokenized_datasets = processor.get_datasets()

    # 3. Entrenamiento del modelo
    print("\n=== Iniciando Entrenamiento ===")
    trainer = ModelTrainer(
        tokenized_datasets=tokenized_datasets,
        model_name=Config.MODEL_NAME,
        num_labels=Config.NUM_LABELS
    )
    
    trainer.train(
        output_dir=Config.MODELS_DIR / "results",
        num_train_epochs=Config.NUM_EPOCHS,
        learning_rate=Config.LEARNING_RATE,
        batch_size=Config.TRAIN_BATCH_SIZE
    )

    # 4. Evaluación del modelo
    print("\n=== Evaluando Modelo ===")
    evaluation_results = trainer.evaluate()
    print_metrics(evaluation_results)

    # 5. Guardar modelo
    model_save_path = Config.MODELS_DIR / "trained_model"
    trainer.save_model(output_dir=model_save_path)

    # 6. Prueba de predicción
    print("\n=== Probando Predicciones ===")
    predictor = PhishingPredictor(
        model_path=model_save_path,
        max_length=Config.MAX_LENGTH
    )

    test_emails = [
        """Dear valued customer, Your account has been suspended. 
        Click here immediately to verify your identity: http://suspicious-link.com""",
        
        """Hi team, Here's the agenda for tomorrow's meeting:
        1. Project updates
        2. Budget review
        3. Q&A session
        Best regards, John"""
    ]

    for i, email in enumerate(test_emails, 1):
        result = predictor.predict(email)
        print(f"\nEmail #{i}:")
        print(f"Texto: {email[:100]}...")
        print(f"Predicción: {result['prediction']}")
        print(f"Confianza: {result['confidence']*100:.2f}%")
        print(f"Probabilidad de phishing: {result['probability_phishing']*100:.2f}%")

if __name__ == "__main__":
    main() 