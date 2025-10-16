#!/usr/bin/env python3
"""
Cambia el step del slider a 0.1 para mayor precisión
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Cambiar la línea 1751 de step=0.5 a step=0.1
if "step=0.5," in lines[1750]:
    lines[1750] = "        step=0.1,\n"
    print(f"✅ Línea 1751: Cambiado step de 0.5 a 0.1")
    
    # Guardar
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("✅ Ahora permite precisión de 0.1% (40.1%, 40.2%, 40.3%, etc.)")
else:
    print(f"⚠️ La línea 1751 no tiene step=0.5: {lines[1750].strip()}")
