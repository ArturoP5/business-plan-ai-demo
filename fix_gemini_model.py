#!/usr/bin/env python3
"""
Actualizar el modelo de Gemini al correcto
"""

# Leer el archivo
with open("utils/ai_integration.py", "r", encoding="utf-8") as f:
    content = f.read()

# Reemplazar el modelo antiguo por el nuevo
content = content.replace(
    "self.client = genai.GenerativeModel('gemini-pro')",
    "self.client = genai.GenerativeModel('gemini-1.5-flash')"
)

# Si eso no funcionó, intentar con otro patrón
if 'gemini-1.5-flash' not in content:
    content = content.replace(
        'genai.GenerativeModel("gemini-pro")',
        'genai.GenerativeModel("gemini-1.5-flash")'
    )

# Guardar
with open("utils/ai_integration.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Modelo de Gemini actualizado a 'gemini-1.5-flash'")
print("Este es el modelo gratuito más reciente de Google")

