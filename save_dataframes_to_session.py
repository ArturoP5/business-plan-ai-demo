#!/usr/bin/env python3
"""
Guardar los DataFrames de proyecciones en session_state cuando se generan
"""

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Buscar donde se usa pyl y guardarlo en session_state
modifications = []

# Buscar alrededor de la línea 5533 donde se verifica si pyl existe
for i in range(5530, min(5540, len(lines))):
    if "if pyl is not None and not pyl.empty:" in lines[i]:
        # Agregar guardado en session_state justo después
        indent = len(lines[i]) - len(lines[i].lstrip())
        new_line = " " * (indent + 4) + "st.session_state['pyl_df'] = pyl  # Guardar para el PDF\n"
        lines.insert(i + 1, new_line)
        modifications.append(f"Agregado guardado de pyl_df en línea {i+2}")
        break

# Buscar donde se genera balance_df alrededor de línea 5605
for i in range(5600, min(5650, len(lines))):
    if "balance_tabla = pd.DataFrame({" in lines[i]:
        # Agregar guardado después de crear el DataFrame
        for j in range(i, min(i+20, len(lines))):
            if "})" in lines[j]:  # Fin del DataFrame
                indent = len(lines[i]) - len(lines[i].lstrip())
                new_line = " " * indent + "st.session_state['balance_df'] = balance_tabla  # Guardar para el PDF\n"
                lines.insert(j + 1, new_line)
                modifications.append(f"Agregado guardado de balance_df en línea {j+2}")
                break
        break

# Buscar donde se crea fcf_df o datos de FCF
for i in range(4500, min(4700, len(lines))):
    if "fcf_proyectados" in lines[i] or "free_cash_flow" in lines[i]:
        # Si encuentra FCF, intentar guardarlo
        if "resultado_mck" in lines[i]:
            # Crear DataFrame de FCF desde resultado_mck
            indent = len(lines[i]) - len(lines[i].lstrip())
            new_code = f"""
{" " * indent}# Crear y guardar DataFrame de FCF para el PDF
{" " * indent}if 'resultado_mck' in st.session_state:
{" " * (indent + 4)}fcf_data = st.session_state['resultado_mck'].get('fcf_proyectados', [])
{" " * (indent + 4)}if fcf_data:
{" " * (indent + 8)}fcf_df = pd.DataFrame(fcf_data)
{" " * (indent + 8)}st.session_state['fcf_df'] = fcf_df
"""
            lines.insert(i + 1, new_code)
            modifications.append(f"Agregado creación y guardado de fcf_df en línea {i+2}")
            break

# Guardar cambios
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

if modifications:
    print("✅ DataFrames se guardarán en session_state:")
    for mod in modifications:
        print(f"   - {mod}")
else:
    print("⚠️ No se encontraron los puntos para guardar DataFrames")

