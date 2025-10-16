from utils.importar_excel_definitivo import importar_excel_definitivo

archivo = 'excel_test_final.xlsx'
try:
    datos = importar_excel_definitivo(archivo)
    
    print("=== DATOS LABORALES ===")
    print(f"Datos importados: {datos.get('datos_laborales', {})}")
    
    print("\n=== PARAMETROS ===")
    parametros = datos.get('parametros', {})
    print(f"Días cobro: {parametros.get('dias_cobro')}")
    print(f"Días pago: {parametros.get('dias_pago')}")
    print(f"Días inventario: {parametros.get('dias_inventario')}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
