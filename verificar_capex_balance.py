import pandas as pd

# Verificar CAPEX en Proyecciones_Parametros
print("=== VERIFICANDO CAPEX ===")
df_param_prueba = pd.read_excel('excel_test_final.xlsx', sheet_name='Proyecciones_Parametros')
df_param_plantilla = pd.read_excel('plantilla_v2_actual.xlsx', sheet_name='Proyecciones_Parametros')

print("\nParámetros en Excel de prueba:")
for param in df_param_prueba['Parámetro'].tolist():
    if 'CAPEX' in str(param) or 'DSO' in str(param) or 'DPO' in str(param) or 'inventario' in str(param):
        print(f"  ✓ {param}")

print("\nParámetros en Plantilla v2.0:")
for param in df_param_plantilla['Parámetro'].tolist():
    if 'CAPEX' in str(param) or 'DSO' in str(param) or 'DPO' in str(param) or 'inventario' in str(param):
        print(f"  ✓ {param}")

# Verificar Balance_Check
print("\n=== VERIFICANDO BALANCE_CHECK ===")
if 'Balance_Check' in pd.ExcelFile('plantilla_v2_actual.xlsx').sheet_names:
    print("✅ Balance_Check existe en la plantilla")
    df_check = pd.read_excel('plantilla_v2_actual.xlsx', sheet_name='Balance_Check')
    print(f"   Tiene {df_check.shape[0]} filas y {df_check.shape[1]} columnas")
else:
    print("❌ Balance_Check NO existe en la plantilla")
