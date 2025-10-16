#!/usr/bin/env python3
"""
Data Collector para Informe de Valoración con IA
Recopila TODA la información disponible de forma estructurada
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional

def _extraer_valor_escalar(df_o_dict, key, default=0):
    """Extrae valor escalar de DataFrame o dict"""
    if df_o_dict is None:
        return default
    
    # Si es DataFrame de pandas
    if hasattr(df_o_dict, 'empty'):
        if df_o_dict.empty:
            return default
        if key in df_o_dict.columns:
            val = df_o_dict[key].iloc[0] if len(df_o_dict) > 0 else default
            return float(val) if val is not None else default
        return default
    
    # Si es dict normal
    return df_o_dict.get(key, default)


def recopilar_datos_completos() -> Dict[str, Any]:
    """
    Recopila TODA la información disponible para el análisis de IA
    
    Returns:
        Dict con toda la información estructurada en categorías
    """
    
    datos = st.session_state.get('datos_guardados', {})
    
    # ============================================
    # 1. INFORMACIÓN BÁSICA DE LA EMPRESA
    # ============================================
    info_basica = {
        'nombre_empresa': datos.get('nombre_empresa', 'Empresa'),
        'sector': datos.get('sector', 'N/A'),
        'fecha_informe': datetime.now().strftime('%d/%m/%Y'),
        'escenario_seleccionado': st.session_state.get('escenario_seleccionado', 'Base')
    }
    
    # ============================================
    # 2. DESCRIPCIÓN CUALITATIVA DEL NEGOCIO
    # ============================================
    descripcion_negocio = {
        'descripcion_actividad': st.session_state.get('descripcion_actividad_sidebar', 'N/A'),
        'modelo_negocio': st.session_state.get('modelo_negocio', 'N/A'),
        'productos_servicios': st.session_state.get('productos_servicios_sidebar', datos.get('info_general', {}).get('productos_servicios', datos.get('datos_empresa', {}).get('productos_servicios', 'N/A'))),
        'posicionamiento_precio': st.session_state.get('posicionamiento_precio', 'N/A'),
        'competidores_principales': st.session_state.get('competidores_principales', 'N/A'),
        'ventaja_competitiva_clave': st.session_state.get('ventaja_competitiva_clave', 'N/A'),
        'clientes_objetivo': st.session_state.get('clientes_objetivo_sidebar', datos.get('info_general', {}).get('clientes_objetivo', datos.get('datos_empresa', {}).get('clientes_objetivo', 'N/A'))),
        'cuota_mercado': st.session_state.get('cuota_mercado_sidebar', datos.get('info_general', {}).get('cuota_mercado', datos.get('datos_empresa', {}).get('cuota_mercado', st.session_state.get('cuota_mercado', 'N/A')))),
        'principales_riesgos': st.session_state.get('principales_riesgos', datos.get('datos_empresa', {}).get('principales_riesgos', 'N/A'))
    }
    
    # ============================================
    # 3. VISIÓN ESTRATÉGICA
    # ============================================
    vision_estrategica = {
        'corto_plazo': st.session_state.get('vision_corto_plazo', 'N/A'),
        'medio_plazo': st.session_state.get('vision_medio_plazo', 'N/A'),
        'largo_plazo': st.session_state.get('vision_largo_plazo', 'N/A'),
        'principales_riesgos': st.session_state.get('principales_riesgos', 'N/A')
    }
    
    # ============================================
    # 4. DATOS FINANCIEROS COMPLETOS
    # ============================================
    
    # P&L proyectado
    pyl_df = datos.get('pyl')
    pyl_dict = None
    if pyl_df is not None and isinstance(pyl_df, pd.DataFrame):
        pyl_dict = pyl_df.to_dict('records')
    
    # Balance proyectado
    balance_df = datos.get('balance')
    balance_dict = None
    if balance_df is not None and isinstance(balance_df, pd.DataFrame):
        balance_dict = balance_df.to_dict('records')
    
    # Cash Flow proyectado
    cashflow_df = datos.get('cash_flow')
    cashflow_dict = None
    if cashflow_df is not None and isinstance(cashflow_df, pd.DataFrame):
        cashflow_dict = cashflow_df.to_dict('records')
    
    datos_financieros = {
        'pyl': pyl_dict,
        'balance': balance_dict,
        'cash_flow': cashflow_dict,
        'proyecciones_anos': 5
    }
    
    # ============================================
    # 5. MÉTRICAS CLAVE DE VALORACIÓN
    # ============================================
    resultado_mckinsey = datos.get('resultado_mckinsey', {})
    
    
    metricas_valoracion = {
        'enterprise_value': resultado_mckinsey.get('enterprise_value', 0),
        'equity_value': resultado_mckinsey.get('equity_value', 0),
        'wacc': resultado_mckinsey.get('wacc', 0),
        'tir': resultado_mckinsey.get('tir', 0),
        'roic_promedio': resultado_mckinsey.get('roic_promedio', 0),
        'deuda_neta': resultado_mckinsey.get('deuda_neta', 0),
        'fcf_5anos': resultado_mckinsey.get('pv_fcf', 0),
        'valor_terminal': resultado_mckinsey.get('pv_terminal', 0),
        'tasa_crecimiento_perpetuo': resultado_mckinsey.get('g_terminal', resultado_mckinsey.get('wacc', 0) * 0.6)
    }
    
    # ============================================
    # 6. KPIs FINANCIEROS DETALLADOS
    # ============================================
    ratios = datos.get('ratios', {})
    
    # Calcular KPIs adicionales si no están disponibles
    kpis_financieros = {
        # Rentabilidad
        'roic': resultado_mckinsey.get('roic_promedio', 0),
        'roe': _extraer_valor_escalar(ratios, 'roe_%', 0),
        'margen_ebitda_year1': 0,  # Calcularemos después del P&L
        'margen_ebitda_year5': 0,
        'margen_neto_year1': 0,
        'margen_neto_year5': 0,
        
        # Eficiencia
        'rotacion_activos': _extraer_valor_escalar(ratios, 'rotacion_activos', 0),
        'dias_cobro': datos.get('datos_empresa', {}).get('dias_cobro', st.session_state.get('dias_cobro', 60)),
        'dias_pago': datos.get('datos_empresa', {}).get('dias_pago', st.session_state.get('dias_pago', 30)),
        'dias_inventario': datos.get('datos_empresa', {}).get('dias_stock', st.session_state.get('dias_inventario', 45)),
        'cash_conversion_cycle': 0,  # Calcularemos
        
        # Solvencia
        'deuda_neta_ebitda': 0,  # Calcularemos
        'cobertura_intereses': _extraer_valor_escalar(ratios, 'cobertura_intereses', 0),
        'ratio_liquidez': _extraer_valor_escalar(ratios, 'ratio_liquidez', 0),
        
        # Crecimiento
        'cagr_ventas': 0,  # Calcularemos del P&L
        'cagr_ebitda': 0
    }
    
    # Calcular algunos KPIs si tenemos el P&L
    if pyl_df is not None and len(pyl_df) > 0:
        try:
            # Márgenes año 1 y año 5
            if 'EBITDA %' in pyl_df.columns:
                kpis_financieros['margen_ebitda_year1'] = pyl_df['EBITDA %'].iloc[0]
                kpis_financieros['margen_ebitda_year5'] = pyl_df['EBITDA %'].iloc[-1]
            
            if 'Beneficio Neto %' in pyl_df.columns:
                kpis_financieros['margen_neto_year1'] = pyl_df['Beneficio Neto %'].iloc[0]
                kpis_financieros['margen_neto_year5'] = pyl_df['Beneficio Neto %'].iloc[-1]
            
            # CAGR de ventas
            if 'Ventas' in pyl_df.columns:
                ventas_year1 = pyl_df['Ventas'].iloc[0]
                ventas_year5 = pyl_df['Ventas'].iloc[-1]
                if ventas_year1 > 0:
                    kpis_financieros['cagr_ventas'] = ((ventas_year5 / ventas_year1) ** (1/4) - 1) * 100
            
            # CAGR de EBITDA
            if 'EBITDA' in pyl_df.columns:
                ebitda_year1 = pyl_df['EBITDA'].iloc[0]
                ebitda_year5 = pyl_df['EBITDA'].iloc[-1]
                if ebitda_year1 > 0:
                    kpis_financieros['cagr_ebitda'] = ((ebitda_year5 / ebitda_year1) ** (1/4) - 1) * 100
        except:
            pass
    
    # Cash Conversion Cycle
    if kpis_financieros['dias_cobro'] and kpis_financieros['dias_inventario'] and kpis_financieros['dias_pago']:
        kpis_financieros['cash_conversion_cycle'] = (
            kpis_financieros['dias_cobro'] + 
            kpis_financieros['dias_inventario'] - 
            kpis_financieros['dias_pago']
        )
    
    # Deuda Neta / EBITDA
    if pyl_df is not None and 'EBITDA' in pyl_df.columns and len(pyl_df) > 0:
        ebitda_year1 = pyl_df['EBITDA'].iloc[0]
        if ebitda_year1 > 0:
            kpis_financieros['deuda_neta_ebitda'] = metricas_valoracion['deuda_neta'] / ebitda_year1
    
    # ============================================
    # 7. ESTRUCTURA DE COSTES Y APALANCAMIENTO
    # ============================================
    estructura_costes = {
        'porcentaje_costes_fijos': datos.get('datos_empresa', {}).get('porcentaje_fijos', 80),
        'porcentaje_costes_variables': datos.get('datos_empresa', {}).get('porcentaje_variables', 20),
        'sector': info_basica['sector']
    }
    
    # ============================================
    # 8. MODELO DE IA USADO
    # ============================================
    ia_info = {
        'modelo': st.session_state.get('ia_selected', 'gemini'),
        'fecha_generacion': datetime.now().strftime('%d/%m/%Y %H:%M')
    }
    
    # ============================================
    # RETORNAR TODO ESTRUCTURADO
    # ============================================
    return {
        'info_basica': info_basica,
        'descripcion_negocio': descripcion_negocio,
        'vision_estrategica': vision_estrategica,
        'info_empresa': datos.get('datos_empresa', {}),
        'datos_financieros': datos_financieros,
        'metricas_valoracion': metricas_valoracion,
        'kpis_financieros': kpis_financieros,
        'estructura_costes': estructura_costes,
        'ia_info': ia_info
    }


def obtener_resumen_datos(datos_completos: Dict[str, Any]) -> str:
    """
    Genera un resumen legible de los datos recopilados
    Útil para debugging
    """
    resumen = []
    resumen.append("=" * 60)
    resumen.append("RESUMEN DE DATOS RECOPILADOS")
    resumen.append("=" * 60)
    
    # Info básica
    ib = datos_completos['info_basica']
    resumen.append(f"\n📊 EMPRESA: {ib['nombre_empresa']}")
    resumen.append(f"   Sector: {ib['sector']}")
    resumen.append(f"   Escenario: {ib['escenario_seleccionado']}")
    
    # Métricas clave
    mv = datos_completos['metricas_valoracion']
    resumen.append(f"\n💰 VALORACIÓN:")
    resumen.append(f"   Enterprise Value: €{mv['enterprise_value']:,.0f}")
    resumen.append(f"   WACC: {mv['wacc']:.1f}%")
    resumen.append(f"   TIR: {mv['tir']:.1f}%")
    resumen.append(f"   ROIC promedio: {mv['roic_promedio']:.1f}%")
    
    # KPIs
    kpi = datos_completos['kpis_financieros']
    resumen.append(f"\n📈 KPIs CLAVE:")
    resumen.append(f"   CAGR Ventas: {kpi['cagr_ventas']:.1f}%")
    resumen.append(f"   Margen EBITDA (Y1→Y5): {kpi['margen_ebitda_year1']:.1f}% → {kpi['margen_ebitda_year5']:.1f}%")
    
    resumen.append("\n" + "=" * 60)
    
    return "\n".join(resumen)
