# utils/ai_integration.py
"""
Módulo de integración con APIs de IA para análisis empresarial
Soporta: Gemini, GPT-4, Claude 3
"""

import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import anthropic
import json
import re
from typing import Dict, Optional, Any

class AIAnalyzer:
    """Clase principal para análisis con IA"""
    
    def __init__(self):
        self.models = {
            'Gemini Pro (Gratis)': self.setup_gemini,
            'GPT-4 (Potente)': self.setup_gpt4,
            'Claude 3 (Detallado)': self.setup_claude
        }
        self.current_model = None
        self.client = None
    
    def setup_gemini(self, api_key: str) -> bool:
        """Configura Gemini Pro"""
        try:
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel('gemini-2.0-flash')
            self.current_model = 'gemini'
            return True
        except Exception as e:
            st.error(f"Error configurando Gemini: {str(e)}")
            return False
    
    def setup_gpt4(self, api_key: str) -> bool:
        """Configura GPT-4"""
        try:
            self.client = OpenAI(api_key=api_key)
            self.current_model = 'gpt4'
            return True
        except Exception as e:
            st.error(f"Error configurando GPT-4: {str(e)}")
            return False
    
    def setup_claude(self, api_key: str) -> bool:
        """Configura Claude 3"""
        try:
            self.client = anthropic.Anthropic(api_key=api_key)
            self.current_model = 'claude'
            return True
        except Exception as e:
            st.error(f"Error configurando Claude: {str(e)}")
            return False
    
    def generate_swot(self, company_data: Dict[str, Any]) -> Optional[Dict]:
        """Genera análisis SWOT basado en los datos de la empresa"""
        
        # Construir prompt detallado
        prompt = f"""
        Analiza la siguiente empresa y genera un análisis SWOT profesional y detallado:
        
        DATOS DE LA EMPRESA:
        - Nombre: {company_data.get('nombre_empresa', 'No especificado')}
        - Sector: {company_data.get('sector', 'No especificado')}
        - Modelo de Negocio: {company_data.get('modelo_negocio', 'No especificado')}
        - Descripción: {company_data.get('descripcion_actividad', 'No especificado')}
        - Productos/Servicios: {company_data.get('productos_servicios', 'No especificado')}
        - Ventaja Competitiva: {company_data.get('ventaja_competitiva_principal', 'No especificado')}
        - Competidores: {company_data.get('competidores_principales', 'No especificado')}
        - Cuota de Mercado: {company_data.get('cuota_mercado', 0)}%
        - Clientes Objetivo: {company_data.get('clientes_objetivo', 'No especificado')}
        - Visión Corto Plazo: {company_data.get('vision_corto', 'No especificado')}
        - Visión Largo Plazo: {company_data.get('vision_largo', 'No especificado')}
        - Principales Riesgos: {company_data.get('principales_riesgos', 'No especificado')}
        
        INSTRUCCIONES:
        Genera un análisis SWOT específico y relevante para esta empresa.
        Devuelve SOLO un JSON válido con esta estructura exacta:
        {{
            "fortalezas": [
                "Fortaleza específica 1",
                "Fortaleza específica 2",
                "Fortaleza específica 3",
                "Fortaleza específica 4"
            ],
            "debilidades": [
                "Debilidad específica 1",
                "Debilidad específica 2",
                "Debilidad específica 3",
                "Debilidad específica 4"
            ],
            "oportunidades": [
                "Oportunidad específica 1",
                "Oportunidad específica 2",
                "Oportunidad específica 3",
                "Oportunidad específica 4"
            ],
            "amenazas": [
                "Amenaza específica 1",
                "Amenaza específica 2",
                "Amenaza específica 3",
                "Amenaza específica 4"
            ]
        }}
        
        Sé específico y relevante al sector y modelo de negocio. 
        Cada punto debe ser concreto y accionable, no genérico.
        RESPONDE SOLO CON EL JSON, sin texto adicional.
        """
        
        try:
            if self.current_model == 'gemini':
                response = self.client.generate_content(prompt)
                return self._parse_response(response.text)
            
            elif self.current_model == 'gpt4':
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un consultor estratégico experto. Responde solo con JSON válido."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                return self._parse_response(response.choices[0].message.content)
            
            elif self.current_model == 'claude':
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000,
                    temperature=0.7
                )
                return self._parse_response(response.content[0].text)
                
        except Exception as e:
            st.error(f"Error generando SWOT: {str(e)}")
            return None
    
    def generate_strategic_recommendations(self, company_data: Dict[str, Any]) -> Optional[Dict]:
        """Genera recomendaciones estratégicas basadas en los datos"""
        
        prompt = f"""
        Basándote en los siguientes datos de la empresa, genera 5 recomendaciones estratégicas específicas:
        
        EMPRESA: {company_data.get('nombre_empresa')}
        SECTOR: {company_data.get('sector')}
        MODELO: {company_data.get('modelo_negocio')}
        VENTAJA COMPETITIVA: {company_data.get('ventaja_competitiva_principal')}
        RIESGOS: {company_data.get('principales_riesgos')}
        VISIÓN: {company_data.get('vision_largo', '')}
        
        Devuelve SOLO un JSON con esta estructura:
        {{
            "recomendaciones": [
                {{
                    "titulo": "Título de la recomendación",
                    "descripcion": "Descripción detallada",
                    "plazo": "Corto/Medio/Largo",
                    "impacto": "Alto/Medio/Bajo",
                    "prioridad": 1
                }}
            ]
        }}
        
        RESPONDE SOLO CON JSON VÁLIDO.
        """
        
        try:
            if self.current_model == 'gemini':
                response = self.client.generate_content(prompt)
                return self._parse_response(response.text)
            
            elif self.current_model == 'gpt4':
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1500
                )
                return self._parse_response(response.choices[0].message.content)
            
            elif self.current_model == 'claude':
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500
                )
                return self._parse_response(response.content[0].text)
                
        except Exception as e:
            st.error(f"Error generando recomendaciones: {str(e)}")
            return None
    
    
    def analyze_financial_projections(self, financial_data: Dict[str, Any]) -> Optional[Dict]:
        """Analiza las proyecciones financieras completas: P&L, Balance, FCF, Métricas"""
        
        # Extraer datos de McKinsey si están disponibles
        fcf_data = financial_data.get('fcf_proyectados', [])
        noplat_values = [f.get('noplat', 0) for f in fcf_data] if fcf_data else []
        fcf_values = [f.get('fcf', 0) for f in fcf_data] if fcf_data else []
        roic_values = [f.get('roic', 0) for f in fcf_data] if fcf_data else []
        
        prompt = f"""
        Realiza un análisis financiero exhaustivo de la empresa basándote en los siguientes datos:
        
        VALORACIÓN DCF MCKINSEY:
        - Enterprise Value: €{financial_data.get('enterprise_value', 0):,.0f}
        - Equity Value: €{financial_data.get('equity_value', 0):,.0f}
        - WACC: {financial_data.get('wacc', 0):.1f}%
        - TIR del Proyecto: {financial_data.get('tir', 0):.1f}%
        - ROIC Promedio: {financial_data.get('roic_promedio', 0):.1f}%
        
        PROYECCIONES P&L (5 años):
        - NOPLAT por año: {noplat_values}
        - Márgenes operativos esperados
        - Evolución de costes
        
        FREE CASH FLOW PROYECTADO:
        - FCF por año: {fcf_values}
        - Valor Presente FCF: €{financial_data.get('pv_fcf', 0):,.0f}
        - Valor Terminal: €{financial_data.get('valor_terminal', 0):,.0f}
        
        MÉTRICAS DE RENTABILIDAD:
        - ROIC por año: {roic_values}%
        - Comparación ROIC vs WACC
        - Creación/destrucción de valor
        
        ESTRUCTURA DE CAPITAL:
        - Deuda Neta: €{financial_data.get('deuda_neta', 0):,.0f}
        - Ratio D/E objetivo
        
        Genera un análisis profesional detallado en JSON con estas secciones:
        {{
            "analisis_valoracion": "Análisis detallado de la valoración DCF y si el precio es atractivo",
            "analisis_pyl": "Evolución esperada del P&L, márgenes y rentabilidad operativa",
            "analisis_fcf": "Análisis de la generación de caja y su sostenibilidad",
            "analisis_roic_wacc": "Análisis de creación de valor: ROIC vs WACC",
            "analisis_estructura_capital": "Análisis del apalancamiento y estructura de capital",
            "metricas_clave": {{
                "cagr_ventas": "XX%",
                "margen_ebitda_promedio": "XX%",
                "fcf_yield": "XX%",
                "payback": "X años"
            }},
            "fortalezas_financieras": [
                "Fortaleza específica 1 basada en los números",
                "Fortaleza específica 2",
                "Fortaleza específica 3"
            ],
            "riesgos_financieros": [
                "Riesgo específico 1 basado en los números",
                "Riesgo específico 2",
                "Riesgo específico 3"
            ],
            "recomendacion_inversion": "COMPRAR/MANTENER/VENDER con justificación",
            "precio_objetivo": "Rango de valoración justa basada en DCF",
            "conclusiones": "Síntesis ejecutiva del análisis financiero completo"
        }}
        
        Sé muy específico y basa todo en los números proporcionados.
        RESPONDE SOLO CON JSON VÁLIDO.
        """
        
        try:
            if self.current_model == 'gemini':
                response = self.client.generate_content(prompt)
                return self._parse_response(response.text)
            
            elif self.current_model == 'gpt4':
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1500
                )
                return self._parse_response(response.choices[0].message.content)
            
            elif self.current_model == 'claude':
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500
                )
                return self._parse_response(response.content[0].text)
                
        except Exception as e:
            st.error(f"Error analizando proyecciones: {str(e)}")
            return None
    
    def generate_investment_thesis(self, company_data: Dict, financial_data: Dict, valuation_data: Dict) -> Optional[Dict]:
        """Genera una tesis de inversión completa"""
        
        prompt = f"""
        Genera una TESIS DE INVERSIÓN profesional basada en:
        
        EMPRESA: {company_data.get('nombre_empresa')}
        SECTOR: {company_data.get('sector')}
        
        VALORACIÓN:
        - Valor Empresa (DCF): €{valuation_data.get('enterprise_value', 0):,.0f}
        - Múltiplo EV/EBITDA: {valuation_data.get('ev_ebitda_multiple', 0):.1f}x
        - TIR del Proyecto: {valuation_data.get('tir', 0):.1%}
        - Payback: {valuation_data.get('payback', 0)} años
        
        MÉTRICAS CLAVE:
        - Crecimiento Ventas (CAGR 5 años): {financial_data.get('ventas_cagr', 0):.1%}
        - Margen EBITDA Año 5: {financial_data.get('ebitda_margin_y5', 0):.1%}
        - ROE Proyectado: {financial_data.get('roe', 0):.1%}
        - Deuda/EBITDA: {financial_data.get('deuda_ebitda', 0):.1f}x
        
        Genera una tesis de inversión en JSON:
        {{
            "resumen_ejecutivo": "Resumen de 2-3 líneas de la oportunidad",
            "puntos_clave_inversion": [
                "Punto clave 1",
                "Punto clave 2", 
                "Punto clave 3",
                "Punto clave 4"
            ],
            "catalizadores": ["Catalizador 1", "Catalizador 2", "Catalizador 3"],
            "riesgos_principales": ["Riesgo 1", "Riesgo 2", "Riesgo 3"],
            "retorno_esperado": "Descripción del retorno potencial",
            "horizonte_inversion": "Horizonte temporal recomendado",
            "recomendacion": "COMPRAR/MANTENER/VENDER",
            "precio_objetivo": "Rango de valoración objetivo"
        }}
        
        RESPONDE SOLO CON JSON VÁLIDO.
        """
        
        try:
            if self.current_model == 'gemini':
                response = self.client.generate_content(prompt)
                return self._parse_response(response.text)
            
            elif self.current_model == 'gpt4':
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1500
                )
                return self._parse_response(response.choices[0].message.content)
            
            elif self.current_model == 'claude':
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500
                )
                return self._parse_response(response.content[0].text)
                
        except Exception as e:
            st.error(f"Error generando investment thesis: {str(e)}")
            return None
    

    def _parse_response(self, text: str) -> Optional[Dict]:
        """Extrae y valida JSON de la respuesta de texto"""
        try:
            # Limpiar el texto
            text = text.strip()
            
            # Intentar parsear directamente
            try:
                return json.loads(text)
            except:
                pass
            
            # Buscar JSON en el texto
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                # Limpiar caracteres problemáticos
                json_str = json_str.replace('\n', ' ').replace('\r', '')
                return json.loads(json_str)
            
            # Si no encuentra JSON, intentar construirlo desde el texto
            st.warning("No se pudo parsear la respuesta como JSON, usando respuesta en texto")
            return {"respuesta_texto": text}
            
        except Exception as e:
            st.error(f"Error parseando respuesta: {str(e)}")
            return None
