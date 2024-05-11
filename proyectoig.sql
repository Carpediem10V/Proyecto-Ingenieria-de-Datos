CREATE TABLE taxi(
	id_taxi varchar(150),
	company varchar(40),
	PRIMARY KEY(id_taxi, company)
);

CREATE TABLE pickup_info(
	id_pickup integer,
	census_track bigint,
	community_area smallint,
	centroid_lat numeric(3,8),
	centroid_lon numeric(3,8),
	PRIMARY KEY(id_pickup),
	CONSTRAINT pcommunity_area_range CHECK(community_area BETWEEN 0 AND 77)
);

CREATE TABLE dropoff_info(
	id_dropoff integer,
	census_track bigint,
	community_area smallint,
	centroid_lat numeric(3,8),
	centroid_lon numeric(3,8),
	PRIMARY KEY(id_dropoff)
	CONSTRAINT dcommunity_area_range CHECK(community_area BETWEEN 0 AND 77)
);

CREATE TABLE trip(
	id_trip integer,
	start_date date,
	start_time time,
	end_date date,
	end_time time,
	trip_seconds integer,
	trip_miles numeric(10,2),
	pickup_infoid integer,
	dropoff_infoid integer,
	CONSTRAINT fk_trip_pickup
		FOREIGN KEY(pickup_infoid) REFERENCES pickup_info (id_pickup),
	CONSTRAINT fk_trip_dropoff
		FOREIGN KEY(dropoff_infoid) REFERENCES dropoff_info (id_dropoff)
);
	
CREATE TABLE bill(
	trip_number integer,
	taxi_ref varchar(150),
	fare numeric(10,2),
	tips numeric(10,2),
	tolls numeric(10,2),
	extras numeric(10,2),
	total numeric(10,2),
	payment_type varchar(40),
	PRIMARY KEY(trip_number),
	PRIMARY KEY(taxi_ref),
	CONSTRAINT (fk_trip_bill)
		FOREIGN KEY(trip_number) REFERENCES trip (id_trip),
	CONSTRAINT (fk_assigned_taxi)
		FOREIGN KEY(taxi_ref) REFERENCES taxi (id_taxi)
);
	

COPY taxi FROM 'ruta taxi.csv' DELIMITER ',' CSV HEADER:
COPY pickup_info FROM 'ruta pickup.csv' DELIMITER ',' CSV HEADER:
COPY dropoff_info FROM 'ruta dropoff.csv' DELIMITER ',' CSV HEADER:
COPY trip FROM 'ruta trip.csv' DELIMITER ',' CSV HEADER:
COPY bill FROM 'ruta bill.csv' DELIMITER ',' CSV HEADER:

