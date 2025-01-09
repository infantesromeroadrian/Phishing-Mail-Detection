import streamlit as st
import torch
from models.predictor import PhishingPredictor
from utils.config import Config
import os

def load_model():
    """Carga el modelo entrenado."""
    model_path = Config.MODELS_DIR / Config.MODEL_PATH
    print(f"Buscando modelo en: {model_path}")
    
    if not os.path.exists(model_path):
        st.error(f"⚠️ Modelo no encontrado en {model_path}. Por favor, verifica la ubicación del modelo.")
        return None
    
    return PhishingPredictor(
        model_path=model_path,
        max_length=Config.MAX_LENGTH
    )

def display_analysis_results(col1, result):
    """Muestra los resultados del análisis en la columna especificada."""
    st.markdown("### 📊 Resultado del Análisis")
    
    # Determinar el color según la predicción
    if result["is_phishing"]:
        status_color = "🔴"
        recommendation = "⚠️ Ten cuidado con este email. Muestra señales de ser un intento de phishing."
    else:
        status_color = "🟢"
        recommendation = "✅ Este email parece seguro, pero siempre mantén un ojo crítico."

    st.markdown(f"**Predicción:** {status_color} {result['prediction']}")
    st.markdown(f"**Confianza:** {result['confidence']*100:.2f}%")
    
    return recommendation

def display_probabilities(col1, result):
    """Muestra las barras de probabilidad."""
    st.markdown("### Probabilidades")
    st.progress(result["probability_phishing"])
    st.markdown(f"Probabilidad de Phishing: {result['probability_phishing']*100:.2f}%")
    st.progress(result["probability_safe"])
    st.markdown(f"Probabilidad de Email Seguro: {result['probability_safe']*100:.2f}%")

def main():
    st.set_page_config(
        page_title="Detector de Phishing Email",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 Detector de Emails de Phishing")
    st.markdown("""
    Esta aplicación analiza emails para detectar si son intentos de phishing o emails seguros.
    
    ### 📝 Instrucciones:
    1. Ingresa el contenido del email en el área de texto
    2. Haz clic en 'Analizar Email'
    3. Revisa los resultados del análisis
    """)

    # Cargar el modelo
    predictor = load_model()
    if not predictor:
        return

    # Área de entrada de texto
    email_text = st.text_area(
        "Contenido del Email:",
        height=200,
        placeholder="Pega aquí el contenido del email que quieres analizar..."
    )

    # Ejemplos predefinidos
    st.markdown("### 📋 O prueba con un ejemplo:")
    examples = {
        "Email Phishing": """Dear valued customer, Your account has been suspended. 
        Click here immediately to verify your identity: http://suspicious-link.com""",
        
        "Email Seguro": """Hi team, Here's the agenda for tomorrow's meeting:
        1. Project updates
        2. Budget review
        3. Q&A session
        Best regards, John""",
        
        "Email Phishing Urgente": """URGENT: You've won $1,000,000! 
        Send your bank details now to claim your prize!!!"""
    }

    selected_example = st.selectbox("Selecciona un ejemplo:", list(examples.keys()))
    if st.button("Usar ejemplo"):
        email_text = examples[selected_example]
        st.text_area("Contenido del ejemplo:", value=email_text, height=150)

    # Botón de análisis
    if st.button("🔍 Analizar Email") and email_text:
        with st.spinner("Analizando email..."):
            result = predictor.predict(email_text)

        # Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Resultado del Análisis")
            
            # Determinar el color según la predicción
            if result["is_phishing"]:
                status_color = "🔴"
                recommendation = "⚠️ Ten cuidado con este email. Muestra señales de ser un intento de phishing."
            else:
                status_color = "🟢"
                recommendation = "✅ Este email parece seguro, pero siempre mantén un ojo crítico."

            st.markdown(f"**Predicción:** {status_color} {result['prediction']}")
            st.markdown(f"**Confianza:** {result['confidence']*100:.2f}%")
            
            # Barra de probabilidad
            display_probabilities(col1, result)

        with col2:
            st.markdown("### 💡 Recomendación")
            recommendation = display_analysis_results(col1, result)
            
            st.markdown("### 🚩 Señales de Alerta Comunes:")
            st.markdown("""
            - Enlaces sospechosos
            - Urgencia en el mensaje
            - Solicitud de información personal
            - Errores gramaticales
            - Remitente desconocido
            - Ofertas demasiado buenas
            """)

if __name__ == "__main__":
    main() 