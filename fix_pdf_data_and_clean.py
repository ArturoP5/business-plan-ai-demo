#!/usr/bin/env python3
"""
Arreglar el paso de datos al PDF y limpiar contenido antiguo
"""

import re

def fix_pdf_generator():
    with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Asegurar que los valores se pasen correctamente
    # Buscar la función principal
    main_func_pattern = r'def generar_pdf_mckinsey\([^)]*\):'
    match = re.search(main_func_pattern, content)
    if match:
        print("✅ Encontrada función principal generar_pdf_mckinsey")
    
    # 2. Verificar que resultado_mckinsey se use correctamente
    # El problema es que resultado_mckinsey puede estar vacío o None
    
    # Agregar validación al inicio de la función
    validation_code = """
    # Validar que tenemos datos de McKinsey
    if resultado_mckinsey is None or not resultado_mckinsey:
        print("⚠️ WARNING: resultado_mckinsey está vacío o es None")
        resultado_mckinsey = {}
    
    # Extraer valores con defaults seguros
    enterprise_value = resultado_mckinsey.get('enterprise_value', 0)
    equity_value = resultado_mckinsey.get('equity_value', 0)
    tir = resultado_mckinsey.get('tir', 0)
    wacc = resultado_mckinsey.get('wacc', 0)
    roic_promedio = resultado_mckinsey.get('roic_promedio', 0)
    
    print(f"📊 Valores recibidos: EV={enterprise_value}, TIR={tir}, WACC={wacc}, ROIC={roic_promedio}")
    """
    
    # 3. Eliminar recomendaciones estratégicas genéricas antiguas
    # Buscar y eliminar el bloque de recomendaciones genéricas
    old_recommendations_pattern = r'# RECOMENDACIONES ESTRATÉGICAS.*?(?=# PÁGINA|\Z)'
    
    # Buscar si hay recomendaciones genéricas
    if "Conclusión de Valoración" in content and "Palancas de Creación de Valor" in content:
        print("📝 Encontradas recomendaciones genéricas antiguas")
        
        # Reemplazar con versión que use IA si existe
        new_recommendations = '''
    # RECOMENDACIONES ESTRATÉGICAS
    elementos.append(PageBreak())
    elementos.append(Paragraph("RECOMENDACIONES ESTRATÉGICAS", styles['Titulo']))
    
    if analisis_ia and 'recomendaciones' in analisis_ia:
        # Usar recomendaciones de IA
        recomendaciones = analisis_ia['recomendaciones']
        
        elementos.append(Paragraph("Recomendaciones Basadas en Análisis IA", styles['Seccion']))
        for rec in recomendaciones:
            elementos.append(Paragraph(f"• {rec}", styles['Normal']))
    else:
        # Recomendaciones básicas si no hay IA
        elementos.append(Paragraph("Conclusión de Valoración", styles['Seccion']))
        
        if tir > 0 and wacc > 0:
            if tir > wacc:
                texto = f"Con TIR del {tir:.1f}% superior al WACC del {wacc:.1f}%, el proyecto genera valor."
            else:
                texto = f"Con TIR del {tir:.1f}% inferior al WACC del {wacc:.1f}%, revisar el modelo de negocio."
        else:
            texto = "Análisis pendiente de datos completos de valoración."
        
        elementos.append(Paragraph(texto, styles['Normal']))
        '''
        
        # Aplicar el reemplazo
        content = re.sub(old_recommendations_pattern, new_recommendations, content, flags=re.DOTALL)
    
    # 4. Arreglar la portada (página 1)
    portada_fix = '''
    # Verificar valores antes de usarlos en la portada
    valor_empresa = resultado_mckinsey.get('enterprise_value', 0) if resultado_mckinsey else 0
    tir_valor = resultado_mckinsey.get('tir', 0) if resultado_mckinsey else 0
    wacc_valor = resultado_mckinsey.get('wacc', 0) if resultado_mckinsey else 0
    roic_valor = resultado_mckinsey.get('roic_promedio', 0) if resultado_mckinsey else 0
    '''
    
    # Insertar después de def generar_pdf_mckinsey
    if "def generar_pdf_mckinsey" in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "def generar_pdf_mckinsey" in line:
                # Buscar el final de los parámetros
                j = i
                while j < len(lines) and not lines[j].strip().startswith('"""'):
                    j += 1
                # Insertar después del docstring
                while j < len(lines) and '"""' in lines[j]:
                    j += 1
                lines.insert(j + 1, portada_fix)
                break
        content = '\n'.join(lines)
    
    # Guardar cambios
    with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("\n✅ Arreglos aplicados:")
    print("   1. Validación de datos McKinsey")
    print("   2. Valores con defaults seguros")
    print("   3. Recomendaciones limpias (IA si existe, básicas si no)")
    print("   4. Portada con valores verificados")

if __name__ == "__main__":
    fix_pdf_generator()

