# Insertar el control de escalamiento con indentación correcta
with open('app.py', 'r') as f:
    lines = f.readlines()

# Buscar después de Gastos de Marketing (aproximadamente línea 1610)
for i, line in enumerate(lines):
    if "Gastos de Marketing" in line and i > 1600:
        # Buscar el siguiente st.markdown o similar
        for j in range(i+1, min(i+20, len(lines))):
            if lines[j].strip().startswith('st.') or lines[j].strip().startswith('#'):
                # Insertar aquí con la indentación correcta
                indent = "    "  # 4 espacios base
                
                new_control = f'''{indent}# Control de escalamiento de costos
{indent}st.markdown("---")
{indent}st.markdown("#### ⚙️ Estructura de Costos Operativos")
{indent}col_var1, col_var2 = st.columns(2)
{indent}with col_var1:
{indent}    porcentaje_gastos_variables = st.slider(
{indent}        "% Gastos que escalan con ventas",
{indent}        min_value=20,
{indent}        max_value=80,
{indent}        value=35 if sector != "Industrial" else 55,
{indent}        step=5,
{indent}        help="Qué porcentaje de los gastos operativos (personal, generales) son variables vs fijos. Industrial típico: 50-60%. Tecnología: 25-35%"
{indent}    )
{indent}with col_var2:
{indent}    info_text = f"Variables ({porcentaje_gastos_variables}%): Escalan con ventas\\nFijos ({100-porcentaje_gastos_variables}%): Solo inflación"
{indent}    st.info(info_text)
    
'''
                lines.insert(j, new_control)
                print(f"Control insertado en línea {j}")
                break
        break

with open('app.py', 'w') as f:
    f.writelines(lines)

print("Control de escalamiento insertado correctamente")
