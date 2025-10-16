# Insertar análisis del P&L en el lugar correcto
with open('utils/pdf_mckinsey_generator.py', 'r') as f:
    lines = f.readlines()

# Buscar la línea donde termina la tabla P&L (alrededor de línea 1225)
insert_position = -1
for i, line in enumerate(lines):
    if i > 1220 and i < 1230 and 'elementos.append(tabla_pyl)' in line:
        insert_position = i + 1
        break

if insert_position > 0:
    # Código del análisis a insertar
    analysis_code = '''        
        # Análisis profesional del P&L
        elementos.append(Spacer(1, 0.3*inch))
        elementos.append(Paragraph("Análisis de la Evolución Financiera", styles['Seccion']))
        
        # Calcular métricas para análisis
        if len(pyl_df) >= 5:
            cagr_ventas = ((pyl_df['Ventas'].iloc[4] / pyl_df['Ventas'].iloc[0]) ** 0.25 - 1) * 100
            margen_ebitda_inicial = (pyl_df['EBITDA'].iloc[0] / pyl_df['Ventas'].iloc[0]) * 100
            margen_ebitda_final = (pyl_df['EBITDA'].iloc[4] / pyl_df['Ventas'].iloc[4]) * 100
            delta_margen = margen_ebitda_final - margen_ebitda_inicial
            
            # Determinar tendencia
            if delta_margen > 1:
                tendencia = "expansión de márgenes"
                explicacion = "reflejando economías de escala y mejoras operativas"
            elif delta_margen < -1:
                tendencia = "compresión de márgenes"
                explicacion = "indicando presión competitiva o incremento en costos"
            else:
                tendencia = "estabilidad en márgenes"
                explicacion = "mostrando equilibrio entre crecimiento y estructura de costos"
            
            analisis_text = f"""Las proyecciones muestran un crecimiento compuesto anual (CAGR) del {cagr_ventas:.1f}% en ventas, 
            con {tendencia} EBITDA desde {margen_ebitda_inicial:.1f}% hasta {margen_ebitda_final:.1f}%, {explicacion}.
            
            El modelo aplica premisas sectoriales específicas considerando la estructura de costos típica del sector, 
            el grado de madurez de la empresa, y las expectativas macroeconómicas. Los gastos operativos se proyectan 
            según la proporción variable/fija característica del sector, mientras que el crecimiento incorpora tanto 
            factores orgánicos como ajustes por inflación y ciclo económico."""
            
            elementos.append(Paragraph(analisis_text, styles['TextoNormal']))
        
'''
    
    # Insertar el código
    lines.insert(insert_position, analysis_code)
    
    with open('utils/pdf_mckinsey_generator.py', 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Análisis del P&L insertado en línea {insert_position}")
else:
    print("❌ No se encontró el lugar para insertar")
