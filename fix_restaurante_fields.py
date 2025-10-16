#!/usr/bin/env python3
"""
Agrega actualización de campos para Restaurante La Terraza
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar la línea específica del restaurante
for i in range(len(lines)):
    if 'st.success("✅ Cargado: Restaurante La Terraza (Hostelería)")' in lines[i]:
        # Insertar código para actualizar session_state ANTES del success
        indent = '        '
        new_lines = f'''{indent}# Actualizar campos descriptivos en session_state
{indent}if 'descripcion_actividad' in datos_desde_excel:
{indent}    st.session_state['descripcion_actividad_sidebar'] = datos_desde_excel['descripcion_actividad']
{indent}if 'productos_servicios' in datos_desde_excel:
{indent}    st.session_state['productos_servicios_sidebar'] = datos_desde_excel['productos_servicios']
{indent}
'''
        lines.insert(i, new_lines)
        print("✅ Agregada actualización de campos para Restaurante La Terraza")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\nAhora el Restaurante La Terraza también actualizará los campos automáticamente")
