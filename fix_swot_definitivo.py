#!/usr/bin/env python3
"""
Arregla definitivamente el problema del método SWOT
"""

with open('utils/pdf_ai_generator_completo.py', 'r') as f:
    lines = f.readlines()

# 1. Cambiar la llamada incorrecta en línea 76
for i in range(75, 78):
    if '_create_swot_ai' in lines[i]:
        lines[i] = lines[i].replace('_create_swot_ai', '_create_swot_analysis')
        print(f"✅ Corregida llamada al método en línea {i+1}")
        break

# 2. Agregar el método _create_swot_analysis si no existe
# Buscar si ya existe
method_exists = False
for line in lines:
    if 'def _create_swot_analysis' in line:
        method_exists = True
        break

if not method_exists:
    # Buscar donde agregarlo (después de _create_executive_summary)
    for i in range(len(lines)):
        if 'def _create_executive_summary' in lines[i]:
            # Buscar el final de este método
            indent_count = 0
            for j in range(i+1, len(lines)):
                if 'return elements' in lines[j]:
                    # Agregar el método SWOT después
                    swot_method = '''    
    def _create_swot_analysis(self, swot_data):
        """Crea la sección SWOT con datos de IA"""
        elements = []
        
        title = Paragraph("ANÁLISIS SWOT", self.styles['SectionTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        if swot_data and not swot_data.get('fallback'):
            # Crear tabla SWOT 2x2
            data = [
                [Paragraph("<b>FORTALEZAS</b>", self.styles['Normal']),
                 Paragraph("<b>DEBILIDADES</b>", self.styles['Normal'])],
                [self._format_list(swot_data.get('fortalezas', [])),
                 self._format_list(swot_data.get('debilidades', []))],
                [Paragraph("<b>OPORTUNIDADES</b>", self.styles['Normal']),
                 Paragraph("<b>AMENAZAS</b>", self.styles['Normal'])],
                [self._format_list(swot_data.get('oportunidades', [])),
                 self._format_list(swot_data.get('amenazas', []))]
            ]
            
            table = Table(data, colWidths=[8*cm, 8*cm])
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e6f2ff')),
                ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e6f2ff')),
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("Análisis SWOT no disponible", self.styles['Normal']))
        
        return elements
    
    def _format_list(self, items):
        """Formatea una lista para el PDF"""
        if not items:
            return Paragraph("—", self.styles['Normal'])
        
        text = "<br/>".join([f"• {item}" for item in items[:5]])  # Máximo 5 items
        return Paragraph(text, self.styles['Normal'])

'''
                    lines.insert(j+1, swot_method)
                    print(f"✅ Método _create_swot_analysis agregado después de línea {j+1}")
                    break
            break

# Guardar
with open('utils/pdf_ai_generator_completo.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Problema SWOT arreglado completamente")
