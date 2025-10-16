# Leer el archivo problemático
with open('utils/importar_excel_definitivo.py', 'r') as f:
    content = f.read()

# Buscar y reemplazar la sección problemática
old_text = "'leasing_plazo_meses': 60,  # Valor por defecto 60 meses            'leasing_total': float(pasivo_dict.get('Leasing - Importe total', 0)),"
new_text = "'leasing_plazo_meses': 60,  # Valor por defecto 60 meses\n            'leasing_total': float(pasivo_dict.get('Leasing - Importe total', 0)),"

content = content.replace(old_text, new_text)

# Arreglar las otras líneas pegadas
content = content.replace('0)),            ', '0)),\n            ')

# Guardar
with open('utils/importar_excel_definitivo.py', 'w') as f:
    f.write(content)

print("✅ Archivo arreglado")
