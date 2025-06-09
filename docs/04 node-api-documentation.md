### Node API Documentation

#### **Base URL:** 
```
http://<node_address>
```

### **Endpoints**

#### 1. **Mine a Block**
```
GET /mine
```
**Description:**
Starts the mining process on the node. However, the actual mining is handled automatically when a threshold of transactions is reached.

**Response:**
- `200 OK`
  - `message`: "Mining is handled automatically"

#### 2. **Create a New Transaction**
```
POST /transactions/new
```
**Description:**
Creates a new transaction to be added to the next mined block.

**Request Body:**
```json
{
    "sender": "Sender's Name",
    "recipient": "Recipient's Name",
    "amount": Amount,
    "signature": "Signature in Hex"
}
```
**Response:**
- `201 Created`
  - `message`: "Transaction will be added to Block <index>"
- `400 Bad Request`
  - `message`: "Missing values"

#### 3. **Add a New Block**
```
POST /blocks/new
```
**Description:**
Adds a new block to the blockchain.

**Request Body:**
```json
{
    "block": {
        "index": Block Index,
        "timestamp": Timestamp,
        "transactions": Transactions,
        "proof": Proof,
        "previous_hash": "Previous Block Hash",
        "merkle_root": "Merkle Root"
    },
    "sender": "Sender Node Nickname"
}
```
**Response:**
- `201 Created`
  - `message`: "Block has been added"
- `400 Bad Request`
  - `message`: "Missing values"

#### 4. **Register Nodes**
```
POST /nodes/register
```
**Description:**
Registers new nodes to the blockchain network and configures the node with the master controller, difficulty, and broadcast flags.

**Request Body:**
```json
{
    "nodes": ["Node1 Address", "Node2 Address", ...],
    "master_controller": "Master Controller Address",
    "difficulty": Difficulty Level,
    "send_transactions": true,
    "send_blocks": true
}
```
**Response:**
- `200 OK`
  - `message`: "Nodes registered"
- `400 Bad Request`
  - `message`: "Error: Please supply a valid list of nodes, master controller, and difficulty"

#### 5. **Get Blockchain**
```
GET /chain
```
**Description:**
Returns the full blockchain.

**Response:**
- `200 OK`
  - `chain`: The entire blockchain
  - `length`: Length of the blockchain

#### 6. **Get Users**
```
GET /users
```
**Description:**
Returns the list of users and their balances.

**Response:**
- `200 OK`
  - `users`: List of users and their balances

### **Example Requests**

#### **Create a New Transaction**

**Request:**
```bash
curl -X POST http://localhost:5000/transactions/new \
     -H "Content-Type: application/json" \
     -d '{
           "sender": "Alice",
           "recipient": "Bob",
           "amount": 5,
           "signature": "3045022100e99baf2e1f58d...0ed5d4825f"
         }'
```

**Response:**
```json
{
  "message": "Transaction will be added to Block 2"
}
```

#### **Add a New Block**

**Request:**
```bash
curl -X POST http://localhost:5000/blocks/new \
     -H "Content-Type: application/json" \
     -d '{
           "block": {
             "index": 2,
             "timestamp": 1623456789,
             "transactions": [],
             "proof": 12345,
             "previous_hash": "1a2b3c4d5e6f7g8h9i0j",
             "merkle_root": "123abc456def789ghi"
           },
           "sender": "Node1"
         }'
```

**Response:**
```json
{
  "message": "Block has been added"
}
```

#### **Register Nodes**

**Request:**
```bash
curl -X POST http://localhost:5000/nodes/register \
     -H "Content-Type: application/json" \
     -d '{
           "nodes": ["localhost:5001", "localhost:5002"],
           "master_controller": "localhost:5000",
           "difficulty": 4,
           "send_transactions": true,
           "send_blocks": true
         }'
```

**Response:**
```json
{
  "message": "Nodes registered"
}
```

#### **Get Blockchain**

**Request:**
```bash
curl -X GET http://localhost:5000/chain
```

**Response:**
```json
{
  "chain": [...],
  "length": 3
}
```

#### **Get Users**

**Request:**
```bash
curl -X GET http://localhost:5000/users
```

**Response:**
```json
{
  "users": {
    "Alice": {
      "balance": 995,
      "private_key": "-----BEGIN EC PRIVATE KEY-----...",
      "public_key": "-----BEGIN PUBLIC KEY-----..."
    },
    "Bob": {
      "balance": 1005,
      "private_key": "-----BEGIN EC PRIVATE KEY-----...",
      "public_key": "-----BEGIN PUBLIC KEY-----..."
    }
  }
}
```

This documentation provides a detailed guide on how to interact with the node's API, including endpoint descriptions, request and response formats, and example requests.