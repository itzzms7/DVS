// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EVoting {
    address public owner;
    
    // Structure to define a Candidate
    struct Candidate {

        int id;
        string name;
        string symbol;
        uint256 voteCount;
        bool exists; // To check if candidate is registered
    }

    // Mapping to Store candidates by their ID for instant lookup
    mapping(int => Candidate) public candidates;
    
    // Mapping to track who has voted using a cryptographic hash (Privacy & Security)
    mapping(bytes32 => bool) public hasVoted;

    uint256 public totalVotes = 0;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can perform this action");
        _;
    }

    constructor() {
        owner = msg.sender;
        
        // Automatically add candidates upon deployment
        // This saves you from having to do it manually in Remix every time!
        candidates[1] = Candidate(1, "Rahul Gandhi", "Congress", 0, true);
        candidates[2] = Candidate(2, "Narendar Modi", "BJP", 0, true);
        candidates[3] = Candidate(3, "Akhilesh Yadav", "Samajwadi", 0, true);
    }

    // STEP 1: Admin adds candidates BEFORE the election starts
    function addCandidate(int _id, string memory _name, string memory _symbol) public onlyOwner {
        require(!candidates[_id].exists, "Candidate ID already exists");
        candidates[_id] = Candidate(_id, _name, _symbol, 0, true);
    }

    // STEP 2: The actual voting logic (Publicly accessible, secure, O(1) complexity)
    function markVote(int _candidate_ID, bytes32 _voterHash) public {
        // 1. Verify the candidate actually exists
        require(candidates[_candidate_ID].exists, "Invalid candidate ID");
        
        // 2. Prevent duplicate voting
        require(!hasVoted[_voterHash], "This user has already cast a vote");

        // 3. Mark the user as having voted
        hasVoted[_voterHash] = true;

        // 4. Increment the candidate's score directly (No loops needed!)
        candidates[_candidate_ID].voteCount += 1;
        totalVotes += 1;
    }

    // STEP 3: Get results instantly 
    function getCount(int _candidate_ID) public view returns (uint256) {
        require(candidates[_candidate_ID].exists, "Invalid candidate ID");
        return candidates[_candidate_ID].voteCount;
    }
}