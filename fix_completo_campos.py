#!/usr/bin/env python3
"""
Arreglar completamente los campos de las empresas demo y su carga
"""

import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Primero, vamos a agregar los campos faltantes a cada empresa demo

# Restaurante La Terraza
restaurante_old = """'modelo_negocio': 'B2C - Venta a consumidores',
                'posicionamiento_precio': 'Premium - Alto valor',
                'competidores_principales': 'La Mafia (25% mercado local), Tony Roma´s (20%), Foster´s Hollywood (15%)',
                'vision_corto_plazo': 'Abrir segunda ubicación, aumentar ticket medio 15%, implementar delivery propio',
                'vision_medio_plazo': 'Expandir a 5 restaurantes en la región, facturación €3M, crear marca de catering',
                'vision_largo_plazo': 'Franquiciar el concepto, 20 restaurantes nacionales, venta a grupo hostelero',
                'ventaja_competitiva_principal': 'Ubicación privilegiada con terraza única, chef con estrella Michelin',
                'principales_riesgos': 'Estacionalidad (70% ventas en verano), dependencia del chef principal'"""

restaurante_new = """'modelo_negocio': 'B2C - Venta a consumidores',
                'posicionamiento_precio': 'Premium - Alto valor',
                'competidores_principales': 'La Mafia (25% mercado local), Tony Roma´s (20%), Foster´s Hollywood (15%)',
                'vision_corto_plazo': 'Abrir segunda ubicación, aumentar ticket medio 15%, implementar delivery propio',
                'vision_medio_plazo': 'Expandir a 5 restaurantes en la región, facturación €3M, crear marca de catering',
                'vision_largo_plazo': 'Franquiciar el concepto, 20 restaurantes nacionales, venta a grupo hostelero',
                'ventaja_competitiva_principal': 'Ubicación privilegiada con terraza única, chef con estrella Michelin',
                'principales_riesgos': 'Estacionalidad (70% ventas en verano), dependencia del chef principal',
                'descripcion_actividad': 'Restaurante de alta cocina mediterránea con terraza panorámica. Especializado en productos locales de temporada y carta de vinos premium. Eventos corporativos y celebraciones privadas.',
                'productos_servicios': 'Menú degustación (60€), carta tradicional (40€ ticket medio), catering para eventos, servicio de sommelier, cenas maridaje mensuales',
                'cuota_mercado': 15.5,
                'ventajas_competitivas': 'Ubicación única con vistas al mar, chef con estrella Michelin, carta de vinos con 300 referencias, servicio personalizado, terraza climatizada todo el año',
                'clientes_objetivo': 'Parejas 35-55 años poder adquisitivo medio-alto, empresas locales para eventos, turismo gastronómico internacional, celebraciones familiares premium'"""

content = content.replace(restaurante_old, restaurante_new)

# TechStart SaaS
techstart_old = """'modelo_negocio': 'SaaS - Software como servicio',
                'posicionamiento_precio': 'Freemium - Gratuito con opciones de pago',
                'competidores_principales': 'Salesforce (40% mercado), HubSpot (25%), Pipedrive (15%)',
                'vision_corto_plazo': 'Alcanzar 1000 clientes de pago, integración con 10 herramientas populares, Serie A de €5M',
                'vision_medio_plazo': 'Expansión internacional (UK y Alemania), €10M ARR, integración con ERPs',
                'vision_largo_plazo': 'Líder europeo en CRM para PYMES, Serie B de €20M, posible adquisición',
                'ventaja_competitiva_principal': 'Producto 100% adaptado a PYMES españolas, onboarding en 24h',
                'principales_riesgos': 'Churn rate del 15% anual, dependencia de AWS, competencia grandes players'"""

techstart_new = """'modelo_negocio': 'SaaS - Software como servicio',
                'posicionamiento_precio': 'Freemium - Gratuito con opciones de pago',
                'competidores_principales': 'Salesforce (40% mercado), HubSpot (25%), Pipedrive (15%)',
                'vision_corto_plazo': 'Alcanzar 1000 clientes de pago, integración con 10 herramientas populares, Serie A de €5M',
                'vision_medio_plazo': 'Expansión internacional (UK y Alemania), €10M ARR, integración con ERPs',
                'vision_largo_plazo': 'Líder europeo en CRM para PYMES, Serie B de €20M, posible adquisición',
                'ventaja_competitiva_principal': 'Producto 100% adaptado a PYMES españolas, onboarding en 24h',
                'principales_riesgos': 'Churn rate del 15% anual, dependencia de AWS, competencia grandes players',
                'descripcion_actividad': 'Plataforma CRM cloud diseñada específicamente para PYMES españolas. Gestión de clientes, pipeline de ventas, automatización de marketing y analíticas en tiempo real.',
                'productos_servicios': 'Plan Básico (gratis hasta 3 usuarios), Plan Profesional (29€/usuario/mes), Plan Enterprise (59€/usuario/mes), servicios de onboarding y consultoría',
                'cuota_mercado': 8.5,
                'ventajas_competitivas': 'Interfaz 100% en español, cumplimiento RGPD nativo, integración con gestorías españolas, soporte 24/7 en español, precio 50% menor que competidores',
                'clientes_objetivo': 'PYMES españolas 10-100 empleados, startups en crecimiento, equipos comerciales, empresas B2B con proceso de venta complejo, consultoras y agencias'"""

content = content.replace(techstart_old, techstart_new)

