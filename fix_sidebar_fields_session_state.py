#!/usr/bin/env python3
"""
Agrega keys de session_state a todos los campos del sidebar para que persistan
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar los campos en el expander de Descripción del Negocio (alrededor de línea 1594-1700)
fields_to_fix = [
    ('descripcion_actividad = st.text_area', 'key="descripcion_actividad"'),
    ('productos_servicios = st.text_area', 'key="productos_servicios"'),
    ('modelo_negocio = st.selectbox', 'key="modelo_negocio"'),
    ('posicionamiento_precio = st.selectbox', 'key="posicionamiento_precio"'),
    ('competidores_principales = st.text_area', 'key="competidores_principales"'),
    ('vision_corto = st.text_area', 'key="vision_corto"'),
    ('vision_medio = st.text_area', 'key="vision_medio"'),  
    ('vision_largo = st.text_area', 'key="vision_largo"'),
    ('ventaja_competitiva_clave = st.text_area', 'key="ventaja_competitiva_clave"'),
    ('principales_riesgos = st.text_area', 'key="principales_riesgos"'),
    ('cuota_mercado = st.number_input', 'key="cuota_mercado"'),
    ('clientes_objetivo = st.text_area', 'key="clientes_objetivo"')
]

for i in range(1590, 1750):
    if i >= len(lines):
        break
    
    for field_def, key_param in fields_to_fix:
        if field_def in lines[i] and 'key=' not in lines[i]:
            # Agregar key antes del cierre del paréntesis
            if ')' in lines[i]:
                lines[i] = lines[i].replace(')', f', {key_param})')
                print(f"✅ Agregado {key_param} en línea {i+1}")

# Guardar cambios
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Campos del sidebar ahora usan session_state con keys")
