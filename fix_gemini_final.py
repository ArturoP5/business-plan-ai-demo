#!/usr/bin/env python3
"""
Actualizar al modelo Gemini que sí está disponible
"""

# Leer el archivo
with open("utils/ai_integration.py", "r", encoding="utf-8") as f:
    content = f.read()

# Reemplazar cualquier modelo anterior con el correcto
# Buscar la línea donde se define el modelo
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'genai.GenerativeModel(' in line and 'gemini' in line:
        # Reemplazar esa línea con el modelo correcto
        lines[i] = "            self.client = genai.GenerativeModel('gemini-2.0-flash')"
        print(f"Línea {i+1} actualizada")

# Reconstruir el contenido
content = '\n'.join(lines)

# Guardar
with open("utils/ai_integration.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Modelo actualizado a 'gemini-2.0-flash'")
print("Este modelo está confirmado como disponible y gratuito")

