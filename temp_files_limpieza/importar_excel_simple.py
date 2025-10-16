import pandas as pd
import streamlit as st

def importar_excel_simple(archivo):
    """
    Función simplificada pero completa para importar Excel
    """
    try:
        datos = {}
        
        # 1. Información General
        try:
            df_info = pd.read_excel(archivo, sheet_name='Informacion General')
            info_dict = dict(zip(df_info['Campo'].fillna(''), df_info['Valor'].fillna('')))
            
            datos['info_general'] = {
                'nombre_empresa': str(info_dict.get('Nombre de la empresa', 'Mi Empresa')),
                'sector': str(info_dict.get('Sector', 'Tecnología')),
                'pais': str(info_dict.get('País', 'España')),
                'año_fundacion': int(info_dict.get('Año de Fundación', 2020) or 2020),
                'empresa_familiar': str(info_dict.get('¿Empresa familiar?', 'No')),
                'empresa_auditada': str(info_dict.get('¿Cuentas auditadas?', 'Sí')),
                'moneda': str(info_dict.get('Moneda', 'EUR'))
            }
        except:
            datos['info_general'] = {
                'nombre_empresa': 'Mi Empresa',
                'sector': 'Tecnología',
                'pais': 'España',
                'año_fundacion': 2020,
                'empresa_familiar': 'No',
                'empresa_auditada': 'Sí',
                'moneda': 'EUR'
            }
        
        # 2. PYL Histórico
        try:
            df_pyl = pd.read_excel(archivo, sheet_name='Datos Históricos PYL')
            columnas_años = [col for col in df_pyl.columns if col != 'Concepto']
            
            ventas_valores = []
            gastos_personal_valores = []
            gastos_generales_valores = []
            gastos_marketing_valores = []
            
            for año in columnas_años[-3:]:  # Últimos 3 años
                ventas = df_pyl[df_pyl['Concepto'] == 'Ventas'][año].values[0] if 'Ventas' in df_pyl['Concepto'].values else 1000000
                gastos_p = df_pyl[df_pyl['Concepto'] == 'Gastos de Personal'][año].values[0] if 'Gastos de Personal' in df_pyl['Concepto'].values else 300000
                gastos_g = df_pyl[df_pyl['Concepto'] == 'Gastos Generales'][año].values[0] if 'Gastos Generales' in df_pyl['Concepto'].values else 100000
                gastos_m = df_pyl[df_pyl['Concepto'] == 'Gastos de Marketing'][año].values[0] if 'Gastos de Marketing' in df_pyl['Concepto'].values else 50000
                
                ventas_valores.append(float(ventas))
                gastos_personal_valores.append(float(gastos_p))
                gastos_generales_valores.append(float(gastos_g))
                gastos_marketing_valores.append(float(gastos_m))
            
            datos['pyl_historico'] = {
                'ventas': ventas_valores,
                'costos_variables_pct': 40,
                'gastos_personal': gastos_personal_valores,
                'gastos_generales': gastos_generales_valores,
                'gastos_marketing': gastos_marketing_valores
            }
        except:
            datos['pyl_historico'] = {
                'ventas': [1000000, 1100000, 1200000],
                'costos_variables_pct': 40,
                'gastos_personal': [300000, 320000, 340000],
                'gastos_generales': [100000, 110000, 120000],
                'gastos_marketing': [50000, 55000, 60000]
            }
        
        # 3. Datos Laborales (NECESARIO)
        try:
            df_laboral = pd.read_excel(archivo, sheet_name='Datos Laborales')
            laboral_dict = dict(zip(df_laboral['Concepto'].fillna(''), df_laboral['Valor'].fillna(0)))
            
            datos['datos_laborales'] = {
                'num_empleados': int(laboral_dict.get('Número de empleados', 10)),
                'coste_medio_empleado': float(laboral_dict.get('Coste medio por empleado (€/año)', 35000)),
                'antiguedad_media': float(laboral_dict.get('Antigüedad media (años)', 5)),
                'rotacion_anual': float(laboral_dict.get('Rotación anual (%)', 10))
            }
        except:
            datos['datos_laborales'] = {
                'num_empleados': 10,
                'coste_medio_empleado': 35000,
                'antiguedad_media': 5,
                'rotacion_anual': 10.0
            }
        
        # 4. Balance Activo
        try:
            df_activo = pd.read_excel(archivo, sheet_name='Balance - Activo')
            activo_dict = dict(zip(df_activo['Concepto'].fillna(''), df_activo.iloc[:, 1].fillna(0)))
            
            datos['balance_activo'] = {
                'tesoreria_inicial': float(activo_dict.get('Tesorería', 100000)),
                'inversiones_cp': float(activo_dict.get('Inversiones financieras CP', 0)),
                'clientes_inicial': float(activo_dict.get('Clientes', 50000)),
                'inventario_inicial': float(activo_dict.get('Inventario', 30000)),
                'activo_fijo_bruto': float(activo_dict.get('Activo fijo bruto', 500000)),
                'depreciacion_acumulada': float(activo_dict.get('Depreciación acumulada', 100000)),
                'activos_intangibles': float(activo_dict.get('Activos intangibles brutos', 0))
            }
        except:
            datos['balance_activo'] = {
                'tesoreria_inicial': 100000,
                'inversiones_cp': 0,
                'clientes_inicial': 50000,
                'inventario_inicial': 30000,
                'activo_fijo_bruto': 500000,
                'depreciacion_acumulada': 100000,
                'activos_intangibles': 0
            }
        
        # 5. Balance Pasivo
        try:
            df_pasivo = pd.read_excel(archivo, sheet_name='Balance - Pasivo')
            pasivo_dict = dict(zip(df_pasivo['Concepto'].fillna(''), df_pasivo.iloc[:, 1].fillna(0)))
            
            datos['balance_pasivo'] = {
                'proveedores_inicial': float(pasivo_dict.get('Proveedores', 40000)),
                'acreedores_servicios': float(pasivo_dict.get('Acreedores por servicios', 0)),
                'deuda_cp': float(pasivo_dict.get('Deuda financiera CP', 0)),
                'prestamos_lp': float(pasivo_dict.get('Préstamos LP - Importe original', 200000)),                'prestamo_principal': float(pasivo_dict.get('Préstamos LP - Importe original', 200000)),                'prestamo_anos_transcurridos': float(pasivo_dict.get('Préstamos LP - Años transcurridos', 0)),                'hipoteca_principal': float(pasivo_dict.get('Hipotecas - Importe original', 0)),                'hipoteca_meses_transcurridos': float(pasivo_dict.get('Hipotecas - Meses transcurridos', 0)),                'leasing_total': float(pasivo_dict.get('Leasing - Importe total', 0)),                'leasing_meses_pendientes': float(pasivo_dict.get('Leasing - Meses pendientes', 0))
            }
        except:
            datos['balance_pasivo'] = {
                'proveedores_inicial': 40000,
                'acreedores_servicios': 0,
                'deuda_cp': 0,
                'prestamos_lp': float(pasivo_dict.get('Préstamos LP - Importe original', 200000)),                'prestamo_principal': float(pasivo_dict.get('Préstamos LP - Importe original', 200000)),                'prestamo_anos_transcurridos': float(pasivo_dict.get('Préstamos LP - Años transcurridos', 0)),                'hipoteca_principal': float(pasivo_dict.get('Hipotecas - Importe original', 0)),                'hipoteca_meses_transcurridos': float(pasivo_dict.get('Hipotecas - Meses transcurridos', 0)),                'leasing_total': float(pasivo_dict.get('Leasing - Importe total', 0)),                'leasing_meses_pendientes': float(pasivo_dict.get('Leasing - Meses pendientes', 0))
            }
        
        # 6. Patrimonio
        try:
            df_patrimonio = pd.read_excel(archivo, sheet_name='Balance - Patrimonio')
            patrimonio_dict = dict(zip(df_patrimonio['Concepto'].fillna(''), df_patrimonio.iloc[:, 1].fillna(0)))
            
            datos['patrimonio'] = {
                'capital_social': float(patrimonio_dict.get('Capital social', 100000)),
                'prima_emision': float(patrimonio_dict.get('Prima de emisión', 0)),
                'reserva_legal': float(patrimonio_dict.get('Reserva legal', 10000)),
                'reservas': float(patrimonio_dict.get('Otras reservas', 50000)),
                'resultados_acumulados': float(patrimonio_dict.get('Resultados acumulados', 0))
            }
        except:
            datos['patrimonio'] = {
                'capital_social': 100000,
                'prima_emision': 0,
                'reserva_legal': 10000,
                'reservas': 50000,
                'resultados_acumulados': 0
            }
        
        # 7. Líneas de Financiación
        datos['lineas_financiacion'] = []
        try:
            df_lineas = pd.read_excel(archivo, sheet_name='Líneas Financiación')
            for _, row in df_lineas.iterrows():
                if pd.notna(row.get('Tipo de Línea', '')) and row.get('Tipo de Línea', '') != '':
                    datos['lineas_financiacion'].append({
                        'tipo': str(row.get('Tipo de Línea', '')),
                        'banco': str(row.get('Banco', '')),
                        'limite': float(row.get('Límite', 0)),
                        'dispuesto': float(row.get('Dispuesto', 0))
                    })
        except:
            pass
        
        return datos
        
    except Exception as e:
        st.error(f"Error general importando: {str(e)}")
        return None
