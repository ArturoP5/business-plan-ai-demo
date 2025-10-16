#!/usr/bin/env python3
"""
Arregla el método faltante _create_swot_analysis en pdf_ai_generator_completo.py
"""

with open('utils/pdf_ai_generator_completo.py', 'r') as f:
    content = f.read()

# El método se llama _create_swot_analysis pero está definido como _create_swot_analysis
# Buscar y reemplazar la llamada incorrecta
content = content.replace('self._create_swot_analysis(', 'self._create_swot_ai(')

# Guardar
with open('utils/pdf_ai_generator_completo.py', 'w') as f:
    f.write(content)

print("✅ Arreglado nombre del método SWOT")
