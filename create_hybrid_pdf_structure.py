#!/usr/bin/env python3
"""
Reorganizar pdf_mckinsey_generator.py para modelo híbrido
"""

import re

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    content = f.read()

# Hacer backup primero
with open("utils/pdf_mckinsey_generator_backup_hybrid.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Backup creado: pdf_mckinsey_generator_backup_hybrid.py")

# Ahora necesitamos identificar las secciones a reorganizar
# Buscar donde se genera el SWOT de página 8
swot_page8 = re.search(r'# PÁGINA 8.*?SWOT.*?(?=# PÁGINA|\Z)', content, re.DOTALL)
if swot_page8:
    print(f"Encontrado SWOT en página 8 en posición {swot_page8.start()}")

# Buscar donde se generan las proyecciones detalladas
proyecciones = re.search(r'# PROYECCIONES DETALLADAS.*?(?=# RECOMENDACIONES|\Z)', content, re.DOTALL)
if proyecciones:
    print(f"Encontradas proyecciones detalladas en posición {proyecciones.start()}")

print("\n📋 Estructura actual identificada")
print("Necesitamos:")
print("1. Eliminar SWOT de página 8")
print("2. Mover SWOT después de proyecciones año 5")
print("3. Agregar balances bajo cada P&L anual")
print("4. Usar SWOT y Recomendaciones de IA si existen")

