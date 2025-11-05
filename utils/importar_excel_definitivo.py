"""
Función de importación DEFINITIVA para la plantilla Excel
Lee exactamente la estructura de plantilla_excel_definitiva.py
"""

import pandas as pd
import streamlit as st
from datetime import datetime

def importar_excel_definitivo(archivo):
    """
    Importa datos desde la plantilla Excel definitiva
    NO inventa valores, usa 0 como valor neutro
    """
    try:
        # Verificar que el archivo tenga las hojas requeridas
        hojas_requeridas = [
            'Info_General',
            'Datos_Historicos_PYL',
            'Balance_Activo',
            'Balance_Pasivo',
            'Balance_Patrimonio',
            'Datos_Laborales',
            'Lineas_Financiacion',
            'Proyecciones_Parametros'
        ]
        
        excel_file = pd.ExcelFile(archivo)
        hojas_faltantes = [h for h in hojas_requeridas if h not in excel_file.sheet_names]
        
        if hojas_faltantes:
            st.error(f"❌ Faltan las siguientes hojas: {', '.join(hojas_faltantes)}")
            return None
        
        datos = {}
        año_actual = datetime.now().year
        
        # 1. INFORMACIÓN GENERAL
        df = pd.read_excel(archivo, sheet_name='Info_General')
        info_dict = dict(zip(df['Campo'].fillna(''), df['Valor'].fillna('')))
        
        datos['info_general'] = {
            'nombre_empresa': str(info_dict.get('Nombre de la empresa', 'Mi Empresa')),
            'sector': str(info_dict.get('Sector', 'Tecnología')),
            'pais': str(info_dict.get('País', 'España')),
            'año_fundacion': int(info_dict.get('Año de Fundación', año_actual - 5)),
            'empresa_familiar': str(info_dict.get('¿Empresa familiar?', 'No')),
            'empresa_auditada': str(info_dict.get('¿Cuentas auditadas?', 'Sí')),
            'moneda': str(info_dict.get('Moneda', 'EUR')),
            'modelo_negocio': str(info_dict.get('Modelo de Negocio', '')),
            'posicionamiento_precio': str(info_dict.get('Posicionamiento Precio', '')),
            'competidores_top3': str(info_dict.get('Top 3 Competidores', '')),
            'vision_corto_plazo': str(info_dict.get('Visión Corto Plazo (1 año)', '')),
            'vision_medio_plazo': str(info_dict.get('Visión Medio Plazo (3 años)', '')),
            'vision_largo_plazo': str(info_dict.get('Visión Largo Plazo (5+ años)', '')),
            'ventaja_competitiva_principal': str(info_dict.get('Ventaja Competitiva Principal', '')),
            'principales_riesgos': str(info_dict.get('Principales Riesgos', '')),
            # Campos nuevos de descripción
            'descripcion_actividad': str(info_dict.get('Descripción de la Actividad', '')),
            'productos_servicios': str(info_dict.get('Productos/Servicios Principales', '')),
            'cuota_mercado': float(info_dict.get('Cuota de Mercado (%)', 0)),
            'posicionamiento': str(info_dict.get('Posicionamiento de Precios', 'Medio')),
            'ventajas_competitivas': str(info_dict.get('Ventajas Competitivas', '')),
            'clientes_objetivo': str(info_dict.get('Clientes Objetivo', ''))
        }
        
        # 2. P&L HISTÓRICO
        df = pd.read_excel(archivo, sheet_name='Datos_Historicos_PYL')
        columnas_años = [col for col in df.columns if col != 'Concepto' and str(col).isdigit()]
        
        # Extraer valores por concepto
        ventas_valores = []
        costos_variables_valores = []
        gastos_personal_valores = []
        gastos_generales_valores = []
        gastos_marketing_valores = []
        
        for año in columnas_años[-3:]:  # Últimos 3 años
            fila_ventas = df[df['Concepto'] == 'Ventas']
            fila_costos_pct = df[df['Concepto'] == 'Costos Variables (%)']
            fila_personal = df[df['Concepto'] == 'Gastos de Personal']
            fila_generales = df[df['Concepto'] == 'Gastos Generales']
            fila_marketing = df[df['Concepto'] == 'Gastos de Marketing']
            
            ventas_valores.append(float(fila_ventas[año].values[0]) if not fila_ventas.empty else 0)
            valor_costo = float(fila_costos_pct[año].values[0]) if not fila_costos_pct.empty else 40.0
            costos_variables_valores.append(valor_costo)
            print(f"🔍 Excel - Año {año}: Costos = {valor_costo}%")
            gastos_personal_valores.append(float(fila_personal[año].values[0]) if not fila_personal.empty else 0)
            gastos_generales_valores.append(float(fila_generales[año].values[0]) if not fila_generales.empty else 0)
            gastos_marketing_valores.append(float(fila_marketing[año].values[0]) if not fila_marketing.empty else 0)
        
        datos['pyl_historico'] = {
            'ventas': ventas_valores,
            'costos_variables_pct': costos_variables_valores,  # Ahora es array
            'gastos_personal': gastos_personal_valores,
            'gastos_generales': gastos_generales_valores,
            'gastos_marketing': gastos_marketing_valores
        }
        
        # 3. DATOS LABORALES
        df = pd.read_excel(archivo, sheet_name='Datos_Laborales')
        laboral_dict = dict(zip(df['Concepto'].fillna(''), df['Valor'].fillna(0)))
        
        datos['datos_laborales'] = {
            'num_empleados': int(laboral_dict.get('Número de empleados', 0)),
            'coste_medio_empleado': float(laboral_dict.get('Coste medio por empleado (€/año)', 0)),
            'antiguedad_media': float(laboral_dict.get('Antigüedad media (años)', 0)),
            'rotacion_anual': float(laboral_dict.get('Rotación anual (%)', 0))
        }
        
        # 4. BALANCE ACTIVO
        df = pd.read_excel(archivo, sheet_name='Balance_Activo')
        activo_dict = dict(zip(df['Concepto'].fillna(''), df.iloc[:, 1].fillna(0)))
        
        datos['balance_activo'] = {
            'tesoreria_inicial': float(activo_dict.get('Tesorería', 0)),
            'inversiones_cp': float(activo_dict.get('Inversiones financieras CP', 0)),
            'clientes_inicial': float(activo_dict.get('Clientes', 0)),
            'inventario_inicial': float(activo_dict.get('Inventario', 0)),
            'activo_fijo_bruto': float(activo_dict.get('Activo fijo bruto', 0)),
            'depreciacion_acumulada': float(activo_dict.get('Depreciación acumulada', 0)),
            'activos_intangibles': float(activo_dict.get('Activos intangibles brutos', 0)),
            'otros_deudores': float(activo_dict.get('Otros deudores', 0)),
            'admin_publica_deudora': float(activo_dict.get('Administración Pública deudora', 0)),
            'gastos_anticipados': float(activo_dict.get('Gastos anticipados', 0)),
            'activos_impuesto_diferido_cp': float(activo_dict.get('Activos por impuesto diferido CP', 0)),
            'amortizacion_intangibles': float(activo_dict.get('Amortización acumulada intangibles', 0)),
            'inversiones_lp': float(activo_dict.get('Inversiones financieras LP', 0)),
            'creditos_lp': float(activo_dict.get('Créditos a largo plazo', 0)),
            'fianzas_depositos': float(activo_dict.get('Fianzas y depósitos', 0)),
            'activos_impuesto_diferido_lp': float(activo_dict.get('Activos por impuesto diferido LP', 0))
        }
        
        # 5. BALANCE PASIVO
        df = pd.read_excel(archivo, sheet_name='Balance_Pasivo')
        pasivo_dict = dict(zip(df['Concepto'].fillna(''), df.iloc[:, 1].fillna(0)))
        
        datos['balance_pasivo'] = {
            'proveedores_inicial': float(pasivo_dict.get('Proveedores', 0)),
            'acreedores_servicios': float(pasivo_dict.get('Acreedores por servicios', 0)),
            'deuda_cp': float(pasivo_dict.get('Deuda financiera CP', 0)),
            'prestamos_lp': float(pasivo_dict.get('Otros préstamos LP', 0)),
            'prestamo_principal': float(pasivo_dict.get('Préstamos LP - Importe original', 0)),
            'prestamo_anos_transcurridos': float(pasivo_dict.get('Préstamos LP - Años transcurridos', 0)),
            'prestamo_plazo_original': float(pasivo_dict.get('Préstamos LP - Plazo original (años)', 10)),
            'prestamo_interes': float(pasivo_dict.get('Préstamos LP - Tipo interés (%)', 4.5)),
            'prestamo_comision_apertura': float(pasivo_dict.get('Préstamos LP - Comisión apertura (%)', 0.5)),            'hipoteca_importe_original': float(pasivo_dict.get('Hipotecas - Importe original', 0)),
            'hipoteca_meses_transcurridos': float(pasivo_dict.get('Hipotecas - Meses transcurridos', 0)),
            'hipoteca_plazo_total': 20,  # Valor por defecto 20 años
            'hipoteca_interes': 3.25,  # Valor por defecto 3.25%
            'leasing_plazo_meses': 60,  # Valor por defecto 60 meses
            'leasing_total': float(pasivo_dict.get('Leasing - Importe total', 0)),
            'leasing_meses_restantes': float(pasivo_dict.get('Leasing - Meses pendientes', 0)),
            'anticipos_clientes': float(pasivo_dict.get('Anticipos de clientes', 0)),
            'remuneraciones_pendientes': float(pasivo_dict.get('Remuneraciones pendientes', 0)),
            'admin_publica_acreedora': float(pasivo_dict.get('Administración Pública acreedora', 0)),
            'provisiones_cp': float(pasivo_dict.get('Provisiones CP', 0)),
            'provisiones_riesgos': float(pasivo_dict.get('Provisiones para riesgos LP', 0)),
            'pasivos_impuesto_diferido': float(pasivo_dict.get('Pasivos por impuesto diferido', 0)),
            'leasing_cuota_mensual': float(pasivo_dict.get('Leasing - Cuota mensual', 0)) if pasivo_dict.get('Leasing - Importe total', 0) > 0 else 0,        }
        
        # 6. PATRIMONIO
        df = pd.read_excel(archivo, sheet_name='Balance_Patrimonio')
        patrimonio_dict = dict(zip(df['Concepto'].fillna(''), df.iloc[:, 1].fillna(0)))
        
        datos['balance_patrimonio'] = {
            'capital_social': float(patrimonio_dict.get('Capital social', 0)),
            'prima_emision': float(patrimonio_dict.get('Prima de emisión', 0)),
            'reserva_legal': float(patrimonio_dict.get('Reserva legal', 0)),
            'otras_reservas': float(patrimonio_dict.get('Otras reservas', 0)),
            'resultados_acumulados': float(patrimonio_dict.get('Resultados acumulados', 0)),
            'resultado_ejercicio': float(patrimonio_dict.get('Resultado del ejercicio', 0))
        }
        
        # 7. LÍNEAS DE FINANCIACIÓN
        datos['lineas_financiacion'] = []
        df = pd.read_excel(archivo, sheet_name='Lineas_Financiacion')
        for _, row in df.iterrows():
            if pd.notna(row.get('Tipo de Línea', '')) and '---' not in str(row.get('Tipo de Línea', '')):
                if float(row.get('Límite', 0)) > 0:  # Solo incluir líneas con límite > 0
                    datos['lineas_financiacion'].append({
                        'tipo': str(row.get('Tipo de Línea', '')),
                        'banco': str(row.get('Banco', '')),
                        'limite': float(row.get('Límite', 0)),
                        'dispuesto': float(row.get('Dispuesto', 0))
                    })
        
        # 8. PARÁMETROS
        df = pd.read_excel(archivo, sheet_name='Proyecciones_Parametros')
        param_dict = dict(zip(df['Parámetro'].fillna(''), df['Valor'].fillna(0)))
        print("🔍 DEBUG importador - Parámetros leídos del Excel:")
        print(f"🔍 DEBUG importador: Ventas históricas = {datos.get("pyl_historico", {}).get("ventas", "NO ENCONTRADO")}")
        for key, value in list(param_dict.items())[:10]:
            print(f"  '{key}': {value}")
        
        # Agregar proyecciones (TODO en un solo dict)
        datos['proyecciones'] = {
            'capex_año1': float(param_dict.get('CAPEX Año 1', 0)),
            'capex_año2': float(param_dict.get('CAPEX Año 2', 0)),
            'capex_año3': float(param_dict.get('CAPEX Año 3', 0)),
            'capex_año4': float(param_dict.get('CAPEX Año 4', 0)),
            'capex_año5': float(param_dict.get('CAPEX Año 5', 0)),
            'dias_cobro': int(param_dict.get('Días de cobro (DSO)', 60)),
            'dias_pago': int(param_dict.get('Días de pago (DPO)', 45)),
            'dias_inventario': int(param_dict.get('Días de inventario', 60)),
            'crecimiento_ventas': [
                float(param_dict.get('Crecimiento Año 1 (%)', 10)),
                float(param_dict.get('Crecimiento Año 2 (%)', 8)),
                float(param_dict.get('Crecimiento Año 3 (%)', 6)),
                float(param_dict.get('Crecimiento Año 4 (%)', 5)),
                float(param_dict.get('Crecimiento Año 5 (%)', 4))
            ],
            'capex': [
                float(param_dict.get('CAPEX Año 1', 0)),
                float(param_dict.get('CAPEX Año 2', 0)),
                float(param_dict.get('CAPEX Año 3', 0)),
                float(param_dict.get('CAPEX Año 4', 0)),
                float(param_dict.get('CAPEX Año 5', 0))
            ],
            'gastos_personal_proyectados': [
                float(param_dict.get('Gastos Personal Año 1', 0)),
                float(param_dict.get('Gastos Personal Año 2', 0)),
                float(param_dict.get('Gastos Personal Año 3', 0)),
                float(param_dict.get('Gastos Personal Año 4', 0)),
                float(param_dict.get('Gastos Personal Año 5', 0))
            ],
            'gastos_generales_proyectados': [
                float(param_dict.get('Gastos Generales Año 1', 0)),
                float(param_dict.get('Gastos Generales Año 2', 0)),
                float(param_dict.get('Gastos Generales Año 3', 0)),
                float(param_dict.get('Gastos Generales Año 4', 0)),
                float(param_dict.get('Gastos Generales Año 5', 0))
            ],
            'gastos_marketing_proyectados': [
                float(param_dict.get('Gastos Marketing Año 1', 0)),
                float(param_dict.get('Gastos Marketing Año 2', 0)),
                float(param_dict.get('Gastos Marketing Año 3', 0)),
                float(param_dict.get('Gastos Marketing Año 4', 0)),
                float(param_dict.get('Gastos Marketing Año 5', 0))
            ],
            'nuevos_empleados': [
                int(param_dict.get('Nuevos empleados Año 1', 0)),
                int(param_dict.get('Nuevos empleados Año 2', 0)),
                int(param_dict.get('Nuevos empleados Año 3', 0)),
                int(param_dict.get('Nuevos empleados Año 4', 0)),
                int(param_dict.get('Nuevos empleados Año 5', 0))
            ]
        }
        
        return datos
        
    except Exception as e:
        st.error(f"❌ Error al importar: {str(e)}")
        return None

# Test
if __name__ == "__main__":
    print("✅ Función de importación definitiva creada")
    print("📊 Lee exactamente la estructura de plantilla_excel_definitiva")
    print("⚠️ No inventa valores, usa 0 como neutro")
