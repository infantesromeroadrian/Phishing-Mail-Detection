# Phishing Email Detection with BERT

## Description
A deep learning-based solution for detecting phishing emails using BERT (Bidirectional Encoder Representations from Transformers). This project implements a binary classification model that can identify potentially malicious phishing attempts in email content with high accuracy.

## Key Features
- 🤖 BERT-based model for advanced text understanding
- 📊 Real-time email content analysis
- 🎯 High accuracy in phishing detection
- 🖥️ User-friendly Streamlit interface
- 📈 Probability scores and confidence metrics
- ⚡ Fast inference with GPU support
- 🔍 Detailed analysis of suspicious features
- 📋 Example emails for testing
- 📱 Responsive web interface

## Live Demo
Try the live demo at: [Phishing Email Detector](https://phishing-mail-detection.streamlit.app/)

## Project Structure 

PhishingMailDetection/
├── src/
│ ├── data/ # Data processing modules
│ │ ├── init.py
│ │ ├── preprocessor.py
│ │ └── dataset.py
│ ├── models/ # Model architecture and prediction
│ │ ├── init.py
│ │ ├── trainer.py
│ │ └── predictor.py
│ ├── utils/ # Utility functions and configurations
│ │ ├── init.py
│ │ ├── config.py
│ │ ├── history.py
│ │ └── metrics.py
│ ├── app.py # Streamlit web interface
│ └── main.py # Training pipeline
├── models/ # Trained models
│ ├── trained_model/ # Production model
│ └── results/ # Training results
├── data/ # Dataset directory
├── notebooks/ # Jupyter notebooks for development
└── requirements.txt # Project dependencies


## Technical Details

### Model Architecture
- Base Model: BERT (bert-base-uncased)
- Fine-tuned for binary classification
- Input: Email text (max length: 128 tokens)
- Output: Phishing probability and classification

### Performance Metrics
- Accuracy: 98.43%
- Precision: 98.45%
- Recall: 97.32%
- F1-Score: 97.88%

## Installation

1. Clone the repository:

bash
git clone https://github.com/infantesromeroadrian/Phishing-Mail-Detection.git
cd PhishingMailDetection


2. Create and activate a virtual environment:

bash
Windows
python -m venv phisingmail-detection-cuda
.\phisingmail-detection-cuda\Scripts\activate
Linux/Mac
python -m venv phisingmail-detection-cuda
source phisingmail-detection-cuda/bin/activate



3. Install dependencies:

bash
pip install -r requirements.txt



## Usage

### Running the Web Interface
To start the Streamlit application:


bash
streamlit run src/app.py



### Using the Model in Python

python
from models.predictor import PhishingPredictor
Initialize predictor
predictor = PhishingPredictor()
Make predictions
email_text = "Your text here..."
result = predictor.predict(email_text)
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']100:.2f}%")



## Features
- Real-time email analysis
- Confidence score visualization
- Suspicious feature detection
- Analysis history tracking
- Example phishing emails
- Detailed probability breakdown
- Mobile-friendly interface

## Model Training
To train a new model:


bash
python src/main.py


## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- HuggingFace Transformers library
- Streamlit for the web interface
- BERT model from Google Research
- The open-source ML community

## Author
Adrian Infantes Romero

## Contact
- GitHub: [@infantesromeroadrian](https://github.com/infantesromeroadrian)
- LinkedIn: [Adrian Infantes Romero](https://www.linkedin.com/in/adrian-infantes-romero/)

## Future Improvements
- [ ] Multi-language support
- [ ] API endpoint deployment
- [ ] Enhanced feature analysis
- [ ] Model performance optimization
- [ ] Batch processing capability