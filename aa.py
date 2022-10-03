from models_flat import Links
from models_flat import Session

session = Session()
link = []

with open('emil', 'r') as file:
    text = file.readlines()
    for l in text:
        li = Links(link=l)
        link.append(li)

session.add_all(link)
session.commit()

# list = [1,2,3,4,5,6,7,8,9]
#
# for i in list:
#     if i == 5:
#         continue
#     print(i)
