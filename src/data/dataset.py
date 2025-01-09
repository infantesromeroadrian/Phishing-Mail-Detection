from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict

class DatasetProcessor:
    def __init__(self, dataframe, tokenizer, text_column="Email Text", 
                 label_column="Email Type", max_length=128):
        self.dataframe = dataframe
        self.tokenizer = tokenizer
        self.text_column = text_column
        self.label_column = label_column
        self.max_length = max_length
        self.dataset_dict = None

    def split_dataset(self, test_size=0.2, validation_size=0.1, random_state=42):
        """Divide el dataset en train, validation y test."""
        train, test = train_test_split(self.dataframe, test_size=test_size, 
                                     random_state=random_state)
        train, validation = train_test_split(train, test_size=validation_size, 
                                           random_state=random_state)

        self.dataset_dict = DatasetDict({
            "train": Dataset.from_pandas(train),
            "validation": Dataset.from_pandas(validation),
            "test": Dataset.from_pandas(test),
        })
        print("Dataset dividido en train, validation y test.")

    def tokenize(self):
        """Tokeniza los textos del dataset."""
        if not self.dataset_dict:
            raise ValueError("Primero debes dividir el dataset usando `split_dataset`.")

        def tokenize_function(examples):
            tokens = self.tokenizer(
                examples[self.text_column], 
                padding="max_length",
                truncation=True,
                max_length=self.max_length
            )
            tokens["labels"] = [1 if label == "Phishing Email" else 0 
                              for label in examples[self.label_column]]
            return tokens

        self.dataset_dict = self.dataset_dict.map(tokenize_function, batched=True)
        print("Tokenización completada.")

    def get_datasets(self):
        """Devuelve los datasets procesados."""
        if not self.dataset_dict:
            raise ValueError("Primero debes dividir y tokenizar el dataset.")
        return self.dataset_dict 