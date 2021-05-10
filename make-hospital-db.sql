-- Modified 5/5/21
-- Updated datatypes.
CREATE SCHEMA IF NOT EXISTS hospital;

-- drop tables
DROP TABLE IF EXISTS installment;
DROP TABLE IF EXISTS inst_term;
DROP TABLE IF EXISTS amount_due;
DROP TABLE IF EXISTS bill;
DROP TABLE IF EXISTS takes;
DROP TABLE IF EXISTS medicine;
DROP TABLE IF EXISTS out_patient;
DROP TABLE IF EXISTS in_patient;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS insurance_cmp;
DROP TABLE IF EXISTS doctor;
DROP TABLE IF EXISTS employee;

-- create tables

CREATE TABLE employee (
    employee_id     INTEGER         NOT NULL AUTO_INCREMENT,
    employee_type   VARCHAR(50)     NOT NULL,
    name            TINYTEXT        NOT NULL,
    date_of_birth   DATE            NOT NULL,
    address         TINYTEXT        NOT NULL,
    email           TINYTEXT        NOT NULL,
    employment_date DATE            NOT NULL,
    salary          NUMERIC(9, 2)   NOT NULL,
    
    PRIMARY KEY (employee_id)
);

CREATE TABLE doctor (
    doctor_id       INTEGER         NOT NULL,
    specialty       VARCHAR(50)     NOT NULL,
    doctor_fee      NUMERIC(9, 2)   NOT NULL,
    
    PRIMARY KEY    (doctor_id),
    FOREIGN KEY (doctor_id) REFERENCES employee(employee_id)
);

CREATE TABLE insurance_cmp (
    insurance_id    INTEGER         NOT NULL AUTO_INCREMENT,
    cmp_name        VARCHAR(50)     NOT NULL,
    balance         NUMERIC(9, 2)   NOT NULL,
    
    PRIMARY KEY (insurance_id)
);

CREATE TABLE patient (
    patient_id      INTEGER         NOT NULL AUTO_INCREMENT,
    insurance_id    INTEGER         NOT NULL,
    patient_type    VARCHAR(3)      NOT NULL,    
    admit_date      DATETIME        NOT NULL,
    discharge_date  DATETIME        NOT NULL,
    name            TINYTEXT        NOT NULL,
    date_of_birth   DATE            NOT NULL,
    address         TINYTEXT        NOT NULL,
    email           TINYTEXT        NOT NULL,
    
    PRIMARY KEY (patient_id),
    FOREIGN KEY (insurance_id) REFERENCES insurance_cmp(insurance_id),
    
    CHECK (patient_type = 'IN' OR patient_type = 'OUT')
);

CREATE TABLE room (
    room_no         INTEGER         NOT NULL AUTO_INCREMENT,
    room_type       VARCHAR(10)     NOT NULL,
    daily_cost      NUMERIC(9, 2)   NOT NULL,
    
    PRIMARY KEY (room_no)
);

CREATE TABLE in_patient (
    patient_id      INTEGER         NOT NULL,
    doctor_id       INTEGER         NOT NULL,
    room_no         INTEGER         NOT NULL,
    
    PRIMARY KEY (patient_id),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY (room_no) REFERENCES room(room_no)
);

CREATE TABLE out_patient (
    patient_id      INTEGER         NOT NULL,
    doctor_id       INTEGER         NOT NULL,
    lab_no          INTEGER         NOT NULL,
    
    PRIMARY KEY (patient_id),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY (lab_no) REFERENCES room(room_no)
);

CREATE TABLE medicine (
    medicine_id     INTEGER         NOT NULL AUTO_INCREMENT,
    cost            NUMERIC(9, 2)   NOT NULL,
    
    PRIMARY KEY (medicine_id)
);

CREATE TABLE takes (
    patient_id      INTEGER         NOT NULL,
    medicine_id     INTEGER         NOT NULL,
    
    PRIMARY KEY (patient_id, medicine_id),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (medicine_id) REFERENCES medicine(medicine_id)
);

CREATE TABLE bill (
    bill_id         INTEGER         NOT NULL AUTO_INCREMENT,
    patient_id      INTEGER         NOT NULL,
    doctor_fee      NUMERIC(9, 2)   NOT NULL,
    room_cost       NUMERIC(9, 2)   NOT NULL,
    medicine_cost   NUMERIC(9, 2)   NOT NULL,
    
    PRIMARY KEY    (bill_id),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id)
);

CREATE TABLE amount_due (
    bill_id         INTEGER         NOT NULL,
    amount          NUMERIC(9, 2)   NOT NULL,
    due_date        DATE            NOT NULL,
    
    PRIMARY KEY (bill_id),
    FOREIGN KEY (bill_id) REFERENCES bill(bill_id)
);

CREATE TABLE inst_term (
    term            INTEGER         NOT NULL AUTO_INCREMENT,
    val             NUMERIC(9, 2)   NOT NULL,
    
    PRIMARY KEY (term)
);

CREATE TABLE installment (
    patient_id      INTEGER         NOT NULL,
    term            INTEGER         NOT NULL,
    init_date       DATE            NOT NULL,
    
    PRIMARY KEY (patient_id, term),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (term) REFERENCES inst_term(term)
);


DELIMITER !
CREATE TRIGGER trg_mv_branch_insert
BEFORE INSERT ON out_patient FOR EACH ROW
BEGIN
    IF (    SELECT    room_type
            FROM    room
            WHERE    room_no = NEW.lab_no
        ) NOT LIKE 'LAB' THEN
        
        SIGNAL SQLSTATE '45000';
    END IF;        
END!
DELIMITER ;

DELIMITER !
DROP FUNCTION IF EXISTS getBill;
CREATE FUNCTION getBill (p_id INTEGER) RETURNS DOUBLE
BEGIN
	DECLARE tot_bill DOUBLE DEFAULT 0.00;
    SET @a = (SELECT doctor_fee FROM bill WHERE patient_id = p_id);
    SET @a = @a + (SELECT room_cost FROM bill WHERE patient_id = p_id);
    SET @a = @a + (SELECT medicine_cost FROM bill WHERE patient_id = p_id);
    SET tot_bill = @a;
    RETURN tot_bill;
END!
DELIMITER ;


