#!/usr/bin/env python3
"""
Verificar y arreglar la lista de pestañas
"""

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.split('\n')

# Buscar la línea 4579 y las siguientes
for i in range(4575, 4585):
    if i < len(lines):
        print(f"Línea {i+1}: {lines[i][:100]}...")

print("\n" + "="*50)
print("Buscando y arreglando la lista de pestañas...")

# Buscar la lista de pestañas
for i, line in enumerate(lines):
    if '"📊 Dashboard"' in line and '"📚 Glosario"' in line:
        print(f"\nEncontrada lista en línea {i+1}")
        
        # Verificar si ya tiene 9 elementos
        if '"🤖 Análisis IA"' not in line:
            print("Agregando '🤖 Análisis IA' a la lista...")
            # Buscar el cierre de la lista
            if line.strip().endswith(']'):
                lines[i] = line.replace(']', ', "🤖 Análisis IA"]')
            elif line.strip().endswith('"]'):
                lines[i] = line.replace('"]', '", "🤖 Análisis IA"]')
            else:
                # Buscar en la siguiente línea
                if i+1 < len(lines) and ']' in lines[i+1]:
                    lines[i+1] = lines[i+1].replace(']', ', "🤖 Análisis IA"]')
        else:
            print("La pestaña '🤖 Análisis IA' ya está en la lista")

# Guardar
with open("app.py", "w", encoding="utf-8") as f:
    f.write('\n'.join(lines))

print("\n✅ Lista de pestañas actualizada")
print("Ahora debería tener 9 elementos")

