#!/usr/bin/env python3
"""
Encontrar la línea exacta que causa el error
"""

# Agregar logging detallado al PDF generator
with open("utils/pdf_mckinsey_generator.py", "r") as f:
    lines = f.readlines()

# Buscar todas las líneas con corchetes [] que podrían causar el error
print("Líneas problemáticas con acceso directo []:")
for i, line in enumerate(lines):
    if "['" in line or '["' in line or "[0]" in line or "[1]" in line:
        # Excluir definiciones de listas
        if "= [" not in line and "([" not in line:
            print(f"L{i+1}: {line.strip()[:100]}")

