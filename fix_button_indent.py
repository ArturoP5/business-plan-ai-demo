#!/usr/bin/env python3
"""
Arregla la indentación del botón generar_proyeccion_mckinsey
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar la línea con el error (2191)
for i in range(2190, 2195):
    if i < len(lines) and 'generar_proyeccion_mckinsey = st.button(' in lines[i]:
        # Quitar espacios extras - debe tener 4 espacios (mismo nivel que st.markdown)
        lines[i] = '    generar_proyeccion_mckinsey = st.button(\n'
        print(f"✅ Arreglada indentación en línea {i+1}")
        
        # Arreglar las siguientes líneas del botón también
        for j in range(i+1, i+5):
            if j < len(lines):
                # Mantener 8 espacios para los parámetros del botón
                if '"📊 EJECUTAR PROYECCIÓN DCF"' in lines[j]:
                    lines[j] = '        "📊 EJECUTAR PROYECCIÓN DCF", \n'
                elif 'type="primary"' in lines[j]:
                    lines[j] = '        type="primary", \n'
                elif 'use_container_width=True' in lines[j]:
                    lines[j] = '        use_container_width=True,\n'
                elif 'help=' in lines[j]:
                    lines[j] = '        help="Valoración DCF pura con metodología McKinsey (NOPLAT, ROIC, Beta sectorial)"\n'
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Indentación del botón corregida")
