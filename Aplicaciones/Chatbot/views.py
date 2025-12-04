import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from google import genai
from django.conf import settings 

GEMINI_API_KEY = getattr(settings, 'GEMINI_API_KEY', None)
client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("INFO: Cliente de Gemini inicializado correctamente.")
    except Exception as e:
        print(f"ERROR: No se pudo crear el cliente de Gemini. Asegúrate que la clave es válida. {e}")
        client = None
else:
    print("ADVERTENCIA: GEMINI_API_KEY no encontrada en settings.py. El chatbot de IA responderá con un error 503.")
SYSTEM_INSTRUCTION = (
    "Eres un asistente de chatbot amigable y profesional para la empresa 'Grupo Santa Maria', "
    "un concesionario de vehículos que ofrece venta de autos, servicios de taller (mantenimiento, reparación), "
    "venta de repuestos y gestión de convenios. Tu objetivo es ayudar a los clientes con información relevante sobre estos temas. "
    "\n\nREGLAS ESTRICTAS DE RESPUESTA:"
    "\n1. **CONTEXTO ÚNICO:** Solo debes responder preguntas relacionadas directamente con 'Grupo Santa Maria' (vehículos, modelos, precios, repuestos, horarios del taller, tipos de mantenimiento, convenios disponibles, o procesos internos de la empresa)."
    "\n2. **FUERA DE TEMA:** Si el usuario pregunta algo *totalmente* ajeno a Grupo Santa Maria (ej: política, clima, recetas, historia general), debes responder amablemente que tu función es solo asistir con información de la empresa. Usa frases como: 'Lo siento, mi función es solo ayudarte con consultas relacionadas con Grupo Santa Maria (vehículos, taller, repuestos y convenios).' o 'Esa pregunta está fuera de mi alcance. ¿En qué puedo ayudarte sobre nuestros servicios de automoción?'"
    "\n3. **FORMATO:** Mantén las respuestas concisas y profesionales, utilizando saltos de línea para facilitar la lectura."
    "\n4. **IDIOMA:** Responde siempre en español."
)

@csrf_exempt
@require_http_methods(["POST"])
def get_chatbot_response(request):
    if client is None:
        return JsonResponse({'response': "Error 503: El servicio de Inteligencia Artificial (IA) no está disponible. Contacta al administrador si el problema persiste."}, status=503)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({'response': "Por favor, escribe un mensaje."}, status=200)
        config = genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=user_message,
            config=config,
        )

        ai_response = response.text
        
        return JsonResponse({'response': ai_response})

    except json.JSONDecodeError:
        return JsonResponse({'response': 'Formato de solicitud no válido.'}, status=400)
    except Exception as e:
        print(f"Error al llamar a la API de Gemini: {e}")
        return JsonResponse({'response': f"Hubo un error al procesar tu solicitud. Código: {type(e).__name__}. Inténtalo de nuevo."}, status=500)