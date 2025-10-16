#!/usr/bin/env python3
"""
Actualizar al modelo Gemini más reciente disponible
"""

# Leer el archivo
with open("utils/ai_integration.py", "r", encoding="utf-8") as f:
    content = f.read()

# Reemplazar con el modelo que sí funciona
content = content.replace(
    "self.client = genai.GenerativeModel('gemini-1.5-flash')",
    "self.client = genai.GenerativeModel('gemini-1.5-flash-latest')"
)

# Si no encuentra el anterior, buscar otras variaciones
if 'gemini-1.5-flash-latest' not in content:
    content = content.replace(
        "genai.GenerativeModel('gemini",
        "genai.GenerativeModel('gemini-1.5-flash-latest"
    )

# Guardar
with open("utils/ai_integration.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Modelo actualizado a 'gemini-1.5-flash-latest'")
print("\nSi sigue sin funcionar, prueba con GPT-4 que es más estable")

