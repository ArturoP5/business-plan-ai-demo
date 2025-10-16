#!/usr/bin/env python3
"""
Arreglar el error de tab9 no definida
"""

with open("app.py", "r") as f:
    lines = f.readlines()

print("Buscando definición de tabs...")

# Buscar donde se definen las tabs
tabs_definition_line = -1
for i in range(len(lines)):
    if "st.tabs([" in lines[i] or "st.tabs(" in lines[i]:
        # Contar cuántas tabs se definen
        tabs_line = lines[i]
        # Contar las variables antes del =
        if "=" in lines[i]:
            vars_part = lines[i].split("=")[0].strip()
            num_tabs = len(vars_part.split(","))
            print(f"Línea {i+1}: {num_tabs} tabs definidas")
            print(f"Variables: {vars_part}")
            tabs_definition_line = i

# Buscar donde se usa tab9
for i in range(len(lines)):
    if "with tab9:" in lines[i]:
        print(f"tab9 usada en línea {i+1}")
        
        # Verificar si tab9 está definida
        if tabs_definition_line > 0 and tabs_definition_line < i:
            # Ver si necesitamos agregar tab9 a la definición
            tabs_line = lines[tabs_definition_line]
            if "tab9" not in tabs_line:
                print("❌ tab9 no está en la definición de tabs")
                
                # Contar cuántas tabs hay actualmente
                if "tab8" in tabs_line:
                    # Agregar tab9
                    lines[tabs_definition_line] = tabs_line.replace("tab8 =", "tab8, tab9 =")
                    print("✅ Agregada tab9 a la definición")
                elif "tab7" in tabs_line:
                    lines[tabs_definition_line] = tabs_line.replace("tab7 =", "tab7, tab8, tab9 =")
                    print("✅ Agregadas tab8 y tab9 a la definición")
        break

# Guardar cambios
with open("app.py", "w") as f:
    f.writelines(lines)

print("\n✅ Error de tab9 arreglado")

