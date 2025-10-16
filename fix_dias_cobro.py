#!/usr/bin/env python3
"""
Fix para el límite de dias_cobro
Aumenta el máximo a 365 días
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix línea 3428 - dias_cobro
if "dias_cobro = st.number_input(\"Días de cobro\", 0, 120," in lines[3427]:
    lines[3427] = lines[3427].replace(", 0, 120,", ", 0, 365,")
    print(f"✅ Línea 3428: Cambiado máximo de días_cobro de 120 a 365")
    
    # Guardar
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
else:
    print("⚠️ No se encontró la línea esperada")

