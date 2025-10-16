#!/usr/bin/env python3
"""
Corregir el paso de datos McKinsey al generador PDF
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

fixed = False
for i in range(len(lines)):
    if "resultado_mckinsey=datos['valoracion']," in lines[i]:
        print(f"Encontrado problema en línea {i+1}")
        # Reemplazar con la referencia correcta
        lines[i] = "                            resultado_mckinsey=st.session_state.get('resultado_mck', {}),\n"
        fixed = True
        print("✅ Corregido: ahora usa 'resultado_mck' de session_state")
        break

if fixed:
    # También verificar que se esté guardando resultado_mck correctamente
    found_save = False
    for i in range(len(lines)):
        if "resultado_mck = valorador_mck.valorar_empresa" in lines[i]:
            # Verificar si se guarda en session_state
            if i+1 < len(lines) and "st.session_state['resultado_mck']" not in lines[i+1]:
                lines.insert(i+1, "            st.session_state['resultado_mck'] = resultado_mck\n")
                print("✅ Agregado guardado de resultado_mck en session_state")
                found_save = True
                break
    
    # Guardar cambios
    with open("app.py", "w", encoding="utf-8") as f:
        f.writelines(lines)
    
    print("\n✅ Corrección aplicada:")
    print("   - PDF ahora recibe los datos correctos de McKinsey")
    print("   - Los valores deberían aparecer correctamente en páginas 1-6")
else:
    print("⚠️ No se encontró la línea a corregir")
    print("Buscando alternativa...")
    
    # Buscar de otra forma
    for i in range(5400, min(5450, len(lines))):
        if "resultado_mckinsey=" in lines[i]:
            print(f"Encontrado en línea {i+1}: {lines[i].strip()}")

