#!/usr/bin/env python3
"""
Fix para el error de años transcurridos cuando el plazo es muy corto
Solo modifica la línea 2808
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Modificar SOLO la línea 2808 (índice 2807)
old_line = lines[2807]
new_line = "                        max_value=max(prestamo_plazo_original - 1, 0),\n"

print(f"Línea anterior: {old_line.strip()}")
print(f"Línea nueva:    {new_line.strip()}")

# Hacer el cambio
lines[2807] = new_line

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Cambio aplicado en línea 2808")
