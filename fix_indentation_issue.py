# Corregir la indentación del control de costos
with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar y eliminar las líneas mal indentadas (alrededor de 5571-5580)
# Primero, encontrar donde está el problema
for i in range(5569, 5590):
    if i < len(lines) and "Control de escalamiento de costos" in lines[i]:
        # Eliminar desde aquí hasta el siguiente bloque bien indentado
        start_idx = i
        end_idx = i + 15  # Aproximadamente 15 líneas del nuevo código
        
        # Eliminar esas líneas
        del lines[start_idx:end_idx]
        print(f"Eliminadas líneas mal indentadas desde {start_idx}")
        break

with open('app.py', 'w') as f:
    f.writelines(lines)

print("Código mal indentado eliminado")
