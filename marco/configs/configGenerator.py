# Generates the yaml config files used by Marco

import yaml # needed to make config

def addCommand():
    """adds a command to the yaml config

    Returns:
        commadID: String identifying the command
        commandArray : the array of settings to be stored in yaml
    """

    # prompts the user for command settings
    commandID = input("\nEnter command ID: ")

    
    
    try:
        command = input("\nEnter the command in hex: ")
        int(command, 16) # check that command is hex
        
        bp = input("\nEnter the bit period for the signal in seconds: ")
        if float(bp) <= 0: # check that the bit period is greater than zero
            print("Bit period cannot be zero or negative")
            return None, [0,0,0,0]
        
        sleepDelay = input("\nEnter how long to wait to retransmit in seconds: ")
        if float(sleepDelay) < 0: # check that sleep is not negative
            print("Retransmission delay cannot be negative")
            return None, [0,0,0,0]
        
        minDelay = len(format(int(command, 16), '04b')) * float(bp) # calculate how long it will take to transmit the message
        retransmitDelay = float(sleepDelay) + minDelay # calculate the total delay
        retransmitDelay = str(retransmitDelay)
        
        responseFreq = input("\nEnter the frequency the key fob is expected to respond on in hertz: ")
        int(responseFreq) # check that the response freq is an int
        
    except ValueError:
        print("Error, data was entered incorrectly, returning to main menu")
        return None, [0,0,0,0]

    return commandID, [command, bp, retransmitDelay, responseFreq]


if __name__ == "__main__":
    
    print("Marco Transmission Configuration Generator: ")
    
    # grabs filename from user
    fileName = input("\nPlease enter the file name of the config file you wish to generate: ")
    
    # append .yml if needed
    if not fileName.endswith('.yml'):
        fileName = fileName + '.yml'
        
    # print(fileName)
    
    commandDic = {}
    
    while True:
        
        # checks how many commands are in the dictionary
        if len(commandDic.keys()) < 1:
            print("\nConfig file currently has no commands")
        else:
            print(f"\nCurrent commands are: ")
            
            for tmp in commandDic.keys():
                print(tmp)
            
        userSelection = input("\nTo add a command press 1, or press anything else to exit: ")
        
        if userSelection == '1': # add command
            key, cmd = addCommand()
            if key is not None:
                commandDic[key] = cmd
        else:
            break
        
    print(f"\nWriting {fileName}")
    
    with open(fileName, 'w') as file:
        doc = yaml.dump(commandDic, file)
    
    print("exiting the program")
    