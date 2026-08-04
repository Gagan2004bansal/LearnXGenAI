from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: Annotated[ str, Field(max_length = 50, min_length = 2,
     title = "Patient Name", description = "Name of the patient", 
     examples=['Gagan', 'Rohit']) ]
    email: EmailStr
    linkedin_url: Optional[AnyUrl] = None
    age: int = Field(gt = 0, lt = 120)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=False, description = "Married or not")]
    allergies: Annotated[Optional[List[str]], Field(default=None)]
    contacts_info: Dict[str, str]


    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}.")
        
        return value


def insert_pateint_info(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print("Patient data inserted successfully!")

def update_pateint_info(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Patient data updated successfully!")

patient_info = {'name': 'Gagan','email': 'bansalgagan@hdfc.com' ,'age' : 22, 'weight': 55, 'contacts_info': {'mobile': '9996892070'}}

patient = Patient(**patient_info)
# insert_pateint_info(patient)
json_convert = patient.model_dump_json()
print(json_convert)

# PROBLEM WITH PYTHON 

# 1. Type Validation
# 2. Data Validation

# ABOVE SOLUTION WITH PYDANTIC

# def insert_patient_data(name: str, age: int):

#     if type(name) == str and type(age) == int:
#         if age < 0:
#             raise ValueError("Age cannot be negative.")
#         else: 
#             print(name)
#             print(age)
#             print("Patient data inserted successfully!")
#     else:
#         raise ValueError("Invalid data type for name or age.")


# def update_patient_data(name: str, age: int):

#     if type(name) == str and type(age) == int:
#         print(name)
#         print(age)
#         print("Patient data updated successfully!")
#     else:
#         raise ValueError("Invalid data type for name or age.")


# insert_patient_data("John Doe", 23)
