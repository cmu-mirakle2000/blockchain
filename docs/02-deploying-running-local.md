

### Step 1: Connect to Your Server

1. **Connect to your server**:

   - Open Terminal application on your computer
   - Use SSH to connect to your server
     ```bash
     # Example only. Use the appropriate command for your server
     ssh -i ~/labsuser.pem ec2-user@192.168.2.16
     ```

### Step 2: Set Up the Environment
1. **Update the package list and install required packages**:

You only need to do this once, but it doesn't hurt if you run it every time. 
   ```bash
   sudo yum install python3-pip python3 nginx git
   ```
   
2. **Install virtualenv**:
You only need to do this once, but it doesn't hurt if you run it every time. 
   ```bash
   sudo pip3 install virtualenv
   ```

### Step 3: Set Up the Flask Application
1. **Clone your Flask application repository**:
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

Replace `YourName` with your name from the `keys.json` file

For type, use `single` or `network`. For initial tests, use `single`. For running on a remote server, 
use the public IP address of the remote server. Make sure you opened the firewall for the port you choose. 
 
   ```bash
     cd app
     python node.py <type> <YourName> -i <ip-address> -p <port>
     # Example
     python node.py single John -i 127.0.0.1 -p 5000
   ```
