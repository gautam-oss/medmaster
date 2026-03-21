import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def get_gemini_response(user_message, conversation_history=None):
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)

        if not settings.GEMINI_API_KEY:
            return "Gemini API key not configured. Set GEMINI_API_KEY in settings.py to enable AI responses."

        model = genai.GenerativeModel('gemini-2.5-flash')

        healthcare_context = """
        You are a helpful healthcare assistant for MedMaster. Help with general health information,
        medical terms, symptom guidance (not diagnosis), healthy lifestyle tips, and
        appointment guidance. Always recommend consulting a doctor for medical advice.
        Keep responses concise and friendly.
        """

        if conversation_history and len(conversation_history) > 0:
            recent = list(conversation_history)[-5:]
            history_text = "\n".join([
                f"{'User' if m.is_from_user else 'Assistant'}: {m.content[:300]}"
                for m in recent
            ])
            prompt = f"{healthcare_context}\n\nRecent conversation:\n{history_text}\n\nUser: {user_message}\nAssistant:"
        else:
            prompt = f"{healthcare_context}\n\nUser: {user_message}\nAssistant:"

        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=1000,
        )

        response = model.generate_content(prompt, generation_config=generation_config)

        if response and hasattr(response, 'text') and response.text:
            return response.text.strip()
        return "I'm having trouble generating a response. Please try again."

    except ImportError:
        return "google-generativeai package not installed. Run: pip install google-generativeai"
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        if "API_KEY" in str(e).upper():
            return "Invalid API key. Please check your GEMINI_API_KEY setting."
        if "QUOTA" in str(e).upper():
            return "API quota exceeded. Please try again later."
        return "I'm having trouble connecting to the AI service. Please try again later."
