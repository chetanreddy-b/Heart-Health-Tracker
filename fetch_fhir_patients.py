import requests
import json
import os
import pandas as pd
from datetime import datetime

FHIR_BASE_URL = "https://hapi.fhir.org/baseR4"

def fetch_patient(patient_id):
    """Fetch a patient's complete data from FHIR server."""
    patient_data = {}
    
    # 1. Get patient demographics
    patient_url = f"{FHIR_BASE_URL}/Patient/{patient_id}"
    resp = requests.get(patient_url)
    if resp.status_code != 200:
        print(f"Error fetching patient {patient_id}: {resp.status_code}")
        return None
    
    patient_json = resp.json()
    
    # Extract name
    name = patient_json.get("name", [{}])[0]
    given_name = name.get("given", ["Unknown"])[0]
    family_name = name.get("family", "Unknown")
    full_name = f"{given_name} {family_name}"
    
    # Extract gender and birth date
    gender = patient_json.get("gender", "unknown")
    birth_date = patient_json.get("birthDate", "Unknown")
    
    # Calculate age
    try:
        birth_year = int(birth_date.split("-")[0])
        current_year = datetime.now().year
        age = current_year - birth_year
    except:
        age = "Unknown"
    
    patient_data["demographics"] = {
        "id": patient_id,
        "name": full_name,
        "gender": gender,
        "birth_date": birth_date,
        "age": age
    }
    
    # 2. Get conditions
    conditions_url = f"{FHIR_BASE_URL}/Condition?patient={patient_id}&_count=100"
    resp = requests.get(conditions_url)
    conditions = []
    
    if resp.status_code == 200:
        bundle = resp.json()
        if "entry" in bundle:
            for entry in bundle["entry"]:
                resource = entry.get("resource", {})
                coding = resource.get("code", {}).get("coding", [{}])[0]
                display = coding.get("display", "Unknown Condition")
                conditions.append(display)
    
    patient_data["conditions"] = conditions
    
    # 3. Get medications
    meds_url = f"{FHIR_BASE_URL}/MedicationRequest?patient={patient_id}&_count=100"
    resp = requests.get(meds_url)
    medications = []
    
    if resp.status_code == 200:
        bundle = resp.json()
        if "entry" in bundle:
            for entry in bundle["entry"]:
                resource = entry.get("resource", {})
                med_concept = resource.get("medicationCodeableConcept", {})
                if "text" in med_concept:
                    medications.append(med_concept["text"])
                elif "coding" in med_concept and med_concept["coding"]:
                    medications.append(med_concept["coding"][0].get("display", "Unknown Medication"))
    
    patient_data["medications"] = medications
    
    # 4. Get vital signs
    vitals_url = f"{FHIR_BASE_URL}/Observation?patient={patient_id}&category=vital-signs&_count=100"
    resp = requests.get(vitals_url)
    vitals = {}
    
    if resp.status_code == 200:
        bundle = resp.json()
        if "entry" in bundle:
            for entry in bundle["entry"]:
                resource = entry.get("resource", {})
                
                # Get observation code
                code_coding = resource.get("code", {}).get("coding", [{}])[0]
                code = code_coding.get("code", "")
                display = code_coding.get("display", "Unknown Vital")
                
                # Get observation value
                value_quantity = resource.get("valueQuantity", {})
                value = value_quantity.get("value", "")
                unit = value_quantity.get("unit", "")
                
                if code and value:
                    vitals[display] = {
                        "value": value,
                        "unit": unit
                    }
    
    patient_data["vitals"] = vitals
    
    # Determine BP category based on vitals
    systolic = vitals.get("Systolic BP", {}).get("value", 120)
    diastolic = vitals.get("Diastolic BP", {}).get("value", 80)
    
    if isinstance(systolic, str):
        try:
            systolic = float(systolic)
        except:
            systolic = 120
    
    if isinstance(diastolic, str):
        try:
            diastolic = float(diastolic)
        except:
            diastolic = 80
    
    if systolic >= 140 or diastolic >= 90:
        bp_category = "Hypertension Stage 2" if (systolic >= 160 or diastolic >= 100) else "Hypertension Stage 1"
    elif systolic >= 130 or diastolic >= 80:
        bp_category = "Hypertension Stage 1"
    elif systolic >= 120:
        bp_category = "Elevated"
    else:
        bp_category = "Normal"
    
    patient_data["bp_category"] = bp_category
    patient_data["has_hypertension"] = "Hypertension" in conditions or "hypertension" in ' '.join(conditions).lower()
    
    return patient_data

