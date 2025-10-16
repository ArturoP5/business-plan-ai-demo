#!/usr/bin/env python3
"""
Agrega las variables default y el value a los campos estratégicos
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# 1. Agregar defaults después de default_nombre (línea ~1371)
for i in range(1370, 1375):
    if "default_nombre = datos_excel['info_general']['nombre_empresa']" in lines[i]:
        # Agregar las nuevas líneas default
        new_defaults = """        default_descripcion = datos_excel['info_general'].get('descripcion_actividad', '')
        default_productos = datos_excel['info_general'].get('productos_servicios', '')
"""
        lines.insert(i+1, new_defaults)
        print("✅ Agregados defaults cuando hay datos_excel")
        break

# 2. Agregar defaults vacíos después del else (línea ~1464)
for i in range(1462, 1470):
    if 'default_nombre = "Mi Empresa SL"' in lines[i]:
        new_defaults = """        default_descripcion = ""
        default_productos = ""
"""
        lines.insert(i+1, new_defaults)
        print("✅ Agregados defaults vacíos")
        break

# 3. Agregar value a descripcion_actividad (línea ~1552)
for i in range(1550, 1560):
    if 'descripcion_actividad = st.text_area(' in lines[i]:
        # Reemplazar toda la definición con value incluido
        lines[i] = """        descripcion_actividad = st.text_area(
            "Descripción de la Actividad",
            value=default_descripcion if 'default_descripcion' in locals() else "",
"""
        print("✅ Agregado value a descripcion_actividad")
        break

# 4. Agregar value a productos_servicios
for i in range(1558, 1570):
    if 'productos_servicios = st.text_area(' in lines[i]:
        lines[i] = """        productos_servicios = st.text_area(
            "Productos/Servicios Principales",
            value=default_productos if 'default_productos' in locals() else "",
"""
        print("✅ Agregado value a productos_servicios")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\nAhora los campos se cargarán igual que todos los demás")
