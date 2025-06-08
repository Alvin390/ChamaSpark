from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
import openai
from django.conf import settings
from .firebase.firestore_service import SparkGalFirestore
import uuid
import numpy as np
import logging
from django.core.cache import cache
from langdetect import detect, LangDetectException

openai.api_key = settings.OPENAI_API_KEY

# Cache Functions
def get_cached_response(message):
    return cache.get(f"sparkgal:{message}")

def set_cached_response(message, response):
    cache.set(f"sparkgal:{message}", response, timeout=60*60)  # 1 hour

SYSTEM_PROMPT = """
You are Spark Gal, a specialized AI assistant for the Wamama Chama System serving Kenyan women's groups (chamas).

IDENTITY & TONE:
- Warm, empathetic, and encouraging
- Culturally aware of Kenyan contexts and traditions
- Professional but approachable
- Patient with users of all technical abilities

LANGUAGE CAPABILITIES:
- Respond in the same language the user writes in (English, Kiswahili, or Sheng)
- Adapt to informal language, slang, and common misspellings
- For Kiswahili, use standard Kiswahili with occasional coastal phrases when appropriate
- For Sheng, maintain the urban casual style while being clear and respectful

KNOWLEDGE DOMAINS (ONLY discuss these topics):
1. CHAMA OPERATIONS:
   - Group formation, registration, and governance
   - Meeting procedures and record keeping
   - Conflict resolution within groups
   - Leadership rotation and responsibilities

2. FINANCIAL LITERACY:
   - Savings mechanisms and table banking
   - Loan management and interest calculations
   - Investment opportunities for women's groups
   - Financial planning and budgeting
   - Mobile money and digital financial services

3. WOMEN'S EMPOWERMENT:
   - Business skills and entrepreneurship
   - Women's rights and advocacy
   - Education and skill development
   - Work-life balance strategies

4. COMMUNITY DEVELOPMENT:
   - Social impact projects
   - Community health initiatives
   - Environmental sustainability
   - Education support programs

RESPONSE GUIDELINES:
- Keep responses concise (under 3-4 sentences when possible)
- Provide practical, actionable advice
- Include relevant Kenyan context when applicable
- For complex topics, break information into simple steps
- When uncertain, acknowledge limitations rather than providing incorrect information

OFF-TOPIC POLICY:
- For questions outside the knowledge domains, politely decline to answer
- For English: "I'm focused on supporting women's groups and chamas. Could we discuss something related to that instead?"
- For Kiswahili: "Ninalenga kusaidia vikundi vya wanawake na chama. Tunaweza kuzungumza kuhusu hayo badala yake?"
- For Sheng: "Mimi husaidia madem na chama tu. Tunaweza ongea kuhusu hizo mambo badala yake?"

SAFETY:
- Never provide medical diagnoses or treatment recommendations
- Do not give specific legal advice, only general information
- Avoid political discussions or partisan statements
- Prioritize user safety in all recommendations
"""

# Expanded topic keywords for fast, free topic filtering
ALLOWED_TOPICS_KEYWORDS = [
    # Chama operations
    "chama", "group", "registration", "governance", "meeting", "record", "conflict", "leadership",
    # Financial literacy
    "savings", "table banking", "loan", "interest", "investment", "budget", "mobile money", "mpesa", "finance", "financial", "bank",
    # Women's empowerment
    "business", "entrepreneur", "rights", "advocacy", "education", "skill", "work-life", "balance", "empowerment",
    # Community development
    "community", "project", "environment", "sustainability", "support", "initiative", "development",
    # Women's health (EN & SW)
    "health", "woman health", "women's health", "wellness", "nutrition", "reproductive health",
    "afya", "lishe", "uzazi", "mimba", "kliniki", "magonjwa", "mtoto", "mama"
]

def is_on_topic(message):
    msg = message.lower()
    return any(keyword in msg for keyword in ALLOWED_TOPICS_KEYWORDS)

def detect_language(text):
    try:
        lang = detect(text)
        if lang.startswith('sw'):
            return "sw"
        if lang in ("en", "en-US", "en-GB"):
            return "en"
        return lang
    except LangDetectException:
        # Fallback to heuristic
        if any(word in text.lower() for word in ["naomba", "habari", "shida", "mrembo"]):
            return "sw"
        if any(word in text.lower() for word in ["nani", "uko aje", "msee", "mresh"]):
            return "sheng"
        return "en"

def get_conversation_history(conversation_id, n=5):
    # Fetch last n messages from Firestore, newest last
    history = SparkGalFirestore.get_last_n_messages(conversation_id, n)
    # Format as [{"role": "user"/"assistant", "content": ...}, ...]
    return [{"role": m["role"], "content": m["content"]} for m in history]



@method_decorator(csrf_exempt, name='dispatch')
class SparkGalChatView(View):
    def post(self, request):
        user = request.user
        data = request.POST
        message = data.get('message', '')
        conversation_id = data.get('conversation_id')
        language = detect_language(message)
        user_id = str(user.id) if hasattr(user, "id") else "anonymous"

        # Caching
        cached = get_cached_response(message)
        if cached:
            logging.info("Cache hit for message: %s", message)
            return JsonResponse({
                "response": cached,
                "conversation_id": conversation_id
            })

        # Create conversation if not exists
        if not conversation_id:
            conversation_id = SparkGalFirestore.create_conversation(user_id)

        # Save user message
        SparkGalFirestore.save_message(user_id, conversation_id, "user", message, language)

        # Topic filtering (fast keyword-based)
        if not is_on_topic(message):
            polite_reject = {
                "en": "I'm focused on supporting women's groups and chamas. Could we discuss something related to that instead?",
                "sw": "Ninalenga kusaidia vikundi vya wanawake na chama. Tunaweza kuzungumza kuhusu hayo badala yake?",
                "sheng": "Mimi husaidia madem na chama tu. Tunaweza ongea kuhusu hizo mambo badala yake?"
            }
            response = polite_reject.get(language, polite_reject["en"])
            SparkGalFirestore.save_message(user_id, conversation_id, "assistant", response, language)
            logging.info("Off-topic message detected: %s", message)
            return JsonResponse({
                "response": response,
                "conversation_id": conversation_id
            })

        # Conversation context (last 5 messages)
        history = get_conversation_history(conversation_id, n=5)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": message}]

        # Call OpenAI (only one API call per message)
        try:
            logging.info("Calling OpenAI API for user_id=%s, conversation_id=%s, message=%s", user_id, conversation_id, message)
            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=300,
            )
            ai_response = completion.choices[0].message.content.strip()
            logging.info("OpenAI API call successful. Response: %s", ai_response)
        except Exception as e:
            logging.error("OpenAI API call failed: %s", str(e))
            ai_response = "Sorry, Spark Gal is unavailable right now."
            SparkGalFirestore.save_message(user_id, conversation_id, "assistant", ai_response, language)
            return JsonResponse({
                "response": ai_response,
                "conversation_id": conversation_id
            })

        SparkGalFirestore.save_message(user_id, conversation_id, "assistant", ai_response, language)
        SparkGalFirestore.update_last_active(conversation_id)
        set_cached_response(message, ai_response)
        return JsonResponse({
            "response": ai_response,
            "conversation_id": conversation_id
        })