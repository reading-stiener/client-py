from fhirclient import client
from pprint import pprint
from pymongo import MongoClient
import fhirclient.models.patient as patient
import fhirclient.models.organization as organization
import fhirclient.models.allergyintolerance as allergyintolerance 

myclient = MongoClient("mongodb://localhost:27017/")
patient_db = myclient["PATIENT_REC"]

settings = {
    'app_id': 'my_web_app',
    'api_base': 'https://r3.smarthealthit.org/'
}
smart = client.FHIRClient(settings=settings)

resourceList = {"Patient" : patient.Patient, 
                "Organisation" : organization.Organization, 
                "AllergyIntolerance" : allergyintolerance.AllergyIntolerance}

for resource_name, resource in resourceList.items():
    print('Adding {} resources in EHR database'.format(resource_name))  
    resourceBundle = resource.read(rem_id=None, 
                                   server=smart.server, 
                                   return_raw=True)
    resource_col = patient_db[resource_name]
    for doc in resourceBundle['entry']:
        resource_col.insert_one(doc)
