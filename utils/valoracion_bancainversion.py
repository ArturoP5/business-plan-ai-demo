"""
Módulo de Valoración Profesional - Metodología Banca de Inversión
Incluye DCF, Múltiplos Comparables y Análisis de Transacciones
"""

import numpy as np
import numpy_financial as npf
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .api_data_collector import APIDataCollector

class ValoracionBancaInversion:
    """
    Sistema completo de valoración siguiendo metodología de banca de inversión
    """
    
    def __init__(self):
        # Inicializar recopilador de datos de mercado
        self.api_collector = APIDataCollector()
        
        # Datos de mercado España (actualizables vía API)
        self._actualizar_datos_mercado()
        
        self.primas_tamaño = {
            'micro': 3.0,    # < 5M€
            'pequeña': 2.0,  # 5-25M€
            'mediana': 1.0,  # 25-100M€
            'grande': 0.0    # > 100M€
        }
        
        # Descuentos por iliquidez
        self.descuento_iliquidez = {
            'alta': 0.30,    # Empresas muy pequeñas
            'media': 0.20,   # PYMEs típicas
            'baja': 0.10     # Empresas medianas con potencial salida
        }
    
    def _actualizar_datos_mercado(self):
        """Actualiza datos de mercado desde APIs"""
        try:
            datos = self.api_collector.get_datos_macroeconomicos()
            self.tasa_libre_riesgo = datos.get('euribor', 4.0) - 0.5  # Ajuste por bono soberano
            self.inflacion_esperada = datos.get('inflacion', 2.5)
            self.pib_potencial = datos.get('pib', 2.0)
        except:
            # Valores por defecto si fallan las APIs
            self.tasa_libre_riesgo = 3.5
            self.inflacion_esperada = 2.0
            self.pib_potencial = 2.0
        
        # Prima de riesgo de mercado (histórica España)
        self.prima_riesgo_mercado = 5.5  # Más acorde con mercado actual
        
        # Betas sectoriales (Damodaran + ajuste mercado español)
        self.betas_sector = {
            'tecnologia': 1.35,
            'hosteleria': 1.15,
            'ecommerce': 1.25,
            'consultoria': 1.10,
            'retail': 0.95,
            'servicios': 1.00,
            'automocion': 1.20,
            'industrial': 1.10,
            'construccion': 1.30,
            'otro': 1.00
        }
    
    def valoracion_completa(self, modelo_financiero) -> Dict:
        """
        Realiza valoración completa con múltiples metodologías
        
        Args:
            modelo_financiero: Instancia de ModeloFinanciero con proyecciones
            
        Returns:
            Dict con valoraciones por diferentes métodos
        """
        print("\n=== INICIANDO VALORACIÓN COMPLETA ===")
        print(f"Modelo: {modelo_financiero.nombre}")
        print(f"Sector: {modelo_financiero.sector}")

        # 1. Preparar datos financieros
        datos_empresa = self._preparar_datos_financieros(modelo_financiero)
        print(f"Datos preparados: {datos_empresa}")
        
        # 2. Valoración por DCF
        valoracion_dcf = self._valoracion_dcf(datos_empresa, modelo_financiero)
        
        # 3. Valoración por múltiplos
        valoracion_multiples = self._valoracion_multiples(datos_empresa, modelo_financiero)
        
        # 4. Análisis de transacciones comparables
        valoracion_transacciones = self._transacciones_comparables(datos_empresa, modelo_financiero)
        
        # 5. Resumen de valoración (Football Field Chart)
        resumen = self._generar_resumen_valoracion(
            valoracion_dcf, 
            valoracion_multiples, 
            valoracion_transacciones,
            datos_empresa,
            modelo_financiero
        )
        
        return resumen
    
    def _preparar_datos_financieros(self, modelo) -> Dict:
        """Prepara los datos financieros necesarios"""
        return {
            'ventas_actuales': modelo.ingresos_iniciales,
            'ebitda_actual': modelo.ebitda_real if hasattr(modelo, 'ebitda_real') and modelo.ebitda_real else modelo.ingresos_iniciales * (modelo.margen_ebitda_inicial / 100),
            'deuda_neta': modelo.calcular_deuda_total(1, incluir_pasivo_laboral=True) - getattr(modelo, 'tesoreria_inicial', 0),
            'sector': modelo.sector.lower(),
            'empleados': modelo.empleados,
            'crecimiento_historico': modelo.crecimiento_ventas,
            'patrimonio_neto': modelo.balance['patrimonio_neto'].iloc[-1] if hasattr(modelo, 'balance') and modelo.balance is not None else None
        }
    
    def _valoracion_dcf(self, datos: Dict, modelo) -> Dict:
        """Valoración por DCF con metodología profesional"""
        
        # 1. Calcular WACC
        wacc, componentes_wacc = self._calcular_wacc_profesional(datos, modelo)
        
        # 2. Proyectar flujos de caja libre
        fcf_proyectados = self._proyectar_fcf(modelo)
        
        # 3. Calcular tasa de crecimiento terminal
        g_terminal = self._calcular_g_terminal(datos['sector'])
        
        # 4. Calcular valor presente de flujos
        años_proyeccion = len(fcf_proyectados)
        vp_flujos = sum([fcf / (1 + wacc) ** (i + 1) 
                        for i, fcf in enumerate(fcf_proyectados)])
        
        # 5. Calcular valor terminal
        ultimo_fcf = fcf_proyectados[-1]
        valor_terminal = ultimo_fcf * (1 + g_terminal) / (wacc - g_terminal)
        vp_valor_terminal = valor_terminal / (1 + wacc) ** años_proyeccion
        
        # 6. Valor empresa y equity
        valor_empresa = vp_flujos + vp_valor_terminal
        valor_equity = valor_empresa - datos['deuda_neta']

        # 7. Calcular TIR del proyecto
        # Estimar inversión inicial basada en CAPEX promedio y sector
        # Método: Promedio del CAPEX con factor según intensidad de capital
        capex_datos = []
        for i in range(1, 4):  # Primeros 3 años
            capex_key = f'capex_año{i}'
            if capex_key in datos:
                capex_datos.append(datos[capex_key])

        if capex_datos:
            capex_promedio = sum(capex_datos) / len(capex_datos)
            
            # Factor según intensidad de capital del negocio
            # Basado en ratio CAPEX/Ventas
            ventas_actuales = datos.get('ventas_actuales', 1)
            ratio_capex_ventas = capex_promedio / ventas_actuales if ventas_actuales > 0 else 0.1
            
            # Determinar factor según intensidad
            if ratio_capex_ventas < 0.02:  # Menos del 2% (servicios, software)
                factor_inversion = 1.5
            elif ratio_capex_ventas < 0.05:  # 2-5% (retail, distribución)
                factor_inversion = 2.0
            else:  # Más del 5% (industrial, manufactura)
                factor_inversion = 2.5
            
            inversion_inicial = capex_promedio * factor_inversion
        else:
            # Fallback si no hay datos de CAPEX
            inversion_inicial = abs(fcf_proyectados[0]) * 1.5 if fcf_proyectados else 0

        print(f"DEBUG TIR - CAPEX promedio: €{capex_promedio:,.0f}" if capex_datos else "No hay datos CAPEX")
        print(f"DEBUG TIR - Ratio CAPEX/Ventas: {ratio_capex_ventas:.1%}" if capex_datos else "")
        print(f"DEBUG TIR - Factor inversión: {factor_inversion}x" if capex_datos else "")
        print(f"DEBUG TIR - Inversión inicial: €{inversion_inicial:,.0f}")

        tir_proyecto = self.calcular_tir(fcf_proyectados, inversion_inicial)

        # DEBUG
        print(f"\n=== DEBUG VALORACIÓN DCF ===")
        print(f"VP Flujos: €{vp_flujos:,.0f}")
        print(f"VP Valor Terminal: €{vp_valor_terminal:,.0f}")
        print(f"Valor Empresa: €{valor_empresa:,.0f}")
        print(f"Deuda Neta: €{datos['deuda_neta']:,.0f}")
        print(f"Valor Equity: €{valor_equity:,.0f}")
        print(f"WACC: {wacc:.2%}")
        print(f"g terminal: {g_terminal:.2%}")
        print(f"FCF proyectados: {fcf_proyectados}")
        print(f"TIR Proyecto: {tir_proyecto:.2f}%")
        
        # 8. Análisis de sensibilidad
        sensibilidad = self._sensibilidad_dcf(
            fcf_proyectados, wacc, g_terminal, datos['deuda_neta']
        )
        
        return {
            'valor_empresa': valor_empresa,
            'valor_equity': valor_equity,
            'wacc': wacc * 100,
            'g_terminal': g_terminal * 100,
            'componentes_wacc': componentes_wacc,
            'tir': tir_proyecto,
            'sensibilidad': sensibilidad,
            'vp_flujos_explicitos': vp_flujos,
            'vp_valor_terminal': vp_valor_terminal,
            'peso_valor_terminal': vp_valor_terminal / valor_empresa * 100
        }
    
    def _calcular_wacc_profesional(self, datos: Dict, modelo) -> Tuple[float, Dict]:
        """Calcula WACC con metodología de banca de inversión"""
        
        # 1. Costo del equity (CAPM + primas)
        rf = self.tasa_libre_riesgo / 100
        beta = self.betas_sector.get(datos['sector'], 1.0)
        
        # Ajuste Blume para beta
        beta_ajustado = 0.67 * beta + 0.33 * 1.0
        
        # Prima por tamaño
        prima_tamaño = self._obtener_prima_tamaño(datos['ventas_actuales'])
        
        # Prima específica empresa
        prima_especifica = self._calcular_prima_especifica(modelo)
        
        # Ke = Rf + Beta * PRM + Prima Tamaño + Prima Específica
        ke = rf + beta_ajustado * (self.prima_riesgo_mercado / 100) + prima_tamaño + prima_especifica
        
        # 2. Costo de la deuda
        kd_bruto = rf + self._obtener_spread_crediticio(modelo)
        kd = kd_bruto * (1 - modelo.tasa_impuestos / 100)
        
        # 3. Estructura de capital
        # Verificar si hay parámetros de estructura en params_avanzados
        usar_objetivo = getattr(modelo, 'usar_estructura_objetivo', None)

        # DEBUG
        print(f"\n🔍 DEBUG WACC - Estructura Capital:")
        print(f"  usar_objetivo desde modelo: {usar_objetivo}")
        print(f"  pct_deuda_objetivo desde modelo: {pct_deuda_objetivo}")

        pct_deuda_objetivo = getattr(modelo, 'pct_deuda_objetivo', None)
        
        if usar_objetivo is not False and pct_deuda_objetivo is not None:
            # Usar estructura objetivo definida por usuario
            wd = pct_deuda_objetivo
            we = 1 - wd
            print(f"  → Usando estructura OBJETIVO: {wd*100:.0f}% deuda / {we*100:.0f}% equity")
        else:
            # Calcular estructura ACTUAL del balance
            deuda_total = modelo.calcular_deuda_total()
            equity_valor = datos['ventas_actuales'] * 0.8  # Aproximación inicial
            valor_total = deuda_total + equity_valor
            
            wd = deuda_total / valor_total if valor_total > 0 else 0.3
            we = 1 - wd
            print(f"  → Usando estructura ACTUAL: {wd*100:.0f}% deuda / {we*100:.0f}% equity")
        
        # 4. WACC
        wacc = we * ke + wd * kd
        
        # DEBUG WACC
        print(f"\n=== DEBUG COMPONENTES WACC ===")
        print(f"Rf: {rf * 100:.2f}%")
        print(f"Beta ajustado: {beta_ajustado:.2f}")
        print(f"Prima mercado: {self.prima_riesgo_mercado}%")
        print(f"Prima tamaño: {prima_tamaño * 100:.2f}%")
        print(f"Prima específica: {prima_especifica * 100:.2f}%")
        print(f"Ke total: {ke * 100:.2f}%")
        print(f"Kd después impuestos: {kd * 100:.2f}%")
        print(f"We: {we * 100:.1f}%, Wd: {wd * 100:.1f}%")
        print(f"WACC final: {wacc * 100:.2f}%")
        
        componentes = {
            'ke': ke * 100,
            'kd_bruto': kd_bruto * 100,
            'kd_neto': kd * 100,
            'beta': beta,
            'beta_ajustado': beta_ajustado,
            'prima_tamaño': prima_tamaño * 100,
            'prima_especifica': prima_especifica * 100,
            'wd': wd * 100,
            'we': we * 100
        }
        
        return wacc, componentes
    
    def _obtener_prima_tamaño(self, ventas: float) -> float:
        """Determina prima por tamaño según ventas"""
        if ventas < 5_000_000:
            return self.primas_tamaño['micro'] / 100
        elif ventas < 25_000_000:
            return self.primas_tamaño['pequeña'] / 100
        elif ventas < 100_000_000:
            return self.primas_tamaño['mediana'] / 100
        else:
            return self.primas_tamaño['grande'] / 100
    
    def _calcular_prima_especifica(self, modelo) -> float:
        """Calcula prima de riesgo específica de la empresa"""
        prima = 0.0
        
        # Concentración de clientes
        if hasattr(modelo, 'concentracion_clientes'):
            if modelo.concentracion_clientes > 50:
                prima += 0.02
        
        # Antigüedad de la empresa
        años_operacion = datetime.now().year - modelo.año_fundacion
        if años_operacion < 3:
            prima += 0.03
        elif años_operacion < 5:
            prima += 0.01
        
        # Dependencia del fundador
        if modelo.empleados < 20:
            prima += 0.01  # Reducir de 2% a 1%
        
        return prima
    
    def _obtener_spread_crediticio(self, modelo) -> float:
        """Obtiene spread crediticio basado en métricas"""
        # Simplificación: basado en cobertura de intereses
        if hasattr(modelo, 'ebitda'):
            cobertura = modelo.ebitda / max(modelo.gastos_financieros, 1)
            if cobertura > 6:
                return 0.015  # 150 bps
            elif cobertura > 3:
                return 0.03   # 300 bps
            else:
                return 0.05   # 500 bps
        return 0.04  # Default 400 bps
    
    def _proyectar_fcf(self, modelo) -> List[float]:
        """Proyecta flujos de caja libre desde el modelo"""
        fcf_list = []
        
        if modelo.cash_flow is not None and 'free_cash_flow' in modelo.cash_flow:
            # Usar FCF del modelo si está disponible
            fcf_list = modelo.cash_flow['free_cash_flow'].tolist()
        else:
            # Aproximación si no hay cash flow detallado
            for año in range(5):
                ventas = modelo.ingresos_iniciales * (1 + modelo.crecimiento_ventas/100) ** año 
                
                # Aproximaciones
                impuestos = ebitda * 0.25 * 0.7  # EBIT aproximado * tax
                capex = ventas * (modelo.capex_porcentaje / 100)
                wc_cambio = ventas * 0.02  # 2% de ventas
                
                fcf = ebitda - impuestos - capex - wc_cambio
                fcf_list.append(fcf)
        
        return fcf_list
    
    def _calcular_g_terminal(self, sector: str) -> float:
        """Calcula tasa de crecimiento terminal por sector"""
        # Base: inflación esperada + ajuste sectorial
        g_base = self.inflacion_esperada / 100
        
        ajustes_sector = {
            'tecnologia': 0.01,
            'hosteleria': 0.0,
            'servicios': 0.005,
            'industrial': 0.0,
            'construccion': -0.005
        }
        
        ajuste = ajustes_sector.get(sector, 0.0)
        
        # No puede exceder PIB potencial + inflación
        g_max = (self.pib_potencial + self.inflacion_esperada) / 100
        
        return min(g_base + ajuste, g_max)
    
    def _valoracion_multiples(self, datos: Dict, modelo) -> Dict:
        """Valoración por múltiplos comparables"""

        # Obtener múltiplos del sector
        multiples_sector = self.api_collector.get_datos_cnmv(datos['sector'])
        
        # DEBUG: Ver qué múltiplos se están obteniendo
        print(f"\n=== DEBUG MÚLTIPLOS SECTOR ===")
        print(f"Sector solicitado: {datos['sector']}")
        print(f"Múltiplos obtenidos: {multiples_sector}")
        
        # Ajustar múltiplos por tamaño y crecimiento
        multiples_ajustados = self._ajustar_multiples(multiples_sector, datos, modelo)
        
        # Calcular valoraciones
        ebitda_actual = datos['ebitda_actual']
        ventas_actuales = datos['ventas_actuales']
        
        valoraciones = {
            'EV/EBITDA': {
                'multiplo': multiples_ajustados['ev_ebitda'],
                'valor_empresa': ebitda_actual * multiples_ajustados['ev_ebitda'],
                'valor_equity': ebitda_actual * multiples_ajustados['ev_ebitda'] - datos['deuda_neta']
            },
            'EV/Ventas': {
                'multiplo': multiples_ajustados['ev_ventas'],
                'valor_empresa': ventas_actuales * multiples_ajustados['ev_ventas'],
                'valor_equity': ventas_actuales * multiples_ajustados['ev_ventas'] - datos['deuda_neta']
            }
        }
        
        # Rango de valoración (±15%)
        for metodo in valoraciones:
            val = valoraciones[metodo]['valor_equity']
            valoraciones[metodo]['rango'] = {
                'minimo': val * 0.85,
                'maximo': val * 1.15
            }
        
        return valoraciones
    
    def _ajustar_multiples(self, multiples: Dict, datos: Dict, modelo) -> Dict:
        """Ajusta múltiplos por características específicas"""
        # DEBUG: Verificar qué recibe el modelo
        print(f"\n=== DEBUG MODELO EN AJUSTAR MÚLTIPLOS ===")
        print(f"Tiene margen_ebitda_real: {hasattr(modelo, 'margen_ebitda_real')}")
        if hasattr(modelo, 'margen_ebitda_real'):
            print(f"Valor margen_ebitda_real: {modelo.margen_ebitda_real}")
        
        ajustados = multiples.copy()
        
        # Ajuste por tamaño - Metodología M&A profesional
        # Basado en estudios de Duff & Phelps y Damodaran sobre liquidez
        ventas = datos['ventas_actuales']
        
        if ventas < 10_000_000:  # Micro empresas
            factor_tamaño = 0.75  # Descuento 25% por iliquidez severa
            categoria_tamaño = "Micro (<10M€)"
        elif ventas < 25_000_000:  # Pequeñas empresas  
            factor_tamaño = 0.85  # Descuento 15% por iliquidez alta
            categoria_tamaño = "Pequeña (10-25M€)"
        elif ventas < 50_000_000:  # Empresas medianas-pequeñas
            factor_tamaño = 0.95  # Descuento 5% por iliquidez moderada
            categoria_tamaño = "Mediana-pequeña (25-50M€)"
        elif ventas < 100_000_000:  # Empresas medianas
            factor_tamaño = 1.00  # Sin ajuste - tamaño óptimo para PE
            categoria_tamaño = "Mediana (50-100M€)"
        elif ventas < 250_000_000:  # Empresas medianas-grandes
            factor_tamaño = 1.05  # Prima 5% por liquidez
            categoria_tamaño = "Mediana-grande (100-250M€)"
        else:  # Grandes empresas
            factor_tamaño = 1.10  # Prima 10% por alta liquidez
            categoria_tamaño = "Grande (>250M€)"
            
        # Debug
        print(f"Categoría tamaño: {categoria_tamaño}")
        
        # Ajuste por crecimiento
        factor_crecimiento = 1.0
        if modelo.crecimiento_ventas > 10:
            factor_crecimiento = 1.2
        elif modelo.crecimiento_ventas > 5:
            factor_crecimiento = 1.1
        
        # NUEVO: Ajuste por nivel de endeudamiento (Deuda Neta / EBITDA)
        factor_deuda = 1.0
        ratio_deuda_ebitda = datos['deuda_neta'] / datos['ebitda_actual'] if datos['ebitda_actual'] > 0 else 999
        
        if ratio_deuda_ebitda < 1.0:
            factor_deuda = 1.1  # Premio por bajo endeudamiento
        elif ratio_deuda_ebitda < 2.0:
            factor_deuda = 1.0  # Neutral
        elif ratio_deuda_ebitda < 3.0:
            factor_deuda = 0.85  # Penalización moderada
        elif ratio_deuda_ebitda < 4.0:
            factor_deuda = 0.70  # Penalización significativa
        elif ratio_deuda_ebitda < 5.0:
            factor_deuda = 0.55  # Penalización severa
        else:
            factor_deuda = 0.40  # Situación crítica
        
        # NUEVO: Ajuste por margen EBITDA vs sector
        factor_margen = 1.0
        if hasattr(modelo, 'margen_ebitda_real') and modelo.margen_ebitda_real:
            # Obtener margen del sector
            margenes_sector = {
                'Hostelería': 15.0,
                'Tecnología': 25.0,
                'Ecommerce': 10.0,
                'Retail': 12.0,
                'Alimentación': 18.0,
                'Construcción': 8.0,
                'Industrial': 18.0,
                'Otro': 15.0
            }
            margen_sector = margenes_sector.get(datos.get('sector', 'Otro'), 15.0)
            
            # Calcular ratio de margen real vs sector
            ratio_margen = (modelo.margen_ebitda_real * 100) / margen_sector
            
            # Metodología profesional M&A: Ajuste continuo + percentil
            # Basado en Damodaran y prácticas de banca de inversión
            
            # 1. Ajuste continuo base (70% peso)
            # Fórmula: 0.70 + 0.30 × (margen_empresa / margen_sector)
            # Rango resultante: [0.70 - 1.60] para márgenes de 0x a 3x sector
            ajuste_continuo = 0.70 + 0.30 * min(ratio_margen, 2.0)
            
            # 2. Ajuste por percentil (30% peso)
            # Determinar en qué percentil está la empresa dentro del sector
            if ratio_margen >= 1.5:  # Top 10% - Excelencia operativa
                ajuste_percentil = 1.25
            elif ratio_margen >= 1.2:  # Top 25% - Muy eficiente
                ajuste_percentil = 1.15
            elif ratio_margen >= 0.9:  # Percentil 25-75% - Normal
                ajuste_percentil = 1.00
            elif ratio_margen >= 0.7:  # Bottom 25% - Ineficiente
                ajuste_percentil = 0.85
            else:  # Bottom 10% - Reestructuración necesaria
                ajuste_percentil = 0.70
                
            # 3. Factor final ponderado
            factor_margen = (0.70 * ajuste_continuo) + (0.30 * ajuste_percentil)
            
            # 4. Cap máximo y mínimo según estándares M&A
            factor_margen = max(0.65, min(factor_margen, 1.35))
            
            # Debug adicional para transparencia
            print(f"Ratio margen (empresa/sector): {ratio_margen:.2f}x")
            print(f"Ajuste continuo: {ajuste_continuo:.2f}, Ajuste percentil: {ajuste_percentil:.2f}")
        
        # Debug para ver los ajustes
        print(f"\n=== AJUSTES DE MÚLTIPLOS ===")
        print(f"Ratio Deuda/EBITDA: {ratio_deuda_ebitda:.2f}x")
        print(f"Ratio Deuda/EBITDA: {ratio_deuda_ebitda:.2f}x")
        if hasattr(modelo, 'margen_ebitda_real') and modelo.margen_ebitda_real:
            print(f"Margen EBITDA real: {modelo.margen_ebitda_real * 100:.1f}% vs sector: {margen_sector:.1f}%")
        print(f"Factor tamaño: {factor_tamaño}")
        print(f"Factor crecimiento: {factor_crecimiento}")
        print(f"Factor deuda: {factor_deuda}")
        print(f"Factor margen: {factor_margen}")
        
        # Aplicar todos los ajustes
        factor_total = factor_tamaño * factor_crecimiento * factor_deuda * factor_margen
        
        for key in ['ev_ebitda', 'ev_ventas', 'per']:
            if key in ajustados:
                ajustados[key] *= factor_total
                
        print(f"Factor total aplicado: {factor_total:.2f}")
        
        return ajustados
    
    def _transacciones_comparables(self, datos: Dict, modelo) -> Dict:
        """Análisis de transacciones comparables"""
        
        # Por ahora, usar múltiplos con descuento
        # En producción, aquí se conectaría a bases de datos de M&A
        
        multiples_transacciones = {
            'ev_ebitda': 7.5,  # Típico para PYMEs en España
            'ev_ventas': 1.2
        }
        
        # Ajustar por sector
        ajustes_sector = {
            'tecnologia': 1.3,
            'servicios': 0.9,
            'industrial': 0.8,
            'hosteleria': 0.7
        }
        
        factor_sector = ajustes_sector.get(datos['sector'], 1.0)
        
        valoraciones = {}
        for metrica, multiplo in multiples_transacciones.items():
            multiplo_ajustado = multiplo * factor_sector
            
            if metrica == 'ev_ebitda':
                valor_empresa = datos['ebitda_actual'] * multiplo_ajustado
            else:
                valor_empresa = datos['ventas_actuales'] * multiplo_ajustado
            
            valoraciones[metrica] = {
                'multiplo': multiplo_ajustado,
                'valor_empresa': valor_empresa,
                'valor_equity': valor_empresa - datos['deuda_neta']
            }
        
        return valoraciones
    
    def _sensibilidad_dcf(self, fcf: List[float], wacc: float, g: float, deuda: float) -> pd.DataFrame:
        """Análisis de sensibilidad bidimensional WACC vs g"""
        
        # Rangos
        wacc_rango = np.arange(wacc - 0.02, wacc + 0.021, 0.005)
        g_rango = np.arange(g - 0.01, g + 0.011, 0.005)
        
        # Crear tabla
        tabla = pd.DataFrame(
            index=[f"{w:.1%}" for w in wacc_rango],
            columns=[f"{gr:.1%}" for gr in g_rango]
        )
        
        wacc_central = wacc
        g_central = g
        
        for i, w in enumerate(wacc_rango):
            for j, gr in enumerate(g_rango):
                if w > gr:  # WACC debe ser mayor que g
                    # Calcular valor
                    vp_flujos = sum([f / (1 + w) ** (k + 1) for k, f in enumerate(fcf)])
                    valor_terminal = fcf[-1] * (1 + gr) / (w - gr)
                    vp_terminal = valor_terminal / (1 + w) ** len(fcf)
                    valor_equity = vp_flujos + vp_terminal - deuda
                    
                    tabla.iloc[i, j] = round(valor_equity / 1_000_000, 1)  # En millones
                else:
                    tabla.iloc[i, j] = "N/A"
        
        return tabla
    
    def _generar_resumen_valoracion(self, dcf: Dict, multiples: Dict, 
                                   transacciones: Dict, datos: Dict, modelo_financiero=None) -> Dict:
        """Genera resumen ejecutivo de valoración (Football Field)"""
        
        # Recopilar todos los valores
        valores = []
        
        # Determinar pesos dinámicamente según la situación financiera
        ratio_deuda_ebitda = datos['deuda_neta'] / datos['ebitda_actual'] if datos['ebitda_actual'] > 0 else 999
        dcf_es_negativo = dcf['valor_equity'] < 0
        
        # Ajustar pesos según la situación
        if dcf_es_negativo or ratio_deuda_ebitda > 4:
            # Empresa en dificultades: dar más peso al DCF
            peso_dcf = 0.6  # 60%
            peso_multiples = 0.15  # 15% cada uno (30% total)
            peso_transacciones = 0.05  # 5% cada uno (10% total)
            print("\n⚠️ Empresa en situación crítica: ajustando pesos (DCF 60%)")
        elif ratio_deuda_ebitda > 3:
            # Empresa muy endeudada: peso moderado al DCF
            peso_dcf = 0.5  # 50%
            peso_multiples = 0.175  # 17.5% cada uno (35% total)
            peso_transacciones = 0.075  # 7.5% cada uno (15% total)
            print("\n⚠️ Empresa muy endeudada: ajustando pesos (DCF 50%)")
        else:
            # Empresa normal: pesos estándar
            peso_dcf = 0.4  # 40%
            peso_multiples = 0.2  # 20% cada uno (40% total)
            peso_transacciones = 0.1  # 10% cada uno (20% total)
        
        # DCF
        valores.append({
            'metodo': 'DCF',
            'valor_central': dcf['valor_equity'],
            'valor_min': dcf['valor_equity'] * 0.9,
            'valor_max': dcf['valor_equity'] * 1.1,
            'peso': peso_dcf
        })
        
        # Múltiplos
        for metodo, datos_mult in multiples.items():
            valores.append({
                'metodo': f'Múltiplos - {metodo}',
                'valor_central': datos_mult['valor_equity'],
                'valor_min': datos_mult['rango']['minimo'],
                'valor_max': datos_mult['rango']['maximo'],
                'peso': peso_multiples
            })
        
        # Transacciones
        for metodo, datos_trans in transacciones.items():
            valores.append({
                'metodo': f'Transacciones - {metodo}',
                'valor_central': datos_trans['valor_equity'],
                'valor_min': datos_trans['valor_equity'] * 0.85,
                'valor_max': datos_trans['valor_equity'] * 1.15,
                'peso': peso_transacciones
            })
        
        # Calcular valoración ponderada
        valor_ponderado = sum([v['valor_central'] * v['peso'] for v in valores])

        # DEBUG
        print("\n=== DEBUG VALORACIÓN PONDERADA ===")
        for v in valores:
            print(f"{v['metodo']}: €{v['valor_central']:,.0f} (peso: {v['peso']*100}%)")
        print(f"Valor ponderado: €{valor_ponderado:,.0f}")
        
        # Aplicar descuento por iliquidez
        nivel_iliquidez = self._determinar_iliquidez(datos, modelo_financiero)
        descuento = self.descuento_iliquidez[nivel_iliquidez]

        # DEBUG: Imprimir info de empresa familiar
        print(f"\n=== DEBUG EMPRESA FAMILIAR ===")
        if modelo_financiero:
            print(f"¿Tiene atributo empresa_familiar?: {hasattr(modelo_financiero, 'empresa_familiar')}")
            if hasattr(modelo_financiero, 'empresa_familiar'):
                print(f"Valor empresa_familiar: {modelo_financiero.empresa_familiar}")
        print(f"Nivel iliquidez: {nivel_iliquidez}")
        print(f"Descuento aplicado: {descuento*100:.0f}%")

        valor_final = valor_ponderado * (1 - descuento)
        
        # Floor value: Valor mínimo basado en patrimonio neto
        if datos.get('patrimonio_neto') and datos['patrimonio_neto'] > 0:
            # Factor de realización: 0.8 para empresa en marcha, 0.6 si hay problemas
            factor_realizacion = 0.8 if valor_final > 0 else 0.6
            valor_liquidacion = datos['patrimonio_neto'] * factor_realizacion
            
            if valor_final < valor_liquidacion:
                print(f"\n⚠️ Aplicando floor value: Patrimonio Neto €{datos['patrimonio_neto']:,.0f} × {factor_realizacion} = €{valor_liquidacion:,.0f}")
                valor_final = valor_liquidacion
        
        # Resumen
        resumen = {
            'valoracion_final': valor_final,
            'valoracion_pre_descuento': valor_ponderado,
            'descuento_iliquidez': descuento * 100,
            'rango_valoracion': {
                'minimo': valor_final * 0.85,
                'central': valor_final,
                'maximo': valor_final * 1.15
            },
            'detalle_metodos': valores,
            'dcf_detalle': dcf,
            'multiples_detalle': multiples,
            'transacciones_detalle': transacciones,
            'football_field': self._crear_football_field(valores, valor_final),
            'conclusiones': self._generar_conclusiones(valor_final, datos, dcf)
        }
        
        return resumen
    
    def _determinar_iliquidez(self, datos: Dict, modelo=None) -> str:
        """Determina nivel de iliquidez de la empresa considerando factores múltiples"""
        ventas = datos['ventas_actuales']
        
        # Factor base por tamaño
        if ventas < 5_000_000:
            iliquidez_base = 'alta'
        elif ventas < 25_000_000:
            iliquidez_base = 'media'
        else:
            iliquidez_base = 'baja'
            
        # Ajuste por empresa familiar
        if modelo and hasattr(modelo, 'empresa_familiar') and modelo.empresa_familiar == "Sí":
            # Empresa familiar aumenta la iliquidez un nivel
            if iliquidez_base == 'baja':
                return 'media'
            elif iliquidez_base == 'media':
                return 'alta'
        
        return iliquidez_base
    
    def _crear_football_field(self, valores: List[Dict], valor_final: float) -> Dict:
        """Crea datos para gráfico Football Field"""
        football_field = {
            'metodos': [],
            'valores_min': [],
            'valores_central': [],
            'valores_max': [],
            'valor_final': valor_final
        }
        
        for v in valores:
            football_field['metodos'].append(v['metodo'])
            football_field['valores_min'].append(v['valor_min'] / 1_000_000)
            football_field['valores_central'].append(v['valor_central'] / 1_000_000)
            football_field['valores_max'].append(v['valor_max'] / 1_000_000)
        
        return football_field
    
    def _generar_conclusiones(self, valor: float, datos: Dict, dcf: Dict) -> List[str]:
        """Genera conclusiones ejecutivas"""
        conclusiones = []
        
        # Valoración general
        valor_mm = valor / 1_000_000
        conclusiones.append(
            f"La valoración de la empresa se sitúa en €{valor_mm:.1f}M, "
            f"con un rango entre €{valor_mm*0.85:.1f}M y €{valor_mm*1.15:.1f}M"
        )
        
        # Múltiplo implícito
        ev_ebitda_implicito = (valor + datos['deuda_neta']) / datos['ebitda_actual']
        conclusiones.append(
            f"Esto implica un múltiplo EV/EBITDA de {ev_ebitda_implicito:.1f}x, "
            f"en línea con empresas comparables del sector"
        )
        
        # Peso del valor terminal
        if dcf['peso_valor_terminal'] > 75:
            conclusiones.append(
                f"⚠️ El {dcf['peso_valor_terminal']:.0f}% del valor proviene del valor terminal, "
                "sugiriendo alta sensibilidad a supuestos de largo plazo"
            )
        
        # WACC
        conclusiones.append(
            f"El WACC utilizado es {dcf['wacc']:.1f}%, reflejando el perfil de "
            f"riesgo de una PYME del sector {datos['sector']}"
        )
        
        return conclusiones

    def calcular_tir(self, flujos_caja: List[float], inversion_inicial: float = 0) -> float:
        """
        Calcula la TIR (Tasa Interna de Retorno) del proyecto
        """
        try:
            print(f"\nDEBUG calcular_tir:")
            print(f"  - Flujos recibidos: {flujos_caja}")
            print(f"  - Inversión inicial: {inversion_inicial}")
            
            # Si hay inversión inicial, añadirla como flujo negativo
            if inversion_inicial > 0:
                flujos_tir = [-inversion_inicial] + flujos_caja
            else:
                # Asumir que el primer flujo es negativo (inversión)
                flujos_tir = flujos_caja
            
            print(f"  - Flujos para TIR: {flujos_tir}")
            
            # Calcular TIR
            tir = npf.irr(flujos_tir)
            print(f"  - TIR cruda: {tir}")
            
            # Convertir a porcentaje y manejar casos especiales
            if np.isnan(tir) or np.isinf(tir):
                print(f"  - TIR es NaN o Inf, devolviendo 0")
                return 0.0
            
            resultado = float(tir * 100)  # Convertir a porcentaje
            print(f"  - TIR final: {resultado}%")
            
            return resultado
            
        except Exception as e:
            print(f"ERROR calculando TIR: {e}")
            return 0.0

# Funciones de utilidad para integración
def realizar_valoracion_profesional(modelo_financiero) -> Dict:
    """
    Función principal para realizar valoración profesional
    
    Args:
        modelo_financiero: Instancia de ModeloFinanciero con proyecciones
        
    Returns:
        Dict con resultados completos de valoración
    """
    valorador = ValoracionBancaInversion()
    return valorador.valoracion_completa(modelo_financiero)
