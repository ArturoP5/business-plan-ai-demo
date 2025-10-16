#!/usr/bin/env python3
"""
Arregla definitivamente los text_area eliminando los títulos duplicados
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Arreglar descripcion_actividad
for i in range(1555, 1565):
    if 'descripcion_actividad = st.text_area(' in lines[i]:
        # Reconstruir correctamente TODO el text_area
        lines[i:i+9] = [
            '        descripcion_actividad = st.text_area(\n',
            '            "Descripción de la Actividad",\n',
            '            value=default_descripcion if "default_descripcion" in locals() else "",\n',
            '            placeholder="¿Qué hace la empresa? Describa brevemente su actividad principal...",\n',
            '            height=100,\n',
            '            key="descripcion_actividad_sidebar",\n',
            '            help="Esta información mejorará significativamente el análisis"\n',
            '        )\n',
            '        \n'
        ]
        print("✅ Arreglado descripcion_actividad")
        break

# Arreglar productos_servicios
for i in range(1565, 1575):
    if 'productos_servicios = st.text_area(' in lines[i]:
        # Buscar cuántas líneas ocupa actualmente
        end_line = i
        for j in range(i+1, i+10):
            if ')' in lines[j] and lines[j].strip() == ')':
                end_line = j
                break
        
        # Reemplazar todo el bloque
        lines[i:end_line+1] = [
            '        productos_servicios = st.text_area(\n',
            '            "Productos/Servicios Principales",\n',
            '            value=default_productos if "default_productos" in locals() else "",\n',
            '            placeholder="Liste los principales productos o servicios que ofrece...",\n',
            '            height=100,\n',
            '            key="productos_servicios_sidebar"\n',
            '        )\n'
        ]
        print("✅ Arreglado productos_servicios")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Ambos text_area corregidos completamente")
