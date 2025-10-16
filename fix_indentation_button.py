#!/usr/bin/env python3
"""
Arregla la indentación del botón dentro de with col1
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar la línea problemática (5279 - índice 5278)
if lines[5278].strip().startswith('if st.button("📊 Generar Informe de Valoración"'):
    # Agregar 4 espacios más de indentación a esta línea
    lines[5278] = '                    ' + lines[5278].strip() + '\n'
    print("✅ Arreglada indentación del if st.button en línea 5279")
    
    # También arreglar las siguientes líneas del bloque
    # Las líneas try, from, with spinner, etc. también necesitan indentación extra
    for i in range(5279, 5285):
        if i < len(lines):
            # Si la línea tiene contenido y empieza con espacios
            if lines[i].strip():
                # Agregar 4 espacios más
                lines[i] = '    ' + lines[i]
    
    print("✅ Arreglada indentación del bloque completo del botón")

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Indentación corregida")
