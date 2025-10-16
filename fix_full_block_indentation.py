#!/usr/bin/env python3
"""
Arreglar toda la indentación del bloque de Análisis Financiero Completo
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar el bloque problemático (alrededor de línea 1778)
for i in range(1775, min(1900, len(lines))):
    if "💼 Análisis Financiero Completo IA" in lines[i]:
        print(f"Encontrado botón en línea {i+1}")
        
        # Determinar la indentación base correcta
        # Buscar un if anterior para tomar referencia
        base_indent = 8
        for j in range(i-10, i):
            if "if api_key" in lines[j] or "if ai_model" in lines[j]:
                base_indent = len(lines[j]) - len(lines[j].lstrip())
                print(f"Indentación base detectada: {base_indent} espacios")
                break
        
        # Arreglar todo el bloque con indentación consistente
        # El if debe estar al nivel base
        lines[i] = " " * base_indent + lines[i].lstrip()
        
        # Todo lo que está dentro del if debe tener base_indent + 4
        j = i + 1
        block_count = 0
        while j < len(lines) and block_count < 100:
            if lines[j].strip():
                # Detectar el nivel de indentación necesario
                if lines[j].strip().startswith("with st.spinner"):
                    lines[j] = " " * (base_indent + 4) + lines[j].lstrip()
                elif lines[j].strip().startswith("try:"):
                    lines[j] = " " * (base_indent + 8) + lines[j].lstrip()
                elif lines[j].strip().startswith("analyzer"):
                    lines[j] = " " * (base_indent + 12) + lines[j].lstrip()
                elif lines[j].strip().startswith("if analyzer"):
                    lines[j] = " " * (base_indent + 12) + lines[j].lstrip()
                elif lines[j].strip().startswith("company_data"):
                    lines[j] = " " * (base_indent + 16) + lines[j].lstrip()
                elif lines[j].strip().startswith("'"):
                    lines[j] = " " * (base_indent + 20) + lines[j].lstrip()
                elif lines[j].strip().startswith("}"):
                    lines[j] = " " * (base_indent + 16) + lines[j].lstrip()
                elif lines[j].strip().startswith("financial_data"):
                    lines[j] = " " * (base_indent + 16) + lines[j].lstrip()
                elif lines[j].strip().startswith("if "):
                    # Determinar si es un if interno o externo
                    if "resultado_mck" in lines[j]:
                        lines[j] = " " * (base_indent + 16) + lines[j].lstrip()
                    elif "financial_data" in lines[j]:
                        lines[j] = " " * (base_indent + 16) + lines[j].lstrip()
                elif lines[j].strip().startswith("st.sidebar"):
                    lines[j] = " " * (base_indent + 16) + lines[j].lstrip()
                elif lines[j].strip().startswith("else:"):
                    lines[j] = " " * (base_indent + 12) + lines[j].lstrip()
                elif lines[j].strip().startswith("except"):
                    lines[j] = " " * (base_indent + 8) + lines[j].lstrip()
                
                # Si encontramos otro if al nivel base, terminamos
                if j > i + 5 and len(lines[j]) - len(lines[j].lstrip()) <= base_indent and lines[j].strip().startswith("if "):
                    break
            
            j += 1
            block_count += 1
        
        print(f"Arregladas {block_count} líneas del bloque")
        break

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("✅ Bloque de Análisis Financiero Completo re-indentado")

