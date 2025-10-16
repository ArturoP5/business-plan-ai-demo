#!/usr/bin/env python3
"""
Actualiza datos_guardados para usar los valores guardados en session_state
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se define datos_empresa en datos_guardados (alrededor de línea 4526)
for i in range(4525, 4545):
    if i >= len(lines):
        break
    
    if "'datos_empresa': {" in lines[i]:
        # Reemplazar con valores de session_state
        new_datos_empresa = """        'datos_empresa': {
            'nombre_empresa': nombre_empresa,
            'sector': sector,
            'descripcion_actividad': st.session_state.get('descripcion_actividad', ''),
            'productos_servicios': st.session_state.get('productos_servicios', ''),
            'modelo_negocio': st.session_state.get('modelo_negocio', ''),
            'posicionamiento_precio': st.session_state.get('posicionamiento_precio', ''),
            'competidores_principales': st.session_state.get('competidores_principales', ''),
            'vision_corto_plazo': st.session_state.get('vision_corto', ''),
            'vision_medio_plazo': st.session_state.get('vision_medio', ''),
            'vision_largo_plazo': st.session_state.get('vision_largo', ''),
            'ventaja_competitiva_principal': st.session_state.get('ventaja_competitiva_clave', ''),
            'principales_riesgos': st.session_state.get('principales_riesgos', ''),
            'cuota_mercado': st.session_state.get('cuota_mercado', 0),
            'clientes_objetivo': st.session_state.get('clientes_objetivo', '')
        },\n"""
        
        # Buscar el cierre del diccionario datos_empresa
        j = i
        brace_count = 1
        while j < i + 20 and brace_count > 0:
            j += 1
            if '{' in lines[j]:
                brace_count += 1
            if '},' in lines[j]:
                brace_count -= 1
        
        # Reemplazar todo el bloque
        lines[i:j+1] = [new_datos_empresa]
        print(f"✅ Actualizado datos_empresa para usar session_state en líneas {i+1}-{j+1}")
        break

# Guardar cambios
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ datos_guardados ahora usa valores de session_state")
