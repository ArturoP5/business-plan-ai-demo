#!/usr/bin/env python3
"""
Corregir el parámetro value por index en selectbox
"""

import re
from datetime import datetime

# Hacer backup
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

backup_name = f"app.py.backup_selectbox_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
with open(backup_name, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ Backup creado: {backup_name}")

# Buscar el selectbox de modelo_negocio y quitar el parámetro value incorrecto
lines = content.split('\n')
new_lines = []
skip_next = False

for i, line in enumerate(lines):
    if skip_next:
        # Si la línea contiene 'value=' y estamos después de un selectbox, la saltamos
        if 'value=' in line and 'datos_excel' in line:
            skip_next = False
            continue
        else:
            skip_next = False
    
    if 'modelo_negocio = st.selectbox(' in line:
        skip_next = True
    
    new_lines.append(line)

content = '\n'.join(new_lines)

# Ahora agregar los valores por defecto correctamente usando el parámetro index
# Primero, buscar dónde está definido modelo_negocio
pattern = r'(modelo_negocio = st\.selectbox\(\s+"Modelo de Negocio",\s+(\[[^\]]+\])[^)]*\))'

def replace_selectbox(match):
    full_match = match.group(0)
    options_list = match.group(2)
    
    # Construir el nuevo selectbox con index
    new_selectbox = f"""modelo_negocio = st.selectbox(
                "Modelo de Negocio",
                {options_list},
                index={options_list}.index(datos_excel["info_general"].get("modelo_negocio", "B2C - Venta a consumidores")) if datos_excel and datos_excel["info_general"].get("modelo_negocio") in {options_list} else 1,
                help="Seleccione el modelo de negocio principal"
            )"""
    
    return new_selectbox

content = re.sub(pattern, replace_selectbox, content, flags=re.DOTALL)

# Para text_area, sí usa value, así que lo dejamos pero corregimos la sintaxis
# Corregir ventaja_competitiva_clave
pattern2 = r'(ventaja_competitiva_clave = st\.text_area\(\s+"Ventaja Competitiva Principal",)'
replacement2 = r'\1\n            value=datos_excel["info_general"].get("ventaja_competitiva_principal", "") if datos_excel else "",'

content = re.sub(pattern2, replacement2, content)

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Corregido el parámetro de selectbox")
print("✅ Ahora usa 'index' en lugar de 'value' para selectbox")

