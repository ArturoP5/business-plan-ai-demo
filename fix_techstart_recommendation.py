# Simplificar la lógica de recomendaciones para que funcione correctamente
with open('utils/pdf_mckinsey_generator.py', 'r') as f:
    content = f.read()

# Primero, eliminar los debugs que agregamos
content = content.replace('print(f"DEBUG: Sector={sector}, Margenes expanden={margenes_expanden}")', '')
content = content.replace('print(f"DEBUG PDF: Sector detectado = {sector}")', '')

# Ahora, simplificar la condición para Tecnología
old_tech_condition = '''if sector == "Tecnología" and margenes_expanden:
                explicacion_sector = f"Aunque los márgenes EBITDA se expanden (reflejando el alto apalancamiento operativo típico del sector), el tamaño limitado del mercado direccionable y la inversión inicial requerida no justifican el proyecto. La empresa necesita escalar significativamente su mercado potencial o reducir el capital inicial requerido."'''

new_tech_condition = '''if sector == "Tecnología":
                # Para tecnología, verificar si los márgenes expanden
                if margenes_expanden:
                    explicacion_sector = f"Aunque los márgenes EBITDA se expanden (reflejando el alto apalancamiento operativo del sector con 80% costos fijos), el tamaño limitado del mercado y la inversión inicial no justifican el proyecto. Se requiere escalar el mercado potencial o reducir el capital inicial."
                else:
                    explicacion_sector = f"El sector tecnológico típicamente muestra alto apalancamiento operativo, pero este proyecto no captura ese potencial. La estructura de 80% costos fijos requiere mayor escala para ser viable."'''

content = content.replace(old_tech_condition, new_tech_condition)

with open('utils/pdf_mckinsey_generator.py', 'w') as f:
    f.write(content)

print("✅ Lógica de TechStart simplificada")
