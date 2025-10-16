#!/usr/bin/env python3
"""
Agregar la novena pestaña a la lista
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar la línea específica 4580 (índice 4579)
if len(lines) > 4579:
    # Esta es la línea con la lista de pestañas
    line_4580 = lines[4579]
    print(f"Línea actual: {line_4580.strip()}")
    
    # Agregar "🤖 Análisis IA" al final de la lista
    if '"📚 Glosario"]' in line_4580 and '"🤖 Análisis IA"' not in line_4580:
        lines[4579] = line_4580.replace(
            '"📚 Glosario"]',
            '"📚 Glosario", "🤖 Análisis IA"]'
        )
        print("✅ Agregada pestaña '🤖 Análisis IA'")
    elif '"🤖 Análisis IA"' in line_4580:
        print("⚠️ La pestaña ya existe")
    else:
        print("⚠️ Formato inesperado en la línea")

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Lista de pestañas actualizada a 9 elementos")
print("La lista ahora incluye: Dashboard, P&L, Balance, Analytics, Resumen, Valoración, Documentos, Glosario, Análisis IA")

