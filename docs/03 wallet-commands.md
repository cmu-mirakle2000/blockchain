


### Step 1: Start Interactive Wallet


1. **Open a new Terminal window on your computer and start interactive shell**
   
   Switch to your project folder
      ```bash
      cd blockchain
      source venv/bin/activate
      ```

2. **Edit wallet.py and update the following line to match your node's URL**

   ```bash
     node_url = "http://127.0.0.1:8004"
   ```
3. **Start your interactive wallet** 
   ```bash
     python wallet.py
   ```

4. **You will see a prompt along with the network status**

      ```bash
      NodeName:single> 
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


