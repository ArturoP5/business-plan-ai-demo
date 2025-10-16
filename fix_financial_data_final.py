#!/usr/bin/env python3
"""
Arregla definitivamente el mapeo de datos financieros para el PDF
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se define financial_data (alrededor de línea 5359)
for i in range(5355, 5365):
    if "'enterprise_value': st.session_state.get('resultado_mck'" in lines[i]:
        # Cambiar para que busque en datos['resultado_mckinsey']
        lines[i] = "                                                'enterprise_value': datos.get('resultado_mckinsey', {}).get('enterprise_value', 0),\n"
        lines[i+1] = "                                                'wacc': datos.get('resultado_mckinsey', {}).get('wacc', 0),\n"
        lines[i+2] = "                                                'tir': datos.get('resultado_mckinsey', {}).get('tir', 0),\n"
        lines[i+3] = "                                                'payback': datos.get('resultado_mckinsey', {}).get('tir', 0)\n"
        print("✅ Financial data ahora busca en datos['resultado_mckinsey']")
        print("  - enterprise_value")
        print("  - wacc")
        print("  - tir")
        break

# Guardar cambios
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Mapeo corregido para usar datos ya cargados")
