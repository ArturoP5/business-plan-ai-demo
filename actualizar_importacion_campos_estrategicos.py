# Actualizar la función de importación para los nuevos campos

with open('utils/importar_excel_definitivo.py', 'r') as f:
    lines = f.readlines()

# Buscar donde se procesan los campos de info_general
for i, line in enumerate(lines):
    if "'moneda': str(info_dict.get('Moneda', 'EUR'))," in line:
        # Insertar los nuevos campos después de moneda
        nuevos_campos = '''            'modelo_negocio': str(info_dict.get('Modelo de Negocio', '')),
            'posicionamiento_precio': str(info_dict.get('Posicionamiento Precio', '')),
            'competidores_top3': str(info_dict.get('Top 3 Competidores', '')),
            'vision_corto_plazo': str(info_dict.get('Visión Corto Plazo (1 año)', '')),
            'vision_medio_plazo': str(info_dict.get('Visión Medio Plazo (3 años)', '')),
            'vision_largo_plazo': str(info_dict.get('Visión Largo Plazo (5+ años)', '')),
            'ventaja_competitiva_principal': str(info_dict.get('Ventaja Competitiva Principal', '')),
            'principales_riesgos': str(info_dict.get('Principales Riesgos', '')),
'''
        lines[i] = lines[i] + nuevos_campos
        break

# Guardar
with open('utils/importar_excel_definitivo.py', 'w') as f:
    f.writelines(lines)

print("✅ Función de importación actualizada con campos estratégicos")
