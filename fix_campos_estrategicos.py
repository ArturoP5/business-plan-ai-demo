#!/usr/bin/env python3
"""
Script para agregar valores por defecto a los campos estratégicos cuando se carga una empresa demo
"""

import re
from datetime import datetime

# Hacer backup
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

backup_name = f"app.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
with open(backup_name, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ Backup creado: {backup_name}")

# Buscar y reemplazar los campos estratégicos para agregar valores por defecto

# 1. Modelo de negocio
old_modelo = """            modelo_negocio = st.selectbox(
                "Modelo de Negocio",
                ["B2B - Venta a empresas", 
                 "B2C - Venta a consumidores",
                 "B2B2C - Mixto",
                 "SaaS - Software como servicio","""

new_modelo = """            modelo_negocio = st.selectbox(
                "Modelo de Negocio",
                ["B2B - Venta a empresas", 
                 "B2C - Venta a consumidores",
                 "B2B2C - Mixto",
                 "SaaS - Software como servicio","""

# Buscar el patrón completo del modelo_negocio
pattern = r'(modelo_negocio = st\.selectbox\(\s+"Modelo de Negocio",\s+\[[^\]]+\])'
replacement = r'\1,\n                value=datos_excel["info_general"].get("modelo_negocio", "B2C - Venta a consumidores") if datos_excel else "B2C - Venta a consumidores"'

content = re.sub(pattern, replacement, content)

# 2. Ventaja competitiva
pattern2 = r'(ventaja_competitiva_clave = st\.text_area\(\s+"Ventaja Competitiva Principal",)'
replacement2 = r'\1\n            value=datos_excel["info_general"].get("ventaja_competitiva_principal", "") if datos_excel else "",'

content = re.sub(pattern2, replacement2, content)

# 3. Buscar otros campos estratégicos y agregar valores por defecto
# Competidores principales
pattern3 = r'(competidores_principales = st\.text_area\(\s+"Principales Competidores",)'
replacement3 = r'\1\n            value=datos_excel["info_general"].get("competidores_principales", "") if datos_excel else "",'

content = re.sub(pattern3, replacement3, content)

# 4. Visiones
pattern4 = r'(vision_corto = st\.text_area\(\s+"Visión a Corto Plazo[^"]*",)'
replacement4 = r'\1\n            value=datos_excel["info_general"].get("vision_corto_plazo", "") if datos_excel else "",'

content = re.sub(pattern4, replacement4, content)

pattern5 = r'(vision_largo = st\.text_area\(\s+"Visión a Largo Plazo[^"]*",)'
replacement5 = r'\1\n            value=datos_excel["info_general"].get("vision_largo_plazo", "") if datos_excel else "",'

content = re.sub(pattern5, replacement5, content)

# Guardar el archivo modificado
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Campos estratégicos actualizados con valores por defecto")
print("\nCampos modificados:")
print("  - modelo_negocio")
print("  - ventaja_competitiva_clave")
print("  - competidores_principales")
print("  - vision_corto")
print("  - vision_largo")
print("\nAhora los campos estratégicos se cargarán automáticamente con las empresas demo")

