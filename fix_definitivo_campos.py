#!/usr/bin/env python3
"""
Elimina campo duplicado y arregla cuota_mercado definitivamente
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

cambios = 0

# 1. ELIMINAR completamente el campo ventajas_competitivas (líneas ~1696-1701)
for i in range(1695, 1703):
    if i < len(lines) and 'ventajas_competitivas = st.text_area(' in lines[i]:
        # Encontrar donde termina este text_area
        end_line = i
        for j in range(i+1, i+10):
            if j < len(lines) and ')' in lines[j] and lines[j].strip() == ')':
                end_line = j
                break
        
        # Eliminar todas las líneas de este campo
        del lines[i:end_line+1]
        print(f"✅ Eliminado campo 'Ventajas Competitivas' duplicado (líneas {i+1} a {end_line+1})")
        cambios += 1
        break

# 2. Arreglar cuota_mercado - buscar de nuevo porque las líneas cambiaron
for i in range(1680, 1695):
    if i < len(lines) and 'cuota_mercado = st.number_input(' in lines[i]:
        # Buscar la línea con value=
        for j in range(i+1, min(i+8, len(lines))):
            if 'value=' in lines[j]:
                # Reemplazar toda la línea de value
                if 'value=0.0,' in lines[j] or 'value=default_cuota_mercado' in lines[j]:
                    lines[j] = '                value=float(default_cuota_mercado) if "default_cuota_mercado" in locals() else 10.0,\n'
                    print(f"✅ Arreglado value de cuota_mercado en línea {j+1}")
                    cambios += 1
                    break
        break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print(f"\n✅ Total cambios: {cambios}")
print("- Campo duplicado eliminado")
print("- Cuota de mercado debe cargar correctamente ahora")
