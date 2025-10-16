#!/usr/bin/env python3
"""
Arregla el mapeo completo de datos para el PDF con IA
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se preparan los financial_data (alrededor de línea 5359)
for i in range(5355, 5365):
    if "financial_data = {" in lines[i]:
        # Reemplazar todo el bloque de financial_data con el mapeo correcto
        new_financial_data = """                                            financial_data = {
                                                'enterprise_value': st.session_state.get('resultado_mck', {}).get('enterprise_value', 0),
                                                'wacc': st.session_state.get('resultado_mck', {}).get('wacc', 0),
                                                'tir': st.session_state.get('resultado_mck', {}).get('tir_proyecto', 0),
                                                'payback': st.session_state.get('resultado_mck', {}).get('payback_years', 0)
                                            }
"""
        lines[i:i+5] = [new_financial_data]
        print(f"✅ Financial data ahora busca directamente en session_state.resultado_mck")
        break

# Agregar los DataFrames del P&L y Balance para los anexos
for i in range(5370, 5380):
    if "datos['ia_model'] = model_name" in lines[i]:
        # Agregar los DataFrames necesarios
        lines.insert(i+1, "                                            # Agregar DataFrames para anexos\n")
        lines.insert(i+2, "                                            datos['pyl_df'] = st.session_state.datos_guardados.get('pyl')\n")
        lines.insert(i+3, "                                            datos['balance_df'] = st.session_state.datos_guardados.get('balance')\n")
        lines.insert(i+4, "                                            datos['fcf_df'] = st.session_state.datos_guardados.get('cash_flow')\n")
        print("✅ Agregados DataFrames para anexos")
        break

# Guardar cambios
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Mapeo completo arreglado:")
print("  1. financial_data busca en session_state.resultado_mck")
print("  2. DataFrames de P&L, Balance y FCF agregados")
