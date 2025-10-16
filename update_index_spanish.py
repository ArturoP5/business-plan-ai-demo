# Actualizar el índice del PDF en la sección de Documentos
with open('app.py', 'r') as f:
    content = f.read()

# Buscar y reemplazar en el índice
old_index = "- Executive Summary con Investment Thesis"
new_index = "- Resumen Ejecutivo con Tesis de Inversión"

content = content.replace(old_index, new_index)

# También actualizar otras menciones si existen
content = content.replace("Executive Summary", "Resumen Ejecutivo")
content = content.replace("Investment Thesis", "Tesis de Inversión")

with open('app.py', 'w') as f:
    f.write(content)

print("✅ Índice actualizado a español")
