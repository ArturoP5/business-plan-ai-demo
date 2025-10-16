#!/usr/bin/env python3
"""
Arreglar la definición de las pestañas para incluir tab9
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar donde se definen las pestañas
for i, line in enumerate(lines):
    # Buscar la línea que define tab1, tab2, etc.
    if 'tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs' in line:
        print(f"Encontrada definición de pestañas en línea {i+1}")
        # Cambiar a 9 pestañas
        lines[i] = line.replace(
            'tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs',
            'tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs'
        )
        
        # Buscar la siguiente línea con la lista de pestañas
        for j in range(i, min(i+5, len(lines))):
            if '"📊 Dashboard"' in lines[j] and '"📚 Glosario"' in lines[j]:
                print(f"Encontrada lista de pestañas en línea {j+1}")
                # Agregar la pestaña de IA
                lines[j] = lines[j].replace(
                    '"📚 Glosario"]',
                    '"📚 Glosario", "🤖 Análisis IA"]'
                )
                break
        break

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Definición de pestañas corregida")
print("Ahora tab9 está definido correctamente")

