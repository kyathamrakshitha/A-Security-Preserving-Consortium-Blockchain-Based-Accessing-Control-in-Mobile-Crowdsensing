pragma solidity >= 0.8.11 <= 0.8.11;
pragma experimental ABIEncoderV2;
//Crowd Mobile Sense solidity code
contract Crowd {

    uint public taskCount = 0; 
    mapping(uint => task) public taskList; 
     struct task
     {
       string stakeholder;
       string task_keywords;
       string task_date;       
     }
 
   // events 
   event taskCreated(uint indexed _taskId);

  
   //function  to save task details
   function createTask(string memory sh, string memory tk,string memory td) public {
      taskList[taskCount] = task(sh, tk, td);
      emit taskCreated(taskCount);
      taskCount++;
    }

     //get task count
    function getTaskCount()  public view returns (uint) {
          return taskCount;
    }    

    function getStakeholder(uint i) public view returns (string memory) {
        task memory s = taskList[i];
	return s.stakeholder;
    }

    function getKeywords(uint i) public view returns (string memory) {
        task memory s = taskList[i];
	return s.task_keywords;
    }

    function getTaskdate(uint i) public view returns (string memory) {
        task memory s = taskList[i];
	return s.task_date;
    }

    uint public crowdCount = 0; 
    mapping(uint => crowd) public crowdList; 
     struct crowd
     {
       string mobile_device;
       string task_word;
       string sense_file;        
     }
 
   // events
 
   event crowdCreated(uint indexed _crowdId);
 
  function createCrowdData(string memory md, string memory tw, string memory sf) public {
      crowdList[crowdCount] = crowd(md, tw, sf);
      emit crowdCreated(crowdCount);
      crowdCount++;
    }

    //get crowd sense count
    function getCrowdCount()  public view returns (uint) {
          return  crowdCount;
    }

    function getMobiledevice(uint i) public view returns (string memory) {
        crowd memory usr = crowdList[i];
	return usr.mobile_device;
    }

    function getTaskword(uint i) public view returns (string memory) {
        crowd memory usr = crowdList[i];
	return usr.task_word;
    }

    
    function getSensefile(uint i) public view returns (string memory) {
        crowd memory usr = crowdList[i];
	return usr.sense_file;
    }       

    uint public userCount = 0; 
    mapping(uint => user) public userList; 
     struct user
     {
       string username;
       string password;
       string phone;    
       string usertype;
     }
 
   // events
 
   event userCreated(uint indexed _userId);
 
  function createUser(string memory _username, string memory _password, string memory _phone, string memory ut) public {
      userList[userCount] = user(_username, _password, _phone, ut);
      emit userCreated(userCount);
      userCount++;
    }

    //get user count
    function getUserCount()  public view returns (uint) {
          return  userCount;
    }

    function getUsername(uint i) public view returns (string memory) {
        user memory usr = userList[i];
	return usr.username;
    }

    function getPassword(uint i) public view returns (string memory) {
        user memory usr = userList[i];
	return usr.password;
    }

    
    function getPhone(uint i) public view returns (string memory) {
        user memory usr = userList[i];
	return usr.phone;
    }   

    function getUsertype(uint i) public view returns (string memory) {
        user memory usr = userList[i];
	return usr.usertype;
    }   
}