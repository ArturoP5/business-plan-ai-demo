#!/usr/bin/env python3
"""
Agrega value a los campos estratégicos faltantes
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Lista de campos y sus líneas aproximadas
campos = [
    ('vision_medio = st.text_area(', 1638, 'default_vision_medio'),
    ('vision_largo = st.text_area(', 1645, 'default_vision_largo'),
    ('ventaja_competitiva_clave = st.text_area(', 1653, 'default_ventaja_competitiva'),
    ('principales_riesgos = st.text_area(', 1660, 'default_principales_riesgos'),
    ('clientes_objetivo = st.text_area(', 1688, 'default_clientes_objetivo')
]

for campo_buscar, linea_aprox, variable_default in campos:
    # Buscar el campo
    for i in range(linea_aprox-2, linea_aprox+5):
        if i < len(lines) and campo_buscar in lines[i]:
            # Buscar donde insertar value (después del título, antes del placeholder)
            for j in range(i+1, i+5):
                if j < len(lines) and 'placeholder=' in lines[j]:
                    # Insertar value antes del placeholder
                    value_line = f'            value={variable_default} if "{variable_default}" in locals() else "",\n'
                    lines.insert(j, value_line)
                    print(f"✅ Agregado value a {campo_buscar.split(' = ')[0]}")
                    break
            break

# Para cuota_mercado (number_input es diferente)
for i in range(1667, 1672):
    if i < len(lines) and 'cuota_mercado = st.number_input(' in lines[i]:
        # Buscar min_value
        for j in range(i+1, i+5):
            if j < len(lines) and 'min_value=' in lines[j]:
                # Insertar value después de max_value
                for k in range(j, j+3):
                    if 'max_value=' in lines[k]:
                        lines.insert(k+1, '                value=default_cuota_mercado if "default_cuota_mercado" in locals() else 10.0,\n')
                        print("✅ Agregado value a cuota_mercado")
                        break
                break
        break

# También necesitamos agregar el default para cuota_mercado y clientes_objetivo
for i in range(1373, 1385):
    if "default_principales_riesgos = datos_excel['info_general'].get('principales_riesgos', '')" in lines[i]:
        # Agregar los que faltan
        new_defaults = """        default_cuota_mercado = float(datos_excel['info_general'].get('cuota_mercado', 10.0))
        default_clientes_objetivo = datos_excel['info_general'].get('clientes_objetivo', '')
"""
        lines.insert(i+1, new_defaults)
        print("✅ Agregados defaults para cuota_mercado y clientes_objetivo")
        break

# Agregar también en el else
for i in range(1472, 1485):
    if 'default_principales_riesgos = ""' in lines[i]:
        new_defaults = """        default_cuota_mercado = 10.0
        default_clientes_objetivo = ""
"""
        lines.insert(i+1, new_defaults)
        print("✅ Agregados defaults vacíos para cuota_mercado y clientes_objetivo")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Todos los campos estratégicos configurados")
