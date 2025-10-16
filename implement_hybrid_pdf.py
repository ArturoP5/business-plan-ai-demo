#!/usr/bin/env python3
"""
Implementar la estructura híbrida del PDF
"""

def create_hybrid_structure():
    with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    print("📝 Analizando estructura actual...")
    
    # Encontrar las secciones clave
    swot_page8_start = -1
    swot_page8_end = -1
    proyecciones_start = -1
    recomendaciones_start = -1
    
    for i, line in enumerate(lines):
        if "# PÁGINA 8: SWOT" in line or "Análisis SWOT" in line and swot_page8_start == -1:
            swot_page8_start = i
            print(f"  - SWOT página 8 encontrado en línea {i+1}")
        elif swot_page8_start > 0 and swot_page8_end == -1 and "# PÁGINA 9" in line:
            swot_page8_end = i
            print(f"  - SWOT página 8 termina en línea {i}")
        elif "# PROYECCIONES DETALLADAS - AÑO 1" in line:
            proyecciones_start = i
            print(f"  - Proyecciones detalladas en línea {i+1}")
        elif "# RECOMENDACIONES ESTRATÉGICAS" in line:
            recomendaciones_start = i
            print(f"  - Recomendaciones en línea {i+1}")
    
    # Crear la nueva estructura
    new_lines = []
    i = 0
    
    while i < len(lines):
        # Saltar el SWOT de página 8
        if i >= swot_page8_start and i < swot_page8_end and swot_page8_start > 0:
            print(f"  ⏭️ Saltando SWOT de página 8 (líneas {swot_page8_start+1}-{swot_page8_end})")
            i = swot_page8_end
            continue
        
        # Agregar balance después de cada P&L anual
        if "# PROYECCIONES DETALLADAS - AÑO" in lines[i]:
            año = lines[i].split("AÑO")[1].strip()
            print(f"  📊 Procesando Año {año}")
            
            # Agregar P&L
            j = i
            while j < len(lines) and "# PROYECCIONES DETALLADAS - AÑO" not in lines[j+1] and "# RECOMENDACIONES" not in lines[j]:
                new_lines.append(lines[j])
                j += 1
            
            # Agregar código para el Balance
            balance_code = f'''
    # Balance Proyectado Año {año}
    elementos.append(PageBreak())
    elementos.append(Paragraph(f"Balance General Proyectado - Año {año}", styles['Seccion']))
    
    if 'balance_df' in locals() and balance_df is not None:
        # Aquí iría la tabla del balance para el año {año}
        balance_data = [
            ['ACTIVO', '', 'PASIVO Y PATRIMONIO', ''],
            ['Activo Corriente', f'€XXX', 'Pasivo Corriente', f'€XXX'],
            ['Activo No Corriente', f'€XXX', 'Pasivo No Corriente', f'€XXX'],
            ['', '', 'Patrimonio Neto', f'€XXX'],
            ['TOTAL ACTIVO', f'€XXX', 'TOTAL PASIVO + PN', f'€XXX']
        ]
        
        balance_table = Table(balance_data, colWidths=[3*inch, 1.5*inch, 3*inch, 1.5*inch])
        balance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
        ]))
        elementos.append(balance_table)
    
'''
            new_lines.append(balance_code)
            i = j + 1
            continue
            
        # Insertar SWOT con IA después del último año
        if i == recomendaciones_start - 1:
            swot_ia_code = '''
    # SWOT - Usando IA si está disponible
    elementos.append(PageBreak())
    elementos.append(Paragraph("ANÁLISIS SWOT", styles['Titulo']))
    
    if analisis_ia and 'swot' in analisis_ia:
        # Usar SWOT de IA
        swot_data = analisis_ia['swot']
        # Código para generar SWOT de IA
    else:
        # Usar SWOT genérico
        # Código del SWOT original
    
'''
            new_lines.append(swot_ia_code)
        
        new_lines.append(lines[i])
        i += 1
    
    # Guardar el archivo modificado
    with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print("\n✅ Estructura híbrida implementada")
    return True

if __name__ == "__main__":
    create_hybrid_structure()

