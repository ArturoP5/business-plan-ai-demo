#!/usr/bin/env python3
"""
Corregir el value duplicado en cuota_mercado
"""

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Buscar cuota_mercado alrededor de la línea 1654
for i in range(1645, 1665):
    if 'cuota_mercado = st.number_input(' in lines[i]:
        print(f"Encontrado cuota_mercado en línea {i+1}")
        
        # Ver las siguientes líneas para encontrar los values duplicados
        print("\nEstructura actual:")
        for j in range(i, min(i+10, len(lines))):
            print(f"  Línea {j+1}: {lines[j].rstrip()}")
            
        # Contar cuántos 'value=' hay
        value_count = 0
        value_lines = []
        for j in range(i, min(i+10, len(lines))):
            if 'value=' in lines[j]:
                value_count += 1
                value_lines.append(j)
        
        print(f"\nEncontrados {value_count} 'value=' en las líneas: {[l+1 for l in value_lines]}")
        
        if value_count > 1:
            # Eliminar el primer value= (el que dice 0.0) y dejar el segundo (el que tiene datos_excel)
            for j in value_lines[:-1]:  # Eliminar todos menos el último
                lines[j] = lines[j].replace('value=0.0,', '').replace('value=0.0', '')
                lines[j] = lines[j].replace('value=datos_excel["info_general"].get("cuota_mercado", 0.0) if datos_excel else 0.0,', '')
                
            # Asegurarse de que solo quede un value con datos_excel
            lines[value_lines[-1]] = '                value=datos_excel["info_general"].get("cuota_mercado", 0.0) if datos_excel else 0.0,\n'
            print(f"✅ Corregido: eliminados values duplicados")
        
        break

# Guardar
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Campo cuota_mercado corregido")

