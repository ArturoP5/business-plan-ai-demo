# Corregir el error de indentación en el PDF
with open('utils/pdf_mckinsey_generator.py', 'r') as f:
    lines = f.readlines()

# Buscar y corregir las líneas problemáticas (alrededor de 1283-1285)
for i in range(len(lines)):
    if i >= 1282 and i <= 1286:
        # Eliminar la línea suelta que causa el problema
        if "if datos_empresa else 'General'" in lines[i] and "sector = " not in lines[i]:
            lines[i] = ""  # Eliminar esta línea problemática

with open('utils/pdf_mckinsey_generator.py', 'w') as f:
    f.writelines(lines)

print("✅ Error de indentación corregido")
