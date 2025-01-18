import torch
from transformers import BertTokenizer, BertForSequenceClassification

class PhishingPredictor:
    def __init__(self, model_id="infantesromeroadrian/phishing-detection-bert", max_length=128):
        """
        Inicializa el predictor cargando el modelo desde Hugging Face Hub.
        :param model_id: ID del modelo en Hugging Face Hub
        :param max_length: Longitud máxima de la secuencia
        """
        try:
            self.model = BertForSequenceClassification.from_pretrained(model_id)
            self.tokenizer = BertTokenizer.from_pretrained(model_id)
            self.max_length = max_length
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            print(f"Error al cargar el modelo: {str(e)}")
            raise

    def preprocess_text(self, text):
        """Preprocesa el texto para la predicción."""
        inputs = self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        )
        return {k: v.to(self.device) for k, v in inputs.items()}

    def predict(self, text):
        """Realiza la predicción para un texto dado."""
        inputs = self.preprocess_text(text)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            prediction = torch.argmax(probabilities, dim=-1).item()
            confidence = probabilities[0][prediction].item()

        return {
            "is_phishing": bool(prediction),
            "confidence": confidence,
            "prediction": "Phishing Email" if prediction else "Safe Email",
            "probability_phishing": probabilities[0][1].item(),
            "probability_safe": probabilities[0][0].item()
        }

    def predict_batch(self, texts):
        """Realiza predicciones para una lista de textos."""
        return [self.predict(text) for text in texts] 