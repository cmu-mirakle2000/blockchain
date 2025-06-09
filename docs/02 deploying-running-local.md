

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

Replace `YourName` with your name from the `keys.json` file

For type, use `single` or `network`. For initial tests, use `single`
 
   ```bash
     cd app
     python node.py <type> <YourName>
   ```
