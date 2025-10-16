# Corregir problemas en las recomendaciones
with open('utils/pdf_mckinsey_generator.py', 'r') as f:
    content = f.read()

# 1. Eliminar caracteres problemáticos en la recomendación Industrial
old_industrial = 'El proyecto requiere либо mayor crecimiento de volumen, либо mejoras en eficiencia productiva para ser viable.'
new_industrial = 'El proyecto requiere mayor crecimiento de volumen o mejoras significativas en eficiencia productiva para ser viable.'

content = content.replace(old_industrial, new_industrial)

# 2. Asegurar que la lógica del sector se evalúa correctamente
# Verificar que datos_empresa se está usando bien
old_check = '            sector = datos_empresa.get(\'sector\', \'General\')'
new_check = '''            # Obtener sector de datos_empresa o resultado_mckinsey
            sector = datos_empresa.get('sector', 'General') if datos_empresa else 'General'
            if sector == 'General' and 'datos_empresa' in resultado_mckinsey:
                sector = resultado_mckinsey['datos_empresa'].get('sector', 'General')'''

content = content.replace(old_check, new_check)

with open('utils/pdf_mckinsey_generator.py', 'w') as f:
    f.write(content)

print("✅ Problemas de formato y lógica corregidos")
