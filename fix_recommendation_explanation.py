# Mejorar la recomendación para explicar la paradoja ROIC vs TIR
with open('utils/pdf_mckinsey_generator.py', 'r') as f:
    content = f.read()

# Buscar y reemplazar la sección de recomendación
old_recommendation = """    if tir > wacc:
        recomendacion = f"✅ PROYECTO VIABLE: Con TIR {tir:.1f}% superior al WACC {wacc:.1f}%, el proyecto genera valor para los accionistas. El ROIC promedio de {roic:.1f}% confirma la capacidad de creación de valor sostenible."
    elif tir > wacc * 0.9:  # Dentro del 10% del WACC
        recomendacion = f"⚠️ PROYECTO MARGINAL: TIR {tir:.1f}% muy cerca del WACC {wacc:.1f}%. Se requiere optimización de márgenes operativos o revisión de la estructura de costes para mejorar la viabilidad del proyecto."
    else:
        recomendacion = f"❌ PROYECTO NO VIABLE: TIR {tir:.1f}% inferior al WACC {wacc:.1f}%. El proyecto destruye valor en las condiciones actuales. NO se recomienda proceder sin cambios estructurales significativos en el modelo de negocio.\""""

new_recommendation = """    if tir > wacc:
        recomendacion = f"✅ PROYECTO VIABLE: Con TIR {tir:.1f}% superior al WACC {wacc:.1f}%, el proyecto genera valor para los accionistas. El ROIC promedio de {roic:.1f}% confirma la capacidad de creación de valor sostenible."
    elif tir > wacc * 0.9:  # Dentro del 10% del WACC
        recomendacion = f"⚠️ PROYECTO MARGINAL: TIR {tir:.1f}% muy cerca del WACC {wacc:.1f}%. Se requiere optimización de márgenes operativos o revisión de la estructura de costes para mejorar la viabilidad del proyecto."
    else:
        # Explicar la paradoja ROIC alto pero TIR baja
        if roic > wacc:
            recomendacion = f"❌ PROYECTO NO VIABLE (Paradoja Financiera): Aunque el ROIC operativo ({roic:.1f}%) supera al WACC ({wacc:.1f}%), indicando eficiencia operativa, la TIR del proyecto ({tir:.1f}%) es inferior al coste de capital. Esta divergencia se explica por: (1) Alto capital inicial requerido, (2) Crecimiento insuficiente para justificar la inversión, (3) Valor terminal limitado. La empresa es operativamente eficiente pero el proyecto total no genera suficiente valor presente neto. NO se recomienda proceder sin revisar el modelo de crecimiento o reducir la inversión inicial."
        else:
            recomendacion = f"❌ PROYECTO NO VIABLE: TIR {tir:.1f}% inferior al WACC {wacc:.1f}%. El proyecto destruye valor en las condiciones actuales. NO se recomienda proceder sin cambios estructurales significativos.\""""

content = content.replace(old_recommendation, new_recommendation)

with open('utils/pdf_mckinsey_generator.py', 'w') as f:
    f.write(content)

print("Recomendación mejorada con explicación de la paradoja ROIC vs TIR")
