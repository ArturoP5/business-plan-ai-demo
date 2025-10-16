import google.generativeai as genai

# Pega tu API key aquí temporalmente solo para probar
API_KEY = input("Pega tu API key de Gemini: ")
genai.configure(api_key=API_KEY)

# Listar modelos disponibles
print("\nModelos disponibles:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")

