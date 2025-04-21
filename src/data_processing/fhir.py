import requests
import json
import os
import pandas as pd
from datetime import datetime

class FHIRIntegration:
    """
    Class to integrate with FHIR server and local patient data
    """
    
    def __init__(self, base_url="https://hapi.fhir.org/baseR4", data_dir="data/patient_data"):
        self.base_url = base_url
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def fetch_patient(self, patient_id):
        """Fetch a patient's complete data from FHIR server."""
        patient_data = {}
        
        # First try to load from local cache if available
        local_path = os.path.join(self.data_dir, patient_id, "patient_info.json")
        if os.path.exists(local_path):
            try:
                with open(local_path, 'r') as f:
                    return json.load(f)
            except:
                pass  # If loading fails, proceed with fetching from server
        
        # 1. Get patient demographics
        patient_url = f"{self.base_url}/Patient/{patient_id}"
        try:
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
            conditions_url = f"{self.base_url}/Condition?patient={patient_id}&_count=100"
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
            meds_url = f"{self.base_url}/MedicationRequest?patient={patient_id}&_count=100"
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
            vitals_url = f"{self.base_url}/Observation?patient={patient_id}&category=vital-signs&_count=100"
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
            
            # Create directory for this patient
            patient_dir = os.path.join(self.data_dir, patient_id)
            os.makedirs(patient_dir, exist_ok=True)
            
            # Save patient data to JSON
            with open(local_path, "w") as f:
                json.dump(patient_data, f, indent=2)
            
            return patient_data
            
        except Exception as e:
            print(f"Error fetching patient data: {str(e)}")
            return None
    
    def load_device_data(self, patient_id):
        """Load Omron and Google Fit data for a patient from local directory."""
        patient_dir = os.path.join(self.data_dir, patient_id)
        
        # Load Omron data
        omron_path = os.path.join(patient_dir, "omron", "omron_data.csv")
        bp_data = None
        if os.path.exists(omron_path):
            try:
                bp_data = pd.read_csv(omron_path)
                # Convert date columns
                bp_data['date'] = pd.to_datetime(bp_data['date'])
                # Create datetime column by combining date and time
                bp_data['datetime'] = pd.to_datetime(
                    bp_data['date'].dt.strftime('%Y-%m-%d') + ' ' + bp_data['time']
                )
            except Exception as e:
                print(f"Error loading Omron data: {str(e)}")
        
        # Load Google Fit data
        fit_path = os.path.join(patient_dir, "google_fit", "google_fit.csv")
        exercise_data = None
        if os.path.exists(fit_path):
            try:
                exercise_data = pd.read_csv(fit_path)
                # Convert date columns
                exercise_data['date'] = pd.to_datetime(exercise_data['date'])
                # Create datetime column by combining date and time
                exercise_data['datetime'] = pd.to_datetime(
                    exercise_data['date'].dt.strftime('%Y-%m-%d') + ' ' + exercise_data['time']
                )
            except Exception as e:
                print(f"Error loading Google Fit data: {str(e)}")
        
        return bp_data, exercise_data    
    
    def prepare_fhir_data_for_llm(self, patient_data):
        """
        Format FHIR data for LLM recommendation prompt using specific LOINC codes.
        
        Parameters:
        - patient_data: Dictionary containing patient information
        
        Returns:
        Dictionary formatted for LLM recommendation
        """
        if not patient_data:
            return None
        
        # LOINC codes mapping
        loinc_codes = {
            "8867-4": "Heart rate",
            "8480-6": "Systolic BP",
            "8462-4": "Diastolic BP",
            "8310-5": "Body temperature",
            "9279-1": "Respiratory rate",
            "8302-2": "Height",
            "29463-7": "Weight",
            "39156-5": "BMI"
        }
        
        # Prepare LLM-friendly data
        llm_fhir_data = {
            "patient_info": {
                "name": patient_data.get("name", "Unknown"),
                "age": patient_data.get("age", "Unknown"),
                "gender": patient_data.get("gender", "Unknown")
            },
            "conditions": patient_data.get("conditions", []),
            "medications": patient_data.get("medications", []),
            "bp_category": patient_data.get("bp_category", "Unknown"),
            "vital_signs": {},
            "allergies": patient_data.get("allergy_ids", [])
        }
        
        # Process vital signs using LOINC codes
        vitals = patient_data.get("vitals", {})
        for code, display_name in loinc_codes.items():
            # Try to find the vital sign using LOINC code or display name
            value = None
            
            # First, try direct matching
            if code in vitals:
                value = vitals[code]
            elif display_name in vitals:
                value = vitals[display_name]
            
            # If value found, add to vital signs
            if value is not None:
                # Handle different value formats
                if isinstance(value, dict):
                    # If it's a dictionary with 'value' and 'unit'
                    if "value" in value and "unit" in value:
                        llm_fhir_data["vital_signs"][display_name] = f"{value['value']} {value['unit']}"
                    else:
                        llm_fhir_data["vital_signs"][display_name] = str(value)
                else:
                    # If it's a simple value
                    llm_fhir_data["vital_signs"][display_name] = str(value)
        
        return llm_fhir_data
    
    def search_patient_by_name(self, patient_name):
        """
        Search for a patient by full name in the FHIR server
        
        Parameters:
        - patient_name: Full name of the patient (first_name last_name)
        
        Returns:
        Dictionary with patient basic information or None if not found
        """
        search_url = f"{self.base_url}/Patient?name={patient_name}"
        
        try:
            response = requests.get(search_url)
            
            if response.status_code == 200:
                bundle = response.json()
                
                # Check if any patients found
                if bundle.get("total", 0) > 0:
                    # Return the first matching patient
                    first_patient = bundle["entry"][0]["resource"]
                    return {
                        "id": first_patient.get("id"),
                        "name": f"{first_patient.get('name', [{}])[0].get('given', [''])[0]} {first_patient.get('name', [{}])[0].get('family', '')}"
                    }
            
            return None
        
        except Exception as e:
            print(f"Error searching for patient: {str(e)}")
            return None