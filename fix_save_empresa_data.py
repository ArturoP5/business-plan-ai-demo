#!/usr/bin/env python3
"""
Guarda los datos de la empresa en session_state cuando se cargan desde cualquier fuente
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Para cada empresa demo, agregar guardado en session_state después del success message
demos = [
    ("Restaurante La Terraza", 1051),
    ("TechStart SaaS", 1155),
    ("ModaOnline Shop", 1259),
    ("MetalPro Industrial", 1363)
]

for demo_name, approx_line in demos:
    # Buscar la línea de success
    for i in range(approx_line-5, approx_line+5):
        if i < len(lines) and f"✅ Cargado: {demo_name}" in lines[i]:
            # Agregar guardado de datos después del success
            lines.insert(i+1, "        # Guardar datos de la empresa en session_state\n")
            lines.insert(i+2, "        if 'info_general' in datos_excel:\n")
            lines.insert(i+3, "            st.session_state['empresa_demo_data'] = datos_excel['info_general']\n")
            print(f"✅ Agregado guardado para {demo_name} en línea {i+1}")
            break

# Guardar cambios
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Ahora los datos de las empresas se guardan en session_state")
