#!/usr/bin/env python3
"""
Arregla el paso completo de datos de empresa al PDF con IA
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se selecciona una empresa demo (alrededor de línea 2540)
for i in range(2535, 2550):
    if "elif nombre_empresa == 'TechStart SaaS':" in lines[i]:
        # Después de esta línea debe estar la asignación de empresa_seleccionada
        # Necesitamos asegurar que se guarde en session_state
        j = i + 1
        while j < i + 20 and "empresa_seleccionada = {" not in lines[j]:
            j += 1
        
        if j < i + 20:
            # Encontramos donde se define empresa_seleccionada
            # Agregar línea para guardar en session_state
            k = j
            while k < j + 100 and lines[k].strip() != "}":
                k += 1
            
            # Insertar después del cierre del diccionario
            lines.insert(k+1, "                    st.session_state['empresa_demo_data'] = empresa_seleccionada['info_general']\n")
            print(f"✅ Agregado guardado de datos empresa en línea {k+2}")
            break

# Ahora actualizar donde se guardan los datos_guardados (alrededor de línea 4526)
for i in range(4520, 4535):
    if "# 'datos_empresa': empresa_seleccionada," in lines[i]:
        # Cambiar para usar los datos correctos
        lines[i] = "        'datos_empresa': st.session_state.get('empresa_demo_data', {}),\n"
        print(f"✅ Actualizado datos_empresa en línea {i+1}")
        break

# Guardar cambios
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Ruta de datos completada:")
print("  - empresa_demo_data se guarda en session_state")
print("  - datos_guardados ahora incluye datos_empresa correctamente")
