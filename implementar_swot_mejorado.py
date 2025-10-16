# Implementar el SWOT mejorado en el generador PDF

with open('utils/pdf_mckinsey_generator.py', 'r') as f:
    lines = f.readlines()

# Buscar donde empieza el análisis SWOT (después de obtener métricas)
for i, line in enumerate(lines):
    if '# Generar SWOT basado en datos reales' in line:
        # Insertar código para usar campos estratégicos
        codigo_nuevo = '''    # Usar campos estratégicos si están disponibles
    if campos_estrategicos and isinstance(campos_estrategicos, dict):
        ventaja_competitiva = campos_estrategicos.get('ventaja_competitiva', '')
        principales_riesgos = campos_estrategicos.get('riesgos', '')
        vision_corto = campos_estrategicos.get('vision_corto', '')
        competidores = campos_estrategicos.get('competidores', '')
    else:
        ventaja_competitiva = ''
        principales_riesgos = ''
        vision_corto = ''
        competidores = ''
    
'''
        lines.insert(i+1, codigo_nuevo)
        print(f"✅ Código de campos estratégicos insertado en línea {i+1}")
        break

# Ahora mejorar las fortalezas con ventaja competitiva
for i, line in enumerate(lines):
    if 'fortalezas.append("• Experiencia consolidada en el sector")' in line:
        # Agregar ventaja competitiva si existe
        nuevo = '''    # Agregar ventaja competitiva si está disponible
    if ventaja_competitiva:
        fortalezas.insert(0, f"• {ventaja_competitiva[:100]}")
    
'''
        lines.insert(i, nuevo)
        print(f"✅ Ventaja competitiva agregada a fortalezas en línea {i}")
        break

# Guardar
with open('utils/pdf_mckinsey_generator.py', 'w') as f:
    f.writelines(lines)
