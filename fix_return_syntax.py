#!/usr/bin/env python3
"""
Arreglar el error de return fuera de función
"""

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar el return que está fuera de función
found_error = False
for i in range(len(lines)-1, len(lines)-100, -1):  # Buscar desde el final
    if i >= 0 and "return elementos" in lines[i]:
        # Verificar si está dentro de una función
        indent = len(lines[i]) - len(lines[i].lstrip())
        print(f"Encontrado 'return elementos' en línea {i+1} con indentación {indent}")
        
        # Si la indentación es 0, está fuera de función
        if indent == 0:
            print("❌ Error: return está fuera de función")
            # Eliminar esta línea problemática
            del lines[i]
            found_error = True
            print("✅ Línea problemática eliminada")
            break

# Verificar que el archivo termine correctamente
# Buscar la última función y asegurar que termine bien
last_func_line = -1
for i in range(len(lines)-1, 0, -1):
    if "def " in lines[i] and not lines[i].strip().startswith("#"):
        last_func_line = i
        print(f"Última función encontrada en línea {i+1}: {lines[i].strip()}")
        break

# Asegurar que hay un return correcto al final de la última función
if last_func_line > 0:
    # Buscar el return correcto dentro de la función
    found_valid_return = False
    for i in range(last_func_line, min(last_func_line + 200, len(lines))):
        if "return " in lines[i] and len(lines[i]) - len(lines[i].lstrip()) > 0:
            found_valid_return = True
            print(f"✅ Return válido encontrado en línea {i+1}")
            break
    
    if not found_valid_return:
        print("⚠️ No se encontró return en la última función")
        # Buscar dónde debería estar el return
        for i in range(len(lines)-1, last_func_line, -1):
            if "elementos" in lines[i] and "append" in lines[i]:
                # Agregar return después del último append
                lines.insert(i+1, "    return elementos\n")
                print(f"✅ Agregado 'return elementos' en línea {i+2}")
                break

# Guardar cambios
with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Archivo corregido")

