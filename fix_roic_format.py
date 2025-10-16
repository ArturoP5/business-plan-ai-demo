#!/usr/bin/env python3
"""
Arregla el formato del ROIC para mostrar % en lugar de €
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se formatea fcf_display (alrededor de línea 5847-5849)
for i in range(5846, 5852):
    if "for col in fcf_display.columns:" in lines[i]:
        # Reemplazar el formateo para excluir ROIC (%)
        lines[i] = "                for col in fcf_display.columns:\n"
        lines[i+1] = "                    if col not in ['Año']:\n"
        lines[i+2] = "                        if col == 'ROIC (%)':\n"
        lines[i+3] = "                            fcf_display[col] = fcf_display[col].apply(lambda x: f\"{x:.1f}%\")\n"
        lines[i+4] = "                        else:\n"
        lines[i+5] = "                            fcf_display[col] = fcf_display[col].apply(lambda x: f\"{get_simbolo_moneda()}{x:,.0f}\".replace(\",\", \".\"))\n"
        # Eliminar la línea extra que sobra
        if i+6 < len(lines) and "st.dataframe" in lines[i+6]:
            pass  # Mantener st.dataframe donde está
        else:
            lines.insert(i+6, "                st.dataframe(fcf_display, use_container_width=True, hide_index=True)\n")
        print(f"✅ Arreglado formato ROIC en líneas {i+1}-{i+6}")
        break

# Guardar cambios
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ ROIC ahora mostrará % en lugar de €")
