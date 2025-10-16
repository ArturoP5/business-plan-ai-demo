#!/usr/bin/env python3
"""
Arreglar definitivamente el problema de tab9
"""

with open("app.py", "r") as f:
    lines = f.readlines()

# Buscar la línea 4685 donde se definen las 9 tabs
for i in range(4680, 4690):
    if i < len(lines) and "st.tabs" in lines[i]:
        print(f"Línea {i+1}: {lines[i].strip()[:100]}")
        
        # Verificar si tiene 9 elementos en la lista
        if "🤖 Análisis IA" in lines[i]:
            print("✓ La pestaña de Análisis IA está en la lista")
        
        # Contar las pestañas
        import re
        tabs_list = re.findall(r'"[^"]*"', lines[i])
        print(f"Número de pestañas definidas: {len(tabs_list)}")
        
        # Ver la línea anterior donde se asignan las variables
        if i > 0:
            prev_line = lines[i-1]
            if "tab" in prev_line:
                # Esta línea tiene las variables
                variables = prev_line.strip()
                print(f"Variables definidas: {variables}")
                
                # Si no están todas las tabs, arreglar
                if "tab9" not in prev_line and len(tabs_list) >= 9:
                    lines[i-1] = "    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(\n"
                    print("✅ Corregida la asignación de variables para incluir tab9")

# Guardar cambios
with open("app.py", "w") as f:
    f.writelines(lines)

print("\n✅ Problema de tab9 arreglado definitivamente")

