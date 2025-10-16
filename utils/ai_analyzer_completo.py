#!/usr/bin/env python3
"""
Analizador de IA Completo para Informes de Valoración
Genera análisis profesional con estándares de banca de inversión
"""

import google.generativeai as genai
from typing import Dict, Any
import json
import os

class AIAnalyzerCompleto:
    def __init__(self, api_key: str = None):
        """Inicializa el analizador con la API key de Gemini"""
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def generate_complete_analysis(self, company_data: Dict, financial_data: Dict) -> Dict:
        """
        Genera análisis completo para el informe de valoración profesional
        """
        if not self.model:
            return self._get_fallback_analysis()
        
        try:
            # Preparar contexto
            context = self._prepare_context(company_data, financial_data)
            
            # Generar cada componente del análisis
            analysis = {
                'macro_analysis': self._generate_macro_analysis(context),
                'swot': self._generate_swot_analysis(context),
                'risks': self._generate_risk_assessment(context),
                'action_plan': self._generate_action_plan(context),
                'kpis': self._generate_kpis(context),
                'benchmarking': self._generate_benchmarking(context),
                'valuation_commentary': self._generate_valuation_commentary(context, financial_data)
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error en análisis IA: {e}")
            return self._get_fallback_analysis()
    
    def _prepare_context(self, company_data: Dict, financial_data: Dict) -> str:
        """Prepara el contexto para los prompts"""
        return f"""
        Empresa: {company_data.get('nombre_empresa', 'N/A')}
        Sector: {company_data.get('sector', 'N/A')}
        Modelo de negocio: {company_data.get('modelo_negocio', 'N/A')}
        Actividad: {company_data.get('descripcion_actividad', 'N/A')}
        Productos/Servicios: {company_data.get('productos_servicios', 'N/A')}
        Ventaja competitiva: {company_data.get('ventaja_competitiva_principal', 'N/A')}
        Valoración DCF: €{financial_data.get('enterprise_value', 0):,.0f}
        WACC: {financial_data.get('wacc', 0):.1f}%
        TIR: {financial_data.get('tir', 0):.1f}%
        """
    
    def _generate_macro_analysis(self, context: str) -> Dict:
        """Genera análisis macroeconómico y sectorial"""
        prompt = f"""
        Basándote en el siguiente contexto empresarial, genera un análisis macroeconómico 
        y sectorial profesional como lo haría un analista de banca de inversión:
        
        {context}
        
        El análisis debe incluir:
        1. Tendencias macroeconómicas relevantes (PIB, inflación, tipos de interés)
        2. Análisis del sector (tamaño, crecimiento, drivers)
        3. Posicionamiento competitivo
        4. Barreras de entrada y factores críticos de éxito
        
        Responde en formato JSON con la siguiente estructura:
        {{
            "analisis": "texto del análisis completo",
            "metricas_sector": {{
                "tamaño_mercado": "valor estimado",
                "crecimiento_anual": "porcentaje",
                "concentracion": "nivel"
            }},
            "tendencias": ["tendencia 1", "tendencia 2", ...]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return {'fallback': True, 'analisis': 'Análisis macroeconómico en desarrollo'}
    
    def _generate_swot_analysis(self, context: str) -> Dict:
        """Genera análisis SWOT profesional"""
        prompt = f"""
        Genera un análisis SWOT profesional para:
        
        {context}
        
        Considera aspectos internos y externos relevantes para inversores institucionales.
        Cada punto debe ser específico y accionable.
        
        Responde en formato JSON:
        {{
            "fortalezas": ["fortaleza 1", "fortaleza 2", ...],
            "debilidades": ["debilidad 1", "debilidad 2", ...],
            "oportunidades": ["oportunidad 1", "oportunidad 2", ...],
            "amenazas": ["amenaza 1", "amenaza 2", ...]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return self._get_default_swot()
    
    def _generate_risk_assessment(self, context: str) -> Dict:
        """Genera evaluación de riesgos"""
        prompt = f"""
        Genera una matriz de riesgos profesional para:
        
        {context}
        
        Identifica los 5 principales riesgos, evaluando probabilidad e impacto.
        Proporciona estrategias de mitigación específicas.
        
        Responde en formato JSON:
        {{
            "risks": [
                {{
                    "descripcion": "descripción del riesgo",
                    "probabilidad": "Alta/Media/Baja",
                    "impacto": "Alto/Medio/Bajo",
                    "mitigacion": "estrategia de mitigación"
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return {'fallback': True, 'risks': []}
    
    def _generate_action_plan(self, context: str) -> Dict:
        """Genera plan de acción estratégico"""
        prompt = f"""
        Genera un plan de acción estratégico para maximizar el valor de:
        
        {context}
        
        Divide las iniciativas en:
        - Corto plazo (0-12 meses)
        - Medio plazo (1-3 años)  
        - Largo plazo (3+ años)
        
        Responde en formato JSON:
        {{
            "corto_plazo": ["iniciativa 1", "iniciativa 2", ...],
            "medio_plazo": ["iniciativa 1", "iniciativa 2", ...],
            "largo_plazo": ["iniciativa 1", "iniciativa 2", ...]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return {'fallback': True}
    
    def _generate_kpis(self, context: str) -> Dict:
        """Genera KPIs recomendados"""
        prompt = f"""
        Recomienda 8 KPIs críticos para monitorear el desempeño de:
        
        {context}
        
        Incluye objetivos específicos y frecuencia de medición.
        
        Responde en formato JSON:
        {{
            "kpis": [
                {{
                    "nombre": "nombre del KPI",
                    "objetivo": "objetivo específico",
                    "frecuencia": "Mensual/Trimestral/Anual",
                    "responsable": "CEO/CFO/COO/CMO"
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return {'fallback': True, 'kpis': []}
    
    def _generate_benchmarking(self, context: str) -> Dict:
        """Genera análisis de benchmarking sectorial"""
        prompt = f"""
        Genera un análisis de benchmarking sectorial para:
        
        {context}
        
        Compara con las mejores prácticas del sector.
        
        Responde en formato JSON:
        {{
            "posicionamiento": "descripción del posicionamiento",
            "metricas": [
                {{
                    "metrica": "nombre",
                    "empresa": "valor empresa",
                    "media_sector": "valor sector",
                    "posicion": "Superior/Similar/Inferior"
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return {'fallback': True}
    
    def _generate_valuation_commentary(self, context: str, financial_data: Dict) -> Dict:
        """Genera comentario sobre la valoración"""
        wacc = financial_data.get('wacc', 0)
        tir = financial_data.get('tir', 0)
        
        prompt = f"""
        Genera un análisis profesional de la valoración para:
        
        {context}
        
        Con WACC de {wacc:.1f}% y TIR de {tir:.1f}%.
        
        El análisis debe incluir:
        1. Evaluación de la valoración
        2. Análisis de sensibilidad clave
        3. Comparación con múltiplos del sector
        
        Responde en formato JSON:
        {{
            "resumen": "resumen ejecutivo de la valoración",
            "fortalezas_valoracion": ["punto 1", "punto 2"],
            "consideraciones": ["consideración 1", "consideración 2"],
            "recomendacion": "COMPRAR/MANTENER/VENDER"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            return {'fallback': True}
    
    def _get_default_swot(self) -> Dict:
        """SWOT por defecto si falla la IA"""
        return {
            'fortalezas': [
                'Modelo de negocio escalable',
                'Equipo directivo con experiencia',
                'Propuesta de valor diferenciada'
            ],
            'debilidades': [
                'Recursos limitados',
                'Dependencia de mercado local',
                'Necesidad de capital adicional'
            ],
            'oportunidades': [
                'Crecimiento del mercado',
                'Digitalización del sector',
                'Expansión geográfica'
            ],
            'amenazas': [
                'Competencia intensa',
                'Cambios regulatorios',
                'Volatilidad económica'
            ]
        }
    
    def _get_fallback_analysis(self) -> Dict:
        """Análisis de respaldo si falla la IA"""
        return {
            'macro_analysis': {'fallback': True},
            'swot': self._get_default_swot(),
            'risks': {'fallback': True},
            'action_plan': {'fallback': True},
            'kpis': {'fallback': True},
            'benchmarking': {'fallback': True},
            'valuation_commentary': {'fallback': True}
        }
