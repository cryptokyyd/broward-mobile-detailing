#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates every landing page on the site, plus sitemap.xml.

    python build-pages.py

Two families come out of here:

  * SERVICES — one page per thing that can be sold (9 EN + 9 ES)
  * CITIES   — one page per Broward municipality worth ranking for (20 EN + 20 ES)

The Spanish pages are REAL URLs under /es/, not a JavaScript toggle, because
Google only indexes what is in the HTML. Roughly a third of Broward speaks
Spanish at home and almost no detailing competitor bothers. Each pair is
joined with hreflang.

ON THIN CONTENT: every city below carries its own hand-written paragraphs.
Twenty pages that differ only by a swapped city name are the textbook example
of what Google demotes, and they would take the whole domain down with them.
If you add a city, write it real copy or do not add it.
"""
import pathlib, html, datetime

BASE = "https://browardmobiledetailing.com"   # ← the one place the domain lives
OUT = pathlib.Path(__file__).parent
BRAND = "Broward Mobile Detailing"

# =============================================================== SERVICES ===
# price_from: the honest starting number for a sedan. Bigger vehicles cost more
# and the page says so — a "from" price that never applies to anyone is the
# fastest way to burn trust on the phone.
SERVICES = [
    dict(
        slug="full-detail-broward", slug_es="detallado-completo-broward",
        nav="Full detail", nav_es="Detallado completo",
        name="Full Mobile Detail", name_es="Detallado completo a domicilio",
        price_from=199, hours="3–4 hours",
        title="Mobile Full Detail in Broward County | Inside &amp; Out at Your Home",
        title_es="Detallado completo a domicilio en Broward | Por dentro y por fuera",
        meta="Inside-and-out mobile detailing across Broward County. We bring water and power to your driveway. Sedans from $199. Same-week slots.",
        meta_es="Detallado completo a domicilio en todo el condado de Broward. Llevamos agua y electricidad. Desde $199. Citas esta misma semana.",
        lede="The whole car, inside and out, done in your driveway while you get on with your day.",
        lede_es="El carro completo, por dentro y por fuera, en su entrada mientras usted sigue con su día.",
        body=[
            "This is the one most people mean when they say “detail”. The outside gets a two-bucket hand wash, the wheels and arches come clean separately so brake dust never travels back onto the paint, and the whole body is clay-barred to lift the gritty film a wash leaves behind. Then a sealant that actually survives a Florida summer.",
            "Inside, every seat and mat comes out for a hot-water extraction, the vents and cup holders get dug out properly, and the glass is done last so it stays done. Leather gets a pH-correct cleaner and a conditioner with UV block — the dashboard-cracking sun here is not a cliché.",
        ],
        body_es=[
            "Es lo que casi todos quieren decir cuando piden un “detallado”. Por fuera: lavado a mano con dos cubetas, ruedas y pasos de rueda aparte para que el polvo de freno no regrese a la pintura, y clay bar en toda la carrocería para levantar la película que un lavado normal deja. Después, un sellador que sí aguanta el verano de Florida.",
            "Por dentro: asientos y alfombras con extracción de agua caliente, rejillas y portavasos limpiados de verdad, y los vidrios al final para que queden. El cuero lleva un limpiador de pH correcto y acondicionador con filtro UV — el sol que agrieta tableros aquí no es un cuento.",
        ],
        includes=[
            ("Two-bucket hand wash", "Wheels, arches and tyres cleaned as a separate stage."),
            ("Clay bar decontamination", "Lifts the bonded grit a wash cannot."),
            ("Six-month paint sealant", "Rated for Florida sun and summer rain."),
            ("Hot-water extraction", "Seats, carpets and mats, pulled and done properly."),
            ("Leather clean + UV conditioner", "pH-correct, never a silicone shine."),
            ("Glass, vents and door jambs", "The parts that tell you it was done by hand."),
        ],
        includes_es=[
            ("Lavado a mano, dos cubetas", "Ruedas, pasos de rueda y llantas como etapa aparte."),
            ("Descontaminación con clay bar", "Levanta la suciedad adherida que un lavado no saca."),
            ("Sellador de pintura, 6 meses", "Formulado para el sol y la lluvia de Florida."),
            ("Extracción de agua caliente", "Asientos, alfombras y tapetes, hechos de verdad."),
            ("Cuero: limpieza + UV", "pH correcto, nunca un brillo de silicona."),
            ("Vidrios, rejillas y marcos", "Las partes que delatan un trabajo a mano."),
        ],
    ),
    dict(
        slug="interior-detailing-broward", slug_es="limpieza-de-interiores-broward",
        nav="Interior detail", nav_es="Interiores",
        name="Interior Deep Clean", name_es="Limpieza profunda de interiores",
        price_from=149, hours="2–3 hours",
        title="Interior Car Detailing in Broward County | Deep Clean at Your Door",
        title_es="Limpieza de interiores de autos en Broward | A domicilio",
        meta="Mobile interior detailing across Broward. Hot-water extraction, pet hair, stains and odour. Sedans from $149. We come to you.",
        meta_es="Limpieza profunda de interiores a domicilio en Broward. Extracción, pelo de mascota, manchas y olores. Desde $149.",
        lede="For the car that looks fine from the kerb and tells a different story when you open the door.",
        lede_es="Para el carro que se ve bien desde la acera y cuenta otra historia al abrir la puerta.",
        body=[
            "Sand, sunscreen, a spilled cafecito, a dog that rides in the back — a Broward interior takes a specific kind of beating, and vacuuming does not touch most of it. Hot-water extraction pulls what is actually in the fibres up and out instead of pushing it deeper.",
            "Pet hair is charged separately and honestly, because it is genuinely slow work: it gets lifted with a rubber blade before anything else happens, or it just redistributes. Smoke and mildew odour are treated at the source, not covered — if the smell is coming from a wet carpet under the mat, an ozone bomb only buys you a fortnight.",
        ],
        body_es=[
            "Arena, bloqueador, un cafecito derramado, un perro que viaja atrás — el interior de un carro en Broward recibe un castigo muy particular, y aspirar no resuelve casi nada de eso. La extracción de agua caliente saca lo que está metido en la fibra en vez de hundirlo más.",
            "El pelo de mascota se cobra aparte y se dice de frente, porque es trabajo lento de verdad: se levanta con goma antes de cualquier otra cosa, o simplemente se reparte. El olor a humo o a humedad se trata en su origen, no se tapa — si viene de una alfombra mojada bajo el tapete, el ozono solo le compra dos semanas.",
        ],
        includes=[
            ("Full strip-out vacuum", "Seats forward and back, rails, under the mats."),
            ("Hot-water extraction", "Carpets, cloth seats and mats."),
            ("Leather or vinyl treatment", "Cleaned, then conditioned with UV block."),
            ("Vents, screens and console", "Detail brushes and swabs, not a wipe."),
            ("Pet hair removal", "Quoted up front when you tell us on the call."),
            ("Odour treated at source", "We find where it comes from first."),
        ],
        includes_es=[
            ("Aspirado completo", "Asientos adelante y atrás, rieles, bajo los tapetes."),
            ("Extracción de agua caliente", "Alfombras, asientos de tela y tapetes."),
            ("Cuero o vinil", "Limpieza y luego acondicionador con filtro UV."),
            ("Rejillas, pantallas y consola", "Con cepillos y hisopos, no un trapazo."),
            ("Pelo de mascota", "Se cotiza desde la llamada, sin sorpresas."),
            ("Olores desde el origen", "Primero buscamos de dónde viene."),
        ],
    ),
    dict(
        slug="exterior-detailing-broward", slug_es="detallado-exterior-broward",
        nav="Exterior detail", nav_es="Exterior",
        name="Exterior Detail &amp; Wax", name_es="Detallado exterior y cera",
        price_from=99, hours="1.5–2 hours",
        title="Exterior Car Detailing &amp; Hand Wax in Broward County",
        title_es="Detallado exterior y cera a mano en Broward",
        meta="Hand wash, decontamination and wax across Broward County. Salt air and love bug season handled. Sedans from $99.",
        meta_es="Lavado a mano, descontaminación y cera en el condado de Broward. Desde $99. Vamos a su casa.",
        lede="Hand wash, decontamination and a wax that lasts past the next rain.",
        lede_es="Lavado a mano, descontaminación y una cera que dura más que la próxima lluvia.",
        body=[
            "Two things eat paint in this county: salt carried inland off the Atlantic, and love bugs twice a year. Both are acidic, and both etch clear coat if they sit. This service exists to get them off and put a barrier back on.",
            "The wash is by hand with two buckets and a grit guard, because an automatic brush is where most of the fine scratching in a Florida daily driver comes from. Wheels and tyres are a separate stage with their own mitts. Then decontamination, then a sealant or carnauba depending on whether you want it to last or you want it to glow.",
        ],
        body_es=[
            "Dos cosas se comen la pintura en este condado: la sal que entra del Atlántico y los love bugs dos veces al año. Las dos son ácidas y las dos marcan el barniz si se quedan. Este servicio existe para sacarlas y volver a poner una barrera.",
            "El lavado es a mano, con dos cubetas y rejilla, porque el cepillo automático es de donde sale casi todo el rayado fino de un carro de diario en Florida. Ruedas y llantas van aparte con sus propios guantes. Después descontaminación, y luego sellador o carnauba según quiera que dure o que brille.",
        ],
        includes=[
            ("Two-bucket hand wash", "Grit guard, separate wheel mitts."),
            ("Bug and tar removal", "Love bug season is included, not a surcharge."),
            ("Clay bar decontamination", "Leaves the paint genuinely smooth."),
            ("Sealant or carnauba wax", "Your call — we explain the trade-off."),
            ("Tyres dressed, not greased", "A satin finish that does not sling."),
            ("Exterior glass and trim", "Water spots off, trim fed."),
        ],
        includes_es=[
            ("Lavado a mano, dos cubetas", "Con rejilla y guantes aparte para ruedas."),
            ("Insectos y alquitrán", "La temporada de love bugs va incluida."),
            ("Clay bar", "Deja la pintura de verdad lisa."),
            ("Sellador o cera carnauba", "Usted elige — le explicamos la diferencia."),
            ("Llantas con acabado satinado", "Sin grasa que salpique."),
            ("Vidrios y molduras", "Sin manchas de agua, molduras nutridas."),
        ],
    ),
    dict(
        slug="ceramic-coating-broward", slug_es="recubrimiento-ceramico-broward",
        nav="Ceramic coating", nav_es="Cerámico",
        name="Ceramic Coating", name_es="Recubrimiento cerámico",
        price_from=699, hours="1–2 days",
        title="Ceramic Coating in Broward County | Multi-Year Paint Protection",
        title_es="Recubrimiento cerámico en Broward | Protección de años",
        meta="Professional ceramic coating across Broward County. Paint prepped and corrected first. From $699 with a multi-year warranty.",
        meta_es="Recubrimiento cerámico profesional en Broward. Pintura preparada y corregida antes. Desde $699 con garantía.",
        lede="Years of protection instead of months — but only if the paint underneath is right first.",
        lede_es="Años de protección en vez de meses — pero solo si la pintura de abajo está bien primero.",
        body=[
            "A coating is a hard, clear layer that bonds to the clear coat and stops sun, salt and bird mess from reaching it. Done properly it outlasts wax by years and makes every future wash faster.",
            "The honest part: a coating locks in whatever is under it. Put one over swirled, etched paint and you have sealed the damage in for three years. So the paint is inspected first, corrected if it needs it, and if we think you are better off with a $99 wax than a $699 coating, we will say that on the phone rather than after we have your deposit.",
        ],
        body_es=[
            "Un cerámico es una capa dura y transparente que se adhiere al barniz e impide que el sol, la sal y el excremento de pájaro lleguen a él. Bien hecho dura años más que una cera y hace más rápido cada lavado futuro.",
            "La parte honesta: el cerámico encierra lo que quede debajo. Si se aplica sobre pintura rayada o marcada, se sella el daño por tres años. Por eso primero se revisa la pintura, se corrige si hace falta, y si creemos que le conviene más una cera de $99 que un cerámico de $699, se lo decimos por teléfono y no después del depósito.",
        ],
        includes=[
            ("Paint inspection first", "Under proper light, before anything is quoted."),
            ("Decontamination and prep", "Iron fallout, clay, panel wipe."),
            ("Correction as needed", "Quoted separately and only if it helps."),
            ("Professional-grade coating", "Applied in shade, cured properly."),
            ("Multi-year warranty", "In writing, with the care schedule."),
            ("Maintenance wash guide", "How to not ruin it in month two."),
        ],
        includes_es=[
            ("Primero, revisión de pintura", "Con luz adecuada, antes de cotizar."),
            ("Descontaminación y preparación", "Hierro, clay bar y panel wipe."),
            ("Corrección si hace falta", "Se cotiza aparte y solo si suma."),
            ("Cerámico de grado profesional", "Aplicado a la sombra y bien curado."),
            ("Garantía de varios años", "Por escrito, con su plan de cuidado."),
            ("Guía de lavado", "Cómo no arruinarlo al segundo mes."),
        ],
    ),
    dict(
        slug="paint-correction-broward", slug_es="pulido-de-pintura-broward",
        nav="Paint correction", nav_es="Pulido",
        name="Paint Correction", name_es="Corrección y pulido de pintura",
        price_from=449, hours="6 hours – 2 days",
        title="Paint Correction &amp; Swirl Removal in Broward County",
        title_es="Corrección de pintura y eliminación de rayones en Broward",
        meta="Machine polishing and swirl removal across Broward County. Car wash scratches, oxidation and water spots. From $449.",
        meta_es="Pulido a máquina y eliminación de remolinos en Broward. Rayones de lavado, oxidación y manchas. Desde $449.",
        lede="Machine polishing that removes the scratches instead of filling them in for a month.",
        lede_es="Pulido a máquina que elimina los rayones en vez de taparlos por un mes.",
        body=[
            "Those spiderweb swirls that show up under a petrol station canopy are not dirt. They are thousands of fine scratches in the clear coat, mostly from automatic car washes and dry wiping, and no wax removes them — a glaze just hides them until it rains.",
            "Correction levels the clear coat with a machine polisher and a graded set of pads and compounds. Paint depth is measured before we start, because clear coat is finite and a shop that polishes without measuring is spending something you cannot get back. Most cars need one stage; heavily oxidised black and red paint sometimes needs two.",
        ],
        body_es=[
            "Esos remolinos que aparecen bajo la luz de una gasolinera no son suciedad. Son miles de rayones finos en el barniz, casi todos de lavados automáticos y de secar en seco, y ninguna cera los quita — un glaze solo los tapa hasta que llueve.",
            "La corrección nivela el barniz con pulidora y una serie graduada de pads y compuestos. Se mide el espesor de la pintura antes de empezar, porque el barniz es finito y un taller que pule sin medir está gastando algo que no vuelve. La mayoría necesita una etapa; el negro y el rojo muy oxidados a veces dos.",
        ],
        includes=[
            ("Paint depth measured", "Before a machine touches the car."),
            ("Test panel first", "You see the difference before we commit."),
            ("Single or two-stage", "Quoted after the inspection, not before."),
            ("Swirls, oxidation, water spots", "The three that plague cars here."),
            ("Protection applied after", "Bare corrected paint must not be left bare."),
            ("Before and after in daylight", "Photographed under the same light."),
        ],
        includes_es=[
            ("Medición del espesor", "Antes de que una máquina toque el carro."),
            ("Panel de prueba primero", "Usted ve la diferencia antes de decidir."),
            ("Una o dos etapas", "Se cotiza tras la revisión, no antes."),
            ("Remolinos, oxidación, manchas", "Las tres plagas de aquí."),
            ("Protección al terminar", "La pintura corregida no se deja desnuda."),
            ("Antes y después a la luz del día", "Fotografiado con la misma luz."),
        ],
    ),
    dict(
        slug="headlight-restoration-broward", slug_es="restauracion-de-faros-broward",
        nav="Headlight restoration", nav_es="Faros",
        name="Headlight Restoration", name_es="Restauración de faros",
        price_from=89, hours="45–60 minutes",
        title="Headlight Restoration in Broward County | Clear in an Hour",
        title_es="Restauración de faros en Broward | Claros en una hora",
        meta="Yellowed, hazy headlights restored across Broward County. Sanded, polished and UV sealed. $89 a pair, about an hour.",
        meta_es="Faros amarillos y opacos restaurados en Broward. Lijado, pulido y sellado UV. $89 el par, una hora.",
        lede="Yellow, hazy headlights sanded back and UV sealed — not a wipe-on that lasts a month.",
        lede_es="Faros amarillos y opacos lijados y sellados con UV — no un producto que dura un mes.",
        body=[
            "South Florida sun destroys polycarbonate headlights faster than almost anywhere in the country. Past a certain point it is a safety issue, not a cosmetic one — a hazed lens can cut usable night-time light by half, and it is a common note on a Florida vehicle inspection.",
            "The fix is wet sanding through progressive grits, machine polishing, then a genuine UV-resistant clear seal. The last step is the one cheap jobs skip: without it the lens yellows again within a few months, which is why the $20 kit from the parts store feels like it worked and then does not.",
        ],
        body_es=[
            "El sol del sur de Florida destruye los faros de policarbonato más rápido que casi cualquier otro lugar del país. Pasado cierto punto es un tema de seguridad, no estético — un lente opaco puede reducir a la mitad la luz útil de noche.",
            "La solución es lijado en húmedo con granos progresivos, pulido a máquina y luego un sellador transparente con protección UV real. Ese último paso es el que se saltan los trabajos baratos: sin él el lente vuelve a amarillear en pocos meses, y por eso el kit de $20 parece funcionar y después no.",
        ],
        includes=[
            ("Wet sanded, progressive grits", "The haze comes off, not covered up."),
            ("Machine polished clear", "Back to optical clarity."),
            ("UV-resistant sealant", "The step cheap jobs skip."),
            ("Both headlights", "$89 the pair, not each."),
            ("Done at your home or office", "About an hour, in a parking space."),
            ("Twelve-month guarantee", "Hazes again inside a year, we redo it."),
        ],
        includes_es=[
            ("Lijado en húmedo", "La opacidad se quita, no se tapa."),
            ("Pulido a máquina", "De vuelta a la claridad óptica."),
            ("Sellador con filtro UV", "El paso que se saltan los baratos."),
            ("Los dos faros", "$89 el par, no cada uno."),
            ("En su casa u oficina", "Una hora, en un espacio de parqueo."),
            ("Garantía de 12 meses", "Si vuelve a opacarse, se rehace."),
        ],
    ),
    dict(
        slug="engine-bay-cleaning-broward", slug_es="limpieza-de-motor-broward",
        nav="Engine bay", nav_es="Motor",
        name="Engine Bay Cleaning", name_es="Limpieza de compartimento del motor",
        price_from=79, hours="45 minutes",
        title="Engine Bay Cleaning in Broward County | Safe, Low-Pressure",
        title_es="Limpieza del motor en Broward | Segura y a baja presión",
        meta="Safe engine bay detailing across Broward County. Electronics covered, low pressure, dressed not greased. From $79.",
        meta_es="Limpieza segura del compartimento del motor en Broward. Electrónica cubierta, baja presión. Desde $79.",
        lede="Degreased and dressed, with everything that should not get wet covered first.",
        lede_es="Desengrasado y acondicionado, cubriendo antes todo lo que no debe mojarse.",
        body=[
            "A clean engine bay is worth real money at resale and makes any leak obvious the moment it starts. It is also the easiest place for a careless detailer to cause damage, which is why plenty of shops will not touch it.",
            "Alternator, intake, fuse box and any exposed connector get covered before a drop of water is used. Pressure stays low, degreaser is left to work rather than blasted off, and the plastics get a matte dressing — not the wet-look silicone that drips onto the belts and picks up dust for weeks.",
        ],
        body_es=[
            "Un motor limpio vale dinero real a la hora de vender y hace evidente cualquier fuga desde el primer día. También es el lugar más fácil para que un detallador descuidado cause daño, y por eso muchos talleres ni lo tocan.",
            "Alternador, admisión, caja de fusibles y cualquier conector expuesto se cubren antes de usar una gota de agua. La presión se mantiene baja, el desengrasante se deja actuar en vez de arrancarlo a chorro, y los plásticos llevan acabado mate — no la silicona brillante que escurre a las correas y junta polvo por semanas.",
        ],
        includes=[
            ("Electronics covered first", "Alternator, fuse box, intake, connectors."),
            ("Low-pressure rinse only", "No lance anywhere near a connector."),
            ("Degreaser given dwell time", "Dissolved off, not blasted off."),
            ("Matte plastic dressing", "Never the greasy wet look."),
            ("Blown dry", "So nothing sits damp in a crevice."),
            ("Add it to any detail", "Cheaper bundled than booked alone."),
        ],
        includes_es=[
            ("Electrónica cubierta primero", "Alternador, fusibles, admisión, conectores."),
            ("Enjuague a baja presión", "Nada de lanza cerca de un conector."),
            ("Desengrasante con tiempo", "Disuelto, no arrancado a chorro."),
            ("Plásticos en acabado mate", "Nunca el brillo grasoso."),
            ("Secado con aire", "Que nada quede húmedo en un rincón."),
            ("Añádalo a cualquier detallado", "Sale más barato junto que solo."),
        ],
    ),
    dict(
        slug="boat-detailing-broward", slug_es="detallado-de-botes-broward",
        nav="Boat detailing", nav_es="Botes",
        name="Boat &amp; Yacht Detailing", name_es="Detallado de botes y yates",
        price_from=0, hours="Quoted per foot",
        title="Mobile Boat Detailing in Broward County | Dockside or in the Yard",
        title_es="Detallado de botes a domicilio en Broward | En el muelle o el patio",
        meta="Mobile boat and yacht detailing across Broward. Salt, oxidation and waterline stains. Dockside in Fort Lauderdale, Pompano and Dania.",
        meta_es="Detallado de botes y yates a domicilio en Broward. Sal, oxidación y línea de flotación. En muelle o en patio.",
        lede="Salt, oxidation and waterline staining, handled at the dock or on the trailer.",
        lede_es="Sal, oxidación y manchas de línea de flotación, en el muelle o en el tráiler.",
        body=[
            "Broward has more waterway than road in places, and a boat that lives in salt needs a completely different chemistry from a car. Gelcoat oxidises, stainless tea-stains, and the waterline picks up a band no pressure washer will shift.",
            "We work dockside along the New River, Pompano and Dania, and in the yard for anything on a trailer. Wash-downs, compound and wax on oxidised gelcoat, non-skid cleaned without destroying the texture, and vinyl treated with something that will not go brittle in the sun. Quoted by the foot and by condition — send a photo and we will price it before we come out.",
        ],
        body_es=[
            "Broward tiene en partes más canal que calle, y un bote que vive en sal necesita una química completamente distinta a la de un carro. El gelcoat se oxida, el acero inoxidable se mancha y la línea de flotación agarra una banda que ninguna hidrolavadora quita.",
            "Trabajamos en muelle por el New River, Pompano y Dania, y en patio para lo que esté en tráiler. Lavados, compuesto y cera en gelcoat oxidado, antideslizante limpiado sin destruir la textura, y vinil tratado con algo que no se vuelva quebradizo al sol. Se cotiza por pie y por condición — mande una foto y le damos precio antes de salir.",
        ],
        includes=[
            ("Dockside or on the trailer", "Fort Lauderdale, Pompano, Dania, Hollywood."),
            ("Salt wash-down", "The whole boat, not just the topsides."),
            ("Gelcoat compound and wax", "For oxidation and chalking."),
            ("Non-skid cleaned carefully", "Texture kept, not polished flat."),
            ("Stainless de-staining", "Tea stains off the rails and fittings."),
            ("Priced by the foot", "Send a photo, get a number first."),
        ],
        includes_es=[
            ("En muelle o en tráiler", "Fort Lauderdale, Pompano, Dania, Hollywood."),
            ("Lavado de sal", "El bote completo, no solo la obra muerta."),
            ("Compuesto y cera en gelcoat", "Para oxidación y calcificación."),
            ("Antideslizante con cuidado", "Se conserva la textura."),
            ("Acero inoxidable sin manchas", "Barandas y herrajes."),
            ("Precio por pie", "Mande una foto y reciba el número antes."),
        ],
    ),
    dict(
        slug="fleet-detailing-broward", slug_es="detallado-de-flotas-broward",
        nav="Fleet &amp; commercial", nav_es="Flotas",
        name="Fleet &amp; Commercial", name_es="Flotas y comercial",
        price_from=0, hours="Scheduled monthly",
        title="Fleet Vehicle Detailing in Broward County | Vans, Trucks, Rentals",
        title_es="Detallado de flotas en Broward | Vans, camiones y rentas",
        meta="Scheduled fleet detailing across Broward County. Vans, trucks, dealer lots and rentals. Volume pricing, invoiced monthly.",
        meta_es="Detallado programado de flotas en Broward. Vans, camiones, concesionarios y rentas. Precio por volumen, factura mensual.",
        lede="Vans, trucks, dealer lots and rental returns, on a schedule, invoiced monthly.",
        lede_es="Vans, camiones, concesionarios y devoluciones de renta, programado y facturado por mes.",
        body=[
            "A branded van with a dull wrap and bug-covered front is doing your marketing backwards. Fleet work is priced by volume and run on a fixed schedule, so the vehicles stay presentable instead of getting one heroic clean a year.",
            "We come to the yard, before the shift or after it, and work through the line. Wraps get a wrap-safe process — the wrong chemical lifts an edge and that is a reprint, not a rewash. One invoice a month, one point of contact, and a per-vehicle rate that drops as the count goes up.",
        ],
        body_es=[
            "Una van rotulada con el vinil opaco y el frente lleno de insectos hace su publicidad al revés. El trabajo de flota se cotiza por volumen y se corre con horario fijo, para que los vehículos se mantengan presentables en lugar de recibir una limpieza heroica al año.",
            "Vamos al patio, antes o después del turno, y avanzamos por la fila. El vinil lleva un proceso seguro para wraps — el químico equivocado levanta un borde y eso es una reimpresión, no un relavado. Una factura al mes, un solo contacto, y una tarifa por vehículo que baja al subir la cantidad.",
        ],
        includes=[
            ("Volume pricing", "Per-vehicle rate falls as the count rises."),
            ("Wrap-safe chemistry", "The wrong product is a reprint, not a rewash."),
            ("Before or after shift", "We work around your operating hours."),
            ("At your yard", "We bring water and power."),
            ("One monthly invoice", "Net terms available."),
            ("Fixed schedule", "Weekly, fortnightly or monthly."),
        ],
        includes_es=[
            ("Precio por volumen", "La tarifa baja al subir la cantidad."),
            ("Químicos seguros para vinil", "El producto equivocado es una reimpresión."),
            ("Antes o después del turno", "Nos ajustamos a su horario."),
            ("En su patio", "Llevamos agua y electricidad."),
            ("Una factura mensual", "Con términos de crédito disponibles."),
            ("Horario fijo", "Semanal, quincenal o mensual."),
        ],
    ),
]

# ================================================================= CITIES ===
# Each entry gets its own paragraphs. See the note at the top of this file
# about why that is not optional.
CITIES = [
    dict(slug="fort-lauderdale", name="Fort Lauderdale", zip_="33301, 33304, 33305, 33306, 33308, 33312, 33315, 33316",
         areas="Las Olas, Victoria Park, Rio Vista, Coral Ridge, Flagler Village, Harbor Beach",
         hook="Condo garages, kerbside on Las Olas, and boats at the dock.",
         hook_es="Garajes de condominio, la calle en Las Olas y botes en el muelle.",
         para=["Most of our Fort Lauderdale work happens in condo garages, which suits mobile detailing well — covered, shaded, and out of the afternoon storm. We are set up for it: a tank on board means we do not need your building's water, and low-noise equipment keeps the garage manager happy.",
               "If you are in a tower with a loading bay, tell us the building when you call and we will bring the right length of hose and clear it with the front desk. Along the beach, salt off the Atlantic is the thing eating your paint, and it is the reason a sealant here is a six-month item rather than a twelve."],
         para_es=["Casi todo nuestro trabajo en Fort Lauderdale ocurre en garajes de condominio, y eso le va muy bien al detallado móvil: techado, con sombra y lejos de la tormenta de la tarde. Estamos equipados para eso: llevamos tanque propio, así que no dependemos del agua del edificio, y el equipo es silencioso para no incomodar a la administración.",
                  "Si vive en una torre con área de carga, díganos el edificio al llamar y llevamos la manguera del largo correcto y avisamos en recepción. Cerca de la playa, la sal del Atlántico es lo que se come su pintura, y por eso aquí un sellador dura seis meses y no doce."]),
    dict(slug="pembroke-pines", name="Pembroke Pines", zip_="33024, 33025, 33026, 33027, 33028, 33029",
         areas="Chapel Trail, Pembroke Falls, Silver Lakes, Towngate, Grand Palms",
         hook="Driveways, three-row SUVs and school-run interiors.",
         hook_es="Entradas de casa, camionetas de tres filas e interiores de ruta escolar.",
         para=["Pembroke Pines is a driveway town, which is the easiest possible setup for us — pull up, plug into nothing, and work. Most of what we do out here is the family vehicle: a three-row SUV or a minivan that carries kids, sports kit and a lot of spilled drink.",
               "That means interiors are usually the real job and the exterior is the easy half. We price the third row honestly rather than treating a Suburban like a Corolla, and if the car has car seats, leave them in — we work around them and clean underneath, which is where it is always worst."],
         para_es=["Pembroke Pines es una ciudad de entradas de casa, que es la situación más fácil para nosotros: llegamos, no dependemos de nada y trabajamos. Casi todo lo que hacemos aquí es el vehículo familiar: una camioneta de tres filas o una minivan que carga niños, equipo deportivo y mucha bebida derramada.",
                  "Eso significa que el interior suele ser el trabajo real y el exterior es la mitad fácil. Cobramos la tercera fila con honestidad en vez de tratar una Suburban como un Corolla, y si el carro tiene sillas de bebé, déjelas — trabajamos alrededor y limpiamos debajo, que es donde siempre está peor."]),
    dict(slug="hollywood", name="Hollywood", zip_="33019, 33020, 33021, 33023, 33024",
         areas="Hollywood Lakes, Emerald Hills, Hollywood Beach, Downtown, Oakwood",
         hook="Beach sand, salt air and a lot of older paint worth saving.",
         hook_es="Arena de playa, aire salado y mucha pintura antigua que vale la pena salvar.",
         para=["Hollywood splits neatly in two for us. East of Federal, near the Broadwalk, everything is about salt and sand: sand in the carpets from the beach, salt in the paint from the air, and both need dealing with more often than inland.",
               "West, around Emerald Hills, the cars are often older and garaged, and the job is usually correction rather than protection — twenty-year-old clear coat that has never been polished and can look remarkable with one careful stage. We measure paint depth before touching either kind."],
         para_es=["Hollywood se divide en dos para nosotros. Al este de Federal, cerca del Broadwalk, todo es sal y arena: arena en las alfombras por la playa, sal en la pintura por el aire, y las dos hay que atenderlas más seguido que tierra adentro.",
                  "Al oeste, por Emerald Hills, los carros suelen ser mayores y de garaje, y el trabajo casi siempre es corrección más que protección — barniz de veinte años que nunca se ha pulido y que puede quedar notable con una sola etapa cuidadosa. Medimos el espesor de la pintura antes de tocar cualquiera de los dos."]),
    dict(slug="miramar", name="Miramar", zip_="33023, 33025, 33027, 33029",
         areas="Miramar Park, Silver Shores, Riviera Isles, Sunset Lakes, Historic Miramar",
         hook="Newer builds, newer cars, and coatings that make sense.",
         hook_es="Casas nuevas, carros nuevos y cerámicos que sí valen la pena.",
         para=["West Miramar is largely newer construction and newer vehicles, and that changes the advice. On a car that is two years old with paint still in good condition, a ceramic coating is genuinely worth the money — you are protecting something rather than sealing in damage.",
               "It is also a long commute town. Cars that live on I-75 and the Turnpike collect road film and bug splatter at a rate that surprises people, and a maintenance plan usually costs less over a year than two rescue details."],
         para_es=["El oeste de Miramar es en gran parte construcción y vehículos nuevos, y eso cambia el consejo. En un carro de dos años con la pintura todavía en buen estado, un recubrimiento cerámico sí vale el dinero — está protegiendo algo en vez de sellar un daño.",
                  "También es una ciudad de trayectos largos. Los carros que viven en la I-75 y el Turnpike acumulan película de carretera e insectos a un ritmo que sorprende, y un plan de mantenimiento suele costar menos al año que dos detallados de rescate."]),
    dict(slug="coral-springs", name="Coral Springs", zip_="33065, 33067, 33071, 33076",
         areas="Eagle Trace, Heron Bay, Ramblewood, Maplewood, Coral Creek",
         hook="HOA-friendly, low-noise, and no runoff down the street.",
         hook_es="Compatible con HOA, silencioso y sin agua corriendo por la calle.",
         para=["Coral Springs HOAs are stricter than most in the county about contractors, noise and water running into the storm drain. We work within that: the equipment runs quiet, we capture and contain our water, and we are used to being asked for a certificate of insurance before we come through the gate.",
               "If your association needs paperwork in advance, say so when you book and we will send it the same day rather than discovering the problem at the guardhouse."],
         para_es=["Las HOA de Coral Springs son más estrictas que la mayoría del condado con contratistas, ruido y agua que corre al drenaje pluvial. Trabajamos dentro de eso: el equipo es silencioso, contenemos nuestra agua y estamos acostumbrados a que nos pidan certificado de seguro antes de entrar por el portón.",
                  "Si su asociación necesita papeleo por adelantado, avísenos al reservar y lo enviamos el mismo día en vez de descubrir el problema en la caseta."]),
    dict(slug="pompano-beach", name="Pompano Beach", zip_="33060, 33062, 33064, 33069",
         areas="Old Pompano, Cypress Head, Palm Aire, Hillsboro Shores, the Marina district",
         hook="Salt, boats and gelcoat as much as paint.",
         hook_es="Sal, botes y gelcoat tanto como pintura.",
         para=["Pompano is where our boat work concentrates, and the car work here has the same enemy: salt. A vehicle parked within a few blocks of the Intracoastal picks up airborne salt continuously, and it does not wait for rain to start etching.",
               "For cars kept near the water we recommend a shorter protection cycle and, honestly, a plain rinse between details — free, takes five minutes, and does more for your paint than any product we could sell you."],
         para_es=["Pompano es donde se concentra nuestro trabajo de botes, y el trabajo de carros aquí tiene el mismo enemigo: la sal. Un vehículo estacionado a pocas cuadras del Intracoastal recibe sal en el aire de forma continua, y no espera a que llueva para empezar a marcar.",
                  "Para carros cerca del agua recomendamos un ciclo de protección más corto y, con honestidad, un simple enjuague entre detallados — gratis, cinco minutos, y hace más por su pintura que cualquier producto que podamos venderle."]),
    dict(slug="davie", name="Davie", zip_="33314, 33317, 33324, 33325, 33328, 33330, 33331",
         areas="Shenandoah, Forest Ridge, Long Lake Ranches, Orange Park, Pine Island Ridge",
         hook="Trucks, trailers, and mud that is not city dirt.",
         hook_es="Camionetas, tráileres y lodo que no es tierra de ciudad.",
         para=["Davie work is trucks and it is dirtier than the rest of the county — actual mud, hay, feed dust and horse trailers rather than road film. That is a different job and we price it as one instead of quoting you a sedan rate and renegotiating in your driveway.",
               "Lifted trucks, dual rear wheels and trailers are all fine; tell us the vehicle on the call so we bring enough water. Undercarriage rinses are worth it out here in a way they are not in a condo garage."],
         para_es=["El trabajo en Davie es de camionetas y es más sucio que el resto del condado — lodo de verdad, heno, polvo de alimento y tráileres de caballos en vez de película de carretera. Ese es otro trabajo y lo cotizamos como tal, en lugar de darle precio de sedán y renegociar en su entrada.",
                  "Camionetas levantadas, rueda doble y tráileres no son problema; díganos el vehículo en la llamada para llevar suficiente agua. Aquí el enjuague de bajos sí vale la pena, cosa que no pasa en un garaje de condominio."]),
    dict(slug="plantation", name="Plantation", zip_="33313, 33317, 33322, 33324, 33325",
         areas="Plantation Acres, Jacaranda, Hawks Landing, Central Park, Plantation Isles",
         hook="Shaded driveways, mature trees, and a lot of tree sap.",
         hook_es="Entradas con sombra, árboles grandes y mucha savia.",
         para=["Plantation's tree cover is the best in this part of the county and it is also the reason we get called. Sap, pollen and bird mess from mature oaks and ficus do more paint damage here than sun does, and sap in particular etches within days in summer heat.",
               "The upside is shade to work in, which genuinely improves the result — products flash off too fast on hot paint in direct sun, and a shaded driveway lets us do the job properly rather than chasing the panel."],
         para_es=["La sombra de Plantation es la mejor de esta zona del condado y es también la razón por la que nos llaman. La savia, el polen y el excremento de pájaro de robles y ficus maduros dañan más la pintura aquí que el sol, y la savia en particular marca en pocos días con el calor del verano.",
                  "La ventaja es tener sombra para trabajar, y eso sí mejora el resultado — los productos se secan demasiado rápido sobre pintura caliente al sol directo, y una entrada con sombra nos deja hacer el trabajo bien en vez de ir corriendo detrás del panel."]),
    dict(slug="sunrise", name="Sunrise", zip_="33313, 33322, 33323, 33325, 33351",
         areas="Sawgrass, Welleby, Sunrise Golf Village, Bonaventure, Sunrise Lakes",
         hook="Sawgrass commuters and event-day parking lot dust.",
         hook_es="Quienes viajan por Sawgrass y el polvo del estacionamiento en días de evento.",
         para=["Sunrise splits between commuters running Sawgrass Expressway daily and residents around Sunrise Lakes whose cars barely move. Those are opposite problems: one collects road film and bug strike, the other develops flat spots, stale interiors and a layer of settled dust that bonds if left.",
               "A car that sits still is not a car that stays clean, and the fix for it is different — more interior, more decontamination, less protection than a high-mileage commuter needs."],
         para_es=["Sunrise se divide entre quienes recorren el Sawgrass Expressway a diario y residentes por Sunrise Lakes cuyos carros casi no se mueven. Son problemas opuestos: uno acumula película de carretera e insectos, el otro desarrolla interiores viciados y una capa de polvo asentado que se adhiere si se deja.",
                  "Un carro parado no es un carro limpio, y la solución es distinta — más interior, más descontaminación y menos protección de la que necesita alguien que maneja mucho."]),
    dict(slug="weston", name="Weston", zip_="33326, 33327, 33331, 33332",
         areas="Weston Hills, Savanna, Windmill Ranch, The Ridges, Bonaventure",
         hook="Gated, insured, and coatings on cars worth coating.",
         hook_es="Comunidades cerradas, con seguro, y cerámicos en carros que lo merecen.",
         para=["Nearly all of Weston is gated, so bookings here run on gate clearance and a name at the guardhouse. Give us the community and the resident name when you book and it is a non-event; leave it out and we sit at the gate burning your appointment slot.",
               "Weston is also where the most ceramic coating work comes from, and it is usually the right call — the cars are newer, garaged, and worth protecting properly rather than waxing four times a year."],
         para_es=["Casi todo Weston es cerrado, así que las citas aquí dependen del acceso y de un nombre en la caseta. Denos la comunidad y el nombre del residente al reservar y no hay problema; si falta, nos quedamos en el portón quemando su cita.",
                  "Weston es también de donde sale la mayor parte del trabajo de cerámico, y casi siempre es la decisión correcta — son carros más nuevos, de garaje, que vale la pena proteger bien en lugar de encerarlos cuatro veces al año."]),
    dict(slug="deerfield-beach", name="Deerfield Beach", zip_="33441, 33442",
         areas="Deerfield Beach, Century Village, The Cove, Independence Bay",
         hook="Beachfront salt and a lot of long-owned cars.",
         hook_es="Sal frente al mar y muchos carros de un solo dueño.",
         para=["Deerfield's beachfront blocks are as harsh an environment as anywhere in Broward for paint — direct salt spray, not just salt air. Cars parked there need protection on a genuinely shorter cycle and there is no product that changes that.",
               "Inland, around Century Village, we do a lot of work on cars that have had one owner for fifteen years and are worth restoring rather than replacing. Oxidised single-stage paint responds better to correction than most people expect."],
         para_es=["Las cuadras frente al mar de Deerfield son de los ambientes más duros de Broward para la pintura — rocío salino directo, no solo aire salado. Los carros ahí necesitan protección en un ciclo realmente más corto y no hay producto que cambie eso.",
                  "Tierra adentro, por Century Village, hacemos mucho trabajo en carros de un solo dueño por quince años que vale más restaurar que reemplazar. La pintura monocapa oxidada responde a la corrección mejor de lo que la gente espera."]),
    dict(slug="lauderhill", name="Lauderhill", zip_="33311, 33313, 33319, 33351",
         areas="Inverrary, Lauderhill Mall area, Broward Estates, Environ",
         hook="Straight pricing, no upsell, work done at your door.",
         hook_es="Precio claro, sin ventas cruzadas, trabajo en su puerta.",
         para=["Most Lauderhill bookings are the practical end of what we do — a proper interior clean and an honest exterior, on a car that is used hard and needs to look presentable rather than concours.",
               "We quote the whole number on the phone. There is no walk-around at the end where the price changes, and if what you actually need is the $99 exterior rather than the $199 full detail, that is what we will book you for."],
         para_es=["La mayoría de las citas en Lauderhill son la parte práctica de lo que hacemos — un buen interior y un exterior honesto, en un carro que se usa duro y necesita verse presentable, no de concurso.",
                  "Damos el número completo por teléfono. No hay una vuelta al final donde cambia el precio, y si lo que de verdad necesita es el exterior de $99 y no el completo de $199, eso es lo que le reservamos."]),
    dict(slug="tamarac", name="Tamarac", zip_="33319, 33321, 33351",
         areas="Kings Point, Mainlands, Woodmont, Sunflower",
         hook="Low-mileage cars, garage dust, and interiors that need air.",
         hook_es="Carros de poco millaje, polvo de garaje e interiores que necesitan aire.",
         para=["A lot of Tamarac cars do under three thousand miles a year, and the problems that come with that are not the problems a commuter has. Interiors go stale, rubber seals dry out, and a fine grey dust settles and bonds over months of sitting.",
               "The right service here is usually interior-led with a light exterior decontamination, not a heavy correction — the paint is often barely worn. We will tell you when a full detail is more than your car needs."],
         para_es=["Muchos carros en Tamarac hacen menos de tres mil millas al año, y los problemas que trae eso no son los de quien maneja a diario. Los interiores se vician, los sellos de goma se resecan y un polvo gris fino se asienta y se adhiere tras meses parado.",
                  "El servicio correcto aquí suele ser enfocado en interior con una descontaminación exterior ligera, no una corrección pesada — la pintura casi no está desgastada. Le diremos cuándo un detallado completo es más de lo que su carro necesita."]),
    dict(slug="margate", name="Margate", zip_="33063, 33068, 33093",
         areas="Holiday Springs, Oriole Estates, Paradise Hills, Coral Gate",
         hook="Same-week slots and pricing that does not move.",
         hook_es="Citas esta semana y precios que no se mueven.",
         para=["Margate sits central enough in the county that we can almost always fit it in the same week, and often the next day if a slot opens. It is a short run for us from either direction, which is why the travel does not get priced into your quote.",
               "The work here is the everyday version: family cars, commuter sedans and the occasional truck, done in the driveway while you are at work or asleep after a night shift."],
         para_es=["Margate está lo bastante céntrico en el condado como para que casi siempre podamos atenderlo la misma semana, y muchas veces al día siguiente si se abre un espacio. Es un trayecto corto desde cualquier dirección, y por eso el viaje no se le carga a su cotización.",
                  "El trabajo aquí es el de todos los días: carros familiares, sedanes de trabajo y alguna camioneta, hechos en la entrada mientras usted trabaja o duerme después de un turno de noche."]),
    dict(slug="coconut-creek", name="Coconut Creek", zip_="33063, 33066, 33073, 33097",
         areas="Wynmoor, Winston Park, Regency Lakes, Township",
         hook="Gated communities and clean, quiet driveway work.",
         hook_es="Comunidades cerradas y trabajo limpio y silencioso en la entrada.",
         para=["Coconut Creek is heavily gated and heavily HOA-governed, and Wynmoor in particular has firm rules about contractors and hours. We keep to them — quiet equipment, contained water, and we do not start before the hour your community allows.",
               "Bring the gate pass detail to the booking call and the appointment runs on time. It is the single most common reason a mobile detail slips, and it is entirely avoidable."],
         para_es=["Coconut Creek tiene muchas comunidades cerradas y HOA estrictas, y Wynmoor en particular tiene reglas firmes sobre contratistas y horarios. Las respetamos — equipo silencioso, agua contenida, y no empezamos antes de la hora que permita su comunidad.",
                  "Traiga el detalle del acceso a la llamada de reserva y la cita corre a tiempo. Es la razón más común por la que se atrasa un detallado móvil, y es totalmente evitable."]),
    dict(slug="oakland-park", name="Oakland Park", zip_="33304, 33306, 33309, 33311, 33334",
         areas="Coral Heights, Lloyd Estates, North Andrews Gardens, Twin Lakes",
         hook="Close to the beach, priced for every day.",
         hook_es="Cerca de la playa, con precio de todos los días.",
         para=["Oakland Park is close enough to the coast to get the salt and far enough inland to avoid the worst of it, which puts most cars here on a normal protection cycle rather than an accelerated one.",
               "It is a quick run for us off Oakland Park Boulevard, and a good candidate for the maintenance plan — a smaller service every six weeks keeps a car ahead of the weather for less than rescuing it twice a year."],
         para_es=["Oakland Park está lo bastante cerca de la costa para recibir sal y lo bastante tierra adentro para evitar lo peor, lo que pone a la mayoría de los carros en un ciclo de protección normal y no acelerado.",
                  "Es un trayecto rápido para nosotros por Oakland Park Boulevard, y buen candidato para el plan de mantenimiento — un servicio más pequeño cada seis semanas mantiene el carro por delante del clima por menos que rescatarlo dos veces al año."]),
    dict(slug="hallandale-beach", name="Hallandale Beach", zip_="33009",
         areas="Golden Isles, Three Islands, Hallandale Beach, Diplomat area",
         hook="High-rise garages and valet-worn paint.",
         hook_es="Garajes de torre y pintura desgastada por el valet.",
         para=["Hallandale is condo towers, which means garage bookings and, very often, valet-worn paint. Repeated valet parking puts a specific pattern of light scratching around the door handles, the driver's door edge and the boot lid — it is recognisable and it polishes out.",
               "We work in the garage with the building's permission, keep the bay clear, and contain our water. Give us the tower name and your space number when you book."],
         para_es=["Hallandale es de torres de condominios, lo que significa citas en garaje y, muy seguido, pintura desgastada por el valet. El valet repetido deja un patrón muy específico de rayones finos alrededor de las manijas, el borde de la puerta del conductor y la tapa del baúl — es reconocible y sale con pulido.",
                  "Trabajamos en el garaje con permiso del edificio, dejamos el área libre y contenemos el agua. Denos el nombre de la torre y su número de espacio al reservar."]),
    dict(slug="dania-beach", name="Dania Beach", zip_="33004, 33312, 33316",
         areas="Dania Beach, Melaleuca Gardens, Harbour Isle, the marina",
         hook="Boats on trailers and airport-run cars.",
         hook_es="Botes en tráiler y carros que viven en el aeropuerto.",
         para=["Dania sits between the airport and the water, and both show up in the work. Cars that live in long-stay parking come back with a bonded film of jet exhaust and brake dust that a normal wash does not remove — it needs iron fallout treatment and a clay bar.",
               "The marina side is boat work, on the trailer or in the yard, quoted by the foot. Send a photo when you enquire and you will get a number before we come out."],
         para_es=["Dania está entre el aeropuerto y el agua, y las dos cosas aparecen en el trabajo. Los carros que viven en estacionamiento de larga estadía regresan con una película adherida de escape de avión y polvo de freno que un lavado normal no quita — necesita tratamiento de hierro y clay bar.",
                  "Del lado de la marina el trabajo es de botes, en tráiler o en patio, cotizado por pie. Mande una foto al consultar y recibe un número antes de que salgamos."]),
    dict(slug="cooper-city", name="Cooper City", zip_="33024, 33026, 33328, 33330",
         areas="Rock Creek, Monterra, Embassy Lakes, Flamingo Gardens area",
         hook="Family cars, driveway service, evening slots.",
         hook_es="Carros familiares, servicio en la entrada, citas por la tarde.",
         para=["Cooper City runs on school and sport schedules, so most of our bookings here are late afternoon or Saturday morning — after drop-off, before pickup, or while the game is on.",
               "The vehicles are family vehicles and the interiors reflect it. We do not charge extra for the ordinary chaos of children; we charge extra for pet hair and for genuine spill damage, and we say which it is before we start."],
         para_es=["Cooper City se mueve con los horarios de escuela y deporte, así que casi todas nuestras citas aquí son al final de la tarde o el sábado por la mañana — después de dejar a los niños, antes de recogerlos, o mientras hay partido.",
                  "Los vehículos son familiares y los interiores lo reflejan. No cobramos extra por el desorden normal de los niños; cobramos extra por pelo de mascota y por daño real de derrames, y decimos cuál es antes de empezar."]),
    dict(slug="parkland", name="Parkland", zip_="33067, 33076",
         areas="Heron Bay, Parkland Golf &amp; Country Club, Cypress Head, Parkland Isles",
         hook="Gated, quiet hours, and paint worth protecting properly.",
         hook_es="Cerrado, horarios de silencio y pintura que vale proteger bien.",
         para=["Parkland is gated almost end to end and the communities enforce quiet hours seriously. Our equipment is chosen partly for that reason, and we will schedule around your association's contractor window rather than argue with it at the gate.",
               "The cars here justify the higher-end services — correction before coating, coatings with a real warranty, and a maintenance wash schedule that keeps the coating performing instead of letting it die quietly in year two."],
         para_es=["Parkland es cerrado casi de punta a punta y las comunidades hacen cumplir los horarios de silencio en serio. Nuestro equipo se eligió en parte por eso, y programamos dentro de la ventana de contratistas de su asociación en lugar de discutirla en el portón.",
                  "Los carros de aquí justifican los servicios más altos — corrección antes del cerámico, cerámicos con garantía real, y un calendario de lavado de mantenimiento que mantenga el recubrimiento funcionando en vez de dejarlo morir en silencio al segundo año."]),
]

# ================================================================= chrome ===
NAV_MAIN = [("index.html", "Home", "Inicio"),
            ("services.html", "Services", "Servicios"),
            ("pricing.html", "Pricing", "Precios"),
            ("areas.html", "Service area", "Zonas"),
            ("about.html", "About", "Nosotros")]

MARK = '''<svg class="brand__mark" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
        <path d="M32 6c9 11 15 18.5 15 25.5A15 15 0 0 1 17 31.5C17 24.5 23 17 32 6Z" fill="{drop}"/>
        <rect x="6" y="49" width="52" height="4" rx="2" fill="{bar}"/>
        <rect x="14" y="57" width="36" height="3" rx="1.5" fill="{bar}" opacity=".45"/>
      </svg>'''
MARK_HEAD = MARK.format(drop="#2f57c9", bar="#22252f")
MARK_FOOT = MARK.format(drop="#5fb7e0", bar="#dfe6ee")

CHEVRON = ('<svg viewBox="0 0 12 8" aria-hidden="true" focusable="false">'
           '<path d="M1 1.5 6 6.5 11 1.5" fill="none" stroke="currentColor" '
           'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# Only the biggest cities go in the nav dropdown. All of them are on areas.html.
NAV_CITIES = ["fort-lauderdale", "pembroke-pines", "hollywood", "miramar",
              "coral-springs", "pompano-beach", "davie", "plantation"]


def href(target, es, root="../"):
    """A link from a generated page. ES pages live in /es/ and link to their
    ES siblings by bare filename; EN pages sit at the root."""
    return target if not es else target


def submenu(kind, es):
    if kind == "services":
        return [(s["slug_es"] + ".html" if es else s["slug"] + ".html",
                 s["nav_es"] if es else s["nav"]) for s in SERVICES]
    cities = [c for c in CITIES if c["slug"] in NAV_CITIES]
    return [((("" if es else "") + c["slug"] + ("-detallado" if es else "-mobile-detailing") + ".html"),
             c["name"]) for c in cities]


def city_slug(c, es):
    return f'{c["slug"]}-detallado.html' if es else f'{c["slug"]}-mobile-detailing.html'


def nav_entry(target, label, es, mobile, kind=None):
    root = "../" if es else ""
    if kind is None:
        return f'<a href="{root if not es else "../"}{target}">{label}</a>' if not es else f'<a href="../{target}">{label}</a>'
    pad = "      " if mobile else "          "
    kids = ("\n" + pad).join(f'<a href="{h}">{l}</a>' for h, l in submenu(kind, es))
    base = f'<a href="../{target}">{label}</a>' if es else f'<a href="{target}">{label}</a>'
    if mobile:
        return f'{base}\n    <div class="mobile-nav__sub">\n      {kids}\n    </div>'
    mid = "m-" + kind
    return (f'<div class="nav__item">{base}'
            f'<button class="nav__more" type="button" aria-expanded="false" '
            f'aria-controls="{mid}" aria-label="More {kind}">{CHEVRON}</button>'
            f'<div class="nav__menu" id="{mid}">\n          {kids}\n        </div></div>')


def header(es, active=""):
    root = "../" if es else ""
    desktop, mobile = [], []
    for target, en, esl in NAV_MAIN:
        label = esl if es else en
        kind = ("services" if target == "services.html"
                else "areas" if target == "areas.html" else None)
        desktop.append(nav_entry(target, label, es, False, kind))
        mobile.append(nav_entry(target, label, es, True, kind))
    cta = "Cotizar" if es else "Get a quote"
    return f'''<header class="site-head">
    <div class="wrap site-head__in">
      <a class="brand" href="{root}index.html">
        {MARK_HEAD}
        <span class="brand__type">Broward <em>Detailing</em></span>
      </a>
      <nav class="nav" aria-label="{'Principal' if es else 'Primary'}">
        {chr(10).join('        ' + d for d in desktop).strip()}
      </nav>
      <div class="head-tools">
        <button class="lang" type="button" data-lang-toggle>{'EN' if es else 'ES'}</button>
        <a class="btn btn--primary" href="{root}contact.html">{cta}</a>
        <button class="burger" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Menu"><span></span></button>
      </div>
    </div>
    <div class="mobile-nav" id="mobile-nav">
    {chr(10).join('    ' + m for m in mobile).strip()}
    </div>
  </header>'''


def footer(es):
    root = "../" if es else ""
    svc = "\n".join(
        f'        <li><a href="{(s["slug_es"] if es else s["slug"])}.html">{s["nav_es"] if es else s["nav"]}</a></li>'
        for s in SERVICES)
    cities = "\n".join(
        f'        <li><a href="{city_slug(c, es)}">{c["name"]}</a></li>'
        for c in CITIES[:10])
    if es:
        h_s, h_c, h_co = "Servicios", "Ciudades", "Contacto"
        tag = "Detallado de autos a domicilio en todo el condado de Broward."
        legal = "Precios desde, según tamaño y estado del vehículo."
    else:
        h_s, h_c, h_co = "Services", "Cities", "Contact"
        tag = "Mobile car detailing across Broward County, Florida."
        legal = "Prices shown are starting prices and vary by vehicle size and condition."
    return f'''<footer class="site-foot">
    <div class="wrap">
      <div class="foot-grid">
        <div>
          <a class="brand" href="{root}index.html">{MARK_FOOT}<span class="brand__type">Broward <em>Detailing</em></span></a>
          <p style="margin-top:var(--sp-2);font-size:var(--step--1);max-width:30ch">{tag}</p>
        </div>
        <div class="foot-col--wide">
          <h4>{h_s}</h4>
          <ul>
{svc}
          </ul>
        </div>
        <div>
          <h4>{h_c}</h4>
          <ul>
{cities}
            <li><a href="{root}areas.html"><b>{'Ver todas' if es else 'See all'}</b></a></li>
          </ul>
        </div>
        <div>
          <h4>{h_co}</h4>
          <ul>
            <li><a data-tel="text" href="tel:+19545550147">(954) 555-0147</a></li>
            <li><a data-email="text" href="mailto:quotes@browardmobiledetailing.com">quotes@browardmobiledetailing.com</a></li>
            <li><a href="{root}contact.html">{'Pedir cotización' if es else 'Get a quote'}</a></li>
          </ul>
        </div>
      </div>
      <div class="foot-note">
        <span>&copy; {datetime.date.today().year} {BRAND}</span>
        <span>{legal}</span>
      </div>
    </div>
  </footer>'''


def head(title, meta, canonical, alt_href, es, extra=""):
    """<head>. When alt_href is given, the EN/ES pair is joined with hreflang.

    Pages with no translated twin pass alt_href=None and get no alternate
    tags at all — pointing hreflang at a URL that 404s is worse than having
    no hreflang, because Google drops the whole annotation and sometimes
    distrusts the rest of the set with it."""
    lang = "es" if es else "en"
    root = "../" if es else ""
    alt_lang = "en" if es else "es"
    alts = ""
    if alt_href:
        alts = (f'<link rel="alternate" hreflang="{lang}" href="{canonical}">\n'
                f'<link rel="alternate" hreflang="{alt_lang}" href="{alt_href}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{BASE}/">\n')
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{canonical}">
{alts}<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}styles.css">
{extra}</head>
<body>
<a class="skip" href="#main">{'Ir al contenido' if es else 'Skip to content'}</a>
'''


def quote_strip(es, preset="", city=""):
    """The quote form. Appears on every generated page — a landing page with no
    form on it is a page that hands the visitor back to Google."""
    if es:
        h = "Reciba su precio hoy"
        p = "Dígamos el carro y la ciudad. Le devolvemos el número completo por mensaje — sin visita, sin sorpresas."
        f_name, f_phone, f_city, f_veh, f_srv = "Nombre", "Teléfono", "Ciudad", "Vehículo", "Servicio"
        ph_name, ph_phone, ph_veh = "Su nombre", "(954) 555-0147", "Ej. Toyota Camry 2021"
        btn, fine = "Pedir mi precio", "Le respondemos el mismo día. Nunca vendemos su información."
    else:
        h = "Get your price today"
        p = "Tell us the car and the city. You get the whole number back by text — no visit, no surprises."
        f_name, f_phone, f_city, f_veh, f_srv = "Name", "Phone", "City", "Vehicle", "Service"
        ph_name, ph_phone, ph_veh = "Your name", "(954) 555-0147", "e.g. 2021 Toyota Camry"
        btn, fine = "Send me my price", "We reply the same day. We never sell your information."

    # NOT html.escape()'d: the nav labels in SERVICES are already HTML source
    # ("Fleet &amp; commercial"), so escaping here produced &amp;amp; and the
    # submitted value arrived as the literal "Fleet &amp; commercial".
    opts = "\n".join(
        f'            <option value="{s["nav_es"] if es else s["nav"]}"'
        f'{" selected" if s["slug"] == preset else ""}>{s["nav_es"] if es else s["nav"]}</option>'
        for s in SERVICES)
    city_opts = "\n".join(
        f'            <option value="{c["name"]}"{" selected" if c["slug"] == city else ""}>{c["name"]}</option>'
        for c in CITIES)

    return f'''<section class="strip" aria-labelledby="quote-h">
    <div class="wrap">
      <div class="strip__head">
        <h2 id="quote-h">{h}</h2>
        <p>{p}</p>
      </div>
      <form data-quote action="/api/lead" method="post">
        <div class="field">
          <label for="q-name">{f_name}</label>
          <input id="q-name" name="name" type="text" autocomplete="name" required placeholder="{ph_name}">
        </div>
        <div class="field">
          <label for="q-phone">{f_phone}</label>
          <input id="q-phone" name="phone" type="tel" autocomplete="tel" required placeholder="{ph_phone}">
        </div>
        <div class="field">
          <label for="q-city">{f_city}</label>
          <select id="q-city" name="city">
{city_opts}
          </select>
        </div>
        <div class="field">
          <label for="q-vehicle">{f_veh}</label>
          <input id="q-vehicle" name="vehicle" type="text" placeholder="{ph_veh}">
        </div>
        <div class="field">
          <label for="q-service">{f_srv}</label>
          <select id="q-service" name="service">
{opts}
          </select>
        </div>
        <!-- Honeypot. Off-screen rather than display:none, which some bots skip. -->
        <div class="vh" aria-hidden="true">
          <label for="q-company">Company</label>
          <input id="q-company" name="company" type="text" tabindex="-1" autocomplete="off">
        </div>
        <button class="btn btn--flare" type="submit">{btn}</button>
        <p class="strip__fine">{fine}</p>
        <p data-status class="vh" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>'''


def cta_final(es, root=""):
    if es:
        h, p, b1, b2 = ("Su carro se ve peor de lo que debería.",
                        "Se arregla el jueves. Llame o pida su precio en un minuto.",
                        "Llamar ahora", "Pedir precio")
    else:
        h, p, b1, b2 = ("Your car looks worse than it needs to.",
                        "That's fixable by Thursday. Call, or get your price in under a minute.",
                        "Call now", "Get my price")
    return f'''<section class="band band--tight band--drench">
    <div class="wrap cta-final rise">
      <h2>{h}</h2>
      <p>{p}</p>
      <div class="btn-row">
        <a class="btn btn--light" data-tel href="tel:+19545550147">{b1}</a>
        <a class="btn btn--outline-light" href="{root}contact.html">{b2}</a>
      </div>
    </div>
  </section>'''


def scripts(es):
    return f'<script src="{"../" if es else ""}main.js"></script>\n</body>\n</html>\n'


def ld_service(s, es):
    """Schema.org Service. Local search leans on this hard."""
    name = s["name_es"] if es else s["name"]
    price = s["price_from"]
    offer = (f',"offers":{{"@type":"Offer","price":"{price}","priceCurrency":"USD",'
             f'"availability":"https://schema.org/InStock"}}') if price else ""
    # json_str, not html.escape: this sits inside JSON, where the escaping rules
    # are JSON's. HTML-escaping a quote here would emit &quot; into a JSON string.
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","serviceType":{json_str(name)},
"provider":{{"@type":"AutoDetailing","name":"{BRAND}","telephone":"+1-954-555-0147",
"areaServed":{{"@type":"AdministrativeArea","name":"Broward County, Florida"}}}}{offer}}}
</script>
'''


def ld_local(c, es):
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"AutoDetailing","name":"{BRAND}",
"telephone":"+1-954-555-0147","areaServed":{{"@type":"City","name":"{c['name']}","containedInPlace":
{{"@type":"AdministrativeArea","name":"Broward County, Florida"}}}},
"priceRange":"$$","url":"{BASE}/{'es/' if es else ''}{city_slug(c, es)}"}}
</script>
'''


# ========================================================== page builders ===
def service_page(s, es):
    slug = s["slug_es"] if es else s["slug"]
    other = s["slug"] if es else s["slug_es"]
    canonical = f"{BASE}/{'es/' if es else ''}{slug}.html"
    alt = f"{BASE}/{'' if es else 'es/'}{other}.html"
    name = s["name_es"] if es else s["name"]
    root = "../" if es else ""

    inc = "\n".join(
        f'''        <div class="kit__item">
          <h3>{t}</h3>
          <p>{d}</p>
        </div>''' for t, d in (s["includes_es"] if es else s["includes"]))

    paras = "\n".join(f"        <p>{p}</p>" for p in (s["body_es"] if es else s["body"]))

    price_line = ""
    if s["price_from"]:
        price_line = (f'<p class="price">{"Desde" if es else "From"} ${s["price_from"]}'
                      f'<small> · {s["hours"]}</small></p>')
    else:
        price_line = f'<p class="price">{"Cotizado" if es else "Quoted"}<small> · {s["hours"]}</small></p>'

    others = "\n".join(
        f'        <li><a href="{(o["slug_es"] if es else o["slug"])}.html">{o["nav_es"] if es else o["nav"]}</a></li>'
        for o in SERVICES if o["slug"] != s["slug"])

    return (head(s["title_es"] if es else s["title"],
                 s["meta_es"] if es else s["meta"],
                 canonical, alt, es, extra=ld_service(s, es))
            + header(es) + f'''
  <main id="main">
  <section class="band band--steel">
    <div class="wrap">
      <p class="said">{"Servicio a domicilio · Condado de Broward" if es else "Mobile service · Broward County"}</p>
      <h1>{name}</h1>
      <p class="lede">{s["lede_es"] if es else s["lede"]}</p>
      {price_line}
      <div class="btn-row" style="margin-top:var(--sp-3)">
        <a class="btn btn--flare" data-tel href="tel:+19545550147">{"Llamar" if es else "Call"} (954) 555-0147</a>
        <a class="btn btn--outline-light" href="#quote-h">{"Pedir precio" if es else "Get my price"}</a>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap wrap--narrow prose rise">
{paras}
    </div>
  </section>

  <section class="band band--surface" aria-labelledby="inc-h">
    <div class="wrap">
      <div class="head rise">
        <h2 id="inc-h">{"Qué incluye" if es else "What's included"}</h2>
      </div>
      <div class="kit rise">
{inc}
      </div>
    </div>
  </section>

  {quote_strip(es, preset=s["slug"])}

  <section class="band" aria-labelledby="oth-h">
    <div class="wrap">
      <div class="head rise"><h2 id="oth-h">{"Otros servicios" if es else "Other services"}</h2></div>
      <ul class="cities rise">
{others}
      </ul>
    </div>
  </section>

  {cta_final(es, root)}
  </main>
''' + footer(es) + "\n" + scripts(es))


def city_page(c, es):
    slug = city_slug(c, es)
    other = city_slug(c, not es)
    canonical = f"{BASE}/{'es/' if es else ''}{slug}"
    alt = f"{BASE}/{'' if es else 'es/'}{other}"
    root = "../" if es else ""
    n = c["name"]

    if es:
        title = f"Detallado de autos a domicilio en {n}, FL | {BRAND}"
        meta = (f"Detallado móvil en {n}. Vamos a su casa u oficina con agua y "
                f"electricidad propias. Desde $99. Citas esta misma semana.")
        h1 = f"Detallado de autos a domicilio en {n}"
        said = f"{n}, Florida"
    else:
        title = f"Mobile Car Detailing in {n}, FL | We Come to You | {BRAND}"
        meta = (f"Mobile detailing in {n}. We bring our own water and power to your "
                f"home or office. From $99. Same-week appointments.")
        h1 = f"Mobile Car Detailing in {n}"
        said = f"{n}, Florida"

    paras = "\n".join(f"        <p>{p}</p>" for p in (c["para_es"] if es else c["para"]))

    svc_rows = "\n".join(f'''        <div class="row">
          <h3><a href="{(s["slug_es"] if es else s["slug"])}.html" style="color:inherit;text-decoration:none">{s["nav_es"] if es else s["nav"]}</a></h3>
          <p>{s["lede_es"] if es else s["lede"]} {"Desde" if es else "From"} ${s["price_from"]}.</p>
        </div>''' for s in SERVICES if s["price_from"])

    nearby = [o for o in CITIES if o["slug"] != c["slug"]][:8]
    near = "\n".join(f'        <li><a href="{city_slug(o, es)}">{o["name"]}</a></li>' for o in nearby)

    return (head(title, meta, canonical, alt, es, extra=ld_local(c, es))
            + header(es) + f'''
  <main id="main">
  <section class="band band--steel">
    <div class="wrap">
      <p class="said">{said}</p>
      <h1>{h1}</h1>
      <p class="lede">{c["hook_es"] if es else c["hook"]} {"Llevamos nuestra propia agua y electricidad." if es else "We bring our own water and power."}</p>
      <div class="trust" style="margin-top:var(--sp-4)">
        <div class="trust__i"><span class="trust__n">$99</span><span class="trust__l">{"Exterior, desde" if es else "Exterior detail, from"}</span></div>
        <div class="trust__i"><span class="trust__n">{"Esta semana" if es else "This week"}</span><span class="trust__l">{"Citas disponibles" if es else "Appointments available"}</span></div>
        <div class="trust__i"><span class="trust__n">{"0 gal"}</span><span class="trust__l">{"De su agua" if es else "Of your water used"}</span></div>
        <div class="trust__i"><span class="trust__n">{"1 min"}</span><span class="trust__l">{"Para su precio" if es else "To get your price"}</span></div>
      </div>
      <div class="btn-row" style="margin-top:var(--sp-4)">
        <a class="btn btn--flare" data-tel href="tel:+19545550147">{"Llamar" if es else "Call"} (954) 555-0147</a>
        <a class="btn btn--outline-light" href="#quote-h">{"Pedir precio" if es else "Get my price"}</a>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap wrap--narrow prose rise">
      <h2>{"Detallado en" if es else "Detailing in"} {n}</h2>
{paras}
      <p style="color:var(--muted);font-size:var(--step--1);margin-top:var(--sp-3)">
        <b>{"Zonas" if es else "Areas"}:</b> {c["areas"]}<br>
        <b>{"Códigos postales" if es else "ZIP codes"}:</b> {c["zip_"]}
      </p>
    </div>
  </section>

  <section class="band band--surface" aria-labelledby="svc-h">
    <div class="wrap">
      <div class="head rise"><h2 id="svc-h">{"Servicios en" if es else "Services in"} {n}</h2></div>
      <div class="rows rise">
{svc_rows}
      </div>
    </div>
  </section>

  {quote_strip(es, city=c["slug"])}

  <section class="band" aria-labelledby="near-h">
    <div class="wrap">
      <div class="head rise"><h2 id="near-h">{"También atendemos" if es else "We also cover"}</h2></div>
      <ul class="cities rise">
{near}
        <li><a href="{root}areas.html"><b>{"Todo el condado" if es else "All of Broward"}</b></a></li>
      </ul>
    </div>
  </section>

  {cta_final(es, root)}
  </main>
''' + footer(es) + "\n" + scripts(es))


# ============================================================= core pages ===
# Vehicle tiers. Every "from" price on the site is the sedan number; these are
# the multipliers that turn it into the real one. Published, because the
# argument this site makes is that you get the whole number without a visit.
TIERS = [
    ("Coupe / sedan", "Cupé / sedán", "Base price", "Precio base"),
    ("SUV / small truck", "SUV / camioneta", "+$40", "+$40"),
    ("3-row SUV / van / dually", "SUV de 3 filas / van", "+$80", "+$80"),
]

FAQ = [
    ("Do you need my water or electricity?",
     "¿Necesitan mi agua o electricidad?",
     "No. The van carries its own water tank and generator, so we can work in a condo garage, an office car park or a driveway with the tap shut off. If you would rather we used your hose, that is fine too.",
     "No. La van lleva su propio tanque de agua y generador, así que podemos trabajar en un garaje de condominio, un estacionamiento de oficina o una entrada con la llave cerrada. Si prefiere que usemos su manguera, también está bien."),
    ("How long does it take?",
     "¿Cuánto tarda?",
     "An exterior detail is about 90 minutes, a full detail three to four hours, and a ceramic coating is a one or two day job because the paint has to be prepped and the coating has to cure. We give you the real window when we book, not an optimistic one.",
     "Un detallado exterior toma unos 90 minutos, uno completo de tres a cuatro horas, y un recubrimiento cerámico es trabajo de uno o dos días porque hay que preparar la pintura y dejar curar. Le damos la ventana real al reservar, no una optimista."),
    ("Do I have to be there?",
     "¿Tengo que estar presente?",
     "No, as long as we can reach the vehicle and you are reachable by phone. Plenty of our work happens while people are at work or asleep after a night shift. For gated communities we need your name at the guardhouse in advance.",
     "No, mientras podamos llegar al vehículo y usted esté disponible por teléfono. Mucho de nuestro trabajo ocurre mientras la gente trabaja o duerme después de un turno de noche. En comunidades cerradas necesitamos su nombre en la caseta con anticipación."),
    ("What if it rains?",
     "¿Y si llueve?",
     "This is Florida, so it will. If a storm lands mid-job we wait it out or reschedule at no charge — you are never billed for a job the weather cut short. Covered garages are unaffected, which is why we like them.",
     "Esto es Florida, así que va a llover. Si cae una tormenta a mitad del trabajo, esperamos o reprogramamos sin cargo — nunca se le cobra por un trabajo que el clima cortó. Los garajes techados no se ven afectados, y por eso nos gustan."),
    ("Is the price you quote the price I pay?",
     "¿El precio que cotizan es el que pago?",
     "Yes. The only things that change a quote are things you tell us about on the call — pet hair, heavy pet or smoke odour, or a vehicle much bigger than described. We would rather have that conversation on the phone than in your driveway.",
     "Sí. Lo único que cambia una cotización son cosas que usted nos cuenta en la llamada — pelo de mascota, olor fuerte a mascota o humo, o un vehículo mucho más grande de lo descrito. Preferimos esa conversación por teléfono y no en su entrada."),
    ("Which areas do you cover?",
     "¿Qué zonas cubren?",
     "All of Broward County, from Deerfield Beach down to Hallandale and west to Weston. Travel is not charged separately anywhere in the county.",
     "Todo el condado de Broward, desde Deerfield Beach hasta Hallandale y al oeste hasta Weston. El viaje no se cobra aparte en ningún punto del condado."),
]


def faq_block(es):
    items = "\n".join(f'''      <details>
        <summary>{q_es if es else q}</summary>
        <div>{a_es if es else a}</div>
      </details>''' for q, q_es, a, a_es in FAQ)
    ld = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (json_str(q_es if es else q), json_str(a_es if es else a))
        for q, q_es, a, a_es in FAQ)
    return f'''<section class="band" aria-labelledby="faq-h">
    <div class="wrap wrap--narrow">
      <div class="head rise"><h2 id="faq-h">{"Preguntas frecuentes" if es else "Common questions"}</h2></div>
      <div class="faq rise">
{items}
      </div>
    </div>
  </section>
  <script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{ld}]}}
  </script>'''


def json_str(s):
    """JSON string literal for embedding in ld+json."""
    import json as _json
    return _json.dumps(html.unescape(s))


def plans_block(es):
    """Three headline packages. The middle one is the one we want booked."""
    picks = [
        (SERVICES[2], False),   # exterior
        (SERVICES[0], True),    # full detail — the pick
        (SERVICES[3], False),   # ceramic
    ]
    out = []
    for s, pick in picks:
        items = "\n".join(f"          <li>{t}</li>" for t, _ in (s["includes_es"] if es else s["includes"])[:5])
        tag = f'<span class="plan__tag">{"Más pedido" if es else "Most booked"}</span>' if pick else ""
        out.append(f'''      <div class="plan{' plan--pick' if pick else ''}">
        {tag}
        <h3>{s["name_es"] if es else s["name"]}</h3>
        <div class="plan__from">
          <span class="plan__price">${s["price_from"]}</span>
          <span class="plan__unit">{"desde · " if es else "from · "}{s["hours"]}</span>
        </div>
        <ul>
{items}
        </ul>
        <a class="btn btn--primary" href="{(s["slug_es"] if es else s["slug"])}.html">{"Ver detalles" if es else "See what's included"}</a>
      </div>''')
    return "\n".join(out)


def home(es):
    canonical = f"{BASE}/{'es/' if es else ''}"
    alt = f"{BASE}/{'' if es else 'es/'}"
    root = "../" if es else ""
    if es:
        title = "Detallado de autos a domicilio en Broward County | Vamos a su casa"
        meta = ("Detallado móvil en todo el condado de Broward. Llevamos agua y electricidad. "
                "Desde $99. Reciba su precio completo por mensaje en un minuto.")
        h1 = 'Su carro limpio<br>sin salir de <span class="wet">casa</span>'
        sub = ("Detallado a domicilio en todo el condado de Broward. Llevamos nuestra propia agua "
               "y electricidad. Usted recibe el precio completo por mensaje — sin visita, sin sorpresas.")
    else:
        title = "Mobile Car Detailing in Broward County FL | We Come to You"
        meta = ("Mobile detailing across Broward County. We bring our own water and power. "
                "From $99. Get your full price by text in under a minute.")
        h1 = 'Your car, detailed<br>in your own <span class="wet">driveway</span>'
        sub = ("Mobile detailing across all of Broward County. We bring our own water and power. "
               "You get the whole price by text — no visit, no surprises.")

    tiles = "\n".join(f'''        <a class="tile{' tile--wide' if i == 0 else ''}" href="{(s["slug_es"] if es else s["slug"])}.html">
          <h3>{s["nav_es"] if es else s["nav"]}</h3>
          <p>{s["lede_es"] if es else s["lede"]}</p>
        </a>''' for i, s in enumerate(SERVICES[:6]))

    steps = [
        ("Tell us the car", "Díganos el carro", "Make, model and your city. Thirty seconds by phone or form.",
         "Marca, modelo y su ciudad. Treinta segundos por teléfono o formulario."),
        ("Get the whole number", "Reciba el número completo", "By text, before anyone comes out. Not a range, not a 'starting at'.",
         "Por mensaje, antes de que alguien salga. No un rango ni un 'desde'."),
        ("We come to you", "Vamos a usted", "Home, office or condo garage. We bring water and power.",
         "Casa, oficina o garaje. Llevamos agua y electricidad."),
        ("Pay when it's done", "Pague al terminar", "Card, cash or Zelle, after you have looked at it.",
         "Tarjeta, efectivo o Zelle, después de que lo revise."),
    ]
    steps_html = "\n".join(f'''        <div class="step">
          <h3>{t_es if es else t}</h3>
          <p>{d_es if es else d}</p>
        </div>''' for t, t_es, d, d_es in steps)

    cities_html = "\n".join(f'        <li><a href="{city_slug(c, es)}">{c["name"]}</a></li>' for c in CITIES)

    return (head(title, meta, canonical, alt, es) + header(es) + f'''
  <main id="main">
  <section class="hero">
    <div class="hero__scrim"></div>
    <div class="hero__glow"></div>
    <div class="wrap hero__in">
      <h1>{h1}</h1>
      <p class="hero__sub">{sub}</p>
      <div class="btn-row">
        <a class="btn btn--flare" data-tel href="tel:+19545550147">{"Llamar" if es else "Call"} (954) 555-0147</a>
        <a class="btn btn--outline-light" href="#quote-h">{"Pedir mi precio" if es else "Get my price"}</a>
      </div>
      <div class="trust">
        <div class="trust__i"><span class="trust__n">31</span><span class="trust__l">{"Ciudades de Broward atendidas" if es else "Broward cities covered"}</span></div>
        <div class="trust__i"><span class="trust__n">$99</span><span class="trust__l">{"Exterior completo, desde" if es else "Full exterior detail, from"}</span></div>
        <div class="trust__i"><span class="trust__n">0</span><span class="trust__l">{"Galones de su agua" if es else "Gallons of your water used"}</span></div>
        <div class="trust__i"><span class="trust__n">1 min</span><span class="trust__l">{"Para tener su precio" if es else "To get your price"}</span></div>
      </div>
    </div>
  </section>

  {quote_strip(es)}

  <section class="band" aria-labelledby="svc-h">
    <div class="wrap">
      <div class="head head--split rise">
        <h2 id="svc-h">{"Lo que hacemos" if es else "What we do"}</h2>
        <p class="lede">{"Desde un lavado a mano hasta un cerámico de varios años. Todo en su entrada." if es else "From a hand wash to a multi-year ceramic coating. All of it in your driveway."}</p>
      </div>
      <div class="tiles tiles--six rise">
{tiles}
      </div>
    </div>
  </section>

  <section class="band band--surface" aria-labelledby="how-h">
    <div class="wrap">
      <div class="head rise"><h2 id="how-h">{"Cómo funciona" if es else "How it works"}</h2></div>
      <div class="steps rise">
{steps_html}
      </div>
    </div>
  </section>

  <section class="band" aria-labelledby="plan-h">
    <div class="wrap">
      <div class="head head--split rise">
        <h2 id="plan-h">{"Paquetes" if es else "Packages"}</h2>
        <p class="lede">{"Precios para sedán. Los vehículos más grandes cuestan más y aquí decimos cuánto." if es else "Sedan prices. Bigger vehicles cost more, and we tell you how much."}</p>
      </div>
      <div class="plans rise">
{plans_block(es)}
      </div>
      <p style="margin-top:var(--sp-4)"><a href="{root}pricing.html">{"Ver todos los precios y tamaños →" if es else "See every price and vehicle size →"}</a></p>
    </div>
  </section>

  <section class="band band--steel" aria-labelledby="area-h">
    <div class="wrap">
      <div class="head head--split rise">
        <h2 id="area-h">{"Todo el condado de Broward" if es else "All of Broward County"}</h2>
        <p class="lede">{"El viaje no se cobra aparte en ningún punto del condado." if es else "Travel is not charged separately anywhere in the county."}</p>
      </div>
      <ul class="cities rise">
{cities_html}
      </ul>
    </div>
  </section>

  {faq_block(es)}

  {cta_final(es, root)}
  </main>
''' + footer(es) + "\n" + scripts(es))


def simple_page(es, slug, title, meta, h1, lede, body_html, extra_ld=""):
    """The core pages that are mostly prose. One chrome, one footer."""
    canonical = f"{BASE}/{slug}"
    return (head(title, meta, canonical, None, es, extra=extra_ld) + header(es) + f'''
  <main id="main">
  <section class="band band--steel">
    <div class="wrap">
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
    </div>
  </section>
{body_html}
  {cta_final(es)}
  </main>
''' + footer(es) + "\n" + scripts(es))


def services_page():
    rows = "\n".join(f'''        <div class="row">
          <h3><a href="{s["slug"]}.html" style="color:inherit;text-decoration:none">{s["name"]}</a></h3>
          <p>{s["lede"]} <b>{"From $" + str(s["price_from"]) if s["price_from"] else "Quoted per job"}</b> · {s["hours"]}</p>
        </div>''' for s in SERVICES)
    body = f'''  <section class="band">
    <div class="wrap">
      <div class="rows rise">
{rows}
      </div>
    </div>
  </section>

  {quote_strip(False)}
'''
    return simple_page(False, "services.html",
                       f"Mobile Detailing Services in Broward County | {BRAND}",
                       "Every mobile detailing service we offer across Broward County — full details, interiors, ceramic coating, paint correction, boats and fleets.",
                       "Everything we do",
                       "Nine services, all of them mobile, all of them priced before anyone comes out.",
                       body)


def pricing_page():
    rows = "\n".join(f'''        <div class="row">
          <h3>{s["name"]}</h3>
          <p><b>{"From $" + str(s["price_from"]) if s["price_from"] else "Quoted per job"}</b> · {s["hours"]}<br>{s["lede"]}</p>
        </div>''' for s in SERVICES)
    tiers = "\n".join(f'''        <div class="row">
          <h3>{en}</h3>
          <p>{adj_en}</p>
        </div>''' for en, _, adj_en, _ in TIERS)
    body = f'''  <section class="band">
    <div class="wrap">
      <div class="head rise"><h2>Starting prices</h2>
      <p class="lede">Every number below is for a coupe or sedan in normal condition.</p></div>
      <div class="rows rise">
{rows}
      </div>
    </div>
  </section>

  <section class="band band--surface">
    <div class="wrap">
      <div class="head rise"><h2>Vehicle size</h2>
      <p class="lede">Published rather than discovered in your driveway.</p></div>
      <div class="rows rise">
{tiers}
      </div>
      <p class="form-note" style="margin-top:var(--sp-4)">
        Two things can move a quote beyond size, and we ask about both on the call:
        heavy pet hair, and smoke or mildew odour. Everything else is included.
      </p>
    </div>
  </section>

  {quote_strip(False)}
'''
    return simple_page(False, "pricing.html",
                       f"Mobile Detailing Prices in Broward County | {BRAND}",
                       "What mobile detailing costs in Broward County. Starting prices for every service and what each vehicle size adds. No hidden fees.",
                       "What it costs",
                       "The whole price list, including what bigger vehicles add. No estimate visit, no surprises at the end.",
                       body)


def areas_page():
    cities_html = "\n".join(
        f'        <li><a href="{city_slug(c, False)}">{c["name"]}</a></li>' for c in CITIES)
    # Municipalities we serve but have not written a page for. Listed honestly
    # as plain text — linking them to nothing, or to a thin page, helps nobody.
    others = ["Lauderdale Lakes", "North Lauderdale", "Wilton Manors", "Lighthouse Point",
              "Lauderdale-by-the-Sea", "Hillsboro Beach", "Pembroke Park", "West Park",
              "Southwest Ranches", "Sea Ranch Lakes", "Lazy Lake"]
    body = f'''  <section class="band">
    <div class="wrap">
      <div class="head rise"><h2>Cities we cover</h2>
      <p class="lede">Travel is not charged separately anywhere in Broward County.</p></div>
      <ul class="cities rise">
{cities_html}
      </ul>
      <p class="form-note" style="margin-top:var(--sp-5)">
        We also cover {", ".join(others[:-1])} and {others[-1]} — call for a slot.
      </p>
    </div>
  </section>

  {quote_strip(False)}
'''
    return simple_page(False, "areas.html",
                       f"Service Area — All of Broward County | {BRAND}",
                       "Mobile detailing across every city in Broward County, from Deerfield Beach to Hallandale and west to Weston. No travel charge.",
                       "Where we work",
                       "Every municipality in Broward County, from Deerfield Beach down to Hallandale and west to Weston.",
                       body)


def about_page():
    body = '''  <section class="band">
    <div class="wrap wrap--narrow prose rise">
      <h2>Why mobile, and why the price up front</h2>
      <p>Two things make detailing frustrating to buy. The first is the estimate visit
      — driving somewhere, leaving the car, waiting for a number. The second is the
      number itself, which has a habit of arriving as "starting at" and finishing
      somewhere else entirely.</p>
      <p>We built this around removing both. You tell us the vehicle and the city, and
      you get the complete price back by text before anyone gets in a van. The van
      carries its own water and generator, so the work happens where the car already
      is — a driveway in Cooper City, a condo garage in Hallandale, an office car park
      in Sunrise.</p>
      <h2>What we will talk you out of</h2>
      <p>A ceramic coating over damaged paint seals the damage in for three years. A
      full detail on a garage-kept car that does 2,000 miles a year is usually more
      than it needs. Headlight kits from the parts store work for about six weeks.</p>
      <p>We would rather book you the ninety-dollar job that is right than the
      seven-hundred-dollar one that is not, because this business runs on the second
      call and the neighbour who saw us in the driveway.</p>
      <h2>Working in Broward</h2>
      <p>This county has its own rules. Gated communities need a name at the guardhouse.
      HOAs in Coral Springs and Coconut Creek care about noise, hours and where the
      water goes. Buildings in Fort Lauderdale and Hallandale want to know who is
      running a generator in their garage. We deal with all of it as a matter of
      routine — tell us the situation when you book and it stops being a problem.</p>
    </div>
  </section>

  ''' + quote_strip(False) + "\n"
    return simple_page(False, "about.html",
                       f"About {BRAND} | Mobile Detailing Done at Your Door",
                       "Why we quote the whole price before anyone comes out, and what we will talk you out of. Mobile detailing across Broward County.",
                       "Straight price, at your door",
                       "No estimate visit, no moving number, and honest advice about what your car actually needs.",
                       body)


def contact_page():
    body = f'''  <section class="band">
    <div class="wrap split">
      <div class="rise">
        <h2>Get your price</h2>
        <p class="lede" style="color:var(--muted)">Tell us the vehicle and the city. We reply the same day with the whole number.</p>
        <div class="rail" style="margin-top:var(--sp-5)">
          <div class="rail__item">
            <span class="rail__label">Call or text</span>
            <a class="rail__value" data-tel="text" href="tel:+19545550147">(954) 555-0147</a>
          </div>
          <div class="rail__item">
            <span class="rail__label">Email</span>
            <a class="rail__value" data-email="text" href="mailto:quotes@browardmobiledetailing.com">quotes@browardmobiledetailing.com</a>
          </div>
          <div class="rail__item">
            <span class="rail__label">Hours</span>
            <span class="rail__value">Mon–Sat, 8am–6pm</span>
          </div>
          <div class="rail__item">
            <span class="rail__label">Service area</span>
            <span class="rail__value">All of Broward County</span>
          </div>
        </div>
      </div>
      <div class="rise">
        <form class="form-light" data-quote action="/api/lead" method="post">
          <div class="field">
            <label for="c-name">Name</label>
            <input id="c-name" name="name" type="text" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="c-phone">Phone</label>
            <input id="c-phone" name="phone" type="tel" autocomplete="tel" required>
          </div>
          <div class="field">
            <label for="c-email">Email <span style="color:var(--muted);font-weight:400">(optional)</span></label>
            <input id="c-email" name="email" type="email" autocomplete="email">
          </div>
          <div class="field">
            <label for="c-city">City</label>
            <select id="c-city" name="city">
{chr(10).join(f'              <option value="{c["name"]}">{c["name"]}</option>' for c in CITIES)}
              <option value="Other Broward">Somewhere else in Broward</option>
            </select>
          </div>
          <div class="field">
            <label for="c-vehicle">Vehicle</label>
            <input id="c-vehicle" name="vehicle" type="text" placeholder="e.g. 2021 Toyota Camry">
          </div>
          <div class="field">
            <label for="c-service">Service</label>
            <select id="c-service" name="service">
{chr(10).join(f'              <option value="{s["nav"]}">{s["nav"]}</option>' for s in SERVICES)}
              <option value="Not sure">Not sure — tell me what it needs</option>
            </select>
          </div>
          <div class="field">
            <label for="c-notes">Anything we should know? <span style="color:var(--muted);font-weight:400">(optional)</span></label>
            <textarea id="c-notes" name="notes" placeholder="Pet hair, a gated community, a stain you want gone…"></textarea>
          </div>
          <div class="vh" aria-hidden="true">
            <label for="c-company">Company</label>
            <input id="c-company" name="company" type="text" tabindex="-1" autocomplete="off">
          </div>
          <div class="form-foot">
            <button class="btn btn--primary" type="submit">Send me my price</button>
            <p class="form-note">We reply the same day, Monday to Saturday. We never sell your information.</p>
            <p data-status class="vh" role="status" aria-live="polite"></p>
          </div>
        </form>
      </div>
    </div>
  </section>
'''
    return simple_page(False, "contact.html",
                       f"Get a Quote | {BRAND}",
                       "Tell us the vehicle and your city and get the whole price back the same day. Mobile detailing across Broward County.",
                       "Get your price",
                       "One minute now, the whole number back today. No estimate visit.",
                       body)


# =================================================================== write ===
def write(path, content):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return path


def main():
    # Core pages first — same chrome as everything else, generated from the
    # same nav data, so the header can never drift between the hand-made and
    # the generated half of the site.
    write("index.html", home(False))
    write("es/index.html", home(True))
    write("services.html", services_page())
    write("pricing.html", pricing_page())
    write("areas.html", areas_page())
    write("about.html", about_page())
    write("contact.html", contact_page())

    written = []
    for s in SERVICES:
        written.append(write(f'{s["slug"]}.html', service_page(s, False)))
        written.append(write(f'es/{s["slug_es"]}.html', service_page(s, True)))
    for c in CITIES:
        written.append(write(city_slug(c, False), city_page(c, False)))
        written.append(write(f'es/{city_slug(c, True)}', city_page(c, True)))

    # ------------------------------------------------------------ sitemap ---
    static = ["index.html", "services.html", "pricing.html", "areas.html",
              "about.html", "contact.html", "es/index.html"]
    today = datetime.date.today().isoformat()
    urls = []
    for path in static + written:
        # cleanUrls is on in vercel.json, so index.html is served at / and
        # foo.html at /foo. The sitemap must match what is actually served or
        # every entry redirects.
        loc = path[:-len("index.html")] if path.endswith("index.html") else path[:-len(".html")]
        prio = "1.0" if path == "index.html" else "0.8" if path in static else "0.7"
        urls.append(f"  <url><loc>{BASE}/{loc}</loc><lastmod>{today}</lastmod>"
                    f"<priority>{prio}</priority></url>")
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(urls) + "\n</urlset>\n")

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")

    print(f"{len(written)} landing pages")
    print(f"  {len(SERVICES)} services × 2 languages")
    print(f"  {len(CITIES)} cities × 2 languages")
    print(f"sitemap.xml: {len(urls)} URLs")


if __name__ == "__main__":
    main()
