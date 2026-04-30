from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from web3 import Web3
from django.contrib.auth import authenticate, login, logout
from .models import Voter

# ==========================================
# 1. WEB3 AND SMART CONTRACT SETUP
# ==========================================
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) 
contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'  # Deployed contract address

contract_abi = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "int256",
				"name": "_id",
				"type": "int256"
			},
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_symbol",
				"type": "string"
			}
		],
		"name": "addCandidate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "int256",
				"name": "",
				"type": "int256"
			}
		],
		"name": "candidates",
		"outputs": [
			{
				"internalType": "int256",
				"name": "id",
				"type": "int256"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "symbol",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "voteCount",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "exists",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "int256",
				"name": "_candidate_ID",
				"type": "int256"
			}
		],
		"name": "getCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"name": "hasVoted",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "int256",
				"name": "_candidate_ID",
				"type": "int256"
			},
			{
				"internalType": "bytes32",
				"name": "_voterHash",
				"type": "bytes32"
			}
		],
		"name": "markVote",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalVotes",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Initialize Contract and Admin Account globally
contract = w3.eth.contract(address=contract_address, abi=contract_abi)
admin_account = w3.eth.accounts[0]


# ==========================================
# 2. BLOCKCHAIN INTERACTION FUNCTIONS
# ==========================================

def saveVote(candidate_id, voter, aadhar):
    try:
        # Hash the Aadhar for privacy
        voter_hash = Web3.keccak(text=str(aadhar))
        
        # Call the smart contract
        tx_hash = contract.functions.markVote(int(candidate_id), voter_hash).transact({'from': admin_account})
        
        # Wait for block confirmation
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return True, 'Your vote saved inside Ethereum Blockchain!'
    except Exception as e:
        # Print actual technical error to terminal for debugging
        print("\n!!! BLOCKCHAIN ERROR DETECTED !!!")
        print(f"Details: {str(e)}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        
        # Return a cleaner message to the UI
        error_msg = str(e)
        if "revert" in error_msg.lower():
            return False, 'Blockchain Rejection: You have already voted'
        return False, f'Technical Error: {error_msg[:100]}...'

def getVote(candidate_id):
    try:
        count = contract.functions.getCount(int(candidate_id)).call()
        return count
    except Exception as e:
        return 0


# ==========================================
# 3. DJANGO VIEWS (ROUTING)
# ==========================================

def CastVoteAction(request):
    if request.method == 'POST':
        candidate_id = request.POST.get('t1', False)
        voter = request.POST.get('t2', False)
        aadhar = request.POST.get('t3', False)
        
        # --- SECURITY CHECK ---
        is_authorized = Voter.objects.filter(aadhar_number=aadhar).exists()
        
        if not is_authorized:
            context = {'data': 'Authorization Failed: This ID is not registered in our database.'}
            return render(request, 'index.html', context)
            
        # --- BLOCKCHAIN EXECUTION ---
        success, message = saveVote(candidate_id, voter, aadhar)
        
        context = {'data': message}
        return render(request, 'index.html', context)
    
def AdminLogin(request):
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        
        user = authenticate(request, username=u, password=p)
        
        if user is not None and user.is_superuser:
            login(request, user)
            context= {'data':'Welcome Admin'}
            return render(request, "AdminScreen.html", context)
        else:
            context= {'data':'Invalid Admin credentials!'}
            return render(request, 'Admin.html', context)

def AdminLogout(request):
    logout(request)
    return redirect('index')

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def ViewCount(request):
    if request.method == 'GET':
       return render(request, 'ViewCount.html', {})    

def Admin(request):
    if request.method == 'GET':
       return render(request, 'Admin.html', {})

def Vote(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="">'
        arr = ['Candidate ID','Candidate Name','Symbol','Cast Your Vote']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        output += "<tr><td>"+font+"1"+"</td>"
        output += "<td>"+font+"Rahul Gandhi"+"</td>"
        output+='<td><img src=/static/symbols/congress.png height=100 width=100/></td>'
        output+='<td><a href=\'CastVote?t1=1\'><font size=3 >Click Here</font></a></td></tr>'
        output += "<tr><td>"+font+"2"+"</td>"
        output += "<td>"+font+"Narendar Modi"+"</td>"
        output+='<td><img src=/static/symbols/bjp.png height=100 width=100/></td>'
        output+='<td><a href=\'CastVote?t1=2\'><font size=3 >Click Here</font></a></td></tr>'
        output += "<tr><td>"+font+"3"+"</td>"
        output += "<td>"+font+"Akhilesh Yadav"+"</td>"
        output+='<td><img src=/static/symbols/samajvadi.png height=100 width=100/></td>'
        output+='<td><a href=\'CastVote?t1=3\'><font size=3 >Click Here</font></a></td></tr>'         
        context= {'data':output}        
        return render(request, 'Vote.html', context)

def CastVote(request):
    if request.method == 'GET':
        candidate = request.GET.get('t1', False)
        output = '<TR><TH align="left"><font size="" color="white">Candidate&nbsp;ID<TD><Input type=text name="t1" value="'+candidate+'" class="form-control" readonly></TD></TR>'
        context= {'data1':output}        
        return render(request, 'CastVote.html', context)

def ViewCountAction(request):
    if request.method == 'POST':
        candidate = request.POST.get('t1', False)
        count = getVote(int(candidate))
        
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" >'
        arr = ['Candidate ID','Candidate Name','Symbol','Total Votes Received']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        if candidate == "1":
            output += "<tr><td>"+font+"1"+"</td>"
            output += "<td>"+font+"Rahul Gandhi"+"</td>"
            output+='<td><img src=/static/symbols/congress.png height=100 width=100/></td>'
            output+='<td><font size=3 >'+str(count)+'</font></a></td></tr>'
        if candidate == "2":
            output += "<tr><td>"+font+"2"+"</td>"
            output += "<td>"+font+"Narendar Modi"+"</td>"
            output+='<td><img src=/static/symbols/bjp.png height=100 width=100/></td>'
            output+='<td><font size=3 >'+str(count)+'</font></a></td></tr>'
        if candidate == "3":
            output += "<tr><td>"+font+"3"+"</td>"
            output += "<td>"+font+"Akhilesh Yadav"+"</td>"
            output+='<td><img src=/static/symbols/samajvadi.png height=100 width=100/></td>'
            output+='<td><font size=3 >'+str(count)+'</font></a></td></tr>'         
        context= {'data':output}        
        return render(request, 'ViewResult.html', context)