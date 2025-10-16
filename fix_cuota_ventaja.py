#!/usr/bin/env python3
"""
Arregla cuota_mercado value y elimina campo duplicado de ventajas competitivas
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# 1. Arreglar el value de cuota_mercado
for i in range(1685, 1695):
    if 'cuota_mercado = st.number_input(' in lines[i]:
        # Buscar la línea con value=0.0
        for j in range(i+1, i+10):
            if 'value=0.0,' in lines[j]:
                lines[j] = '                value=default_cuota_mercado if "default_cuota_mercado" in locals() else 10.0,\n'
                print("✅ Arreglado value de cuota_mercado")
                break
        break

# 2. Buscar y comentar o eliminar el campo duplicado "Ventajas Competitivas"
# Primero buscar dónde está
for i in range(1670, 1685):
    if '"Ventajas Competitivas"' in lines[i]:
        # Encontrar el bloque completo del text_area y comentarlo
        start = i - 1  # Incluir la línea anterior si es parte de la definición
        end = i
        # Buscar el cierre del text_area
        for j in range(i, i+10):
            if ')' in lines[j] and lines[j].strip() == ')':
                end = j
                break
        
        # Comentar todo el bloque
        for k in range(start, end+1):
            lines[k] = '        # ' + lines[k].lstrip()
        print(f"✅ Comentado campo duplicado 'Ventajas Competitivas' (líneas {start+1} a {end+1})")
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Cuota de mercado arreglada y campo duplicado eliminado")
