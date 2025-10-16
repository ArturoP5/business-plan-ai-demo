#!/usr/bin/env python3
"""
Arreglar el error de sintaxis en el bloque try-except
"""

with open("models/modelo_financiero.py", "r") as f:
    lines = f.readlines()

print("Buscando el bloque try alrededor de línea 1825...")

# Buscar el bloque try que contiene la línea problemática
try_line = -1
for i in range(1820, min(1830, len(lines))):
    if "try:" in lines[i]:
        try_line = i
        print(f"Encontrado 'try:' en línea {i+1}")
        break

if try_line > 0:
    # Buscar el except correspondiente
    except_line = -1
    for i in range(try_line + 1, min(try_line + 20, len(lines))):
        if "except" in lines[i]:
            except_line = i
            print(f"Encontrado 'except' en línea {i+1}")
            break
    
    # El return que agregamos está interfiriendo con el try-except
    # Necesitamos moverlo o arreglarlo
    for i in range(try_line, min(except_line if except_line > 0 else try_line + 10, len(lines))):
        if "return {}  # Modelo de banca" in lines[i]:
            print(f"Encontrado return problemático en línea {i+1}")
            # Eliminar esta línea
            del lines[i]
            # En su lugar, hacer que la valoración retorne un dict vacío
            for j in range(try_line + 1, min(try_line + 10, len(lines))):
                if "valoracion = " in lines[j] and "#" in lines[j]:
                    # Cambiar la línea comentada por una asignación vacía
                    lines[j] = "        valoracion = {}  # Modelo de banca inversión desactivado\n"
                    print(f"Reemplazada línea {j+1} con asignación vacía")
                    break
            break
else:
    print("No se encontró bloque try, buscando alternativa...")
    # Si no hay try, simplemente comentar la línea problemática
    for i in range(1824, min(1827, len(lines))):
        if "return {}" in lines[i]:
            del lines[i]
            print(f"Eliminado return problemático en línea {i+1}")
            break

# Guardar cambios
with open("models/modelo_financiero.py", "w") as f:
    f.writelines(lines)

print("✅ Error de sintaxis arreglado")

