You can use the Wallet app to send commands to the server. 

### Step 1: Start Interactive Wallet


1. **Open a new Terminal window on your server and start interactive shell**

(You can also connect to a remote server from your laptop. You just need to clone the repository to your laptop as well and follow the deployment commands to get your virtual environment working)

   Switch to your project folder
      ```bash
      cd blockchain
      source venv/bin/activate
      ```

2**Start your interactive wallet** 
Specify the IP address and port number of your node server on the remote machine. 
   ```bash
     python wallet.py -i <ip-adress> -p <port>
   ```

4. **You will see a prompt along with the network status and IP details**

      ```bash
      NodeName@127.0.0.1:5000:single> 
      ```
   Type `help` to see a list of available commands. Every command has a single letter shortcut listed right after it. 

### Step 2: Run Wallet Commands

2. **Reset your blockchain and mine a genesis block (works only in Single mode)**
   
   It is important to do this before you do any of the following commands

      ```bash 
      reset
      ```
3. **See the current chain of blocks  (Works in Single and Network mode)**
      ```bash
      chain
      ```
4. **List current users and their wallets  (Works in Single and Network mode)**
      ```bash
      users
      ```
5. **Send money from your wallet. (Works in Single and Network mode)**

   Replace Recipient with name from the users list above
      ```bash
      send <Recipient> <Amount>
      send Joe John 10
      ```
   Send five transactions to mine a block. You can see the hashes being generated and validated by the proof of work function. 

6**Send money from ANY wallet (works only in Single mode).**

   Replace Sender and Recipient with names from the users list above
      ```bash
      transaction <Sender> <Recipient> <Amount>
      transaction Joe John 10
      ```
   Send five transactions to mine a block. You can see the hashes being generated and validated by the proof of work function. 

7**Change Difficulty (works only in Single mode)**
   
   After you change difficulty, the blockchain resets. Send new transactions to mine a block. Keep incrementing the difficulty until you see the proof of work take some meaningful time (5 to 10 seconds). 
      ```bash
      difficulty 2
      ```

You can reset the blockchain and rerun commands 3 to 6 any time. 


