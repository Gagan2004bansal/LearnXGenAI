from pydantic import BaseModel, EmailStr, Field
from typing import Optional 

class Student(BaseModel): 
    name: str = 'Gagan Bansal' 
    age: Optional[int] = None 
    email: EmailStr 
    cgpa : float = Field(gt=0, lt=10, default=5, description="The CGPA of the student, must be between 0 and 10")
    

new_student = {'age': 22, 'email': 'bansalgagan2004@gmail.com'} 

# This is a pydantic object, which has been validated and parsed according to the defined schema. 
student = Student(**new_student) 
print(student) 

# To convert in to a dictionary, we can use the .dict() method provided by pydantic. 
student_dict = student.model_dump() 
print(student_dict) 

# To Convert in to JSON, we can use the .json() method provided by pydantic. 
student_json = student.model_dump_json() 
print(student_json)