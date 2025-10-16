# Crear recomendación completa que maneje todos los casos ROIC vs TIR vs WACC
with open('utils/pdf_mckinsey_generator.py', 'r') as f:
    content = f.read()

# Buscar la sección de recomendación actual
old_section_start = "    # Generar recomendación basada en métricas reales"
old_section_end = "    elementos.append(Paragraph(recomendacion, styles['TextoNormal']))"

# Nueva lógica completa
new_recommendation_logic = '''    # Generar recomendación basada en métricas reales
    tir = resultado_mckinsey.get('tir', 0)
    wacc = resultado_mckinsey.get('wacc', 0)
    roic = resultado_mckinsey.get('roic_promedio', 0)
    
    # Análisis completo de todas las combinaciones
    if tir > wacc:
        if roic > wacc:
            # Caso ideal: Todo positivo
            recomendacion = f"✅ PROYECTO VIABLE (Escenario Óptimo): TIR {tir:.1f}% > WACC {wacc:.1f}% y ROIC {roic:.1f}% > WACC. El proyecto genera valor tanto a nivel operativo como de inversión total. Recomendación: PROCEDER con la inversión."
        else:
            # TIR buena pero ROIC bajo (raro pero posible)
            recomendacion = f"⚠️ PROYECTO VIABLE CON RIESGOS: Aunque la TIR {tir:.1f}% supera al WACC {wacc:.1f}%, el ROIC operativo {roic:.1f}% es inferior al coste de capital. Esto sugiere que el valor viene principalmente del crecimiento o valor terminal, no de la eficiencia operativa actual. Riesgo: Dependencia excesiva de proyecciones futuras. Recomendación: PROCEDER CON CAUTELA y monitorear eficiencia operativa."
    
    elif tir > wacc * 0.9:  # TIR marginal (dentro del 10% del WACC)
        if roic > wacc:
            recomendacion = f"⚠️ PROYECTO MARGINAL: TIR {tir:.1f}% cercana al WACC {wacc:.1f}%. Aunque el ROIC {roic:.1f}% indica buena eficiencia operativa, el retorno total es ajustado. Recomendación: OPTIMIZAR estructura de capital y costes antes de proceder."
        else:
            recomendacion = f"❌ PROYECTO DÉBIL: TIR {tir:.1f}% y ROIC {roic:.1f}% ambos cercanos o inferiores al WACC {wacc:.1f}%. Señales de alerta en eficiencia y retorno. Recomendación: REPLANTEAR el modelo de negocio."
    
    else:  # TIR < WACC * 0.9
        if roic > wacc:
            # La paradoja que mencionaste
            recomendacion = f"❌ PROYECTO NO VIABLE (Paradoja ROIC vs TIR): El ROIC operativo ({roic:.1f}%) supera al WACC ({wacc:.1f}%), indicando eficiencia operativa actual. Sin embargo, la TIR del proyecto ({tir:.1f}%) es significativamente inferior al coste de capital. Esta divergencia indica: (1) Inversión inicial excesiva para los flujos generados, (2) Crecimiento insuficiente para justificar el capital requerido, (3) Deterioro esperado de márgenes en el tiempo. La eficiencia operativa actual no compensa el bajo retorno total del proyecto. Recomendación: NO PROCEDER sin reestructuración significativa del plan de inversión."
        else:
            # Ambos malos
            recomendacion = f"❌ PROYECTO NO VIABLE: Tanto la TIR ({tir:.1f}%) como el ROIC ({roic:.1f}%) son inferiores al WACC ({wacc:.1f}%). El proyecto destruye valor tanto operativa como financieramente. Recomendación: NO PROCEDER - buscar alternativas de inversión."
    
    # Si hay recomendación de la IA, agregarla como contexto adicional
    recomendacion_ia = analisis_ia.get('recomendacion_principal', '')
    if recomendacion_ia and not any(x in recomendacion_ia.lower() for x in ['atractivo', 'viable', 'proceder']):
        recomendacion = recomendacion + "\\n\\n" + recomendacion_ia
    
    elementos.append(Paragraph(recomendacion, styles['TextoNormal']))'''

# Encontrar y reemplazar la sección
import re
pattern = re.compile(
    re.escape(old_section_start) + ".*?" + re.escape(old_section_end),
    re.DOTALL
)
content = pattern.sub(new_recommendation_logic, content)

with open('utils/pdf_mckinsey_generator.py', 'w') as f:
    f.write(content)

print("Lógica de recomendación actualizada para cubrir TODOS los casos posibles")
