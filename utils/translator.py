from deep_translator import GoogleTranslator

def translate_to_english(text: str) -> str:
    """
    Har qanday matnni ingliz tiliga tarjima qiladi.
    Agar matn allaqachon ingliz tilida bo‘lsa, o‘sha matnni qaytaradi.
    """
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated
    except Exception as e:
        # Agar tarjima xato bersa, original matnni qaytaramiz
        print(f"Translation error: {e}")
        return text 