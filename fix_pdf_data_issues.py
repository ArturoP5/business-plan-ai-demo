#!/usr/bin/env python3
"""
Arregla los problemas de datos en el PDF con IA
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se preparan los datos para el PDF (alrededor de línea 5345)
for i in range(5340, 5365):
    if "company_data = datos.get('datos_empresa', {})" in lines[i]:
        # Reemplazar con la forma correcta de obtener los datos
        lines[i] = """                                            # Preparar datos de la empresa correctamente
                                            company_data = {
                                                'nombre_empresa': datos.get('datos_empresa', {}).get('nombre', 'Empresa'),
                                                'sector': datos.get('datos_empresa', {}).get('sector', ''),
                                                'descripcion_actividad': datos.get('datos_empresa', {}).get('descripcion_actividad', ''),
                                                'productos_servicios': datos.get('datos_empresa', {}).get('productos_servicios', ''),
                                                'modelo_negocio': datos.get('datos_empresa', {}).get('modelo_negocio', ''),
                                                'competidores_principales': datos.get('datos_empresa', {}).get('competidores_principales', ''),
                                                'cuota_mercado': datos.get('datos_empresa', {}).get('cuota_mercado', 0),
                                                'vision_corto_plazo': datos.get('datos_empresa', {}).get('vision_corto', ''),
                                                'vision_medio_plazo': datos.get('datos_empresa', {}).get('vision_medio', ''),
                                                'vision_largo_plazo': datos.get('datos_empresa', {}).get('vision_largo', ''),
                                                'ventaja_competitiva_principal': datos.get('datos_empresa', {}).get('ventaja_competitiva_principal', ''),
                                                'principales_riesgos': datos.get('datos_empresa', {}).get('principales_riesgos', ''),
                                                'clientes_objetivo': datos.get('datos_empresa', {}).get('clientes_objetivo', '')
                                            }
"""
        print(f"✅ Arreglado mapeo de datos de empresa en línea {i+1}")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Problema de datos arreglado")
print("Ahora el PDF debería mostrar:")
print("  - Nombre correcto de la empresa")
print("  - Todos los campos estratégicos")
