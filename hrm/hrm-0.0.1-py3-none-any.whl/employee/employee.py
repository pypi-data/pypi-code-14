import json

class Employee:
  'Base class for all employees'

  count = 0

  def __init__(self, name, id, dept):
    self.name = name
    self.id = id
    self.dept = dept
    Employee.count += 1

  def displayEmployee(self):
    print "Name: ", self.name, ", Id: ",self.id,", Dept: ", self.dept

  def empCount(self):
    print "Total employee: %d", Employee.count 
  
  def dump_to_file(self, file):
     print "Dumping info of employee with id: ", self.id, " to a file: ", file
     file = open(file, 'w')
     file.write(self.name)
     file.close

  def jdefault(self,o):
    return o.__dict__
  
  def dump_json(self, file):
     file = open(file, 'w')

     data = {u"id": str(self.id), u"name": self.name, u"dept": self.dept }
     print "DATA::: ", data
     
     print " JSON Create Idented Object::: ",json.dumps(data, indent=2)     
     print " JSON Dump Class Object::: ",json.dumps(self,default=self.jdefault)

     print "Dumping info of employee with id: ", self.id, " to a file with JSON format: ", file  
     json.dump(data,file)
     file.close

     

     
