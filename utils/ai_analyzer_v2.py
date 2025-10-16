#!/usr/bin/env python3
"""
AI Analyzer V2 - Análisis profundo con IA para informe de valoración
Integra data_collector y ai_prompts para generar análisis completo
"""

import json
import re
from typing import Dict, Any, Optional
import google.generativeai as genai
from anthropic import Anthropic
from openai import OpenAI

from .data_collector import recopilar_datos_completos
from .ai_prompts import (
    generar_prompt_executive_summary,
    generar_prompt_macro_sectorial,
    generar_prompt_swot,
    generar_prompt_kpis_detalle,
    generar_prompt_riesgos,
    generar_prompt_recomendaciones
)


class AIAnalyzerV2:
    """
    Analizador de IA V2 con análisis profundo y especializado
    """
    
    def __init__(self, modelo: str = "gemini", api_key: Optional[str] = None):
        """
        Inicializa el analizador
        
        Args:
            modelo: 'gemini', 'claude', o 'openai'
            api_key: API key del servicio (opcional si está en session_state)
        """
        self.modelo = modelo.lower()
        self.api_key = api_key
        
        # Configurar cliente según el modelo
        if self.modelo == "gemini":
            if api_key:
                genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel('gemini-2.5-flash')
        elif self.modelo == "claude":
            self.client = Anthropic(api_key=api_key)
        elif self.modelo == "openai":
            self.client = OpenAI(api_key=api_key)
        else:
            raise ValueError(f"Modelo no soportado: {modelo}")
    
    
    def _llamar_ia(self, prompt: str) -> str:
        """
        Realiza la llamada a la IA según el modelo configurado
        
        Args:
            prompt: Texto del prompt
            
        Returns:
            Respuesta de la IA en texto
        """
        try:
            if self.modelo == "gemini":
                response = self.client.generate_content(prompt)
                return response.text
            
            elif self.modelo == "claude":
                message = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            
            elif self.modelo == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4000
                )
                return response.choices[0].message.content
            
        except Exception as e:
            return json.dumps({"error": f"Error en llamada a IA: {str(e)}"})
    
    
    def _extraer_json(self, texto: str) -> Dict[str, Any]:
        """
        Extrae JSON de la respuesta de la IA (puede venir con markdown)
        
        Args:
            texto: Respuesta de la IA
            
        Returns:
            Diccionario parseado
        """
        # Eliminar bloques de código markdown si existen
        texto = re.sub(r'```json\s*', '', texto)
        texto = re.sub(r'```\s*', '', texto)
        texto = texto.strip()
        
        try:
            return json.loads(texto)
        except json.JSONDecodeError:
            # Si falla, intentar extraer el JSON del texto
            match = re.search(r'\{.*\}', texto, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
            
            return {"error": "No se pudo parsear JSON", "texto_crudo": texto}
    
    
    def generar_analisis_completo(self) -> Dict[str, Any]:
        """
        Genera análisis completo usando todos los prompts especializados
        
        Returns:
            Diccionario con todos los análisis generados
        """
        # Recopilar todos los datos disponibles
        datos_completos = recopilar_datos_completos()
        
        print("🤖 Iniciando análisis con IA...")
        print(f"   Modelo: {self.modelo}")
        print(f"   Empresa: {datos_completos['info_basica']['nombre_empresa']}")
        
        analisis = {
            "datos_base": datos_completos,
            "modelo_ia": self.modelo
        }
        
        # 1. Executive Summary
        print("\n📊 Generando Executive Summary...")
        prompt_exec = generar_prompt_executive_summary(datos_completos)
        respuesta_exec = self._llamar_ia(prompt_exec)
        analisis["executive_summary"] = self._extraer_json(respuesta_exec)
        
        # 2. Análisis Macro y Sectorial
        print("🌍 Generando Análisis Macroeconómico y Sectorial...")
        prompt_macro = generar_prompt_macro_sectorial(datos_completos)
        respuesta_macro = self._llamar_ia(prompt_macro)
        analisis["macro_sectorial"] = self._extraer_json(respuesta_macro)
        
        # 3. SWOT
        print("⚡ Generando Análisis SWOT...")
        prompt_swot = generar_prompt_swot(datos_completos)
        respuesta_swot = self._llamar_ia(prompt_swot)
        analisis["swot"] = self._extraer_json(respuesta_swot)
        
        # 4. KPIs Detallados
        print("📈 Generando Análisis de KPIs...")
        prompt_kpis = generar_prompt_kpis_detalle(datos_completos)
        respuesta_kpis = self._llamar_ia(prompt_kpis)
        analisis["kpis_detalle"] = self._extraer_json(respuesta_kpis)
        
        # 5. Análisis de Riesgos
        print("⚠️  Generando Análisis de Riesgos...")
        prompt_riesgos = generar_prompt_riesgos(datos_completos)
        respuesta_riesgos = self._llamar_ia(prompt_riesgos)
        analisis["riesgos"] = self._extraer_json(respuesta_riesgos)
        
        # 6. Recomendaciones Estratégicas
        print("🎯 Generando Recomendaciones Estratégicas...")
        prompt_recom = generar_prompt_recomendaciones(datos_completos)
        respuesta_recom = self._llamar_ia(prompt_recom)
        analisis["recomendaciones"] = self._extraer_json(respuesta_recom)
        
        print("\n✅ Análisis completo generado exitosamente")
        
        return analisis
    
    
    def generar_resumen_analisis(self, analisis: Dict[str, Any]) -> str:
        """
        Genera un resumen legible del análisis para debugging
        """
        resumen = []
        resumen.append("=" * 80)
        resumen.append("RESUMEN DEL ANÁLISIS GENERADO POR IA")
        resumen.append("=" * 80)
        
        # Executive Summary
        if "executive_summary" in analisis and "recomendacion" in analisis["executive_summary"]:
            exec_sum = analisis["executive_summary"]
            resumen.append(f"\n📊 RECOMENDACIÓN: {exec_sum.get('recomendacion', 'N/A')}")
            resumen.append(f"   Rating: {exec_sum.get('rating', 'N/A')}")
        
        # SWOT
        if "swot" in analisis and "fortalezas" in analisis["swot"]:
            swot = analisis["swot"]
            resumen.append(f"\n⚡ SWOT:")
            resumen.append(f"   Fortalezas: {len(swot.get('fortalezas', []))} identificadas")
            resumen.append(f"   Oportunidades: {len(swot.get('oportunidades', []))} identificadas")
        
        # Riesgos
        if "riesgos" in analisis and "riesgos" in analisis["riesgos"]:
            riesgos = analisis["riesgos"]
            resumen.append(f"\n⚠️  RIESGOS:")
            resumen.append(f"   Total identificados: {len(riesgos.get('riesgos', []))}")
            resumen.append(f"   Nivel global: {riesgos.get('nivel_riesgo_global', 'N/A')}")
        
        # Recomendaciones
        if "recomendaciones" in analisis:
            recom = analisis["recomendaciones"]
            resumen.append(f"\n🎯 RECOMENDACIONES:")
            resumen.append(f"   Quick Wins: {len(recom.get('quick_wins', []))}")
            resumen.append(f"   Medio Plazo: {len(recom.get('medio_plazo', []))}")
            resumen.append(f"   Largo Plazo: {len(recom.get('largo_plazo', []))}")
        
        resumen.append("\n" + "=" * 80)
        
        return "\n".join(resumen)


# Función de conveniencia para uso directo
def generar_analisis_ia(modelo: str = "gemini", api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Función de conveniencia para generar análisis completo
    
    Args:
        modelo: 'gemini', 'claude', o 'openai'
        api_key: API key del servicio
        
    Returns:
        Diccionario con análisis completo
    """
    analyzer = AIAnalyzerV2(modelo=modelo, api_key=api_key)
    return analyzer.generar_analisis_completo()

