#!/usr/bin/env python3
"""
Arregla todos los problemas del PDF con IA:
1. Mapeo correcto de datos
2. Formato de tablas
3. Anexos financieros
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar y arreglar el mapeo de datos financieros (alrededor de línea 5345)
for i in range(5340, 5365):
    if "financial_data = {" in lines[i]:
        # Reemplazar las siguientes líneas con el mapeo correcto
        new_mapping = """                                            financial_data = {
                                                'enterprise_value': datos.get('resultado_mck', {}).get('enterprise_value', 0),
                                                'wacc': datos.get('resultado_mck', {}).get('wacc', 0),
                                                'tir': datos.get('resultado_mck', {}).get('tir_proyecto', 0),
                                                'payback': datos.get('resultado_mck', {}).get('payback_years', 0)
                                            }
"""
        # Reemplazar las 5 líneas del financial_data
        lines[i:i+6] = [new_mapping]
        print(f"✅ Corregido mapeo de datos financieros (línea {i+1})")
        break

# Buscar y corregir el mapeo del nombre de la empresa
for i in range(5340, 5365):
    if "'nombre_empresa': datos.get('datos_empresa', {}).get('nombre'," in lines[i]:
        lines[i] = "                                                'nombre_empresa': datos.get('datos_empresa', {}).get('nombre_empresa', datos.get('datos_empresa', {}).get('nombre', 'Empresa')),\n"
        print(f"✅ Corregido mapeo del nombre (línea {i+1})")
        break

# Guardar cambios en app.py
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Arreglados problemas de mapeo en app.py")

# Ahora arreglar las tablas en el PDF
with open('utils/pdf_ai_generator_completo.py', 'r') as f:
    pdf_lines = f.readlines()

# Aumentar tamaño de fuente en tablas (de 9 a 10)
for i in range(len(pdf_lines)):
    if "('FONTSIZE', (0, 0), (-1, -1), 9)" in pdf_lines[i]:
        pdf_lines[i] = pdf_lines[i].replace("9)", "10)")
        print(f"✅ Aumentado tamaño de fuente en línea {i+1}")

# Ajustar anchos de columnas para matriz de riesgos
for i in range(len(pdf_lines)):
    if "risk_table = Table(risk_table_data, colWidths=[4*cm, 2.5*cm, 2.5*cm, 7*cm])" in pdf_lines[i]:
        pdf_lines[i] = "        risk_table = Table(risk_table_data, colWidths=[5*cm, 2*cm, 2*cm, 7*cm])\n"
        print(f"✅ Ajustados anchos de columna de riesgos (línea {i+1})")
        break

# Guardar cambios en PDF
with open('utils/pdf_ai_generator_completo.py', 'w') as f:
    f.writelines(pdf_lines)

print("✅ Arreglados problemas de formato en PDF")
print("\nCambios aplicados:")
print("  - Mapeo corregido: resultado_mckinsey → resultado_mck")
print("  - Nombre de empresa: busca 'nombre_empresa' y 'nombre'")
print("  - Tamaño de fuente: 9 → 10")
print("  - Anchos de columna ajustados")
