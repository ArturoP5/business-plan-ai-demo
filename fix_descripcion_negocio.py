#!/usr/bin/env python3
"""
Agregar valores de datos_excel a los campos de Descripción del Negocio
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

cambios = []

# Buscar "Descripción de la Actividad" en línea 1550
for i in range(1545, 1560):
    if '"Descripción de la Actividad"' in lines[i]:
        print(f"Encontrado 'Descripción de la Actividad' en línea {i+1}")
        
        # Buscar dónde insertar el value (después del placeholder)
        for j in range(i+1, min(i+5, len(lines))):
            if 'placeholder=' in lines[j]:
                # Verificar si ya tiene value
                if 'value=' not in lines[j+1]:
                    # Insertar value después del placeholder
                    lines[j] = lines[j].rstrip() + '\n            value=datos_excel["info_general"].get("descripcion_actividad", "") if datos_excel else "",\n'
                    cambios.append("Descripción de la Actividad")
                    print(f"  Agregado value en línea {j+1}")
                break
        break

# Buscar "Productos/Servicios Principales" alrededor de línea 1558
for i in range(1555, 1570):
    if '"Productos/Servicios Principales"' in lines[i]:
        print(f"Encontrado 'Productos/Servicios Principales' en línea {i+1}")
        
        # Buscar dónde insertar el value
        for j in range(i+1, min(i+5, len(lines))):
            if 'placeholder=' in lines[j]:
                # Verificar si ya tiene value
                if 'value=' not in lines[j+1]:
                    # Insertar value después del placeholder
                    lines[j] = lines[j].rstrip() + '\n            value=datos_excel["info_general"].get("productos_servicios", "") if datos_excel else "",\n'
                    cambios.append("Productos/Servicios Principales")
                    print(f"  Agregado value en línea {j+1}")
                break
        break

# Guardar los cambios
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

if cambios:
    print(f"\n✅ Campos modificados: {', '.join(cambios)}")
else:
    print("\n⚠️ Los campos ya tienen valores o no se encontraron")

# Verificar la estructura actual
print("\nVerificando estructura actual de los campos...")
for i in range(1545, 1570):
    if 'Descripción' in lines[i] or 'Productos' in lines[i]:
        print(f"Línea {i+1}: {lines[i].strip()[:60]}...")

