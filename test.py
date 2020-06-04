from fhirclient import client
from pprint import pprint

settings = {
    'app_id': 'my_web_app',
    'api_base': 'https://r3.smarthealthit.org/'
}
smart = client.FHIRClient(settings=settings)
import fhirclient.models.patient as p

patient = p.Patient.read(rem_id='008076b8-7fba-4645-ba41-0b8ffe10e82b', 
                         server=smart.server)

patientBundle = p.Patient.read(rem_id=None, 
                               server=smart.server, 
                               return_raw = True)
pprint(patientBundle.keys)

print(patient.birthDate)
print(patient.birthDate.isostring)
# '1963-06-12'
print(smart.human_name(patient.name[0]))