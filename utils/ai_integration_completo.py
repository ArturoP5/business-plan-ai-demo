"""
Módulo mejorado de integración con APIs de IA para análisis empresarial completo
Soporta: Gemini, GPT-4, Claude 3
Incluye: SWOT, Benchmarking, Matriz de Riesgos, KPIs, Plan de Acción
"""

import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import anthropic
import json
import re
from typing import Dict, Optional, Any, List

class AIAnalyzerCompleto:
    """Clase mejorada para análisis completo con IA"""
    
    def __init__(self):
        self.models = {
            'gemini': self.setup_gemini,
            'openai': self.setup_gpt4,
            'claude': self.setup_claude
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
    
    def generate_complete_analysis(self, datos_empresa: Dict, datos_financieros: Dict) -> Dict:
        """Genera análisis completo con todas las secciones"""
        
        analysis = {}
        
        # 1. SWOT
        analysis['swot'] = self.generate_swot(datos_empresa)
        
        # 2. Investment Thesis
        analysis['investment_thesis'] = self.generate_investment_thesis(datos_empresa, datos_financieros)
        
        # 3. Benchmarking
        analysis['benchmarking'] = self.generate_benchmarking(datos_empresa)
        
        # 4. Risk Matrix
        analysis['risk_matrix'] = self.generate_risk_matrix(datos_empresa)
        
        # 5. Valuation Commentary
        analysis['valuation_commentary'] = self.generate_valuation_commentary(datos_financieros)
        
        # 6. Recommended KPIs
        analysis['recommended_kpis'] = self.generate_kpis(datos_empresa)
        
        # 7. Action Plan
        analysis['action_plan'] = self.generate_action_plan(datos_empresa)
        
        return analysis
    
    def generate_swot(self, company_data: Dict) -> Dict:
        """Genera análisis SWOT detallado"""
        
        prompt = f"""
        Analiza la siguiente empresa y genera un análisis SWOT profesional:
        
        EMPRESA: {company_data.get('nombre_empresa', 'No especificado')}
        SECTOR: {company_data.get('sector', 'No especificado')}
        DESCRIPCIÓN: {company_data.get('descripcion_actividad', 'No especificado')}
        PRODUCTOS: {company_data.get('productos_servicios', 'No especificado')}
        VENTAJA COMPETITIVA: {company_data.get('ventaja_competitiva_principal', 'No especificado')}
        COMPETIDORES: {company_data.get('competidores_principales', 'No especificado')}
        CUOTA MERCADO: {company_data.get('cuota_mercado', 0)}%
        
        Genera un SWOT en formato JSON:
        {{
            "fortalezas": ["Fortaleza 1", "Fortaleza 2", "Fortaleza 3", "Fortaleza 4"],
            "debilidades": ["Debilidad 1", "Debilidad 2", "Debilidad 3"],
            "oportunidades": ["Oportunidad 1", "Oportunidad 2", "Oportunidad 3"],
            "amenazas": ["Amenaza 1", "Amenaza 2", "Amenaza 3"]
        }}
        
        RESPONDE SOLO CON JSON VÁLIDO.
        """
        
        return self._execute_prompt(prompt)
    
    def generate_benchmarking(self, company_data: Dict) -> Dict:
        """Genera análisis de benchmarking sectorial"""
        
        prompt = f"""
        Realiza un benchmarking sectorial para:
        
        EMPRESA: {company_data.get('nombre_empresa')}
        SECTOR: {company_data.get('sector')}
        CUOTA MERCADO: {company_data.get('cuota_mercado', 0)}%
        COMPETIDORES: {company_data.get('competidores_principales')}
        
        Genera el análisis en JSON:
        {{
            "posicionamiento": "Descripción del posicionamiento competitivo",
            "comparacion": [
                {{"metrica": "Cuota de mercado", "empresa": "X%", "sector": "Y%", "posicion": "Superior/Inferior"}},
                {{"metrica": "Margen EBITDA", "empresa": "X%", "sector": "Y%", "posicion": "Superior/Inferior"}},
                {{"metrica": "Crecimiento", "empresa": "X%", "sector": "Y%", "posicion": "Superior/Inferior"}},
                {{"metrica": "Eficiencia", "empresa": "X", "sector": "Y", "posicion": "Superior/Inferior"}}
            ],
            "ventajas_competitivas": ["Ventaja 1", "Ventaja 2"],
            "areas_mejora": ["Área 1", "Área 2"]
        }}
        
        RESPONDE SOLO CON JSON VÁLIDO.
        """
        
        return self._execute_prompt(prompt)
    
    def generate_risk_matrix(self, company_data: Dict) -> Dict:
        """Genera matriz de riesgos detallada"""
        
        prompt = f"""
        Crea una matriz de riesgos para:
        
        EMPRESA: {company_data.get('nombre_empresa')}
        SECTOR: {company_data.get('sector')}
        RIESGOS IDENTIFICADOS: {company_data.get('principales_riesgos')}
        
        Genera la matriz en JSON con 5 riesgos principales:
        {{
            "risks": [
                {{
                    "descripcion": "Descripción del riesgo",
                    "probabilidad": "Alta/Media/Baja",
                    "impacto": "Alto/Medio/Bajo",
                    "mitigacion": "Estrategia de mitigación"
                }}
            ]
        }}
        
        RESPONDE SOLO CON JSON VÁLIDO.
        """
        
        return self._execute_prompt(prompt)
    
    def generate_valuation_commentary(self, financial_data: Dict) -> Dict:
        """Genera comentario sobre la valoración DCF"""
        
        prompt = f"""
        Analiza la siguiente valoración:
        
        VALOR EMPRESA (DCF): €{financial_data.get('enterprise_value', 0):,.0f}
        WACC: {financial_data.get('wacc', 0):.1%}
        TIR: {financial_data.get('tir', 0):.1%}
        PAYBACK: {financial_data.get('payback', 0)} años
        
        Genera análisis en JSON:
        {{
            "analisis": "Análisis detallado de la valoración (2-3 párrafos)",
            "sensibilidad": "Análisis de sensibilidad y variables clave",
            "rango_valor": "Rango de valoración recomendado",
            "confianza": "Alta/Media/Baja"
        }}
        
        RESPONDE SOLO CON JSON VÁLIDO.
        """
        
        return self._execute_prompt(prompt)
    
    def generate_kpis(self, company_data: Dict) -> Dict:
        """Genera KPIs recomendados para seguimiento"""
        
        prompt = f"""
        Recomienda KPIs para:
        
        EMPRESA: {company_data.get('nombre_empresa')}
        SECTOR: {company_data.get('sector')}
        MODELO NEGOCIO: {company_data.get('modelo_negocio')}
        
        Genera 8 KPIs principales en JSON:
        {{
            "kpis": [
                {{
                    "nombre": "Nombre del KPI",
                    "objetivo": "Valor objetivo",
                    "frecuencia": "Mensual/Trimestral/Anual",
                    "responsable": "CEO/CFO/CMO/COO"
                }}
            ]
        }}
        
        RESPONDE SOLO CON JSON VÁLIDO.
        """
        
        return self._execute_prompt(prompt)
    
    def generate_action_plan(self, company_data: Dict) -> Dict:
        """Genera plan de acción prioritizado"""
        
        prompt = f"""
        Crea un plan de acción para:
        
        EMPRESA: {company_data.get('nombre_empresa')}
        VISIÓN CORTO PLAZO: {company_data.get('vision_corto_plazo')}
        VISIÓN MEDIO PLAZO: {company_data.get('vision_medio_plazo')}
        VISIÓN LARGO PLAZO: {company_data.get('vision_largo_plazo')}
        
        Genera el plan en JSON:
        {{
            "corto_plazo": ["Acción 1 (Q1)", "Acción 2 (Q1)", "Acción 3 (Q2)"],
            "medio_plazo": ["Acción 1 (Año 2)", "Acción 2 (Año 2-3)"],
            "largo_plazo": ["Acción 1 (3-5 años)", "Acción 2 (5+ años)"]
        }}
        
        RESPONDE SOLO CON JSON VÁLIDO.
        """
        
        return self._execute_prompt(prompt)
    
    def generate_investment_thesis(self, company_data: Dict, financial_data: Dict) -> Dict:
        """Genera tesis de inversión completa"""
        
        prompt = f"""
        Genera una tesis de inversión para:
        
        EMPRESA: {company_data.get('nombre_empresa')}
        VALORACIÓN DCF: €{financial_data.get('enterprise_value', 0):,.0f}
        TIR: {financial_data.get('tir', 0):.1%}
        PAYBACK: {financial_data.get('payback', 0)} años
        
        Genera en JSON:
        {{
            "resumen_ejecutivo": "Resumen de 2-3 líneas",
            "puntos_clave_inversion": ["Punto 1", "Punto 2", "Punto 3"],
            "recomendacion": "COMPRAR/MANTENER/VENDER",
            "horizonte_inversion": "Corto/Medio/Largo plazo",
            "retorno_esperado": "X-Y% anual"
        }}
        
        RESPONDE SOLO CON JSON VÁLIDO.
        """
        
        return self._execute_prompt(prompt)
    
    def _execute_prompt(self, prompt: str) -> Optional[Dict]:
        """Ejecuta el prompt según el modelo configurado"""
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
            st.error(f"Error ejecutando análisis: {str(e)}")
            return self._get_fallback_response()
    
    def _parse_response(self, text: str) -> Dict:
        """Extrae y valida JSON de la respuesta"""
        try:
            # Limpiar el texto
            text = text.strip()
            
            # Buscar JSON en el texto
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            
            return self._get_fallback_response()
            
        except Exception as e:
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> Dict:
        """Respuesta por defecto si falla la IA"""
        return {
            "error": "No se pudo generar el análisis",
            "fallback": True
        }