def main():
    # Create directory for patient data
    os.makedirs("data/patient_data", exist_ok=True)
    
    # Read in patient IDs from a file or command line
    # For now, let's use a sample ID
    patient_ids = input("Enter patient IDs (comma-separated) to fetch: ").split(",")
    
    fetched_patients = []
    
    for patient_id in patient_ids:
        patient_id = patient_id.strip()
        print(f"Fetching data for patient {patient_id}...")
        
        patient_data = fetch_patient(patient_id)
        if patient_data:
            fetched_patients.append(patient_data)
            
            # Create directory for this patient
            patient_dir = f"data/patient_data/{patient_id}"
            os.makedirs(patient_dir, exist_ok=True)
            
            # Save patient data to JSON
            with open(f"{patient_dir}/patient_info.json", "w") as f:
                json.dump(patient_data, f, indent=2)
            
            print(f"✅ Successfully fetched data for {patient_data['demographics']['name']}")
            
            # Generate synthetic Omron and Google Fit data for this patient
            generate_synthetic_device_data(patient_data)
            
            print(f"✅ Generated synthetic device data for {patient_data['demographics']['name']}")
        else:
            print(f"❌ Failed to fetch data for patient {patient_id}")
    
    print(f"\nFetched data for {len(fetched_patients)} patients.")

