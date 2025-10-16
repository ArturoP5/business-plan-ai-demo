#!/usr/bin/env python3
"""
Guarda los datos de empresa desde CUALQUIER fuente (demos, Excel, manual)
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# 1. Agregar MetalPro Industrial (que faltó)
for i in range(1365, 1375):
    if i < len(lines) and "✅ Cargado: MetalPro Industrial" in lines[i]:
        lines.insert(i+1, "        # Guardar datos de la empresa en session_state\n")
        lines.insert(i+2, "        if 'info_general' in datos_excel:\n")
        lines.insert(i+3, "            st.session_state['empresa_demo_data'] = datos_excel['info_general']\n")
        print(f"✅ Agregado guardado para MetalPro Industrial en línea {i+1}")
        break

# 2. Para carga desde Excel, buscar donde se procesa
for i in range(920, 950):
    if "if empresa_demo == \"📁 Cargar desde Excel\":" in lines[i]:
        # Buscar donde se procesa el archivo Excel exitosamente
        j = i
        while j < i + 100 and "st.success" not in lines[j]:
            j += 1
        if j < i + 100 and "Datos cargados correctamente" in lines[j]:
            lines.insert(j+1, "                # Guardar datos de empresa desde Excel\n")
            lines.insert(j+2, "                if 'info_general' in datos_excel:\n")
            lines.insert(j+3, "                    st.session_state['empresa_demo_data'] = datos_excel['info_general']\n")
            print(f"✅ Agregado guardado para carga desde Excel en línea {j+1}")
            break

# Guardar cambios
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Datos de empresa se guardan desde TODAS las fuentes")
