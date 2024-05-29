import psycopg2
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd


try:
    connection=psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '123456789',
        database = 'kaggle1'
    )
    print("Connected")
    cursor = connection.cursor()
    cursor.execute("SELECT version()")
    row = cursor.fetchone()
    print(row)


    app = dash.Dash(__name__)
    ################################################################################################################
    #GRAFICAS ESCENARIO 1

    cursor.execute('''SELECT t.company, COUNT(id_trip) AS number_of_trips, AVG(trip_miles) AS avg_miles_per_trip,
				AVG(trip_seconds) AS avg_time_per_trip			  
                FROM trip tr
                JOIN bill b ON tr.id_trip = b.trip_number
                JOIN taxi t ON b.taxi_ref = t.id_taxi AND b.company_name = t.company
                GROUP BY t.company;''')

    rows = cursor.fetchall()
    
    fig1 = px.scatter_3d(rows, x= 1, y= 2, z=3,
            color= 0, title="Taxi performance per company")
    
    fig1.update_scenes(xaxis_title_text="Number of Trips",  
                  yaxis_title_text= "Average miles per Trip (mi)",  
                  zaxis_title_text="Average time per Trip (s)" )
    fig1.update_layout(width=700, margin=dict(r=10, l=10, b=10, t=10))

    

    cursor.execute('''SELECT company_name, COUNT(trip_number) FROM bill GROUP BY company_name;
                    ''')
    rows = cursor.fetchall()
    fig11 = px.bar(rows, x = 0, y = 1, color_discrete_sequence=["#b52a64"])
    fig11.update_layout(
        xaxis_title="Company",
        yaxis_title="Number of Trips")


    cursor.execute('''SELECT t.company, AVG(trip_miles) AS avg_miles_per_trip			  
                FROM trip tr
                JOIN bill b ON tr.id_trip = b.trip_number
                JOIN taxi t ON b.taxi_ref = t.id_taxi AND b.company_name = t.company
                GROUP BY t.company;''')
    rows = cursor.fetchall()
    fig12 = px.bar(rows, x = 0, y = 1, color_discrete_sequence=["#FF5733"])
    fig12.update_layout(
        xaxis_title="Company",
        yaxis_title="Average miles per trip (mi)")


    cursor.execute('''SELECT t.company, AVG(trip_seconds) AS avg_time_per_trip			  
                FROM trip tr
                JOIN bill b ON tr.id_trip = b.trip_number
                JOIN taxi t ON b.taxi_ref = t.id_taxi AND b.company_name = t.company
                GROUP BY t.company;''')
    rows = cursor.fetchall()
    fig13 = px.bar(rows, x = 0, y = 1, color_discrete_sequence=["#FFC300"])
    fig13.update_layout(
        xaxis_title="Company",
        yaxis_title="Average time per trip (s)")


    cursor.execute('''SELECT t.company, AVG(total) AS avg_bill_total, SUM(total) AS total_profit			  
                FROM bill b
                JOIN taxi t ON b.taxi_ref = t.id_taxi AND b.company_name = t.company
                GROUP BY t.company;''')
    rows = cursor.fetchall()
    fig2 = px.bar(rows, x = 1, y = 0, color = 2, orientation = 'h')
    fig2.update_layout(
        xaxis_title="Profit per trip (USD)",
        yaxis_title="Company",
        legend_title= "Total Profit")
    #########################################################################################################
    #GRAFICAS ESCENARIO 2

    cursor.execute('''SELECT p.community_area, COUNT(t.id_trip) AS total_trips, EXTRACT(HOUR FROM t.start_time) AS trip_hour,
                    CASE
                        WHEN EXTRACT(HOUR FROM t.start_time) BETWEEN 6 AND 10 THEN 'Morning Peak'
                        WHEN EXTRACT(HOUR FROM t.start_time) BETWEEN 11 AND 15 THEN 'Midday'
                        WHEN EXTRACT(HOUR FROM t.start_time) BETWEEN 16 AND 20 THEN 'Evening Peak'
                        ELSE 'Off-Peak'
                    END AS peak_time
                FROM trip t 
                JOIN pickup_info p ON t.pickup_infoid = p.id_pickup
                GROUP BY p.community_area, trip_hour
                ORDER BY p.community_area, trip_hour;''')
    rows = cursor.fetchall()
    fig3 = px.scatter(rows, x = 2, y = 0, size = 1, color = 3, width=2000, height=800)
    fig3.update_layout(
        title = "Peak times per Community Area",
        xaxis_title="Hour",
        yaxis_title="Community Area Number",
        legend_title= "Peak Type",
        hovermode = 'y unified')
    fig3.update_yaxes(tick0=0, dtick= 5)
    fig3.update_xaxes(tick0=0, dtick= 1)
    
    #########################################################################################################
    #GRAFICAS ESCENARIO 3

    cursor.execute('''SELECT b.payment_type, COUNT(*) AS payment_count, p.community_area
                    FROM bill b
                    JOIN trip t ON b.trip_number = t.id_trip
                    JOIN pickup_info p ON t.pickup_infoid = p.id_pickup
                    GROUP BY b.payment_type, p.community_area
                    ORDER BY p.community_area;''')
    rows = cursor.fetchall()
    fig4 = px.scatter(rows, x = 2, y = 1, facet_col= 0, log_y= True, width=2500, height=1000)
    fig4.update_traces(marker_size=8)
    fig4.update_yaxes(tick0=0, dtick= 5)
    fig4.update_xaxes(tick0=0, dtick= 5)
    fig4.update_layout(
        title = "Payment method by Area and Time",
        xaxis_title="Community Area Number",
        yaxis_title="Payments realized",
        legend_title= "Payment method")
    
    #########################################################################################################
    #GRAFICAS ESCENARIO 3

    cursor.execute('''SELECT  COUNT(id_trip),
                    CASE 
                        WHEN EXTRACT(MONTH FROM start_date) = 1 THEN 'Enero'
                        WHEN EXTRACT(MONTH FROM start_date) = 2 THEN 'Febrero'
                        WHEN EXTRACT(MONTH FROM start_date) = 3 THEN 'Marzo'
                        WHEN EXTRACT(MONTH FROM start_date) = 4 THEN 'Abril'
                        WHEN EXTRACT(MONTH FROM start_date) = 5 THEN 'Mayo'
                        WHEN EXTRACT(MONTH FROM start_date) = 6 THEN 'Junio'
                        WHEN EXTRACT(MONTH FROM start_date) = 7 THEN 'Julio'
                        WHEN EXTRACT(MONTH FROM start_date) = 8 THEN 'Agosto'
                        WHEN EXTRACT(MONTH FROM start_date) = 9 THEN 'Septiembre'
                        WHEN EXTRACT(MONTH FROM start_date) = 10 THEN 'Octubre'
                        WHEN EXTRACT(MONTH FROM start_date) = 11 THEN 'Noviembre'
                        WHEN EXTRACT(MONTH FROM start_date) = 12 THEN 'Diciembre'
                END AS month
                FROM trip
                   GROUP BY month
                   ORDER BY month;''')
    rows = cursor.fetchall()
    fig5 = px.bar(rows, x= 1, y=0 ,width=2000, height=1000)
    
    ###########################################################################################################
   
    app.layout = html.Div(children=[
            html.H1(children = "Chicago Taxi Trips Analytics"),

            html.H2('ESCENARIO 1: Análisis de Rendimiento de Taxis por Empresas'),
            html.Div(children = '''Este análisis se centra en examinar el rendimiento de las diferentes empresas de taxis en términos de tiempo y distancia de viaje,
                                    así como la cantidad de ingresos generados. 
                                    Calculando métricas como la cantidad promedio de millas por viaje, el tiempo promedio de viaje y los ingresos promedio por viaje, por empresa. 
                                    Esto podría ayudar a las empresas de taxis identificar áreas de mejora y optimización de sus servicios.'''),
            html.Br(),
            dcc.Graph(id = 'g1', figure = fig1),
            dcc.Graph(id = 'g2', figure = fig2),
            html.Br(),
            html.H3('Subgráficos'),
            dcc.Graph(id = 'g1.1', figure = fig11),
            dcc.Graph(id = 'g1.2', figure = fig12),
            dcc.Graph(id = 'g1.3', figure = fig13),

            html.H3('Bloque de análisis'),

            html.P('''Por mi parte en este primer escenario de análisis puede visualizar que la compañía “Flash Cab” es la que recibe más propinas con diferencia seguido por la compañía “Taxi Affiliation Services”
                    además de que estas compañías no realizan los viajes más largos en cuanto a tiempo ni recorrido.
                    Esto quiere decir que probablemente estas sean las compañías de taxis que ofrecen un mejor servicio ya sea por atención al cliente o por la calidad y comodidad del taxi en sí.
                    Si se contara con datos de satisfacción de los clientes esta información se podría corroborar pero lamentablemente no es así.'''),

            html.P(''' A: En el primer escenario las empresas de taxis que logran un equilibrio entre tiempos de viaje cortos y distancias adecuadas demuestran una gestión eficiente de su flota y rutas,
                    optimizando así los recursos y mejorando la satisfacción del cliente. La eficiencia operativa se refleja en una reducción de costos y una mayor rapidez en el servicio,
                    lo que resulta en una mejor experiencia para los pasajeros. Adicionalmente, las empresas que reciben propinas más altas probablemente ofrecen un servicio de mayor calidad,
                    lo que se traduce en clientes más satisfechos y una mayor rentabilidad. Mantener altos estándares de servicio y atención al cliente es crucial para seguir siendo competitivos en el mercado.'''),
            
            html.P(''' J: En este  escenario, se observa que las empresas de taxis logran tiempos de viaje más cortos y gestionan bien las distancias ,y en la cual da una mayor eficiencia operativa.
                    Cabe añadir que refleja una gestión eficaz de su flota y rutas, lo que no solo reduce costos operativos, sino que también mejora la satisfacción del cliente al garantizar un servicio más rápido y confiable.
                    Además, los ingresos por viaje y las propinas recibidas son indicadores cruciales de la rentabilidad y la calidad del servicio ofrecido.
                    Estas empresas que reciben propinas más altas tienden a proporcionar un servicio superior,
                    lo que se traduce en clientes más satisfechos y así se da una gestión eficiente y un servicio de calidad que no solo mejoran la experiencia del cliente, sino que también incrementan la rentabilidad y sostenibilidad de las empresas de taxis.'''),

            html.P(''' S:  En este escenario podemos identificar que no son necesariamente las empresas que mayor número de viajes realizan las que mayores ingresos poseen.
                    Podemos apreciar que las empresas que realmente mantiene los ingresos totales mayores poseen un valor alto en el número de viajes realizados,
                    pero manteniendo un promedio de tarifa que roza los valores medios de la tabla,
                    las empresas con la mayor cantidad de viajes no posee los mayores ingresos debido a que las tarifas de estos viajes suelen ser mucho más bajas al tener menor duración y distancia.
                    En conjunto, la mejor estrategia que una empresa puede poner en su marcha es enviar la mayoría de sus vehículos a completar principalmente viajes de una duración considerable en la mayor cantidad posible,
                    y enviar conjuntos específicos de vehículos a completar los viajes fuera del rendimiento óptimo, aquellos viajes muy cortos o muy largos que se demandan en menores cantidades.'''),

            html.Br(),
            html.H2('ESCENARIO 2: Análisis de Patrones de Viaje por Área Urbana'),

            html.Div(children = '''Este análisis involucra la identificación de patrones de viajes realizados en cada área, las horas picos de viaje, las distancias de medias de viaje, etc.
                      Esto podría ayudar a las autoridades locales a las empresas de transporte a comprender mejor la demanda de transporte en diferentes áreas y planificar en consecuencia.'''),
            
            dcc.Graph(id = 'g3', figure = fig3),

            html.P(''' V:  En este análisis podemos observar que hay varias áreas urbanas donde se solicita mucho más el servicio de taxi que en otras y también podemos observar que generalmente entre las 11am y las 5 pm es cuando el servicio es más utilizado,
                    a excepción de la community area 75 donde el servicio de taxi se encuentra en su pico de uso entre las 4pm y las 8pm'''),

            html.P('''A: En el segundo análisis la identificación de áreas urbanas con alta demanda de taxis, como centros comerciales y zonas turísticas, permite a las empresas optimizar la distribución de sus vehículos, reduciendo así los tiempos de espera para los pasajeros.
                    Al ajustar la disponibilidad de taxis según los momentos de mayor actividad, las empresas pueden satisfacer mejor la demanda durante las horas pico, lo que se traduce en una mayor eficiencia operativa y una mejora en la satisfacción del cliente.
                    Este enfoque estratégico no solo optimiza el uso de la flota, sino que también incrementa la rentabilidad al asegurar un servicio más efectivo y puntual.'''),

            html.P(''' J: En este análisis, se deduce que hay una afinidad de áreas con alta demanda de taxis dado que en este escenario se puede ver un horario entre las 11:00 AM y las 5:00PM este fenómeno, como lugares de shopping  y distritos financieros,
                    y en la cual permite a las empresas optimizar la distribución de su flota y reducir los tiempos de espera, y donde va mejorando la eficiencia operativa y la satisfacción del cliente. Conocer los momentos de mayor actividad, o las horas pico,
                    permite ajustar la disponibilidad de taxis para satisfacer la demanda en estos periodos críticos, asegurando un servicio más eficiente y reduciendo la 
                    frustración de los clientes por la espera prolongada. Este enfoque estratégico no solo mejora la experiencia del usuario, sino que también maximiza el uso de recursos y aumenta la rentabilidad para las empresas de taxis.'''),


            html.P(''' S: Para este escenario se puede ver claramente como en las áreas 8, 32 y 76 se presenta una alta densidad en la demanda del servicio de taxi principalmente a cualquier hora frente a las otras áreas analizadas, esto puede ser debido a que estas áreas puedan contener espacios turísticos regularmente concurridos,
                    zonas laborales o viviendas masivas en conjunto. En adición, podemos notar que la densidad de la demanda aumenta en torno a las 7 am y las 5 pm, horario que se conoce comúnmente por ser el horario de oficina, y justamente este aumento comienza y termina en horas pico.
                    Fijándonos a detalle, observamos que en el área número 76 el aumento en la densidad de la demanda se continúa viendo en mayor cantidad hasta las 11 pm, por lo que podemos deducir que en dicha área se pueden encontrar lugares y eventos sociales nocturnos como bares o discotecas.'''),

            html.Br(),
            html.H2('ESCENARIO 3: Análisis de Preferencia de Pago'),
         
            html.Div(children = '''Este análisis se centra en comprender las preferencias de pago de los pasajeros. Investiga la frecuencia de uso de diferentes métodos de pago
                      (por ejemplo, efectivo, tarjeta de crédito, aplicación móvil) y cómo varían según el momento del día o la ubicación geográfica. Esto podría ser útil para
                      las empresas de taxis y proveedores de servicios de pago para adaptar sus servicios y opciones de pago según las necesidades y preferencias de los usuarios.'''),
         
            dcc.Graph(id = 'g4', figure = fig4),

            html.P(''' V: A la hora de analizar las preferencias de pago por parte de los clientes del servicio se puede evidenciar que la mayoría de los clientes pagan con efectivo o con tarjeta de crédito no habiendo mucha diferencia entre estos dos métodos de pago,
                    también otros métodos de pago que podemos observar es el uso de aplicaciones móviles para pagar u otro tipo de tarjetas, una desventaja que tenemos en este análisis es que para muchos viajes realizados no se encuentra información de pago en la base de datos por lo que no podemos ofrecer un análisis total y perfecto de este escenario.'''),
           
            html.P(''' A: En el tercer análisis necesitamos comprender las preferencias de pago de los pasajeros es esencial para adaptar los servicios de pago a sus necesidades. El análisis revela una creciente tendencia hacia los pagos digitales, que son preferidos por su rapidez y seguridad. Implementar tecnologías de pago
                    sin contacto y ofrecer incentivos para su uso puede mejorar la experiencia del cliente y la eficiencia operativa. Además, observar las variaciones en las preferencias de pago según el momento del día y la ubicación geográfica permite a las empresas de taxis personalizar sus servicios de pago,
                    lo que incrementa la satisfacción del cliente y fortalece la competitividad en el mercado.'''),
            
            html.P(''' J: En este escenario, es necesario analizar  las inclinaciones al momento del pago de los pasajeros ya que es crucial adaptar estos servicios y opciones para satisfacer  sus necesidades, revelando tendencias importantes como una creciente preferencia por pagos digitales que son más rápidos y seguros y en donde
                    se Identifican variaciones en los métodos de pago utilizados durante las horas pico versus las horas más tranquilas del día la cual permite a las empresas de taxis implementar tecnologías de pago adecuados, como pagos sin contacto, para mejorar la experiencia del usuario. Al ver estas diferencias entre áreas geográficas,
                    las empresas podrían adaptar sus servicios de pago en varios tipos de zonas urbanas optimizando así la eficiencia operativa y satisfaciendo mejor las expectativas de los clientes.'''),

            html.P(''' S: Este escenario nos permite comprender la utilización de cada método de pago a detalle, se puede ver que los clientes prefieren en gran medida el uso del efectivo y las tarjetas de crédito en mayor medida, sin embargo mantener todos los medios de pago posibles que
                    sienten con una conectividad efectiva entre sí siempre será la opción más viable para cualquier empresa de alto nivel territorial. Otro análisis que puede ser preocupante es la gran cantidad de viajes cancelados a último momento o que no presentan registro de método de pago,
                    estos registros incompletos pueden provocar confusiones en las cuentas de las empresas y los análisis de gestión que puedan ser realizados a futuro, principalmente hablando de el aumento del margen de error en las cuentas monetarias, por lo que considero que cada empresa debería adoctrinar el obligatorio registro de los datos de pago de cada viaje.'''),

            html.Br(),
            html.H2('ESCENARIO 4: Análisis de Tendencias Estacionales en el Uso del Taxi'),

            html.Div(children = '''Al examinar la cantidad de viajes realizados durante diferentes estaciones del año, es posible identificar tendencias estacionales en el uso del taxi.
                      Por ejemplo, descubrir si hay un aumento en la demanda durante las vacaciones o durante ciertos eventos estacionales, lo que podría ayudar a las empresas de taxis
                      a ajustar sus operaciones y recursos en consecuencia.'''),

            dcc.Graph(id = 'g5', figure = fig5),

            html.P(''' V: Dado nuestra cantidad limitada de datos para poder realizar este escenario no podemos brindar un análisis tan detallado de cómo cambia el uso del servicio del taxi dependiendo de las estaciones, sin embargo con los datos que contamos podemos evidenciar un gran uso de taxis a lo largo de enero y febrero,
                    también observando como este tenía un gran crecimiento a lo largo de marzo dando a entender así que la gente usa mucho el servicio a lo largo de finales de invierno y comienzos de primavera.'''),

            html.P(''' A:  Identificar las tendencias estacionales en el uso del taxi permite a las empresas prepararse mejor para los picos de demanda durante ciertas épocas del año, como las vacaciones de verano o las festividades. Ajustar la disponibilidad de vehículos y mejorar la coordinación logística durante estos periodos asegura que las empresas puedan satisfacer la demanda de manera efectiva.
                    Además, aprovechar eventos estacionales específicos mediante campañas de marketing dirigidas puede atraer más clientes y aumentar los ingresos. Esta capacidad de adaptación es crucial para mantener la eficiencia operativa y la satisfacción del cliente durante todo el año.'''),

            html.P(''' J: En este escenario, al revisar los datos dados, se pueden identificar tendencias estacionales en el uso del taxi, evidenciando aumentos en la demanda durante el invierno o las festividades. Esta información permite que las empresas  ajusten sus operaciones y recursos para satisfacer mejor las necesidades de los clientes en estas épocas.
                    Por ejemplo, los datos de la tabla "trip", que registra detalles de cada viaje, y la tabla "bill", que contiene la información de facturación, pueden mostrar incrementos en la cantidad de viajes y en los ingresos durante estos períodos. Ya ahí se anticipan picos de demanda para así preparar las flotas para eventos específicos como festivales o eventos deportivos importantes,
                    basándose en estas tendencias,la cual mejora la disponibilidad y eficiencia del servicio, aumentando así una buena opinión del cliente y la rentabilidad operativa a lo largo del año.'''),
            
            html.P(''' S: A pesar de que nuestros registros sólo cuentan con datos entre enero y marzo, podemos destacar la gran cantidad de registros consolidados entre enero y febrero. Con una búsqueda rápida podemos concluir que esta cantidad de registros consolidados supera el promedio mensual registrado anualmente,
                    por lo que es posible afirmar que el hecho de que estos valores se encuentren por encima del promedio mensual significa que hay un aumento en la demanda de servicios de taxi en la temporada de invierno.''')

    ]), html.Div(children=[
            html.Br(),
            html.H2(children='CONCLUSIONES'),

            html.P('''Al analizar varios aspectos del servicio de taxis, como el rendimiento de las empresas, los patrones de viaje en diferentes áreas urbanas, las preferencias de pago de los pasajeros y la eficiencia de las tarifas, queda claro que una buena gestión y adaptación son esenciales para tener éxito en esta industria.
                    Las empresas que son rápidas y eficientes en sus viajes logran manejar mejor sus flotas y rutas, reduciendo costos y aumentando la satisfacción del cliente.
                    En resumen, una estructura que equilibre la eficiencia operativa, la adaptabilidad a la demanda, la diversidad en los métodos de pago y la flexibilidad en las tarifas no solo mejora la rentabilidad y la eficiencia, sino que también permite responder de manera más efectiva a las necesidades cambiantes de los pasajeros.
                    Esto es fundamental para mantenerse competitivos en un mercado dinámico y en constante evolución, garantizando una experiencia positiva y consistente para los usuarios.'''),
            html.P(''' A: En un mercado de transporte cada vez más competitivo, las empresas de taxis deben centrarse en la optimización de su eficiencia operativa y en la mejora continua de la satisfacción del cliente. Este proyecto ha subrayado la importancia de una gestión integral que considere todos los aspectos clave del funcionamiento del servicio de taxis.
                    Implementar los insights obtenidos permitirá a las empresas no solo satisfacer mejor las necesidades de sus clientes, sino también mejorar su rentabilidad y sostenibilidad a largo plazo. Al adoptar una estrategia basada en datos y centrada en el cliente, las empresas de taxis pueden asegurar un futuro exitoso y competitivo.'''),

            html.P(''' J: Se puede concluir que dentro de los análisis detallados se revela los insights,clave para mejorar la eficiencia operativa y la satisfacción del cliente en el servicio de taxis,
                    la cual al examinar los tiempos de viaje y propinas, se puede identificar patrones que indican la eficiencia y rentabilidad de las empresa en la gestión de sus viajes. Además al analizar las zonas de alta demanda y las horas pico ya registradas,
                    permite adaptar la infraestructura de pago para satisfacer las necesidades de los clientes modernos, especialmente en términos de la adopción de métodos digitales. De ese modo las tendencias estacionales en el uso del servicio, identificadas a través de análisis de datos temporales como en las tablas "trip" y "bill",
                    las empresas pueden ajustar estratégicamente sus operaciones para satisfacer la demanda durante períodos específicos del año, maximizando así la eficiencia y la rentabilidad. En resumen, estos escenarios me hicieron ver lo que proporciona una visión integral que permite a las empresas de taxis no solo mejorar la gestión operativa,
                    sino también optimizar la distribución de recursos y adaptarse a las preferencias cambiantes de los usuarios, lo que conduce a una mejor experiencia del cliente y resultados financieros más sólidos.'''),

            html.P(''' S: El análisis de los registros aportados por el dataset fue gratificante y acertado para ayudar a las empresas a comprender de forma más óptima los recursos que pueden necesitar para 
                   plantear una mejor gestión de sus unidades vehiculares y para aumentar su productividad y sus estrategias con el fin de obtener una clientela mucho más satisfecha y variada, visualizando el comportamiento
                    del panorama general en el nicho de los servicios de taxi en la ciudad de Chicago.
''')
         ])

    

    if __name__ == '__main__':
        app.run_server(debug = False)

except Exception as ex:
    print(ex)
finally:
    connection.close()
    print("Disconnected")

