#!/usr/bin/env python3
"""
Fix para que años transcurridos no sea mayor que el plazo
Modifica línea 1411
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# La línea anterior (1410) ya tiene el plazo corregido
# Ahora asegurar que años transcurridos sea coherente
old_line = lines[1410]
new_line = "        default_prestamo_años_transcurridos = min(int(datos_excel['balance_pasivo'].get('prestamo_años_transcurridos', 5)), max(default_prestamo_plazo - 1, 0))\n"

print(f"Línea anterior: {old_line.strip()}")
print(f"Línea nueva:    {new_line.strip()}")

# Hacer el cambio
lines[1410] = new_line

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Cambio aplicado en línea 1411")
