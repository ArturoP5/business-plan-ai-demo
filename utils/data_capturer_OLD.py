"""
Sistema centralizado de captura de datos para PDF con IA
Garantiza que TODOS los datos fluyan correctamente desde cualquier fuente
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any


def capturar_datos_completos() -> Dict[str, Any]:
    """
    Captura TODOS los datos disponibles en session_state
    Retorna un diccionario completo listo para PDF con IA
    """
    datos = {}
    
    # 1. DATOS DE EMPRESA (manual, demo o Excel)
    datos['info_empresa'] = {
        'nombre_empresa': st.session_state.get('nombre_empresa', 'N/A'),
        'sector': st.session_state.get('sector', 'N/A'),
        'descripcion_actividad': st.session_state.get('descripcion_actividad', 'N/A'),
        'productos_servicios': st.session_state.get('productos_servicios', 'N/A'),
        'modelo_negocio': st.session_state.get('modelo_negocio', 'N/A'),
        'posicionamiento_precio': st.session_state.get('posicionamiento_precio', 'N/A'),
        'competidores_principales': st.session_state.get('competidores_principales', 'N/A'),
        'vision_corto_plazo': st.session_state.get('vision_corto_plazo', 'N/A'),
        'vision_medio_plazo': st.session_state.get('vision_medio_plazo', 'N/A'),
        'vision_largo_plazo': st.session_state.get('vision_largo_plazo', 'N/A'),
        'ventaja_competitiva_clave': st.session_state.get('ventaja_competitiva_clave', 'N/A'),
        'principales_riesgos': st.session_state.get('principales_riesgos', 'N/A'),
        'cuota_mercado': st.session_state.get('cuota_mercado', 'N/A'),
        'clientes_objetivo': st.session_state.get('clientes_objetivo', 'N/A'),
    }
    
    # 2. DATAFRAMES FINANCIEROS
    if 'datos_guardados' in st.session_state:
        dg = st.session_state.datos_guardados
        datos['pyl_df'] = dg.get('pyl', pd.DataFrame())
        datos['balance_df'] = dg.get('balance', pd.DataFrame())
        datos['fcf_df'] = dg.get('fcf_df', pd.DataFrame())
        datos['ratios_df'] = dg.get('ratios', pd.DataFrame())
        datos['wc_df'] = dg.get('wc_df', pd.DataFrame())
    else:
        datos['pyl_df'] = pd.DataFrame()
        datos['balance_df'] = pd.DataFrame()
        datos['fcf_df'] = pd.DataFrame()
        datos['ratios_df'] = pd.DataFrame()
        datos['wc_df'] = pd.DataFrame()
    
    # 3. MÉTRICAS DE VALORACIÓN
    if 'datos_guardados' in st.session_state:
        valoracion = st.session_state.datos_guardados.get('valoracion', {})
        datos['valoracion'] = {
            'wacc': valoracion.get('wacc', 0),
            'tir': valoracion.get('tir', 0),
            'van': valoracion.get('van', 0),
            'valor_empresa': valoracion.get('valor_empresa', 0),
            'valor_equity': valoracion.get('valor_equity', 0),
            'ev_ebitda': valoracion.get('ev_ebitda', 0),
        }
    else:
        datos['valoracion'] = {}
    
    # 4. ANÁLISIS IA (si existe)
    datos['analisis_ia'] = st.session_state.get('analisis_ia_completo', {})
    
    return datos


def guardar_datos_demo(datos_demo: Dict[str, Any]) -> None:
    """
    Guarda datos de empresa demo en session_state
    con las keys correctas para que fluyan al PDF
    """
    if 'info_general' in datos_demo:
        info = datos_demo['info_general']
        
        # Guardar cada campo con su key específica
        st.session_state['nombre_empresa'] = info.get('nombre_empresa', '')
        st.session_state['sector'] = info.get('sector', '')
        st.session_state['descripcion_actividad'] = info.get('descripcion_actividad', '')
        st.session_state['productos_servicios'] = info.get('productos_servicios', '')
        st.session_state['modelo_negocio'] = info.get('modelo_negocio', '')
        st.session_state['posicionamiento_precio'] = info.get('posicionamiento_precio', '')
        st.session_state['competidores_principales'] = info.get('competidores_principales', '')
        st.session_state['vision_corto_plazo'] = info.get('vision_corto_plazo', '')
        st.session_state['vision_medio_plazo'] = info.get('vision_medio_plazo', '')
        st.session_state['vision_largo_plazo'] = info.get('vision_largo_plazo', '')
        st.session_state['ventaja_competitiva_clave'] = info.get('ventaja_competitiva_clave', '')
        st.session_state['principales_riesgos'] = info.get('principales_riesgos', '')
        st.session_state['cuota_mercado'] = info.get('cuota_mercado', '')
        st.session_state['clientes_objetivo'] = info.get('clientes_objetivo', '')
        
    # Guardar también el diccionario completo por si acaso
    st.session_state['empresa_demo_data'] = datos_demo
