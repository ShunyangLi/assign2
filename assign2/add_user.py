import csv
from event import User,db

Name, Zid, Email, Password, Role = [], [], [], [], []

filename = 'user.csv'

with open(filename) as file:
    head = csv.reader(file)
    next(head)
    
    for row in head:
        Name.append(row[0])
        Zid.append(row[1])
        Email.append(row[2])
        Password.append(row[3])
        Role.append(row[4])
        
for i in range(0, len(Name), 1):
    u = User(Name[i], Zid[i], Email[i], Password[i], Role[i])
    db.session.add(u)

db.session.commit()
