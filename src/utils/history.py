import json
from datetime import datetime
from pathlib import Path

class AnalysisHistory:
    def __init__(self, history_file="analysis_history.json"):
        self.history_file = Path("data") / history_file
        self.history_file.parent.mkdir(exist_ok=True)
        self.load_history()

    def load_history(self):
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = []

    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add_analysis(self, email_text, result):
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'email_preview': email_text[:100] + "...",
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'is_phishing': result['is_phishing']
        }
        self.history.append(analysis)
        self.save_history()

    def get_recent_analyses(self, limit=5):
        return self.history[-limit:] 