#!/usr/bin/env python3
"""
Hacer que los campos del sidebar usen los valores de datos_excel
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar la sección de Descripción del Negocio
cambios_realizados = []

# 1. Buscar y modificar "Descripción de la Actividad"
for i, line in enumerate(lines):
    if '"Descripción de la Actividad"' in line and 'st.text_area' in line:
        # Ver las siguientes líneas
        if i + 3 < len(lines):
            # Agregar value= si no existe
            if 'value=' not in lines[i+1] and 'value=' not in lines[i+2]:
                lines[i+1] = lines[i+1].rstrip() + '\n'
                lines[i+2] = '            value=datos_excel["info_general"].get("descripcion_actividad", "") if datos_excel else "",\n' + lines[i+2]
                cambios_realizados.append(f"Línea {i+1}: Agregado value para Descripción de la Actividad")

# 2. Buscar y modificar "Productos/Servicios Principales"
for i, line in enumerate(lines):
    if '"Productos/Servicios Principales"' in line and 'st.text_area' in line:
        if i + 3 < len(lines):
            if 'value=' not in lines[i+1] and 'value=' not in lines[i+2]:
                lines[i+1] = lines[i+1].rstrip() + '\n'
                lines[i+2] = '            value=datos_excel["info_general"].get("productos_servicios", "") if datos_excel else "",\n' + lines[i+2]
                cambios_realizados.append(f"Línea {i+1}: Agregado value para Productos/Servicios")

# 3. Modificar cuota_mercado para que use el valor de datos_excel
for i, line in enumerate(lines):
    if 'cuota_mercado = st.number_input(' in line:
        # Buscar la línea de value=
        for j in range(i+1, min(i+10, len(lines))):
            if 'value=' in lines[j] and '0.0' in lines[j]:
                lines[j] = '                value=datos_excel["info_general"].get("cuota_mercado", 0.0) if datos_excel else 0.0,\n'
                cambios_realizados.append(f"Línea {j+1}: Modificado value de cuota_mercado")
                break

# 4. Buscar ventajas_competitivas (el del sidebar, no el principal)
for i, line in enumerate(lines):
    if 'ventajas_competitivas = st.text_area(' in line and 'ventajas_competitivas_sidebar' in lines[i+4]:
        # Este es el campo del sidebar
        for j in range(i+1, min(i+6, len(lines))):
            if 'placeholder=' in lines[j]:
                # Insertar value después del placeholder
                lines[j] = lines[j].rstrip() + '\n'
                lines[j] = lines[j] + '            value=datos_excel["info_general"].get("ventajas_competitivas", "") if datos_excel else "",\n'
                cambios_realizados.append(f"Línea {j+1}: Agregado value para ventajas_competitivas")
                break

# 5. Buscar clientes_objetivo
for i, line in enumerate(lines):
    if 'clientes_objetivo = st.text_area(' in line and 'clientes_objetivo_sidebar' in lines[i+4]:
        for j in range(i+1, min(i+6, len(lines))):
            if 'placeholder=' in lines[j]:
                lines[j] = lines[j].rstrip() + '\n'
                lines[j] = lines[j] + '            value=datos_excel["info_general"].get("clientes_objetivo", "") if datos_excel else "",\n'
                cambios_realizados.append(f"Línea {j+1}: Agregado value para clientes_objetivo")
                break

# Guardar los cambios
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Modificados los campos del sidebar para usar datos_excel:")
for cambio in cambios_realizados:
    print(f"  - {cambio}")

if not cambios_realizados:
    print("\n⚠️ No se encontraron campos para modificar.")
    print("Buscando la estructura actual de los campos...")
    
    # Buscar donde están estos campos
    with open('app.py', 'r') as f:
        content = f.read()
    
    if 'Descripción de la Actividad' in content:
        print("✓ Campo 'Descripción de la Actividad' existe en el archivo")
    if 'Productos/Servicios Principales' in content:
        print("✓ Campo 'Productos/Servicios Principales' existe en el archivo")