def generate_synthetic_device_data(patient):
    """Generate synthetic Omron (BP) and Google Fit (exercise) data for a fetched patient."""
    import random
    from datetime import datetime, timedelta
    
    patient_id = patient["demographics"]["id"]
    patient_dir = f"data/patient_data/{patient_id}"
    
    # Create subdirectories for each data type
    os.makedirs(f"{patient_dir}/omron", exist_ok=True)
    os.makedirs(f"{patient_dir}/google_fit", exist_ok=True)
    
    # Adjust data generation based on patient characteristics
    has_hypertension = patient["has_hypertension"]
    bp_category = patient["bp_category"]
    age = patient["demographics"]["age"]
    if isinstance(age, str):
        try:
            age = int(age)
        except:
            age = 60  # Default age if unknown
    
    # Determine base BP values from patient vitals
    systolic_base = patient["vitals"].get("Systolic BP", {}).get("value", 120)
    diastolic_base = patient["vitals"].get("Diastolic BP", {}).get("value", 80)
    
    if isinstance(systolic_base, str):
        try:
            systolic_base = float(systolic_base)
        except:
            systolic_base = 120
    
    if isinstance(diastolic_base, str):
        try:
            diastolic_base = float(diastolic_base)
        except:
            diastolic_base = 80
    
    # Determine exercise habits based on age, conditions
    if age < 40:
        exercise_frequency = random.choices([2, 3, 4, 5], weights=[0.2, 0.3, 0.3, 0.2])[0]  # days per week
        exercise_intensity = random.choices(["Low", "Moderate", "High"], weights=[0.2, 0.5, 0.3])[0]
    elif age < 60:
        exercise_frequency = random.choices([1, 2, 3, 4], weights=[0.3, 0.4, 0.2, 0.1])[0]
        exercise_intensity = random.choices(["Low", "Moderate", "High"], weights=[0.3, 0.6, 0.1])[0]
    else:
        exercise_frequency = random.choices([0, 1, 2, 3], weights=[0.2, 0.4, 0.3, 0.1])[0]
        exercise_intensity = random.choices(["Low", "Moderate", "High"], weights=[0.6, 0.3, 0.1])[0]
    
    # Generate 90 days of data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    # Generate BP readings (Omron data)
    bp_readings = []
    for day in range(90):
        # More frequent readings if hypertension exists
        num_readings = random.choices([0, 1, 2], weights=[0.4, 0.5, 0.1])[0]
        if has_hypertension:
            num_readings = random.choices([0, 1, 2], weights=[0.2, 0.6, 0.2])[0]
        
        date = start_date + timedelta(days=day)
        
        for _ in range(num_readings):
            # Morning or evening reading
            time_of_day = random.choice(["Morning", "Evening"])
            if time_of_day == "Morning":
                hour = random.randint(6, 10)
            else:
                hour = random.randint(17, 22)
            
            minute = random.choice([0, 15, 30, 45])
            time_str = f"{hour:02d}:{minute:02d}"
            
            # Calculate BP with random variation
            systolic = max(90, min(180, int(systolic_base + random.normalvariate(0, 5))))
            diastolic = max(60, min(110, int(diastolic_base + random.normalvariate(0, 3))))
            pulse = max(50, min(100, int(random.normalvariate(75, 8))))
            
            bp_readings.append({
                "date": date.strftime("%Y-%m-%d"),
                "time": time_str,
                "systolic": systolic,
                "diastolic": diastolic,
                "pulse": pulse,
                "time_of_day": time_of_day
            })
    
    # Save BP data
    bp_df = pd.DataFrame(bp_readings)
    if not bp_df.empty:
        bp_df.to_csv(f"{patient_dir}/omron/omron_data.csv", index=False)
    
    # Generate exercise data (Google Fit)
    exercise_data = []
    exercise_types = ["Walking", "Running", "Cycling", "Swimming", "Weight Training", "Yoga", "HIIT"]
    
    # Determine preferred exercises based on age and conditions
    if age < 40:
        preferred_types = random.sample(exercise_types, k=min(4, len(exercise_types)))
    elif age < 60:
        preferred_types = random.sample(exercise_types, k=min(3, len(exercise_types)))
    else:
        preferred_types = random.sample(exercise_types[:4], k=min(2, 4))  # Less intense types for older
    
    # Adjust based on conditions
    if "Heart failure" in patient["conditions"] or "Myocardial Infarction" in patient["conditions"]:
        # Remove high-intensity exercises for heart conditions
        if "HIIT" in preferred_types:
            preferred_types.remove("HIIT")
        if "Running" in preferred_types and age > 60:
            preferred_types.remove("Running")
    
    if "Arthritis" in patient["conditions"]:
        # Favor low-impact exercises for arthritis
        if "Swimming" not in preferred_types and len(preferred_types) > 1:
            preferred_types.append("Swimming")
            preferred_types.pop(0)
    
    for day in range(90):
        date = start_date + timedelta(days=day)
        
        # Determine if exercise happens this day based on weekly frequency
        if day % 7 < exercise_frequency:
            # Exercise time more likely in morning or evening
            hour = random.choices([7, 8, 12, 17, 18, 19], weights=[0.2, 0.2, 0.1, 0.2, 0.2, 0.1])[0]
            minute = random.choice([0, 15, 30, 45])
            time_str = f"{hour:02d}:{minute:02d}"
            
            # Select exercise type weighted toward preferred activities
            exercise_type = random.choices(
                exercise_types, 
                weights=[3 if t in preferred_types else 1 for t in exercise_types]
            )[0]
            
            # Determine intensity - weighted based on patient's overall intensity level
            if exercise_intensity == "Low":
                intensity = random.choices(["Low", "Moderate", "High"], weights=[0.7, 0.25, 0.05])[0]
            elif exercise_intensity == "Moderate":
                intensity = random.choices(["Low", "Moderate", "High"], weights=[0.2, 0.6, 0.2])[0]
            else:  # High
                intensity = random.choices(["Low", "Moderate", "High"], weights=[0.05, 0.35, 0.6])[0]
            
            # Duration based on exercise type and intensity
            if intensity == "Low":
                duration = random.randint(15, 30)
            elif intensity == "Moderate":
                duration = random.randint(30, 50)
            else:  # High
                duration = random.randint(20, 40)
                
            # Modify duration based on age
            if age > 60:
                duration = max(10, int(duration * 0.8))  # Shorter workouts for older patients
            
            # Calculate calories and heart rate
            calories_base = {"Low": 4, "Moderate": 7, "High": 10}
            calories_multiplier = {
                "Walking": 1.0, 
                "Running": 1.8, 
                "Cycling": 1.5, 
                "Swimming": 1.6, 
                "Weight Training": 1.3, 
                "Yoga": 0.8, 
                "HIIT": 2.0
            }
            
            calories = int(duration * calories_base[intensity] * calories_multiplier[exercise_type])
            
            # Heart rate during exercise
            base_heart_rate = 70  # Default if not available
            if "Heart Rate" in patient["vitals"]:
                try:
                    base_heart_rate = float(patient["vitals"]["Heart Rate"]["value"])
                except:
                    pass
                
            heart_rate_increase = {"Low": 20, "Moderate": 50, "High": 80}
            avg_heart_rate = int(base_heart_rate + heart_rate_increase[intensity] * random.uniform(0.8, 1.2))
            
            # Steps only relevant for walking and running
            steps = 0
            if exercise_type in ["Walking", "Running"]:
                step_rate = {"Walking": 100, "Running": 160}
                steps = int(duration * step_rate[exercise_type] * random.uniform(0.9, 1.1))
            
            exercise_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "time": time_str,
                "exercise_type": exercise_type,
                "duration_minutes": duration,
                "intensity": intensity,
                "calories_burned": calories,
                "avg_heart_rate": avg_heart_rate,
                "steps": steps
            })
    
    # Save exercise data
    exercise_df = pd.DataFrame(exercise_data)
    if not exercise_df.empty:
        exercise_df.to_csv(f"{patient_dir}/google_fit/google_fit.csv", index=False)
    
    # Create patient exercise summary for LLM recommendations
    exercise_summary = {
        "weekly_frequency": exercise_frequency,
        "preferred_intensity": exercise_intensity,
        "preferred_activities": preferred_types,
        "avg_duration": int(exercise_df["duration_minutes"].mean()) if not exercise_df.empty else 0,
        "exercise_count": len(exercise_data)
    }
    
    # Save exercise summary
    with open(f"{patient_dir}/exercise_summary.json", "w") as f:
        json.dump(exercise_summary, f, indent=2)

if __name__ == "__main__":
    main()