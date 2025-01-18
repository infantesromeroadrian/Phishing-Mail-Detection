import streamlit as st
import torch
from models.predictor import PhishingPredictor
from utils.config import Config
import os
from utils.history import AnalysisHistory
from pathlib import Path

def load_model():
    """Carga el modelo desde Hugging Face Hub."""
    try:
        print("Intentando cargar modelo desde Hugging Face Hub...")
        predictor = PhishingPredictor(
            model_id="infantesromeroadrian/phishing-detection-bert",
            max_length=Config.MAX_LENGTH
        )
        # Verificar que el modelo se cargó correctamente
        test_text = "Test email"
        predictor.predict(test_text)
        print("Modelo cargado exitosamente")
        return predictor
    except Exception as e:
        st.error(f"⚠️ Error al cargar el modelo: {str(e)}")
        st.info("Por favor, verifica la conexión a internet y los permisos")
        return None

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

def display_email_analysis(email_text, result):
    """Muestra un análisis detallado del email."""
    st.markdown("### 📧 Análisis de Características")
    
    # Análisis de características sospechosas
    suspicious_features = []
    
    # Detectar URLs
    if "http://" in email_text or "https://" in email_text:
        suspicious_features.append("Contiene enlaces URL")
    
    # Detectar urgencia
    urgent_words = ["urgent", "immediately", "now", "quick", "urgente", "inmediatamente"]
    if any(word in email_text.lower() for word in urgent_words):
        suspicious_features.append("Usa lenguaje de urgencia")
    
    # Detectar solicitudes de información sensible
    sensitive_words = ["password", "credit card", "bank", "account", "social security"]
    if any(word in email_text.lower() for word in sensitive_words):
        suspicious_features.append("Solicita información sensible")
    
    # Mostrar características
    if suspicious_features:
        st.warning("⚠️ Características sospechosas detectadas:")
        for feature in suspicious_features:
            st.markdown(f"- {feature}")
    else:
        st.success("✅ No se detectaron características sospechosas obvias")

def display_confidence_gauge(result):
    """Muestra un medidor de confianza estilizado."""
    confidence = result['confidence'] * 100
    
    # Determinar color basado en la predicción y confianza
    if result['is_phishing']:
        color = "red" if confidence > 90 else "orange"
    else:
        color = "green" if confidence > 90 else "blue"
    
    # Crear medidor HTML personalizado
    html_gauge = f"""
        <div style="text-align: center;">
            <div style="
                width: 200px;
                height: 200px;
                margin: auto;
                background: conic-gradient({color} {confidence}%, #f0f0f0 0);
                border-radius: 50%;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-size: 24px;
                    font-weight: bold;
                ">
                    {confidence:.1f}%
                </div>
            </div>
        </div>
    """
    st.components.v1.html(html_gauge, height=250)

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

    # Agregar pestañas
    tab1, tab2, tab3 = st.tabs(["📧 Análisis", "📊 Historial", "ℹ️ Ayuda"])
    
    with tab1:
        # Código existente de análisis
        if st.button("🔍 Analizar Email") and email_text:
            with st.spinner("Analizando email..."):
                result = predictor.predict(email_text)
                
                # Mostrar resultados en un diseño más atractivo
                col1, col2 = st.columns(2)
                with col1:
                    display_confidence_gauge(result)
                    display_probabilities(col1, result)
                
                with col2:
                    display_email_analysis(email_text, result)
                    display_analysis_results(col2, result)
                
                # Guardar en historial
                history = AnalysisHistory()
                history.add_analysis(email_text, result)
    
    with tab2:
        st.markdown("### 📊 Historial de Análisis")
        history = AnalysisHistory()
        recent = history.get_recent_analyses()
        
        for analysis in recent:
            with st.expander(f"{analysis['timestamp']} - {analysis['prediction']}"):
                st.text(analysis['email_preview'])
                st.metric("Confianza", f"{analysis['confidence']*100:.1f}%")
    
    with tab3:
        st.markdown("""
        ### 🔍 Cómo Usar el Detector
        1. Pega el contenido del email que quieres analizar
        2. Haz clic en 'Analizar Email'
        3. Revisa los resultados y las características sospechosas
        
        ### 🚩 Señales Comunes de Phishing
        - Urgencia excesiva en el mensaje
        - Solicitudes de información personal
        - Enlaces sospechosos
        - Ofertas demasiado buenas
        - Errores gramaticales
        - Remitente desconocido
        """)

if __name__ == "__main__":
    main() 