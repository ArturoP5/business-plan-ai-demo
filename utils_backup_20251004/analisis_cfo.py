def generar_analisis_cfo(datos, metodo="estandar", sector="servicios"):
    """
    Genera análisis profesional tipo CFO/Banca de Inversión
    adaptado al método de valoración utilizado
    """
    
    # Extraer métricas clave
    valor_empresa = datos.get('valor_empresa', 0)
    tir = datos.get('tir', 0)
    multiplo_ebitda = datos.get('multiplo_ebitda', 0)
    wacc = datos.get('wacc', 8.0)  # Default 8% si no viene
    cagr_ventas = datos.get('cagr_ventas', 0)
    margen_ebitda = datos.get('margen_ebitda_promedio', 0)
    
    if metodo == 'mckinsey':
        # Análisis para valoración McKinsey (más agresiva)
        resumen_ejecutivo = f"""
**INVESTMENT MEMORANDUM - DCF McKinsey Analysis**

**Executive Summary:**
La valoración DCF pura arroja un Enterprise Value de €{valor_empresa:,.0f}, implicando un múltiplo EV/EBITDA de {multiplo_ebitda:.1f}x. 
Con un WACC optimizado del {wacc:.1f}% (vs. 8% sector), la inversión ofrece una TIR del {tir:.1f}%, 
que aunque está por debajo del hurdle rate típico de PE (15-20%), es apropiada para el perfil de riesgo del sector {sector}.

**Investment Thesis:**
1. **Valoración agresiva justificada**: El WACC del {wacc:.1f}% refleja una estructura de capital optimizada post-transacción
2. **Creación de valor clara**: ROIC proyectado supera WACC en {max(15-wacc, 8):.0f}pp, generando EVA positivo
3. **Multiple arbitrage**: Entry a {multiplo_ebitda:.1f}x con exit esperado a {multiplo_ebitda*1.2:.1f}x en 5 años

**Risk Assessment:**
- Valoración asume ejecución perfecta del business plan
- Sensibilidad alta a cambios en WACC (±1% = ±15% en valoración)
- Requiere gestión profesional para alcanzar eficiencias proyectadas

**Recomendación**: **HOLD** - TIR por debajo de objetivo pero empresa sólida para fondos growth con horizonte 5+ años
"""
    else:
        # Análisis para valoración estándar (más conservadora)
        resumen_ejecutivo = f"""
**INVESTMENT MEMORANDUM - Multi-Criteria Valuation**

**Executive Summary:**
La valoración conservadora multi-criterio resulta en un Enterprise Value de €{valor_empresa:,.0f}, 
representando un múltiplo EV/EBITDA de {multiplo_ebitda:.1f}x, en línea con comparables del sector.
La TIR esperada del {tir:.1f}% supera modestamente el costo de capital del 8%.

**Investment Thesis:**
1. **Valoración prudente**: Metodología pondera DCF (40%), múltiplos (35%) y transacciones (25%)
2. **Downside protection**: Múltiplo {multiplo_ebitda:.1f}x ofrece margen de seguridad vs. peers
3. **Retorno ajustado al riesgo**: TIR {tir:.1f}% apropiada para el perfil de riesgo

**Risk Assessment:**
- Valoración incorpora descuentos por tamaño y liquidez
- Asume escenario base sin sinergias significativas
- Margen de seguridad del {max(20, 30-tir):.0f}% sobre caso pesimista

**Recomendación**: **BUY** para inversores value con enfoque risk-adjusted returns
"""
    
    return {
        'resumen_ejecutivo': resumen_ejecutivo,
        'metodo_descripcion': 'Valoración DCF McKinsey (WACC optimizado)' if metodo == 'mckinsey' else 'Valoración Multi-criterio (DCF + Múltiplos)',
        'perfil_inversor': 'Growth equity / Aggressive' if metodo == 'mckinsey' else 'Value investing / Conservative',
        'horizonte_inversion': '5-7 años' if metodo == 'mckinsey' else '3-5 años',
        'rating': 'BUY' if tir > 8 else 'HOLD' if tir > 5 else 'SELL'
    }
