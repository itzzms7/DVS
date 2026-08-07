#  Decentralized E-Voting System (DVS)

A secure, transparent, and immutable full-stack decentralized voting application built with Solidity, Hardhat, Remix, and Django.

This project ensures one-vote-per-citizen using cryptographic hashing and restricts voting to authorized individuals (verified via their registered identification numbers) through a secure Django backend and database whitelist.

## 🛠️ Tech Stack & Architecture

- **Smart Contract:** Solidity (^0.8.0)
- **Blockchain Environment:** Hardhat (Local Node) & Remix IDE
- **Backend Framework:** Python 3.x / Django
- **Database:** SQLite3 (For voter registration & authorization whitelist)
- **Web3 Bridge:** Web3.py
- **Frontend Interface:** HTML5, CSS3, JavaScript (Django Templates)

## 📁 Project Structure

```text
├── contracts/
│   └── EVoting.sol          # Solidity smart contract for voting logic & tallying
├── EVotingApp/
│   ├── models.py            # SQLite database models (Voter whitelist)
│   ├── views.py             # Django controllers, Web3 instance & transaction management
│   ├── urls.py              # Application routing
│   └── templates/           # Frontend HTML templates
├── manage.py                # Django administrative utility
└── README.md                # Project documentation
```

## 🔒 Security Features

- **Cryptographic Privacy:** Identification numbers are hashed using `keccak256` before hitting the network, ensuring personal identifiers are never stored directly on the public ledger.
- **Double-Voting Prevention:** The smart contract uses a `mapping(bytes32 => bool)` to natively track voter hashes and reject duplicate transaction attempts at the EVM level.
- **Database Bouncer:** Django verifies whether an incoming voter exists in the authorized `Voter` database prior to executing any smart contract functions.
- **Immutable Tallying:** Vote counts are stored on-chain and incremented directly without intermediary databases, eliminating vote tampering.

## ⚡ Demo Day Setup & Deployment Guide

Because Hardhat operates as an in-memory blockchain, the network state resets whenever the node is restarted. Follow these step-by-step instructions to spin up the local environment:

### Step 1: Start the Local Blockchain Node

- Open your project in VS Code.
- Open a new Terminal window.
- Run the following command:

```bash
npx hardhat node
```

- Keep this terminal running continuously in the background.

### Step 2: Deploy the Smart Contract via Remix

- Open Remix IDE in your web browser.
- Open your `EVoting.sol` contract and compile it (ensure a green checkmark appears on the compiler tab).
- Open the **Deploy & Run Transactions** tab on the left sidebar.
- Change the **Environment** dropdown to **Custom - External Http Provider** and verify the endpoint is set to `http://127.0.0.1:8545`.
- Click **Deploy**.
- Under **Deployed Contracts** at the bottom left, click the **Copy** icon next to the deployed contract instance to get its address.

### Step 3: Link Contract Address to Django

- Open `EVotingApp/views.py` in VS Code.
- Locate the global setup section:

```python
contract_address = '0x...'
```

- Update `contract_address` with the newly deployed contract address copied from Remix and save the file (`Ctrl + S`).

### Step 4: Run the Django Web Server

- Open a second terminal window in VS Code (do not close the Hardhat node terminal).
- Start the Django application server:

```bash
python manage.py runserver
```

- Open `http://127.0.0.1:8000/` in your web browser.

### Step 5: Authorize Voters (Admin Setup)

- Navigate to `http://127.0.0.1:8000/admin`.
- Log in using your Django superuser credentials.
- Open the **Voters** database table.
- Add the registered voter identification records that are permitted to cast votes during the session.

## 💡 How It Works (Transaction Workflow)

- **User Casts Vote:** The voter navigates to the UI, selects a candidate, enters their registered identification number, and submits the form.
- **Authorization Check:** Django queries `Voter.objects.filter(...)` to verify if the individual is authorized to vote.
- **Hashing:** Python generates a `bytes32` hash of the identification number using `Web3.keccak(text=...)`.
- **Smart Contract Execution:** Django calls `markVote(candidate_id, voter_hash)` using `Web3.py`.
- **EVM Verification:** The smart contract checks:
  - Whether `candidates[candidate_id].exists` is `true`.
  - Whether `hasVoted[voter_hash]` is `false`.
- **State Mutation:** If valid, `hasVoted[voter_hash]` is flipped to `true`, the candidate's `voteCount` increments by `1`, and a block confirmation is returned.
