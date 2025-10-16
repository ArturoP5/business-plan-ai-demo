#!/usr/bin/env python3
"""
Arreglar los estilos faltantes en el PDF
"""

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar dónde se definen los estilos
styles_found = False
for i in range(len(lines)):
    if "getSampleStyleSheet()" in lines[i]:
        print(f"Encontrada definición de estilos en línea {i+1}")
        styles_found = True
        
        # Buscar si ya hay estilos personalizados
        custom_styles_exist = False
        for j in range(i, min(i+50, len(lines))):
            if "styles.add" in lines[j] or "ParagraphStyle" in lines[j]:
                custom_styles_exist = True
                break
        
        if not custom_styles_exist:
            # Agregar definiciones de estilos personalizados
            styles_code = """
    # Agregar estilos personalizados
    styles.add(ParagraphStyle(
        name='Titulo',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a5f'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='Seccion',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e3a5f'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='Subseccion',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    ))
    
"""
            # Insertar después de getSampleStyleSheet()
            lines.insert(i+1, styles_code)
            print("✅ Agregados estilos personalizados")
        break

# También verificar que los imports necesarios estén presentes
imports_needed = [
    "from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle",
    "from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY"
]

for imp in imports_needed:
    found = False
    for line in lines[:50]:  # Buscar en las primeras 50 líneas
        if imp.split('import')[1].strip() in line:
            found = True
            break
    if not found:
        # Agregar el import al inicio
        lines.insert(2, imp + "\n")
        print(f"✅ Agregado import: {imp}")

# Guardar cambios
with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Estilos del PDF arreglados")

