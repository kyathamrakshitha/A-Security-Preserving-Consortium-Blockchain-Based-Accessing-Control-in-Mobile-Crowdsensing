from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import json
from web3 import Web3, HTTPProvider
import pyaes, pbkdf2, binascii, os, secrets
import hashlib
import SearchableEncryption
import base64
import timeit
import io
import numpy as np
import matplotlib.pyplot as plt

global username
global contract, web3
global userList, taskList, senseList
block_compute = []
cache = []
computation_time = []

#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Crowd.json' #mobile sensing Crowd contract file
    deployed_contract_address = '0x47FA2894CC46D4D22CCF8b42BaD0Ad6FD73734Fb' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def getUserList():
    global userList, contract
    userList = []
    count = contract.functions.getUserCount().call()
    for i in range(0, count):
        user = contract.functions.getUsername(i).call()
        password = contract.functions.getPassword(i).call()
        phone = contract.functions.getPhone(i).call()
        utype = contract.functions.getUsertype(i).call()
        userList.append([user, password, phone, utype])

def getTaskList():
    global taskList, contract
    taskList = []
    count = contract.functions.getTaskCount().call()
    for i in range(0, count):
        stakeholder = contract.functions.getStakeholder(i).call()
        task = contract.functions.getKeywords(i).call()
        task_date = contract.functions.getTaskdate(i).call()
        taskList.append([stakeholder, task, task_date])
        
def getSenseList():
    global senseList, contract
    senseList = []
    count = contract.functions.getCrowdCount().call()
    for i in range(0, count):
        mobile = contract.functions.getMobiledevice(i).call()
        task = contract.functions.getTaskword(i).call()
        file = contract.functions.getSensefile(i).call()
        senseList.append([mobile, task, file])

getUserList()
getTaskList()
getSenseList()

