import pandas as pd

class DataPreprocessor:
    def __init__(self, file_path, columns_to_keep=None):
        """
        Inicializa el preprocesador con la ruta al archivo y las columnas a conservar.
        :param file_path: Ruta al archivo CSV.
        :param columns_to_keep: Lista de columnas importantes a conservar.
        """
        self.file_path = file_path
        self.columns_to_keep = columns_to_keep
        self.df = None

    def load_dataset(self):
        """Carga el dataset desde el archivo CSV."""
        self.df = pd.read_csv(self.file_path)
        print("Dataset cargado con éxito.")

    def keep_columns(self):
        """Conserva solo las columnas especificadas."""
        if self.columns_to_keep:
            self.df = self.df[self.columns_to_keep]
            print(f"Columnas conservadas: {list(self.df.columns)}")
        else:
            print("No se especificaron columnas para conservar.")

    def handle_missing_values(self):
        """Maneja los valores nulos."""
        self.df["Email Text"] = self.df["Email Text"].fillna("")
        print(f"Valores nulos en 'Email Text': {self.df['Email Text'].isnull().sum()}")

    def convert_to_strings(self):
        """Convierte todos los valores de Email Text a strings."""
        self.df["Email Text"] = self.df["Email Text"].astype(str)
        print("Todos los valores de 'Email Text' convertidos a cadenas.")

    def remove_duplicates(self):
        """Elimina registros duplicados."""
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        final_count = len(self.df)
        print(f"Registros duplicados eliminados: {initial_count - final_count}")

    def filter_short_texts(self, min_length=5):
        """Filtra textos demasiado cortos."""
        initial_count = len(self.df)
        self.df = self.df[self.df["Email Text"].apply(len) > min_length]
        final_count = len(self.df)
        print(f"Registros eliminados por textos cortos: {initial_count - final_count}")

    def validate_labels(self):
        """Verifica y muestra la distribución de las etiquetas."""
        label_counts = self.df["Email Type"].value_counts()
        print("Distribución de etiquetas:")
        print(label_counts)

    def preprocess(self):
        """Ejecuta todos los pasos de preprocesamiento."""
        self.load_dataset()
        self.keep_columns()
        self.handle_missing_values()
        self.convert_to_strings()
        self.remove_duplicates()
        self.filter_short_texts()
        self.validate_labels()
        print("Preprocesamiento completado.")

    def get_dataset(self):
        """Devuelve el dataset preprocesado."""
        return self.df 