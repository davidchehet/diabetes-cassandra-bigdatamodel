-- [CREATE_SILVER_LEVEL_TABLE]
CREATE TABLE IF NOT EXISTS diabetes.silver_level (
    patient_id UUID,
    year INT,
    gender INT,
    age INT,
    location TEXT,
    race_african_american INT,
    race_asian INT,
    race_caucasian INT,
    race_hispanic INT,
    race_other INT,
    hypertension INT,
    heart_disease INT,
    smoking_history INT,
    bmi FLOAT,
    hba1c_level FLOAT,
    blood_glucose_level FLOAT,
    diabetes INT,
    PRIMARY KEY (patient_id)
);

-- [INSERT_CLEANSED_DATA]
INSERT INTO diabetes.silver_level
    (patient_id, year, gender, age, location, race_african_american, race_asian, race_caucasian, race_hispanic, race_other, hypertension, heart_disease, smoking_history, bmi, hba1c_level, blood_glucose_level, diabetes)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);

-- [SELECT_VIS_THREE]
SELECT age, bmi, hba1c_level, blood_glucose_level, diabetes
FROM diabetes.silver_level;

-- [RANDOM_FOREST]
SELECT age, bmi, hba1c_level, blood_glucose_level, hypertension, heart_disease, gender, smoking_history, race_african_american, race_asian,
race_caucasian, race_hispanic, race_other, diabetes
FROM diabetes.silver_level;