# ModaOnline Shop
modaonline_old = """'modelo_negocio': 'B2C - Venta a consumidores',
                'posicionamiento_precio': 'Medio - Calidad-precio',
                'competidores_principales': 'Zara Online (35% mercado), Mango (20%), Shein (30%)',
                'vision_corto_plazo': 'Lanzar app móvil, colaboración con 5 influencers, abrir showroom físico',
                'vision_medio_plazo': 'Marca propia 50% del catálogo, expansión a Portugal y Francia, €15M facturación',
                'vision_largo_plazo': 'Omnicanalidad completa, 10 tiendas físicas, sostenibilidad como diferenciador',
                'ventaja_competitiva_principal': 'Curación de marcas sostenibles, entrega en 24h, personal shopper virtual',
                'principales_riesgos': 'Estacionalidad de moda, costes de adquisición de cliente altos, dependencia de Instagram/Google'"""

modaonline_new = """'modelo_negocio': 'B2C - Venta a consumidores',
                'posicionamiento_precio': 'Medio - Calidad-precio',
                'competidores_principales': 'Zara Online (35% mercado), Mango (20%), Shein (30%)',
                'vision_corto_plazo': 'Lanzar app móvil, colaboración con 5 influencers, abrir showroom físico',
                'vision_medio_plazo': 'Marca propia 50% del catálogo, expansión a Portugal y Francia, €15M facturación',
                'vision_largo_plazo': 'Omnicanalidad completa, 10 tiendas físicas, sostenibilidad como diferenciador',
                'ventaja_competitiva_principal': 'Curación de marcas sostenibles, entrega en 24h, personal shopper virtual',
                'principales_riesgos': 'Estacionalidad de moda, costes de adquisición de cliente altos, dependencia de Instagram/Google',
                'descripcion_actividad': 'E-commerce de moda sostenible con curación de marcas europeas. Tecnología de recomendación por IA, servicio de personal shopper y programa de fidelización.',
                'productos_servicios': 'Ropa mujer (60%), hombre (25%), accesorios (15%). Servicio personal shopper online, suscripción premium con envíos gratis y descuentos exclusivos',
                'cuota_mercado': 2.3,
                'ventajas_competitivas': 'Marcas sostenibles exclusivas, entrega en 24h garantizada, devoluciones gratuitas 60 días, personal shopper por IA, programa de reciclaje textil',
                'clientes_objetivo': 'Mujeres 25-40 años urbanas, conciencia ecológica, renta media-alta, early adopters de moda, profesionales que valoran calidad y sostenibilidad'"""

content = content.replace(modaonline_old, modaonline_new)

# MetalPro Industrial
metalpro_old = """'modelo_negocio': 'B2B - Venta a empresas',
                'posicionamiento_precio': 'Premium - Alto valor',
                'competidores_principales': 'ThyssenKrupp (30% mercado), ArcelorMittal (25%), Acerinox (20%)',
                'vision_corto_plazo': 'Certificación ISO 14001, nuevo horno de alta eficiencia, reducir plazos entrega 20%',
                'vision_medio_plazo': 'Planta de reciclaje propia, exportar 40% producción, €50M facturación',
                'vision_largo_plazo': 'Líder nacional en aceros especiales, planta en Marruecos, integración vertical completa',
                'ventaja_competitiva_principal': 'Especialización en aleaciones para aeronáutica, entrega JIT, I+D propio',
                'principales_riesgos': 'Volatilidad precio materias primas, dependencia sector auto (60% ventas), regulación ambiental'"""

metalpro_new = """'modelo_negocio': 'B2B - Venta a empresas',
                'posicionamiento_precio': 'Premium - Alto valor',
                'competidores_principales': 'ThyssenKrupp (30% mercado), ArcelorMittal (25%), Acerinox (20%)',
                'vision_corto_plazo': 'Certificación ISO 14001, nuevo horno de alta eficiencia, reducir plazos entrega 20%',
                'vision_medio_plazo': 'Planta de reciclaje propia, exportar 40% producción, €50M facturación',
                'vision_largo_plazo': 'Líder nacional en aceros especiales, planta en Marruecos, integración vertical completa',
                'ventaja_competitiva_principal': 'Especialización en aleaciones para aeronáutica, entrega JIT, I+D propio',
                'principales_riesgos': 'Volatilidad precio materias primas, dependencia sector auto (60% ventas), regulación ambiental',
                'descripcion_actividad': 'Fabricación de componentes metálicos de alta precisión para automoción y aeronáutica. Especialistas en aleaciones especiales y tratamientos térmicos avanzados.',
                'productos_servicios': 'Piezas forjadas para motor, componentes aeronáuticos certificados, servicios de mecanizado CNC, prototipado rápido, ingeniería de diseño colaborativo',
                'cuota_mercado': 12.0,
                'ventajas_competitivas': 'Certificaciones aeronáuticas NADCAP, tecnología de forja en caliente única, entregas JIT garantizadas, departamento I+D con 15 ingenieros, 30 años de experiencia',
                'clientes_objetivo': 'OEMs automoción (Seat, VW, Ford), Tier 1 aeronáutica (Airbus, ITP Aero), fabricantes de maquinaria industrial, empresas de defensa'"""

content = content.replace(metalpro_old, metalpro_new)

# Guardar los cambios
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Agregados todos los campos faltantes a las 4 empresas demo:")
print("  - descripcion_actividad")
print("  - productos_servicios")
print("  - cuota_mercado")
print("  - ventajas_competitivas")
print("  - clientes_objetivo")
print("\n✅ Todos los campos estratégicos ahora tienen datos completos")

