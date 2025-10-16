import pandas as pd
from utils.plantilla_excel_v2 import crear_plantilla_v2

# Crear la plantilla v2.0
plantilla = crear_plantilla_v2()
with open("plantilla_v2_actual.xlsx", "wb") as f:
    f.write(plantilla.getvalue())

# Cargar ambos excels
excel_prueba = pd.ExcelFile('excel_test_final.xlsx')
excel_plantilla = pd.ExcelFile('plantilla_v2_actual.xlsx')

print("=== COMPARACIÓN DE HOJAS ===\n")
print("Excel de prueba tiene estas hojas:")
for sheet in excel_prueba.sheet_names:
    print(f"  • {sheet}")

print("\nPlantilla v2.0 tiene estas hojas:")
for sheet in excel_plantilla.sheet_names:
    print(f"  • {sheet}")

# Verificar campos específicos importantes
print("\n=== VERIFICANDO CAMPOS CLAVE ===")

# Balance_Pasivo - verificar préstamos
df_pasivo_prueba = pd.read_excel('excel_test_final.xlsx', sheet_name='Balance_Pasivo')
df_pasivo_plantilla = pd.read_excel('plantilla_v2_actual.xlsx', sheet_name='Balance_Pasivo')

print("\nCampos en Balance_Pasivo (prueba):")
print(df_pasivo_prueba['Concepto'].tolist()[:15])

print("\nCampos en Balance_Pasivo (plantilla):")
print(df_pasivo_plantilla['Concepto'].tolist()[:15])
