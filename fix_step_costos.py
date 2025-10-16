#!/usr/bin/env python3
"""
Cambia el step del slider de costos variables a 0.5
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Cambiar la línea 1751 (índice 1750)
if lines[1750].strip() == "step=1,":
    lines[1750] = "        step=0.5,\n"
    print(f"✅ Línea 1751: Cambiado step de 1 a 0.5")
    
    # Guardar
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("✅ Ahora el slider permite decimales (40.5%, 41%, etc.)")
else:
    print(f"⚠️ La línea 1751 no tiene el contenido esperado: {lines[1750].strip()}")
