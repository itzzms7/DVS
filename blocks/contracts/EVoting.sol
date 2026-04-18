// Solidity program to implement
// the above approach
pragma solidity >= 0.8.21 <= 0.8.21;
  
// Build the Contract of EVoting
contract EVoting
{
    // Create a structure for 
    // student details
    struct Party
    {
        int candidate_ID;
        string candidate_Name;
        string voting_symbol;
	string voter_name;
	string aadhar_number;       
    }
  
    address owner;
    int public voteCount = 0;
    mapping(int => Party) public partyRecords;
  
    modifier onlyOwner
    {
        require(owner == msg.sender);
        _;
    }
    constructor()
    {
        owner=msg.sender;
    }
  
    // Create a function to add 
    // the new records
    function markVote(int _candidate_ID, 
                           string memory _candidate_Name,
                           string memory _voting_symbol,
                           string memory _voter_name,
			   string memory _aadhar_number) public onlyOwner
    {
        // Increase the count by 1
          
        // Fetch the party details 
        // with the help of candidate id
        partyRecords[voteCount] = Party(_candidate_ID, _candidate_Name, _voting_symbol, _voter_name,_aadhar_number);
	//uint total = partyRecords.length;
	voteCount = voteCount + 1;
    }
  
    // Create a function to add bonus marks 
    function getCount(int _candidate_ID) public view returns (int count) {
	
    for (int i = 0; i < voteCount; i++) {
        if (partyRecords[i].candidate_ID == _candidate_ID) {
	   count = count + 1;
         }
    }
    return count;
}
}