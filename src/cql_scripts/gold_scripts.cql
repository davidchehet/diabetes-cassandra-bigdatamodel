-- [CREATE_GOLD_DIAB_BY_RACE_AND_HEALTH_CONDITION]
CREATE TABLE IF NOT EXISTS diabetes.gold_diabetes_by_race_condition (
    race text,
    condition_group text,
    diabetes_prevalence float,
    PRIMARY KEY (race, condition_group)
);

-- [SELECT_RACE_HEALTH]
SELECT race_african_american, race_asian, race_caucasian, race_hispanic, race_other, diabetes, hypertension, heart_disease
FROM diabetes.silver_level;

-- [INSERT_INTO_RACE_HEALTH_TABLE]
INSERT INTO diabetes.gold_diabetes_by_race_condition (race, condition_group, diabetes_prevalence) 
VALUES (?, ?, ?);

-- [SELECT_FROM_NEW_GOLD_TABLE_RACE_HEALTHCONDITION]
SELECT race, condition_group, diabetes_prevalence 
FROM diabetes.gold_diabetes_by_race_condition;

-- [CREATE_LOC_TABLE]
CREATE TABLE IF NOT EXISTS diabetes.gold_diabetes_by_location (
    location text,
    diabetes_prevalence float,
    PRIMARY KEY (location)
);

-- [SELECT_LOC_INFO_SILVER]
SELECT location, diabetes
FROM diabetes.silver_level;

-- [INSERT_INTO_LOC]
INSERT INTO diabetes.gold_diabetes_by_location (location, diabetes_prevalence)
VALUES (?, ?);

-- [SELECT_FROM_NEW_GOLD_BY_LOC]
SELECT location AS NAME, diabetes_prevalence
FROM diabetes.gold_diabetes_by_location;