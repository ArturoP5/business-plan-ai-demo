import pandas as pd
import sys

archivo = "plantilla_business_plan_v2_202509303.xlsx"

try:
    excel = pd.ExcelFile(archivo)
    print("📋 HOJAS ENCONTRADAS EN LA PLANTILLA:")
    print("=" * 50)
    
    for i, sheet_name in enumerate(excel.sheet_names, 1):
        print(f"{i}. {sheet_name}")
    
    print("\n🔍 VERIFICANDO HOJA 'Informacion General':")
    print("=" * 50)
    
    if 'Informacion General' in excel.sheet_names:
        df = pd.read_excel(archivo, sheet_name='Informacion General')
        print("\nCampos encontrados:")
        for idx, campo in enumerate(df['Campo'].values):
            if pd.notna(campo):
                print(f"  - {campo}")
        
        # Verificar si están los nuevos campos
        campos_nuevos = [
            'Descripción de la Actividad',
            'Productos/Servicios Principales',
            'Cuota de Mercado (%)',
            'Posicionamiento de Precios',
            'Ventajas Competitivas',
            'Clientes Objetivo'
        ]
        
        print("\n✅ VERIFICACIÓN DE CAMPOS NUEVOS:")
        campos_excel = df['Campo'].fillna('').values
        for campo_nuevo in campos_nuevos:
            if campo_nuevo in campos_excel:
                print(f"  ✅ {campo_nuevo} - ENCONTRADO")
            else:
                print(f"  ❌ {campo_nuevo} - NO ENCONTRADO")
    else:
        print("❌ No se encontró la hoja 'Informacion General'")
        
except Exception as e:
    print(f"Error al leer el archivo: {e}")
