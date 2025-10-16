#!/usr/bin/env python3
"""
Arreglar completamente el bloque de análisis financiero completo
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar el bloque problemático
for i in range(1775, min(1850, len(lines))):
    if "Análisis Financiero Completo IA" in lines[i]:
        print(f"Encontrado bloque en línea {i+1}")
        
        # Verificar y corregir la indentación de todo el bloque
        base_indent = len(lines[i]) - len(lines[i].lstrip())
        
        # El with spinner debe tener la misma indentación base + 4
        for j in range(i+1, min(i+60, len(lines))):
            if "with st.spinner" in lines[j]:
                lines[j] = " " * (base_indent + 4) + lines[j].lstrip()
                
                # Todo dentro del with debe tener base_indent + 8
                k = j + 1
                while k < len(lines) and lines[k].strip():
                    if not lines[k].strip().startswith("#"):
                        lines[k] = " " * (base_indent + 8) + lines[k].lstrip()
                    k += 1
                    # Parar si encontramos algo que no es parte del bloque
                    if k < len(lines) and "# Guardar en session_state" in lines[k]:
                        break
                break
        break

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ Bloque de análisis completo arreglado")

