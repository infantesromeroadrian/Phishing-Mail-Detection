from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import numpy as np

def calculate_metrics(y_true, y_pred):
    """
    Calcula métricas detalladas de rendimiento del modelo.
    """
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')
    conf_matrix = confusion_matrix(y_true, y_pred)
    
    tn, fp, fn, tp = conf_matrix.ravel()
    specificity = tn / (tn + fp)
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "specificity": specificity,
        "confusion_matrix": conf_matrix,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "true_positives": tp
    }

def print_metrics(metrics):
    """
    Imprime las métricas de forma legible.
    """
    print("\n=== Métricas de Rendimiento ===")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-Score: {metrics['f1_score']:.4f}")
    print(f"Specificity: {metrics['specificity']:.4f}")
    
    print("\n=== Matriz de Confusión ===")
    print("TN:", metrics['true_negatives'])
    print("FP:", metrics['false_positives'])
    print("FN:", metrics['false_negatives'])
    print("TP:", metrics['true_positives']) 