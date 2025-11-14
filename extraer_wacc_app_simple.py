"""
Extraer componentes WACC - Versión Simplificada
"""
import sys

# Mock mínimo del modelo
class MockModelo:
    def __init__(self):
        self.ingresos_iniciales = 2_715_239
        self.tasa_crecimiento = 0.05
        self.margen_ebitda = 0.133
        self.tasa_impositiva = 0.25
        self.sector = "Industrial"

# Importar solo lo necesario
sys.path.insert(0, 'utils')
from valoracion_mckinsey import ValoracionMcKinsey

modelo = MockModelo()

# Params completos que usa la app
params_mck = {
    'tasa_libre_riesgo': 0.03,
    'prima_mercado': 0.055,
    'costo_deuda_bruta': 0.04,  # 4% coste deuda
    'tasa_impositiva': 0.25,
    'g_terminal': 0.02,
    'target_equity_weight': 0.70,
    'target_debt_weight': 0.30
}

try:
    valorador = ValoracionMcKinsey(modelo)
    wacc, componentes = valorador.calcular_wacc_mckinsey(params_mck)

    print("=" * 80)
    print("COMPONENTES WACC - APP")
    print("=" * 80)

    print(f"\n📊 COSTE DE EQUITY (Ke):")
    print(f"  Risk-free (Rf):           {componentes['rf']*100:>6.2f}%")
    print(f"  Beta sectorial:           {componentes['beta']:>6.2f}")
    print(f"  Prima Mercado:            {componentes['prima_mercado']*100:>6.2f}%")
    print(f"  Beta × Prima:             {(componentes['beta'] * componentes['prima_mercado'])*100:>6.2f}%")
    print(f"  Prima Tamaño:             {componentes['size_premium']*100:>6.2f}%")
    print(f"  Prima PYME:               {componentes.get('prima_pyme', 0)*100:>6.2f}%")
    print(f"  Riesgo País:              {componentes['riesgo_pais']*100:>6.2f}%")
    print(f"  Riesgo Sector:            {componentes['riesgo_sector']*100:>6.2f}%")
    print(f"  ─────────────────────────────────")
    print(f"  Ke TOTAL:                 {componentes['cost_of_equity']*100:>6.2f}%")

    print(f"\n💰 COSTE DE DEUDA (Kd):")
    print(f"  Kd antes tax:             {params_mck['costo_deuda_bruta']*100:>6.2f}%")
    print(f"  Kd después tax (25%):     {componentes['cost_of_debt_after_tax']*100:>6.2f}%")

    print(f"\n⚖️ ESTRUCTURA CAPITAL:")
    print(f"  Peso Equity:              {componentes['weights']['equity']*100:>6.1f}%")
    print(f"  Peso Deuda:               {componentes['weights']['debt']*100:>6.1f}%")

    print(f"\n📈 WACC FINAL:")
    print(f"  WACC:                     {wacc*100:>6.2f}%")

    print("\n" + "=" * 80)
    print("COMPARACIÓN CON MI CÁLCULO:")
    print("=" * 80)

    mi_rf = 3.5
    mi_beta = 1.1
    mi_prima_mercado = 5.5
    mi_prima_tamano = 2.0
    mi_riesgo_sector = 0.5
    mi_ke = 12.05
    mi_wacc = 9.45

    print(f"\n{'Componente':<25} {'APP':<12} {'MI CÁLCULO':<12} {'DIFERENCIA':<15}")
    print("-" * 70)
    print(f"{'Rf':<25} {componentes['rf']*100:>6.2f}%      {mi_rf:>6.2f}%      {(componentes['rf']*100 - mi_rf):>+6.2f}pp")
    print(f"{'Beta':<25} {componentes['beta']:>6.2f}       {mi_beta:>6.2f}       {(componentes['beta'] - mi_beta):>+6.2f}")
    print(f"{'Prima Mercado':<25} {componentes['prima_mercado']*100:>6.2f}%      {mi_prima_mercado:>6.2f}%      {(componentes['prima_mercado']*100 - mi_prima_mercado):>+6.2f}pp")
    print(f"{'Prima Tamaño':<25} {componentes['size_premium']*100:>6.2f}%      {mi_prima_tamano:>6.2f}%      {(componentes['size_premium']*100 - mi_prima_tamano):>+6.2f}pp")
    print(f"{'Riesgo Sector':<25} {componentes['riesgo_sector']*100:>6.2f}%      {mi_riesgo_sector:>6.2f}%      {(componentes['riesgo_sector']*100 - mi_riesgo_sector):>+6.2f}pp")
    print(f"{'Ke TOTAL':<25} {componentes['cost_of_equity']*100:>6.2f}%      {mi_ke:>6.2f}%      {(componentes['cost_of_equity']*100 - mi_ke):>+6.2f}pp")
    print(f"{'WACC':<25} {wacc*100:>6.2f}%      {mi_wacc:>6.2f}%      {(wacc*100 - mi_wacc):>+6.2f}pp")

    print("\n" + "=" * 80)
    print("🎯 CONCLUSIÓN:")
    print("=" * 80)
    diferencia_wacc = wacc*100 - mi_wacc
    if abs(diferencia_wacc) < 0.5:
        print("✅ WACC prácticamente idénticos")
    elif diferencia_wacc > 0:
        print(f"⚠️ WACC app es {diferencia_wacc:.2f}pp MAYOR → valora MENOS")
    else:
        print(f"⚠️ Mi WACC es {abs(diferencia_wacc):.2f}pp MAYOR → valoro MENOS")
        print(f"   Esto explica por qué mi valoración (€3M) > app (€1M)")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)

