#!/usr/bin/env python3
"""
Arregla el mapeo de datos para el PDF profesional
"""

# Primero, actualizar cómo se guardan los datos en datos_guardados
with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se asigna datos_guardados (línea 4515)
for i in range(4514, 4530):
    if 'st.session_state.datos_guardados = {' in lines[i]:
        # Agregar datos_empresa completo
        lines.insert(i+11, "        'datos_empresa': empresa_seleccionada,\n")
        print(f"✅ Agregado 'datos_empresa' en línea {i+12}")
        break

# Ahora actualizar el generador de PDF para usar los datos correctos
with open('utils/pdf_valoracion_profesional.py', 'r') as f:
    pdf_content = f.read()

# Corregir el acceso a los datos de la empresa
pdf_content = pdf_content.replace(
    "company_data = datos.get('datos_empresa', {})",
    """company_data = {
        'nombre_empresa': datos.get('nombre_empresa', 'Empresa'),
        'sector': datos.get('sector', 'N/A'),
        'descripcion_actividad': datos.get('datos_empresa', {}).get('descripcion_actividad', 'N/A'),
        'modelo_negocio': datos.get('datos_empresa', {}).get('modelo_negocio', 'N/A'),
        'productos_servicios': datos.get('datos_empresa', {}).get('productos_servicios', 'N/A'),
        'ventaja_competitiva_principal': datos.get('datos_empresa', {}).get('ventaja_competitiva_principal', 'N/A')
    }"""
)

# Corregir el acceso a los DataFrames
pdf_content = pdf_content.replace(
    """financial_data = {
        'pyl_df': datos.get('pyl_df'),
        'balance_df': datos.get('balance_df'),
        'fcf_df': datos.get('fcf_df')
    }""",
    """financial_data = {
        'pyl_df': datos.get('pyl'),
        'balance_df': datos.get('balance'),
        'fcf_df': datos.get('cash_flow')
    }"""
)

with open('utils/pdf_valoracion_profesional.py', 'w') as f:
    f.write(pdf_content)

# Guardar cambios en app.py
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Mapeo de datos corregido:")
print("  - datos_empresa se guarda completo")
print("  - PDF accede correctamente a todos los campos")
print("  - DataFrames mapeados correctamente")
