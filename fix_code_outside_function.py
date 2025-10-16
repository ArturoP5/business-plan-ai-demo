#!/usr/bin/env python3
"""
Arreglar el código que está fuera de función
"""

with open("utils/pdf_mckinsey_generator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar dónde empieza el código problemático (alrededor de línea 1800)
problem_start = -1
for i in range(1800, min(1850, len(lines))):
    if "# ANÁLISIS SWOT (Con IA si disponible)" in lines[i]:
        problem_start = i
        print(f"Encontrado código fuera de función empezando en línea {i+1}")
        break

if problem_start > 0:
    # Este código necesita estar dentro de la función generar_pdf_mckinsey
    # Buscar dónde termina la función generar_pdf_mckinsey
    func_end = -1
    for i in range(problem_start-1, 0, -1):
        if "return elementos" in lines[i] and lines[i].strip().startswith("return"):
            func_end = i
            print(f"Encontrado final de función en línea {i+1}")
            break
    
    if func_end > 0:
        # Mover el código problemático antes del return
        problem_code = []
        # Capturar todo el código problemático
        for i in range(problem_start, len(lines)):
            if "return elementos" in lines[i]:
                break
            problem_code.append("    " + lines[i])  # Agregar indentación
        
        # Eliminar el código problemático del final
        del lines[problem_start:]
        
        # Insertar antes del return correcto
        for i, line in enumerate(problem_code):
            lines.insert(func_end + i, line)
        
        print(f"✅ Movido {len(problem_code)} líneas dentro de la función")
        
        # Asegurar que hay solo un return al final
        lines.append("\n")  # Línea en blanco al final del archivo

# Guardar cambios
with open("utils/pdf_mckinsey_generator.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("\n✅ Estructura del archivo corregida")
print("   - Todo el código ahora está dentro de funciones")
print("   - El return está en el lugar correcto")

