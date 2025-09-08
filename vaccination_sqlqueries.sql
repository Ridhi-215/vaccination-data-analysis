
USE vaccination_db;

SHOW TABLES;

DESCRIBE coverage;
DESCRIBE incidence;
DESCRIBE reported_cases;
DESCRIBE vaccine_introduction;
DESCRIBE vaccine_schedule;


ALTER TABLE coverage 
ADD PRIMARY KEY (code, year, antigen);

ALTER TABLE incidence 
ADD PRIMARY KEY (code, year, disease);

ALTER TABLE reported_cases 
ADD PRIMARY KEY (code, year, disease);

ALTER TABLE vaccine_introduction 
ADD PRIMARY KEY (iso_3_code, year, description);

ALTER TABLE vaccine_schedule 
ADD PRIMARY KEY (iso_3_code, year, vaccinecode, schedulerounds);


-- incidence → coverage
ALTER TABLE incidence
ADD CONSTRAINT fk_incidence_code
FOREIGN KEY (code, year)
REFERENCES coverage(code, year);

-- reported_cases → coverage
ALTER TABLE reported_cases
ADD CONSTRAINT fk_reported_code
FOREIGN KEY (code, year)
REFERENCES coverage(code, year);

-- vaccine_introduction → coverage
ALTER TABLE vaccine_introduction
ADD CONSTRAINT fk_intro_code
FOREIGN KEY (iso_3_code, year)
REFERENCES coverage(code, year);

-- vaccine_schedule → coverage
ALTER TABLE vaccine_schedule
ADD CONSTRAINT fk_schedule_code
FOREIGN KEY (iso_3_code, year)
REFERENCES coverage(code, year);

-- coverage → vaccine_schedule
ALTER TABLE coverage
ADD CONSTRAINT fk_coverage_schedule
FOREIGN KEY (code, year, antigen)
REFERENCES vaccine_schedule (iso_3_code, year, vaccinecode);

SELECT '✅ Database schema and relationships successfully applied!' AS status;
