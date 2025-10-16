import pandas as pd

# Examinar una de las plantillas TEST que sí funciona
archivo = "TEST_plantilla_211217.xlsx"

try:
    # Ver estructura de Datos Históricos PYL
    df = pd.read_excel(archivo, sheet_name='Datos Históricos PYL')
    
    print("📊 ESTRUCTURA DE 'Datos Históricos PYL':")
    print("=" * 50)
    print("Columnas:", list(df.columns))
    print("\nPrimeras 10 filas:")
    print(df.head(10))
    print("\n¿Tiene columna 'Concepto'?:", 'Concepto' in df.columns)
    
except Exception as e:
    print(f"Error: {e}")
