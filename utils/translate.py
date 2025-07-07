from google.cloud import translate_v2 as translate

client = translate.Client()

def translate_to_kannada(text):
    result = client.translate(text, target_language='kn')
    return result['translatedText']