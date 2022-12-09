HOSPITAL BLOCKCHAIN

Blockchain makes use of 3 main smart contracts:
    createNewHospital.py
    hospitalTransactions.py
    validatePatientData.py 

createNewHospital:
    generate_hospital_node(): generates a new algorand account corresponding to the new hospital

hospitalTransactions:
    trainModel()            : runs the train model function on the blockchain with provided information
    uploadPatientData()     : sends patient data from hospital node to itself to store in blockchain
    setUpTransaction()      : ensure two hospital nodes can send one another transactions (opt-in function)
    sendTransaction()       : sends either patient data or model updates over the blockchain

Saved for future implementations:
    validatePatientData.py functions:
        initHospitalMap()   : (IPFS) initialize map of (patient data : hospital it came from)   
        isExistsHospital()  : (IPFS) does requested data exist in the requested hospital 
    
    createNewHospital.py functions:
        validate_new_node() : ensure that the new hospital does not already exist
        sendToCA()          : ensure that the hospital requesting to generate node can join the blockchain
        
    hospitalTransaction.py functions:
        uploadModelData()   : used to upload model data to related IPFS node
 
