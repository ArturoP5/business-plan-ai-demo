from utils.importar_excel_definitivo import importar_excel_definitivo

# Probar la importación con el Excel de prueba
archivo = 'excel_test_final.xlsx'
try:
    datos = importar_excel_definitivo(archivo)
    
    print("=== DATOS LABORALES ===")
    print(f"Datos importados: {datos.get('datos_laborales', {})}")
    
    print("\n=== PROYECCIONES ===")
    proyecciones = datos.get('proyecciones', {})
    print(f"Días cobro: {proyecciones.get('dias_cobro')}")
    print(f"Días pago: {proyecciones.get('dias_pago')}")
    print(f"Días inventario: {proyecciones.get('dias_inventario')}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
