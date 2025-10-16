#!/usr/bin/env python3
"""
Arregla el value duplicado en cuota_mercado y cambia step a 0.1
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar cuota_mercado y arreglar
for i in range(1684, 1695):
    if 'cuota_mercado = st.number_input(' in lines[i]:
        # Reescribir todo el bloque correctamente
        lines[i:i+8] = [
            '            cuota_mercado = st.number_input(\n',
            '                "Cuota de Mercado (%)",\n',
            '                min_value=0.0,\n',
            '                max_value=100.0,\n',
            '                value=float(default_cuota_mercado) if "default_cuota_mercado" in locals() else 10.0,\n',
            '                step=0.1,\n',
            '                key="cuota_mercado_sidebar",\n',
            '                help="% estimado en su segmento"\n'
        ]
        print("✅ Arreglado cuota_mercado:")
        print("  - Eliminado value duplicado")
        print("  - Cambiado step de 0.5 a 0.1")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)
