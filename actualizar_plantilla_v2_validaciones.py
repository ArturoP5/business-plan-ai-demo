# Agregar al final de utils/plantilla_excel_v2.py
import re

# Buscar el archivo y agregar las importaciones necesarias
with open('utils/plantilla_excel_v2.py', 'r') as f:
    content = f.read()

# Verificar si ya tiene la importación de DataValidation
if 'from openpyxl.worksheet.datavalidation import DataValidation' not in content:
    # Agregar la importación después de las otras importaciones de openpyxl
    content = content.replace(
        'from openpyxl.styles import PatternFill, Font, Alignment, Border, Side',
        'from openpyxl.styles import PatternFill, Font, Alignment, Border, Side\nfrom openpyxl.worksheet.datavalidation import DataValidation'
    )

# Buscar donde se crea la hoja Info_General y agregar validaciones
# Esto requiere encontrar el lugar exacto en el código
marker = 'ws = wb.create_sheet("Info_General")'
if marker in content:
    # Insertar código para validaciones después de crear los datos
    validation_code = '''
    # Agregar validaciones de datos (listas desplegables)
    dv_sector = DataValidation(type="list", 
                              formula1='"Tecnología,Hostelería,Ecommerce,Consultoría,Retail,Servicios,Automoción,Industrial,Otro"',
                              allow_blank=False)
    dv_sector.add(ws['B3'])
    
    dv_si_no = DataValidation(type="list", formula1='"Sí,No"', allow_blank=False)
    dv_si_no.add(ws['B6'])
    dv_si_no.add(ws['B7'])
    
    dv_moneda = DataValidation(type="list", formula1='"EUR,USD,GBP"', allow_blank=False)
    dv_moneda.add(ws['B8'])
    
    ws.add_data_validation(dv_sector)
    ws.add_data_validation(dv_si_no)
    ws.add_data_validation(dv_moneda)
'''
    # Encontrar dónde insertar (después de los append de Info_General)
    insert_pos = content.find('ws.append(row)')
    insert_pos = content.find('\n    \n', insert_pos) # Buscar línea vacía después
    if insert_pos > 0:
        content = content[:insert_pos] + validation_code + content[insert_pos:]

# Guardar
with open('utils/plantilla_excel_v2_con_validaciones.py', 'w') as f:
    f.write(content)

print("✅ Código de validaciones preparado")
