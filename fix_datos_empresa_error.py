# Corregir el error de datos_empresa no definida
with open('utils/pdf_mckinsey_generator.py', 'r') as f:
    content = f.read()

# Buscar la definición de la función para ver qué parámetros recibe
old_func_def = "def crear_proyecciones_financieras(pyl_df: pd.DataFrame, balance_df: pd.DataFrame, styles) -> List:"
new_func_def = "def crear_proyecciones_financieras(pyl_df: pd.DataFrame, balance_df: pd.DataFrame, styles, datos_empresa: dict = None) -> List:"

content = content.replace(old_func_def, new_func_def)

# Ahora actualizar la llamada a la función
old_call = "story.extend(crear_proyecciones_financieras(pyl_df, balance_df, styles))"
new_call = "story.extend(crear_proyecciones_financieras(pyl_df, balance_df, styles, datos_empresa))"

content = content.replace(old_call, new_call)

# Agregar validación en caso de que datos_empresa sea None
old_sector_line = "            sector = datos_empresa.get('sector', 'General')"
new_sector_line = "            sector = datos_empresa.get('sector', 'General') if datos_empresa else 'General'"

content = content.replace(old_sector_line, new_sector_line)

old_madura_line = "            empresa_madura = (datos_empresa.get('año_fundacion', 2020) < 2010)"
new_madura_line = "            empresa_madura = (datos_empresa.get('año_fundacion', 2020) < 2010) if datos_empresa else True"

content = content.replace(old_madura_line, new_madura_line)

with open('utils/pdf_mckinsey_generator.py', 'w') as f:
    f.write(content)

print("✅ Error de datos_empresa corregido")