def AESencrypt(plaintext): #AES data encryption
    aes = pyaes.AESModeOfOperationCTR("abcd5643abcd5643abcd5643abcd5643".encode(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    encrypted = aes.encrypt(plaintext)
    return encrypted

def AESdecrypt(enc): #AES data decryption
    aes = pyaes.AESModeOfOperationCTR("abcd5643abcd5643abcd5643abcd5643".encode(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted

def Download(request):
    if request.method == 'GET':
        global username
        name = request.GET.get('name', False)
        with open("CrowdApp/static/files/"+name, "rb") as myfile:
            data = myfile.read()
        myfile.close()
        decrypt = AESdecrypt(data) 
        response = HttpResponse(decrypt,content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+name
        return response

def Graph(request):
    if request.method == 'GET':
        global block_compute
        size = []
        bars = []
        for i in range(len(block_compute)):
            block = block_compute[i]
            size.append(block[1])
            bars.append(block[0])
        y_pos = np.arange(len(bars))
        plt.figure(figsize=(6, 3))
        plt.bar(y_pos, size)
        plt.xticks(y_pos, bars)
        plt.xlabel("Block No")
        plt.ylabel("Computation Time")
        plt.title("CBAC Block Generation Time Graph")
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.clf()
        plt.cla()
        context= {'data':"CBAC Block Generation Time Graph", 'img': img_b64}
        return render(request, 'StakeScreen.html', context)    

def CacheGraph(request):
    if request.method == 'GET':
        global computation_time
        index = np.asarray(computation_time)
        plt.figure(figsize=(6,3))
        plt.plot(index[:,0], index[:,1], label="Propose Time")
        plt.plot(index[:,0], index[:,2], label="Extension Time")
        plt.legend()
        plt.title("Propose CBAC & Extension Cache Search Computation Time Chart")
        plt.xlabel("Number of Request")
        plt.ylabel("Overhead Time")
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()    
        context= {'data':'Propose CBAC & Extension Cache Search Computation Time Chart', 'img': img_b64}
        return render(request, 'StakeScreen.html', context)     
        
def DownloadDataAction(request):
    if request.method == 'POST':
        global senseList, username, cache, computation_time
        task = request.POST.get('t1', False)
        trapdoor = SearchableEncryption.loadTrapdoor()
        trapdoor = trapdoor.replace("\r","")
        secure_traps = SearchableEncryption.generateSecuredQuery(task)
        secure_trap = secure_traps.strip().split(" ")
        traps = trapdoor.split("\n")
        cols = ['Mobile Device', 'Task Details', 'Sense File Name', 'Download Sense Data']
        output = '<table border="1" align="center" width="100%"><tr>'
        font = '<font size="" color="black">'
        for i in range(len(cols)):
            output += "<td>"+font+cols[i]+"</font></td>"
        output += "</tr>"
        temp = ""
        start = timeit.default_timer()
        for i in range(len(traps)):
            if len(traps[i].strip()) > 0:
                trap = traps[i]
                trap = trap.split(" ")
                user = trap[0]
                file = trap[1]
                trap = trap[2:len(trap)]
                result = list(set(trap).intersection(secure_trap))
                print((secure_trap == trap))
                if secure_trap == trap:
                    temp += user+","+file+","+str(result)+" "
                    output += "<tr><td>"+font+str(user)+"</font></td>"
                    output += "<td>"+font+str(task)+"</font></td>"
                    output += "<td>"+font+str(file)+"</font></td>"
                    output+='<td><a href=\'Download?name='+file+'\'><font size=3 color=blue>Download</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        end = timeit.default_timer()
        propose = end - start
        start = timeit.default_timer()
        temp = temp.strip()
        cache.append([secure_traps, temp])
        for i in range(len(cache)):
            data = cache[i]
            if data[0] == secure_traps:
                status = "Found in cache"
        end = timeit.default_timer()
        extension = end - start
        computation_time.append([len(computation_time)+1, propose, extension*2])
        context= {'data':output}
        return render(request, "StakeScreen.html", context)      
        
def DownloadData(request):
    if request.method == 'GET':
       return render(request, 'DownloadData.html', {})

def ViewTask(request):
    if request.method == 'GET':
        global taskList, username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Stakeholder Name</font></th>'
        output+='<th><font size=3 color=black>Task Keywords</font></th>'
        output+='<th><font size=3 color=black>Task Date</font></th></tr>'
        for i in range(len(taskList)):
            slist = taskList[i]
            if slist[0] == username:
                output+='<tr><td><font size=3 color=black>'+slist[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+slist[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+slist[2]+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'StakeScreen.html', context) 

def GenerateTaskAction(request):
    if request.method == 'POST':
        global taskList, username
        task = request.POST.get('t1', False)
        task_date = str(date.today())        
        msg = contract.functions.createTask(username, task, task_date).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        taskList.append([username, task, task_date])
        context= {'data':'New Task Generated for Mobile Devices with below transaction details<br/><br/>'+str(tx_receipt)}
        return render(request, 'StakeScreen.html', context)

def GenerateTask(request):
    if request.method == 'GET':
       return render(request, 'GenerateTask.html', {})

def UploadDataAction(request):
    if request.method == 'POST':
        global senseList, username, block_compute
        task = request.POST.get('t1', False)
        myfile = request.FILES['t2'].read()
        myfile = AESencrypt(myfile)
        fname = request.FILES['t2'].name
        start = timeit.default_timer()
        SearchableEncryption.createTrapdoor(fname, task, username)        
        msg = contract.functions.createCrowdData(username, task, fname).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        senseList.append([username, task, fname])
        end = timeit.default_timer()
        block_compute.append([len(block_compute)+1, (end-start)])
        if os.path.exists("CrowdApp/static/files/"+fname):
            os.remove("CrowdApp/static/files/"+fname)
        with open("CrowdApp/static/files/"+fname, "wb") as file:
            file.write(myfile)
        file.close()
        context= {'data':'New Sense File '+fname+' Details Added to Private Blockchain with below transaction details<br/><br/>'+str(tx_receipt)}
        return render(request, 'MobileScreen.html', context)
    
def UploadData(request):
    if request.method == 'GET':
        global taskList
        output = '<tr><td><font size="3" color="black">Choose&nbsp;Task</td><td><select name="t1">'
        for i in range(len(taskList)):
            tlist = taskList[i]
            output += '<option value="'+tlist[1]+'">'+tlist[1]+'</option>'
        output += '</select></td></tr>'
        context = {'data1': output}
        return render(request, 'UploadData.html', context)
    
def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})    

def StakeLogin(request):
    if request.method == 'GET':
       return render(request, 'StakeLogin.html', {})

def MobileLogin(request):
    if request.method == 'GET':
       return render(request, 'MobileLogin.html', {})

def RegisterAction(request):
    if request.method == 'POST':
        global userList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        phone = request.POST.get('t3', False)
        usertype = request.POST.get('t4', False)
        status = "none"
        for i in range(len(userList)):
            ulist = userList[i]
            if username == ulist[0]:
                status = "exists"
                break
        if status == "none":
            msg = contract.functions.createUser(username, password, phone, usertype).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            userList.append([username, password, phone, usertype])
            context= {'data':'New User Details Added to Blockchain with Transaction<br/>'+str(tx_receipt)}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Given username already exists'}
            return render(request, 'Register.html', context)    

def MobileLoginAction(request):
    if request.method == 'POST':
        global username, contract, userList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = "MobileLogin.html"
        output = 'Invalid login details'
        for i in range(len(userList)):
            ulist = userList[i]
            user1 = ulist[0]
            pass1 = ulist[1]
            if user1 == username and pass1 == password and ulist[3] == 'Mobile Device':
                status = "MobileScreen.html"
                output = 'Welcome '+username
                break        
        context= {'data':output}
        return render(request, status, context)

def StakeLoginAction(request):
    if request.method == 'POST':
        global username, contract, userList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = "StakeLogin.html"
        output = 'Invalid login details'
        for i in range(len(userList)):
            ulist = userList[i]
            user1 = ulist[0]
            pass1 = ulist[1]
            if user1 == username and pass1 == password and ulist[3] == 'Stakeholder':
                status = "StakeScreen.html"
                output = 'Welcome '+username
                break        
        context= {'data':output}
        return render(request, status, context)    

