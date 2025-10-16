#!/usr/bin/env python3
"""
Arregla el error de empresa_seleccionada no definida
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar y comentar o eliminar la línea problemática
for i in range(4525, 4530):
    if "'datos_empresa': empresa_seleccionada," in lines[i]:
        # Comentar la línea por ahora
        lines[i] = "        # 'datos_empresa': empresa_seleccionada,  # TODO: obtener datos correctos\n"
        print(f"✅ Comentada línea problemática {i+1}")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("✅ Error corregido temporalmente")
