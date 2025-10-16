#!/usr/bin/env python3
"""
Conecta los campos descripcion_actividad y productos_servicios 
de las empresas demo con los campos del sidebar
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se cargan las empresas demo y agregar los campos al session_state
empresas = [
    ('Restaurante La Terraza SL', '🍕 Restaurante La Terraza'),
    ('TechStart SaaS', '💻 TechStart SaaS'),
    ('ModaOnline Shop', '🛍️ ModaOnline Shop'),
    ('MetalPro Industrial', '🏭 MetalPro Industrial')
]

cambios = 0

for empresa_nombre, empresa_emoji in empresas:
    for i in range(len(lines)):
        # Buscar donde se hace el st.success de cada empresa
        if f'st.success("✅ Cargado: {empresa_nombre}' in lines[i]:
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
            cambios += 1
            print(f"✅ Agregada actualización de campos para {empresa_nombre}")
            break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print(f"\n✅ Total: {cambios} empresas actualizadas")
print("Ahora los campos descripcion_actividad y productos_servicios se cargarán automáticamente")
