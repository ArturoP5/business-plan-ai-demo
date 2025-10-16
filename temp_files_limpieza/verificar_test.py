import pandas as pd

archivo = "TEST_plantilla_211217.xlsx"

try:
    excel = pd.ExcelFile(archivo)
    print("📋 HOJAS EN LA PLANTILLA:")
    for i, sheet in enumerate(excel.sheet_names, 1):
        print(f"  {i}. {sheet}")
    
    print("\n🔍 CAMPOS EN 'Informacion General':")
    if 'Informacion General' in excel.sheet_names:
        df = pd.read_excel(archivo, sheet_name='Informacion General')
        for campo in df['Campo'].dropna():
            if 'DESCRIPCIÓN' in str(campo).upper():
                print(f"  🆕 {campo}")
            elif campo:
                print(f"  - {campo}")
    
    print("\n📊 VERIFICANDO 'Líneas Financiación':")
    if 'Líneas Financiación' in excel.sheet_names:
        df = pd.read_excel(archivo, sheet_name='Líneas Financiación')
        print(f"  Columnas: {list(df.columns)}")
        print(f"  Filas: {len(df)}")
        tipos = df.iloc[:, 0].dropna().unique()
        print("  Tipos encontrados:")
        for tipo in tipos[:10]:
            if tipo and '---' not in str(tipo):
                print(f"    • {tipo}")
                
except Exception as e:
    print(f"Error: {e}")
