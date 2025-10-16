#!/usr/bin/env python3
"""
Script de validación de correcciones para KPIs
Verifica que todas las correcciones estén aplicadas correctamente
"""

def test_app_roic():
    """Verifica que app.py incluya roic_promedio en dcf_detalle"""
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '"roic_promedio": resultado_mck.get("roic_promedio", 0)' in content:
        print("✅ TEST 1 PASS: app.py incluye roic_promedio en dcf_detalle")
        return True
    else:
        print("❌ TEST 1 FAIL: app.py NO incluye roic_promedio")
        return False

def test_app_session_state():
    """Verifica que app.py guarde dias_cobro, dias_pago, dias_inventario"""
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ('st.session_state["dias_cobro"]', 'dias_cobro'),
        ('st.session_state["dias_pago"]', 'dias_pago'),
        ('st.session_state["dias_inventario"]', 'dias_inventario')
    ]
    
    all_ok = True
    for check, name in checks:
        if check in content:
            print(f"✅ TEST 2.{name} PASS: app.py guarda {name}")
        else:
            print(f"❌ TEST 2.{name} FAIL: app.py NO guarda {name}")
            all_ok = False
    
    return all_ok

def test_data_collector_columnas():
    """Verifica que data_collector.py use nombres correctos de columnas"""
    with open('utils/data_collector.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("'Margen EBITDA (%)'", 'Margen EBITDA (%)'),
        ("'Margen Neto (%)'", 'Margen Neto (%)')
    ]
    
    all_ok = True
    for check, name in checks:
        if check in content:
            print(f"✅ TEST 3.{name} PASS: data_collector.py usa {name}")
        else:
            print(f"❌ TEST 3.{name} FAIL: data_collector.py NO usa {name}")
            all_ok = False
    
    return all_ok

def test_data_collector_dias():
    """Verifica que data_collector.py lea dias desde datos"""
    with open('utils/data_collector.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("datos.get('dias_cobro'", 'dias_cobro desde datos'),
        ("datos.get('dias_pago'", 'dias_pago desde datos'),
        ("datos.get('dias_inventario'", 'dias_inventario desde datos')
    ]
    
    all_ok = True
    for check, name in checks:
        if check in content:
            print(f"✅ TEST 4.{name} PASS: data_collector.py lee {name}")
        else:
            print(f"❌ TEST 4.{name} FAIL: data_collector.py NO lee {name}")
            all_ok = False
    
    return all_ok

if __name__ == "__main__":
    print("=" * 60)
    print("VALIDACIÓN DE CORRECCIONES - KPIs EN 0")
    print("=" * 60)
    print()
    
    results = []
    results.append(test_app_roic())
    print()
    results.append(test_app_session_state())
    print()
    results.append(test_data_collector_columnas())
    print()
    results.append(test_data_collector_dias())
    print()
    
    print("=" * 60)
    if all(results):
        print("✅ TODAS LAS CORRECCIONES APLICADAS CORRECTAMENTE")
    else:
        print("❌ ALGUNAS CORRECCIONES FALLARON")
    print("=" * 60)
