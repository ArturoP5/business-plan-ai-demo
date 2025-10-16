#!/usr/bin/env python3
"""
Arregla definitivamente el problema de datos en el PDF con IA
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se genera el PDF con IA (alrededor de línea 5370)
for i in range(5365, 5375):
    if "datos['ia_model'] = model_name" in lines[i]:
        # Insertar la línea que falta ANTES de agregar ia_model
        lines.insert(i, "                                            datos = st.session_state.datos_guardados\n")
        print(f"✅ Agregada línea en posición {i+1}: datos = st.session_state.datos_guardados")
        
        # También necesitamos asegurar que datos_empresa tenga el nombre correcto
        # Agregar línea para corregir el nombre
        lines.insert(i+1, "                                            # Asegurar que el nombre esté disponible\n")
        lines.insert(i+2, "                                            if 'nombre_empresa' not in datos['datos_empresa']:\n")
        lines.insert(i+3, "                                                datos['datos_empresa']['nombre_empresa'] = datos.get('nombre_empresa', 'Empresa')\n")
        print("✅ Agregada corrección del nombre de empresa")
        break

# Guardar cambios
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Problema de datos arreglado:")
print("  - datos ahora toma los valores de session_state.datos_guardados")
print("  - nombre_empresa se asegura que exista en datos_empresa")
