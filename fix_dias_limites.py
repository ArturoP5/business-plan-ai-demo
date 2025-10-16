#!/usr/bin/env python3
"""
Fix para los límites de días de cobro, pago y stock
Hace los máximos más flexibles
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = 0

# Fix línea 3430 - dias_pago
if "dias_pago = st.number_input(\"Días de pago\", 0, 90," in lines[3429]:
    old_line = lines[3429]
    lines[3429] = lines[3429].replace(", 0, 90,", ", 0, 365,")
    print(f"✅ Línea 3430: Cambiado máximo de días_pago de 90 a 365")
    changes += 1

# Fix línea 3432 - dias_stock  
if "dias_stock = st.number_input(\"Días de stock\", 0, 90," in lines[3431]:
    old_line = lines[3431]
    lines[3431] = lines[3431].replace(", 0, 90,", ", 0, 365,")
    print(f"✅ Línea 3432: Cambiado máximo de días_stock de 90 a 365")
    changes += 1

# Guardar si hubo cambios
if changes > 0:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"\n✅ Total de cambios aplicados: {changes}")
else:
    print("⚠️ No se encontraron las líneas esperadas")

