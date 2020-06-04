from fhirclient import client
from pprint import pprint
from pymongo import MongoClient
import fhirclient.models.patient as patient
import fhirclient.models.organization as organization
import fhirclient.models.allergyintolerance as allergyintolerance
import fhirclient.models.encounter as encounter
import fhirclient.models.careplan as careplan
import fhirclient.models.diagnosticreport as diagnosticreport
import fhirclient.models.encounter as encounter
import fhirclient.models.goal as goal
import fhirclient.models.immunization as immunization
import fhirclient.models.medication as medication
import fhirclient.models.medicationrequest as medicationrequest
import fhirclient.models.observation as observation
import fhirclient.models.procedure as procedure

myclient = MongoClient("mongodb://localhost:27017/")
patient_db = myclient["PATIENT_REC"]

settings = {
    'app_id': 'my_web_app',
    'api_base': 'https://r3.smarthealthit.org/'
}
smart = client.FHIRClient(settings=settings)

# tried pulling all patients but limited me to 50
resourceList = {#"Organization" : organization.Organization,
                "AllergyIntolerance" : allergyintolerance.AllergyIntolerance, 
                "CarePlan" : careplan.CarePlan,
                "DiagnosticReport" : diagnosticreport.DiagnosticReport,
                "Encounter" : encounter.Encounter,
                "Goal" : goal.Goal,
                "Immunization" : immunization.Immunization,
                #"Medication" : medication.Medication,
                "MedicationRequest" : medicationrequest.MedicationRequest,
                "Observation" : observation.Observation,
                "Procedure" : procedure.Procedure}


print('Adding {} resources in EHR database'.format('Patient'))
patient_resource = patient.Patient
patient_bundle = patient_resource.read(rem_id=None, 
                                server=smart.server, 
                                return_raw=True)

for patient in patient_bundle['entry']:
    patient_col = patient_db['Patient']
    patient_col.insert_one(patient)

    patient_id = patient['resource']['id']
    print('Record for patient with {} id'.format(patient_id))

    for resource_name, resource in resourceList.items():
        resource_rec = resource.read(rem_id='?patient=Patient/'+patient_id,
                                     server=smart.server,
                                     return_raw=True)
        
        print('Patient has {} number of {} resource type'.format(resource_rec['total'], resource_name))
        try: 
            for entry in resource_rec['entry']:
                resource_type = entry['resource']['resourceType']
                
                resource_col = patient_db[resource_type]
                resource_col.insert_one(entry)
        except KeyError: 
            continue
