#!/usr/bin/env python3
"""
Arregla el error de sintaxis en financial_data
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar la línea con el error (alrededor de 5365)
for i in range(5358, 5368):
    if lines[i].strip() == '}':
        # Esta es la línea problemática, necesita cerrar correctamente
        if 'financial_data = {' in lines[i-6]:
            # Asegurar que el diccionario esté bien cerrado
            lines[i] = "                                            }\n"
            print(f"✅ Arreglado cierre del diccionario en línea {i+1}")
            break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("✅ Error de sintaxis corregido")
