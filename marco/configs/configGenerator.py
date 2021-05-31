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

    command = input("\nEnter the command in hex: ")

    centerFreq = input("\nEnter the center frequency in hertz: ")

    centerFreq = input("\nEnter the offset frequency in hertz, or 0 if there is none: ")

    pulseWidth = input("\nEnter the pulse width for the signal in seconds: ")

    repeatCount = input("\nEnter how many times to repeat the signal per run: ")

    sleepDelay = input("\nEnter how long to wait to retransmit in seconds: ")

    return commandID, [command, centerFreq, pulseWidth, repeatCount, sleepDelay]


def quickTest():
    shortWake = '1' * 11 + '0101010111010'
    spacer = '0' * 48
    longWake = '1' * 10 + '0110101110101110111010'
    temp = shortWake + spacer + longWake
    dec = int(temp, 2)
    hexString = hex(dec)

    print(shortWake + f" : {str(len(shortWake))} bits")
    print(hex(int(shortWake, 2)))
    print('\n')

    print(spacer + f" : {str(len(spacer))} bits")
    print(hex(int(spacer, 2)))
    print('\n')

    print(longWake + f" : {str(len(longWake))} bits")
    print(hex(int(longWake, 2)))
    print('\n')

    print(temp + f" : {str(len(temp))} bits")
    print(hexString)


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
            commandDic[key] = cmd
        else:
            break
        
    print(f"\nWriting {fileName}")
    
    with open(fileName, 'w') as file:
        doc = yaml.dump(commandDic, file)
    
    print("exiting the program")
    