#!/usr/bin/env python3
"""
Arreglar error de indentación en el bloque with st.spinner
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar la línea 1778-1779
if len(lines) > 1779:
    print(f"Línea 1778: {lines[1777].rstrip()}")
    print(f"Línea 1779: {lines[1778].rstrip()}")
    
    # Ver si la línea 1779 necesita más indentación
    if "with st.spinner" in lines[1777]:
        # La siguiente línea debe estar más indentada
        current_indent = len(lines[1778]) - len(lines[1778].lstrip())
        needed_indent = len(lines[1777]) - len(lines[1777].lstrip()) + 4
        
        print(f"Indentación actual: {current_indent} espacios")
        print(f"Indentación necesaria: {needed_indent} espacios")
        
        # Arreglar todas las líneas dentro del bloque with
        i = 1778
        while i < len(lines) and lines[i].strip():
            # Si la línea no está vacía y pertenece al bloque
            if lines[i].strip() and not lines[i].strip().startswith("#"):
                # Calcular nueva indentación
                old_indent = len(lines[i]) - len(lines[i].lstrip())
                if old_indent < needed_indent:
                    lines[i] = " " * needed_indent + lines[i].lstrip()
            i += 1
            
            # Si encontramos otro if o elif al mismo nivel, parar
            if i < len(lines) and lines[i].strip().startswith(("if ", "elif ", "else:")):
                if len(lines[i]) - len(lines[i].lstrip()) <= len(lines[1777]) - len(lines[1777].lstrip()):
                    break
        
        print(f"✅ Corregidas {i - 1778} líneas")

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Indentación corregida")

