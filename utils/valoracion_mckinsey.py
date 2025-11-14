"""
Implementación del modelo de valoración McKinsey DCF
Basado en "Valuation: Measuring and Managing the Value of Companies"
"""

import pandas as pd
import numpy as np
from utils.api_data_collector import APIDataCollector
import numpy_financial as npf
from typing import Dict, Tuple

class ValoracionMcKinsey:
    """Modelo de valoración DCF según metodología McKinsey"""
    
    # Betas sectoriales basados en Damodaran
    BETAS_SECTORIALES = {
        "Hostelería": 1.15,
        "Tecnología": 1.35,
        "Ecommerce": 1.25,
        "Consultoría": 1.10,
        "Retail": 1.05,
        "Servicios": 0.95,
        "Automoción": 1.20,
        "Industrial": 1.10,
        "Otro": 1.00
    }
    
    def __init__(self, modelo_financiero):
        self.modelo = modelo_financiero
        self.sector = modelo_financiero.sector
        self.beta = self.BETAS_SECTORIALES.get(self.sector, 1.0)
        
        # Primas de riesgo país (fallback si API falla)
        self.PRIMAS_PAIS = {
            'España': 0.005,
            'Alemania': 0.0,
            'Francia': 0.003,
            'Italia': 0.012,
            'Portugal': 0.008,
            'Reino Unido': 0.004,
            'Estados Unidos': 0.002
        }
        
        # Primas de riesgo sector
        self.PRIMAS_SECTOR = {
            'Retail': 0.010,
            'Hostelería': 0.015,
            'Tecnología': 0.005,
            'Industrial': 0.008,
            'Ecommerce': 0.012,
            'Servicios': 0.007,
            'Consultoría': 0.006,
            'Automoción': 0.010
        }
    
    def calcular_wacc_mckinsey(self, params_mercado: Dict = None) -> Tuple[float, Dict]:
        """
        Calcula WACC usando CAPM y estructura óptima de capital
        """
        if params_mercado is None:
            params_mercado = {
                'tasa_libre_riesgo': 0.03,
                'prima_mercado': 0.065,
                'costo_deuda_bruta': 0.06
            }
        
        # Cost of Equity (CAPM + Size Premium)
        rf = params_mercado['tasa_libre_riesgo']
        rm_rf = params_mercado['prima_mercado']
        
        # Prima por tamaño (empresas <10M€)
        size_premium = 0.02 if self.modelo.ingresos_iniciales < 10000000 else 0
        
        # Riesgo país desde FRED API
        pais = self.modelo.pais if hasattr(self.modelo, 'pais') else 'España'
        try:
            api_collector = APIDataCollector()
            riesgo_pais = api_collector.get_spread_bonos_pais(pais)
        except Exception as e:
            print(f"⚠️  Error obteniendo spread FRED: {e}, usando fallback")
            riesgo_pais = self.PRIMAS_PAIS.get(pais, 0.005)
        
        # Riesgo sector
        riesgo_sector = self.PRIMAS_SECTOR.get(self.sector, 0.008)
        
        # CAPM completo
        cost_of_equity = rf + self.beta * rm_rf + size_premium + riesgo_pais + riesgo_sector
        
        # Prima adicional conservadora para PYMEs
        if self.modelo.ingresos_iniciales < 250000000:  # Empresas <250M€
            prima_pyme = 0.01  # 1% adicional
            cost_of_equity += prima_pyme        
        # Cost of Debt
        rd = params_mercado['costo_deuda_bruta']
        tax_rate = self.modelo.tasa_impuestos / 100
        cost_of_debt_after_tax = rd * (1 - tax_rate)
        
        # Estructura de capital objetivo por sector
        target_debt_ratios = {
            "Industrial": 0.40,
            "Tecnología": 0.20,
            "Retail": 0.35,
            "Hostelería": 0.45,
            "Servicios": 0.30
        }
        
        # Verificar si el modelo tiene parámetros de estructura definidos por el usuario
        usar_objetivo = getattr(self.modelo, 'usar_estructura_objetivo', None)
        pct_deuda_obj = getattr(self.modelo, 'pct_deuda_objetivo', None)
        
        if usar_objetivo is not False and pct_deuda_obj is not None:
            # Usar estructura objetivo del usuario
            target_d_v = pct_deuda_obj
            target_e_v = 1 - target_d_v
            print(f"  ✓ WACC usa estructura OBJETIVO del usuario: {target_d_v*100:.0f}% deuda / {target_e_v*100:.0f}% equity")
        else:
            # Calcular estructura ACTUAL del balance
            if hasattr(self.modelo, 'balance') and self.modelo.balance is not None:
                deuda_total = self.modelo.calcular_deuda_total()
                patrimonio = self.modelo.balance['patrimonio_neto'].iloc[-1]
                total = deuda_total + patrimonio
                target_d_v = deuda_total / total if total > 0 else 0.0
                target_e_v = 1 - target_d_v
                print(f"  ✓ WACC usa estructura ACTUAL: {target_d_v*100:.0f}% deuda / {target_e_v*100:.0f}% equity")
            else:
                # Fallback: estructura del sector
                target_d_v = target_debt_ratios.get(self.sector, 0.30)
                target_e_v = 1 - target_d_v
                print(f"  ⚠ WACC usa estructura SECTOR (fallback): {target_d_v*100:.0f}% deuda")
        
        # WACC
        wacc = target_e_v * cost_of_equity + target_d_v * cost_of_debt_after_tax
        
        componentes = {
            'cost_of_equity': cost_of_equity,
            'cost_of_debt_after_tax': cost_of_debt_after_tax,
            'beta': self.beta,
            'rf': rf,
            'prima_mercado': rm_rf,
            'size_premium': size_premium,
            'riesgo_pais': riesgo_pais,
            'riesgo_sector': riesgo_sector,
            'prima_pyme': prima_pyme if self.modelo.ingresos_iniciales < 250000000 else 0,
            'weights': {'equity': target_e_v, 'debt': target_d_v}
        }
        
        return wacc, componentes
    
    def calcular_noplat(self, año: int) -> float:
        """
        Calcula NOPLAT (Net Operating Profit Less Adjusted Taxes)
        Usa impuestos_operativos del P&L (sobre EBIT, no BAI)
        """
        ebit = self.modelo.pyl[self.modelo.pyl['año'] == año]['ebit'].values[0]
        impuestos_op = self.modelo.pyl[self.modelo.pyl['año'] == año]['impuestos_operativos'].values[0]
        noplat = ebit - impuestos_op
        return noplat
    def calcular_invested_capital(self, año: int) -> float:
        """
        Calcula el capital invertido
        """
        balance = self.modelo.balance[self.modelo.balance['año'] == año]
        
        # Operating Working Capital
        working_capital = (
            balance['clientes'].values[0] +
            balance['inventario'].values[0] -
            balance['proveedores'].values[0]
        )
        
        # Net PP&E
        fixed_assets = balance['activo_fijo_neto'].values[0]
        
        # Total Invested Capital
        invested_capital = working_capital + fixed_assets
        
        return invested_capital
    
    def calcular_fcf_mckinsey(self, año: int) -> Dict:
        """
        Calcula FCF según metodología McKinsey
        FCF = NOPLAT + Non-cash charges - Investment in Invested Capital
        """
        # NOPLAT
        noplat = self.calcular_noplat(año)
        
        # Add back depreciation (non-cash charge)
        depreciation = self.modelo.pyl[self.modelo.pyl['año'] == año]['amortizacion'].values[0]
        
        # Calculate change in invested capital
        ic_current = self.calcular_invested_capital(año)
        
        if año > 1:
            ic_previous = self.calcular_invested_capital(año - 1)
            delta_ic = ic_current - ic_previous
        else:
            # Para año 1, usar el cambio vs año 0
            wc_inicial = (
                self.modelo.clientes_inicial +
                self.modelo.otros_deudores_inicial +
                self.modelo.admin_publica_deudora_inicial +
                self.modelo.inventario_inicial -
                self.modelo.proveedores_inicial
            )
            activo_fijo_inicial = self.modelo.activo_fijo_neto_inicial
            ic_inicial = wc_inicial + activo_fijo_inicial
            delta_ic = ic_current - ic_inicial
        
        # FCF = NOPLAT - Change in Invested Capital
        # Delta IC ya incluye CAPEX neto de depreciación (Δ AFN = CAPEX - D&A)
        fcf = noplat - delta_ic
        
        # Calculate ROIC
        roic = noplat / ic_previous if año > 1 and ic_previous > 0 else noplat / ic_current
        
        return {
            'fcf': fcf,
            'noplat': noplat,
            'invested_capital': ic_current,
            'delta_ic': delta_ic,
            'roic': roic * 100  # En porcentaje
        }
    
    def valorar_empresa(self, params_mercado: Dict = None) -> Dict:
        """
        Realiza valoración completa usando metodología McKinsey
        """
        # 1. Calcular WACC
        wacc, componentes_wacc = self.calcular_wacc_mckinsey(params_mercado)
        
        fcf_data = []
        for año in range(1, 6):  # 5 años de proyección
            fcf_año = self.calcular_fcf_mckinsey(año)
            fcf_data.append(fcf_año)
        
        # 3. Calcular valor presente de FCF proyectados
        pv_fcf = sum([
            fcf_data[i]['fcf'] / (1 + wacc) ** (i + 1)
            for i in range(5)
        ])
        
        # 4. Valor Terminal (usando Gordon Growth)
        ultimo_noplat = fcf_data[-1]['noplat']
        ultimo_ic = fcf_data[-1]['invested_capital']
        roic_terminal = fcf_data[-1]['roic'] / 100
        # Ajustar ROIC terminal a niveles sostenibles (WACC + 2-3pp máximo)
        roic_sostenible = wacc + 0.025  # WACC + 2.5pp
        roic_terminal = min(roic_terminal, roic_sostenible)        # Tasa de crecimiento terminal por sector
        g_terminal_sector = {
            "Industrial": 0.015,  # 2.0% - Sector maduro
            "Tecnología": 0.030,  # 3.0% - Mayor crecimiento
            "Hostelería": 0.025,  # 2.5% - Crecimiento moderado
            "Retail": 0.020,     # 2.0% - Sector maduro
            "Ecommerce": 0.028,  # 2.8% - Digital en crecimiento
            "Servicios": 0.025,  # 2.5% - Crecimiento estable
            "Consultoría": 0.025, # 2.5% - Servicios profesionales
            "Automoción": 0.018, # 1.8% - Sector en transición
            "Otro": 0.022        # 2.2% - Promedio conservador
        }
        g_terminal = g_terminal_sector.get(self.sector, 0.022)
        
        # Valor terminal = NOPLAT_t+1 * (1 - g/ROIC) / (WACC - g)
        if roic_terminal > g_terminal:
            valor_terminal = (
                ultimo_noplat * (1 + g_terminal) * (1 - g_terminal/roic_terminal) /
                (wacc - g_terminal)
            )
        else:
            # Si ROIC < g, usar método alternativo
            valor_terminal = ultimo_noplat * 10  # Múltiplo conservador
        
        pv_terminal = valor_terminal / (1 + wacc) ** 5
        
        # 5. Enterprise Value
        enterprise_value = pv_fcf + pv_terminal
        
        
        deuda_neta = self.modelo.calcular_deuda_total(0, incluir_pasivo_laboral=False) - self.modelo.tesoreria_inicial
        print(f"🔍 DEBUG: Deuda Total={self.modelo.calcular_deuda_total(0, incluir_pasivo_laboral=False):,.0f}, Tesorería={self.modelo.tesoreria_inicial:,.0f}, Deuda Neta={deuda_neta:,.0f}")
        equity_value = enterprise_value - deuda_neta
        
        # Calcular TIR del proyecto (retorno sobre equity)
        # TIR = tasa donde NPV de flujos al equity = equity_value
        # Flujos al equity = FCF - servicio deuda + nueva deuda
        
        # Para simplificar, usamos FCF libre (asumiendo estructura deuda constante)
        flujos_equity = []
        for i, fcf in enumerate(fcf_data):
            # Año 1-5: FCF operativo disponible para equity
            flujos_equity.append(fcf["fcf"])
        
        # Año 5: Agregar valor terminal
        flujos_equity[-1] += valor_terminal
        
        print(f"  Flujos Equity para TIR: {[f'€{f:,.0f}' for f in flujos_equity]}")
        
        try:
            # TIR sobre equity_value como inversión
            if equity_value > 0:
                flujos_tir_completos = [-equity_value] + flujos_equity
                tir = npf.irr(flujos_tir_completos) * 100
                print(f"  TIR sobre Equity: {tir:.2f}%")
            else:
                # Si equity es negativo, calcular TIR solo de flujos operativos
                tir = npf.irr(flujos_equity) * 100
                print(f"  TIR operativa (sin inversión): {tir:.2f}%")
            
            if np.isnan(tir) or tir < -100 or tir > 1000:
                # Si TIR no converge, usar aproximación ROIC
                roic_avg = np.mean([f['roic'] for f in fcf_data])
                tir = roic_avg
                print(f"  TIR no convergió, usando ROIC promedio: {tir:.2f}%")
        except Exception as e:
            print(f"  Error calculando TIR: {e}")
            # Usar ROIC como proxy
            tir = np.mean([f['roic'] for f in fcf_data])
        return {
            'enterprise_value': enterprise_value,
            'equity_value': equity_value,
            'fcf_proyectados': fcf_data,
            'pv_fcf': pv_fcf,
            'valor_terminal': valor_terminal,
            'pv_terminal': pv_terminal,
            'wacc': wacc * 100,  # En porcentaje
            'componentes_wacc': componentes_wacc,
            'deuda_neta': deuda_neta,
            'roic_promedio': np.mean([f['roic'] for f in fcf_data]),
            'tir': tir,        }
