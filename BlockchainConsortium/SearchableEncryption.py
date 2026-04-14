import os
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import hashlib

recipient_key = generate_eth_key()
recipient_private_key_hex = '0x3dfbb5233d5816a0a14510919bed16a3fa7543a5a5d179ba6ed8cbf8a6564d64'
recipient_public_key_hex = '0x424718c50202bf6973f091d60e2ed92bae439812286837109b12928c0e4ef49916040f1678e9f9be1f68cca050efd6d2d7790e0b5f44fa47079ab9d2d8a7e558'

#function to generate secured searchable query
def generateSecuredQuery(query):
    data = query.strip()
    data = data.lower().strip()
    arr = data.split(" ")
    secure_trap = ""
    for i in range(len(arr)):
        word = arr[i].strip()
        if len(word) > 0:
            kw = encrypt(recipient_public_key_hex, word.encode())
            kw = decrypt(recipient_private_key_hex, kw)
            word = hashlib.sha256(kw).hexdigest()
            secure_trap += word+" "
    return secure_trap

#save trapdoor to cloud db location
def saveTrapdoor(trapdoor):
    with open("CrowdApp/static/trapdoor.txt", "a+") as file:
        file.write(trapdoor)
    file.close()
    
#generate trapdoor
def createTrapdoor(filename, data, username):
    data = data.lower().strip()
    arr = data.split(" ")
    secure_trap = ""
    for i in range(len(arr)):
        word = arr[i].strip()
        if len(word) > 0:
            kw = encrypt(recipient_public_key_hex, word.encode())
            kw = decrypt(recipient_private_key_hex, kw)
            word = hashlib.sha256(kw).hexdigest()
            secure_trap += word+" "
    trapdoor = username+" "+filename+" "+secure_trap.strip()+"\n"    
    saveTrapdoor(trapdoor)

#load existing trapdoor
def loadTrapdoor():
    if os.path.exists("CrowdApp/static/trapdoor.txt"):
        with open("CrowdApp/static/trapdoor.txt", "rb") as file:
            trapdoor = file.read()
        file.close()    
        trapdoor = trapdoor.decode()
    else:
        trapdoor = ""
    return trapdoor

