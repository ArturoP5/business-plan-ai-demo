#!/usr/bin/env python3
"""
Agrega descripcion_actividad y productos_servicios a las empresas demo
Con los nombres correctos
"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Datos a agregar para cada empresa
datos_faltantes = {
    'Restaurante La Terraza': {
        'descripcion_actividad': 'Restaurante de alta cocina mediterránea con terraza panorámica. Especializado en productos locales de temporada y carta de vinos premium. Eventos corporativos y celebraciones privadas.',
        'productos_servicios': 'Menú degustación (80€), carta tradicional renovada, eventos privados, catering premium, escuela de cocina, wine tasting'
    },
    'TechStart SaaS': {
        'descripcion_actividad': 'Plataforma CRM cloud diseñada específicamente para PYMES españolas. Gestión de clientes, pipeline de ventas, automatización de marketing y analíticas en tiempo real.',
        'productos_servicios': 'CRM básico (freemium), CRM Pro (29€/mes), Marketing Suite (49€/mes), API integraciones, consultoría implementación'
    },
    'ModaOnline Shop': {
        'descripcion_actividad': 'E-commerce de moda sostenible con curación de marcas europeas. Tecnología de recomendación por IA, servicio de personal shopper y programa de fidelización.',
        'productos_servicios': 'Venta online ropa/accesorios, suscripción VIP (9€/mes), personal shopper virtual, marketplace para diseñadores, programa afiliados'
    },
    'MetalPro Industrial': {
        'descripcion_actividad': 'Fabricación de componentes metálicos de alta precisión para automoción y aeronáutica. Especialistas en aleaciones especiales y tratamientos térmicos avanzados.',
        'productos_servicios': 'Piezas estampadas para automoción, componentes aeronáuticos certificados, prototipos rápidos, consultoría metalúrgica, tratamientos térmicos especiales'
    }
}

cambios = 0

# Buscar cada empresa por su nombre_empresa
for empresa, campos in datos_faltantes.items():
    for i in range(len(lines)):
        if f"'nombre_empresa': '{empresa}'" in lines[i]:
            # Encontramos la empresa, insertar después de esta línea
            indent = '                '
            # Insertar los campos
            lines.insert(i+1, f"{indent}'descripcion_actividad': '{campos['descripcion_actividad']}',\n")
            lines.insert(i+2, f"{indent}'productos_servicios': '{campos['productos_servicios']}',\n")
            print(f"✅ Agregados campos a {empresa}")
            cambios += 2
            break

# Guardar
with open('app.py', 'w') as f:
    f.writelines(lines)

print(f"\n✅ Total: {cambios} campos agregados a las empresas demo")
