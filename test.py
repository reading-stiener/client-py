from fhirclient import client
from pprint import pprint
from pymongo import MongoClient

settings = {
    'app_id': 'my_web_app',
    'api_base': 'https://r3.smarthealthit.org/'
}
smart = client.FHIRClient(settings=settings)

resourceList = [Patient, Organisation, AllergyIntolerance]

for resource in resourceList:  
    resourceBundle = p.resource.read(rem_id=None, 
                                     server=smart.server)

patientBundle = p.Patient.read(rem_id=None, 
                               server=smart.server, 
                               return_raw = True)
pprint(patientBundle['entry'][0])

print(patient.birthDate)
print(patient.birthDate.isostring)
# '1963-06-12'
print(smart.human_name(patient.name[0]))