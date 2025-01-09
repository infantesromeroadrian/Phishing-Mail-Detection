from transformers import BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

class ModelTrainer:
    def __init__(self, tokenized_datasets, model_name="bert-base-uncased", num_labels=2):
        """
        Inicializa el entrenador del modelo.
        :param tokenized_datasets: DatasetDict tokenizado
        :param model_name: Nombre del modelo preentrenado
        :param num_labels: Número de etiquetas para clasificación
        """
        self.tokenized_datasets = tokenized_datasets
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.trainer = None

    def compute_metrics(self, eval_pred):
        """Calcula métricas de evaluación."""
        logits, labels = eval_pred
        predictions = logits.argmax(axis=-1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="binary")
        acc = accuracy_score(labels, predictions)
        return {
            "accuracy": acc,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }

    def train(self, output_dir="./results", num_train_epochs=3, learning_rate=2e-5, batch_size=16):
        """Configura y entrena el modelo."""
        training_args = TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size * 2,
            num_train_epochs=num_train_epochs,
            weight_decay=0.01,
            logging_dir="./logs",
            load_best_model_at_end=True,
            save_total_limit=2
        )

        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.tokenized_datasets["train"],
            eval_dataset=self.tokenized_datasets["validation"],
            compute_metrics=self.compute_metrics,
        )

        print("Iniciando el entrenamiento...")
        self.trainer.train()
        print("Entrenamiento completado.")

    def evaluate(self):
        """Evalúa el modelo en el conjunto de prueba."""
        if not self.trainer:
            raise ValueError("El modelo no ha sido entrenado aún. Ejecuta `train()` primero.")
        
        print("Evaluando el modelo...")
        results = self.trainer.evaluate(self.tokenized_datasets["test"])
        print("Resultados de evaluación:", results)
        return results

    def save_model(self, output_dir="./trained_model"):
        """Guarda el modelo entrenado."""
        if not self.trainer:
            raise ValueError("El modelo no ha sido entrenado aún. Ejecuta `train()` primero.")
        
        print(f"Guardando el modelo en {output_dir}...")
        self.model.save_pretrained(output_dir)
        print("Modelo guardado con éxito.") 