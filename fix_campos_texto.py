#!/usr/bin/env python3
"""
Agregar valores por defecto a los campos de texto estratégicos
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Buscar y arreglar cada campo
campos_a_arreglar = [
    ('ventaja_competitiva_clave = st.text_area(', 'ventaja_competitiva_principal'),
    ('competidores_principales = st.text_area(', 'competidores_principales'),
    ('vision_corto = st.text_area(', 'vision_corto_plazo'),
    ('vision_largo = st.text_area(', 'vision_largo_plazo'),
    ('principales_riesgos = st.text_area(', 'principales_riesgos')
]

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    campo_encontrado = False
    
    for campo_buscar, campo_datos in campos_a_arreglar:
        if campo_buscar in line:
            campo_encontrado = True
            print(f"Encontrado {campo_buscar} en línea {i+1}")
            
            # Agregar la línea actual
            new_lines.append(line)
            i += 1
            
            # Buscar las siguientes líneas hasta encontrar el paréntesis de cierre
            while i < len(lines):
                if ')' in lines[i]:
                    # Si no tiene value=, agregarlo antes del paréntesis
                    if 'value=' not in lines[i]:
                        # Insertar value antes del cierre
                        lines[i] = lines[i].replace(
                            ')',
                            f',\n            value=datos_excel["info_general"].get("{campo_datos}", "") if datos_excel else ""\n        )'
                        )
                    new_lines.append(lines[i])
                    i += 1
                    break
                else:
                    new_lines.append(lines[i])
                    i += 1
            break
    
    if not campo_encontrado:
        new_lines.append(line)
        i += 1

# Guardar el archivo modificado
with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("\n✅ Campos de texto estratégicos actualizados")
print("Campos modificados:")
for campo, _ in campos_a_arreglar:
    print(f"  - {campo.split(' = ')[0]}")

