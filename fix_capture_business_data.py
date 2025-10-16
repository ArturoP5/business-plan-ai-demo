#!/usr/bin/env python3
"""
Captura todos los datos del expander Descripción del Negocio para el PDF con IA
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se guardan los datos_guardados (alrededor de línea 4515)
for i in range(4514, 4540):
    if "st.session_state.datos_guardados = {" in lines[i]:
        # Buscar donde está datos_empresa
        j = i
        while j < i + 30 and "'datos_empresa':" in lines[j]:
            # Reemplazar para capturar todos los campos del formulario
            lines[j] = """        'datos_empresa': {
            'nombre_empresa': nombre_empresa,
            'sector': sector,
            'descripcion_actividad': descripcion_actividad if 'descripcion_actividad' in locals() else '',
            'productos_servicios': productos_servicios if 'productos_servicios' in locals() else '',
            'modelo_negocio': modelo_negocio if 'modelo_negocio' in locals() else '',
            'posicionamiento_precio': posicionamiento_precio if 'posicionamiento_precio' in locals() else '',
            'competidores_principales': competidores_principales if 'competidores_principales' in locals() else '',
            'vision_corto_plazo': vision_corto if 'vision_corto' in locals() else '',
            'vision_medio_plazo': vision_medio if 'vision_medio' in locals() else '',
            'vision_largo_plazo': vision_largo if 'vision_largo' in locals() else '',
            'ventaja_competitiva_principal': ventaja_competitiva_clave if 'ventaja_competitiva_clave' in locals() else '',
            'principales_riesgos': principales_riesgos if 'principales_riesgos' in locals() else '',
            'cuota_mercado': cuota_mercado if 'cuota_mercado' in locals() else 0,
            'clientes_objetivo': clientes_objetivo if 'clientes_objetivo' in locals() else ''
        },\n"""
            print(f"✅ Actualizado datos_empresa completo en línea {j+1}")
            j += 1
            break
        break

# Guardar cambios
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Ruta completada: Descripción del Negocio → datos_guardados → PDF con IA")
