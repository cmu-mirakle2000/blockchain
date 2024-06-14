

### Step 1: Set up an EC2 Instance

1. **Connect to your EC2 instance**:

   - Open Terminal application on your computer
   - Use the following command to connect to your instance (change the IP address):
     ```bash
     ssh -i ~/labsuser.pem ec2-user@192.168.2.16
     ```

### Step 2: Set Up the Environment
1. **Update the package list and install required packages**:
   ```bash
   sudo yum install python3-pip python3 nginx git
   ```
   
2. **Install virtualenv**:
   ```bash
   sudo pip3 install virtualenv
   ```

### Step 3: Set Up the Flask Application
1. **Clone your Flask application repository or create a new one**:
   ```bash
   git clone https://github.com/cmu-mirakle2000/blockchain.git
   cd blockchain
   ```

2. **Create and activate a virtual environment**:
   ```bash
   virtualenv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Run Your Node

Replace `YourName` with a name from the `keys.json` file

   ```bash
     cd app
     python node.py <YourName>
   ```

### Step 5: Test with the CLI



1. **Open a new Terminal window on your computer**
   
   Use the following command to connect to your instance (change the IP address):
     ```bash
     ssh -i ~/labsuser.pem ec2-user@192.168.2.16
     ```
   Switch to your project folder
      ```bash
      cd blockchain
      ```
2. **Reset your blockchain and mine a genesis block**
      ```bash 
      python cli.py reset
      ```
3. **See the current chain of blocks**
      ```bash
      python cli.py chain
      ```
4. **List current users**
      ```bash
      python cli.py users
      ```
5. **Send transactions to the blockchain.**

   Replace Sender and Recipient with names from the users list above
      ```bash
      python cli.py transaction <Sender> <Recipient> 4
      ```
   Send five transactions to mine a block. You can see the hashes being generated and validated by the proof of work function. 

6. **Change Difficulty**
   
   After you change difficulty, the blockchain resets. Send new transactions to mine a block. Keep incrementing the difficulty until you see the proof of work take some meaningful time (5 to 10 seconds). 
      ```bash
      python cli.py difficulty 2
      ```

   


