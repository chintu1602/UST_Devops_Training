from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
employees = [] 

class Employee(BaseModel):
    id: int
    name: str
    role: str

@app.get('/')
def get_all_employees():
    return employees

@app.post('/add')
def add_employee(e: Employee):
    employees.append({'id': e.id, 'name': e.name, 'role': e.role})
    return {'message': 'Employee added successfully'}

@app.get('/get_details')
def get_employee(id: int):
    for emp in employees:
        if emp['id'] == id:
            return emp
    return {'message': 'Employee not found'}

@app.put('/update')
def update_employee(id: int, name: str, role: str):
    for emp in employees:
        if emp['id'] == id:
            emp['name'] = name
            emp['role'] = role
            return {'message': 'Employee updated successfully'}
    return {'message': 'Employee not found'}

@app.delete('/delete')
def delete_employee(id: int):
    for emp in employees:
        if emp['id'] == id:
            employees.remove(emp)
            return {'message': 'Employee deleted successfully'}
    return {'message': 'Employee not found'}