# Zora Project 
You can find a demo video at this [link](https://www.youtube.com)<br>
In this README you can find a step by step configuration to run the project, you need Python in a version greater than 3.8 and Choregraphe 2.1.4.
## Step 1: Environment configuration
1. Download the project  
    - git clone https://github.com/loriboi/zoraProject.git <br> 
    - cd zoraProject_SentenceClassification 
2. Creating an environment and installing the requirements, it will take a few minutes to download the models.<br>
    - python -m venv env
    ------------------------------
    ### Activate the environment
	#### On windows:
	- cd env/Scripts
	- activate
	#### On macOs:
	- cd env
	- source bin/activate
    ------------------------------	
    ### Install the requirements    
    - cd ..
	- cd server
	- pip install -r requirements.txt

## Step 2: Server side configuration and running
1. Open the 'server' folder, insert the OpenAI API key into the 'config.py' file.
2. Insert the PC's IP address into the 'hostName' variable within the 'server1.py', 'server2.py', 'server3.py', 'server4.py' files.
3. In 4 different terminals, activate the environment and open a server for each terminal using the command 'python serverX.py'."

**Now the servers are ready to perform their tasks.** <br>
*Note: you can easily find your IP address by using the 'ipconfig' command on Windows and 'ifconfig' on macOS*

## Step 3: Choregraphe side configuration and running
1. Open Choregraphe, select 'import project from CRG file', choose the file 'ZoraBotProject_SentenceClassification.crg', and import the file.
2. Change the 'url' variable with the IP inserted in the servers in the following blocks:
   - SpeechToText, SpeechToText(1), Decide
   - AskOrMove -> AskToGpt and modify url in the blocks AskToGPT and TalkAndMove.

**Now you can upload the program to the robot and start using the project.**   