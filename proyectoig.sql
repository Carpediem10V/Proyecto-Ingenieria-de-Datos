CREATE TABLE taxi(
	id_taxi varchar(150),
	company varchar(40),
	PRIMARY KEY(id_taxi, company)
);

CREATE TABLE pickup_info(
	id_pickup integer,
	census_track bigint,
	community_area smallint,
	centroid_lat numeric,
	centroid_lon numeric,
	PRIMARY KEY(id_pickup),
	CONSTRAINT pcommunity_area_range CHECK(community_area BETWEEN 0 AND 77)
);

CREATE TABLE dropoff_info(
	id_dropoff integer,
	census_track bigint,
	community_area smallint,
	centroid_lat numeric,
	centroid_lon numeric,
	PRIMARY KEY(id_dropoff),
	CONSTRAINT dcommunity_area_range CHECK(community_area BETWEEN 0 AND 77)
);

CREATE TABLE trip(
	id_trip bigint,
	start_date date,
	start_time time,
	end_date date,
	end_time time,
	trip_seconds integer,
	trip_miles numeric(10,2),
	pickup_infoid integer,
	dropoff_infoid integer,
	PRIMARY KEY (id_trip),
	CONSTRAINT fk_trip_pickup
		FOREIGN KEY(pickup_infoid) REFERENCES pickup_info (id_pickup),
	CONSTRAINT fk_trip_dropoff
		FOREIGN KEY(dropoff_infoid) REFERENCES dropoff_info (id_dropoff)
);
	
CREATE TABLE bill(
	trip_number bigint,
	taxi_ref varchar(150),
	company_name varchar(40),
	fare numeric(10,2),
	tips numeric(10,2),
	tolls numeric(10,2),
	extras numeric(10,2),
	total numeric(10,2),
	payment_type varchar(40),
	PRIMARY KEY(trip_number),
	CONSTRAINT fk_trip_bill
		FOREIGN KEY(trip_number) REFERENCES trip (id_trip),
	CONSTRAINT fk_assigned_taxi
		FOREIGN KEY(taxi_ref, company_name) REFERENCES taxi (id_taxi, company)
);
	

COPY taxi FROM 'C:\Users\Public\Documents\taxi.csv' DELIMITER ',' CSV HEADER;
COPY pickup_info FROM 'C:\Users\Public\Documents\pickup.csv' DELIMITER ',' CSV HEADER;
COPY dropoff_info FROM 'C:\Users\Public\Documents\dropoff.csv' DELIMITER ',' CSV HEADER;
COPY trip FROM 'C:\Users\Public\Documents\trip.csv' DELIMITER ',' CSV HEADER;
COPY bill FROM 'C:\Users\Public\Documents\bill.csv' DELIMITER ',' CSV HEADER;

