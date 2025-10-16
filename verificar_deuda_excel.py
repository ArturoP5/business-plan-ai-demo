import pandas as pd

# Leer el Excel que el usuario cargó
archivo = 'plantilla_business_plan_v2_202510027.xlsx'

try:
    # Leer Balance_Pasivo
    df_pasivo = pd.read_excel(archivo, sheet_name='Balance_Pasivo')
    print("=== DEUDA EN EL EXCEL ===")
    print("\nDeuda Corto Plazo:")
    for idx, row in df_pasivo.iterrows():
        concepto = row['Concepto']
        if 'Deuda financiera CP' in str(concepto):
            print(f"  {concepto}: {row['Valor']:,.0f}")
    
    print("\nDeuda Largo Plazo:")
    for idx, row in df_pasivo.iterrows():
        concepto = row['Concepto']
        if any(x in str(concepto) for x in ['Préstamos LP', 'Hipoteca', 'Leasing', 'Otros préstamos']):
            print(f"  {concepto}: {row['Valor']:,.0f}")
            
except Exception as e:
    print(f"Error: {e}")
    print("No se pudo leer el archivo")
