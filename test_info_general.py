from utils.importar_excel_definitivo import importar_excel_definitivo

# Probar con el Excel de prueba
archivo = 'excel_test_final.xlsx'
datos = importar_excel_definitivo(archivo)

print("=== INFO GENERAL IMPORTADA ===")
info = datos.get('info_general', {})
for campo, valor in info.items():
    print(f"{campo}: {valor}")

print("\n=== VALORES ESPERADOS ===")
print("Sector debe ser uno de: Hostelería, Tecnología, Ecommerce, Consultoría,")
print("                        Retail, Servicios, Automoción, Industrial, Otro")
print("Empresa familiar: Sí o No")
print("Cuentas auditadas: Sí o No")
