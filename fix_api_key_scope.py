#!/usr/bin/env python3
"""
Arreglar el problema del scope de api_key
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar la línea problemática (1777 aproximadamente)
for i in range(1770, min(1785, len(lines))):
    if "if api_key and st.sidebar.button" in lines[i] and "Análisis Financiero Completo" in lines[i]:
        print(f"Encontrado error en línea {i+1}")
        
        # El problema es que este código está fuera del contexto donde api_key existe
        # Necesitamos mover este código dentro del bloque correcto
        
        # Buscar hacia atrás donde se define api_key
        for j in range(i-1, max(i-50, 0), -1):
            if "api_key = st.sidebar.text_input" in lines[j]:
                print(f"Encontrada definición de api_key en línea {j+1}")
                
                # El botón debe estar indentado al mismo nivel
                # Contar la indentación
                indent = len(lines[j]) - len(lines[j].lstrip())
                
                # Arreglar la indentación del botón problemático
                lines[i] = " " * indent + lines[i].lstrip()
                
                # También arreglar las siguientes líneas del bloque
                for k in range(i+1, min(i+50, len(lines))):
                    if lines[k].strip() and not lines[k].strip().startswith("#"):
                        if "st.sidebar" in lines[k] or "analyzer" in lines[k] or "with st.spinner" in lines[k]:
                            lines[k] = " " * (indent + 4) + lines[k].lstrip()
                        else:
                            # Si ya no es parte del bloque, salir
                            if not lines[k].startswith(" " * indent):
                                break
                print("✅ Indentación corregida")
                break
        break

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Problema de scope arreglado")

