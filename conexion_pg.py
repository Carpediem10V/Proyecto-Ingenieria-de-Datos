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
    fig13 = px.bar(rows, x = 0, y = 1, color_discrete_sequence=["#FFC300 "])
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
    fig3.update_yaxes(tick0=0, dtick= 5)
    fig3.update_xaxes(tick0=0, dtick= 1)
    fig3.update_layout(
        title = "Peak times per Community Area",
        xaxis_title="Hour",
        yaxis_title="Community Area Number",
        legend_title= "Peak Type",
        hovermode = 'y unified')
    
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
    fig5 = px.pie(rows, values= 1, names=0 ,width=2500, height=1000)
    
    ###########################################################################################################
   
    app.layout = html.Div(children=[
            html.H1(children = "Chicago Taxi Trips Analytics"),

            html.H2('ESCENARIO 1'),
            html.Div(children = '''Este análisis se centra en examinar el rendimiento de las diferentes empresas de taxis en términos de tiempo y distancia de viaje,
                                    así como la cantidad de ingresos generados. 
                                    Calculando métricas como la cantidad promedio de millas por viaje, el tiempo promedio de viaje y los ingresos promedio por viaje, por empresa. 
                                    Esto podría ayudar a las empresas de taxis identificar áreas de mejora y optimización de sus servicios.'''),
            dcc.Graph(id = 'g1', figure = fig1),
             dcc.Graph(id = 'g2', figure = fig2),
            html.Br(),
            html.H3('Subgráficos'),
            dcc.Graph(id = 'g1.1', figure = fig11),
            dcc.Graph(id = 'g1.2', figure = fig12),
            dcc.Graph(id = 'g1.3', figure = fig13),
            html.H3('Bloque de análisis'),
            html.P('analisis1'),
            html.P('analisis2'),
            html.P('analisis3'),
            html.P('analisis4'),

            html.Br(),
            html.H2('ESCENARIO 2'),
            html.Div(children = '''Este análisis involucra la identificación de patrones de viajes realizados en cada área, las horas picos de viaje, las distancias de medias de viaje, etc.
                      Esto podría ayudar a las autoridades locales a las empresas de transporte a comprender mejor la demanda de transporte en diferentes áreas y planificar en consecuencia.'''),
            dcc.Graph(id = 'g3', figure = fig3),
            html.P('analisis1'),
            html.P('analisis2'),
            html.P('analisis3'),
            html.P('analisis4'),

            html.Br(),
            html.H2('ESCENARIO 3'),
            html.Div(children = '''Este análisis se centra en comprender las preferencias de pago de los pasajeros. Investiga la frecuencia de uso de diferentes métodos de pago
                      (por ejemplo, efectivo, tarjeta de crédito, aplicación móvil) y cómo varían según el momento del día o la ubicación geográfica. Esto podría ser útil para
                      las empresas de taxis y proveedores de servicios de pago para adaptar sus servicios y opciones de pago según las necesidades y preferencias de los usuarios.'''),
            dcc.Graph(id = 'g4', figure = fig4),
            html.P('analisis1'),
            html.P('analisis2'),
            html.P('analisis3'),
            html.P('analisis4'),

            html.Br(),
            html.H2('ESCENARIO 4'),
            html.Div(children = '''Al examinar la cantidad de viajes realizados durante diferentes estaciones del año, es posible identificar tendencias estacionales en el uso del taxi.
                      Por ejemplo, descubrir si hay un aumento en la demanda durante las vacaciones o durante ciertos eventos estacionales, lo que podría ayudar a las empresas de taxis
                      a ajustar sus operaciones y recursos en consecuencia.'''),
            dcc.Graph(id = 'g5', figure = fig5),
            html.P('analisis1'),
            html.P('analisis2'),
            html.P('analisis3'),
            html.P('analisis4')

    ]), html.Div(children=[
            html.Br(),
            html.H2(children='CONCLUSIONES'),
            html.P('conclusiones1'),
            html.P('conclusiones2'),
            html.P('conclusiones3'),
            html.P('conclusiones4')
         ])

    

    if __name__ == '__main__':
        app.run_server(debug = False)

except Exception as ex:
    print(ex)
finally:
    connection.close()
    print("Disconnected")

