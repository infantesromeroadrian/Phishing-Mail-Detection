import torch
from transformers import BertTokenizer, BertForSequenceClassification

class PhishingPredictor:
    def __init__(self, model_path, tokenizer_path=None, max_length=128):
        """
        Inicializa el predictor con el modelo y tokenizador guardados.
        :param model_path: Ruta al modelo guardado
        :param tokenizer_path: Ruta al tokenizador (si es diferente del modelo)
        :param max_length: Longitud máxima de la secuencia
        """
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path or model_path)
        self.max_length = max_length
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

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