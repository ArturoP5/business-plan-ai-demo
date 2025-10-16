#!/usr/bin/env python3
"""
Fix para el error de hipoteca_meses cuando el plazo es 0
Solo modifica la línea 2988
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Modificar SOLO la línea 2988 (índice 2987)
old_line = lines[2987]
new_line = "                        max_value=max(hipoteca_plazo_total * 12, 1),\n"

print(f"Línea anterior: {old_line.strip()}")
print(f"Línea nueva:    {new_line.strip()}")

# Hacer el cambio
lines[2987] = new_line

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Cambio aplicado en línea 2988")
