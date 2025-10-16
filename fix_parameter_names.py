#!/usr/bin/env python3
"""
Arreglar la duplicación de parámetros y unificar nombres
"""

# Primero arreglar el generador PDF
with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    content = f.read()

# Eliminar el parámetro duplicado ai_analysis=None)
content = content.replace(", ai_analysis=None)", ")")

# Ya tiene analisis_ia, así que vamos a usar ese nombre consistentemente
# Cambiar las referencias de ai_analysis a analisis_ia dentro del código nuevo
content = content.replace("if ai_analysis and len(ai_analysis) > 0:", "if analisis_ia and len(analisis_ia) > 0:")
content = content.replace("if 'swot' in ai_analysis and ai_analysis['swot']:", "if 'swot' in analisis_ia and analisis_ia['swot']:")
content = content.replace("swot_data = ai_analysis['swot']", "swot_data = analisis_ia['swot']")

# Guardar
with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Generador PDF arreglado - usando 'analisis_ia' consistentemente")

# Ahora arreglar app.py para que use analisis_ia en lugar de ai_analysis
with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar donde se llama a generar_pdf_mckinsey y cambiar ai_analysis por analisis_ia
for i in range(5340, min(5360, len(lines))):
    if "ai_analysis=ai_analysis" in lines[i]:
        lines[i] = lines[i].replace("ai_analysis=ai_analysis", "analisis_ia=ai_analysis")
        print(f"✅ Cambiado parámetro en línea {i+1}")
        break

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Nombres de parámetros unificados")
print("   - El generador PDF usa 'analisis_ia'")
print("   - app.py recopila como 'ai_analysis' y pasa como 'analisis_ia'")

