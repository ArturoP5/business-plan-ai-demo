# Corregir la condición de Tecnología para que no dependa de margenes_expanden
with open('utils/pdf_mckinsey_generator.py', 'r') as f:
    content = f.read()

# Reemplazar la condición problemática
old_condition = """            if sector == "Tecnología" and margenes_expanden:
                
                explicacion_sector = f"Aunque los márgenes EBITDA se expanden (reflejando el alto apalancamiento operativo típico del sector), el tamaño limitado del mercado direccionable y la inversión inicial requerida no justifican el proyecto. La empresa necesita escalar significativamente su mercado potencial o reducir el capital inicial requerido.\""""

new_condition = """            if sector == "Tecnología":
                if margenes_expanden:
                    explicacion_sector = f"Aunque los márgenes EBITDA se expanden (reflejando el alto apalancamiento operativo del sector con 80% costos fijos), el tamaño limitado del mercado y la inversión inicial no justifican el proyecto. Se requiere escalar el mercado potencial o reducir el capital inicial."
                else:
                    explicacion_sector = f"Para un sector con estructura 80% costos fijos como Tecnología, el proyecto no genera suficiente escala para aprovechar el apalancamiento operativo. El tamaño del mercado o la inversión inicial limitan la viabilidad.\""""

content = content.replace(old_condition, new_condition)

with open('utils/pdf_mckinsey_generator.py', 'w') as f:
    f.write(content)

print("✅ Condición de Tecnología corregida para funcionar siempre")
