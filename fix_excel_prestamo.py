#!/usr/bin/env python3
"""
Fix para el error de prestamo_plazo cuando viene 0 del Excel
Solo modifica la línea 1410
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Modificar SOLO la línea 1410 (índice 1409)
old_line = lines[1409]
new_line = "        default_prestamo_plazo = max(1, int(datos_excel['balance_pasivo'].get('prestamo_plazo_original', 10)))\n"

print(f"Línea anterior: {old_line.strip()}")
print(f"Línea nueva:    {new_line.strip()}")

# Hacer el cambio
lines[1409] = new_line

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Cambio aplicado en línea 1410")
