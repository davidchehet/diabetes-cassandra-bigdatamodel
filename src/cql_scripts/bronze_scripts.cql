-- [CREATE_BRONZE_LEVEL_TABLE]
CREATE TABLE IF NOT EXISTS diabetes.bronze_level (
    patient_id UUID,
    year INT,
    gender TEXT,
    age FLOAT,
    location TEXT,
    race_african_american INT,
    race_asian INT,
    race_caucasian INT,
    race_hispanic INT,
    race_other INT,
    hypertension INT,
    heart_disease INT,
    smoking_history TEXT,
    bmi FLOAT,
    hba1c_level FLOAT,
    blood_glucose_level FLOAT,
    diabetes INT,
    clinical_notes TEXT,
    PRIMARY KEY (patient_id)
);

-- [INSERT_RAW_DATA]
INSERT INTO diabetes.bronze_level
    (patient_id, year, gender, age, location, race_african_american, race_asian, race_caucasian, race_hispanic, race_other, hypertension, heart_disease, smoking_history, bmi, hba1c_level, blood_glucose_level, diabetes, clinical_notes)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);

-- [SELECT_FOR_SILVER]
SELECT patient_id, year, gender, age, location, race_african_american, race_asian, race_caucasian, race_hispanic, race_other, hypertension, heart_disease, smoking_history, bmi, hba1c_level, blood_glucose_level, diabetes
FROM diabetes.bronze_level;
