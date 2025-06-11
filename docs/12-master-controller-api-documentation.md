### Master Controller API Documentation

#### **Base URL:** 
```
http://<master_controller_address>
```

### **Endpoints**

#### 1. **Configure Master Controller**
```
POST /configure
```
**Description:**
Configures the master controller with the provided nodes, master controller URL, difficulty level, and broadcast flags.

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
  - Returns the updated configuration

#### 2. **Send Configuration to Nodes**
```
POST /send_configuration
```
**Description:**
Sends the current configuration to all the registered nodes.

**Response:**
- `200 OK`
  - `message`: "Configuration sent to all nodes"

#### 3. **Log Messages from Nodes**
```
POST /log
```
**Description:**
Receives and logs messages from nodes.

**Request Body:**
```json
{
    "message": "Log message"
}
```
**Response:**
- `200 OK`
  - `message`: "Log received"

#### 4. **Get Current Configuration**
```
GET /configuration
```
**Description:**
Returns the current configuration of the master controller.

**Response:**
- `200 OK`
  - Returns the current configuration

#### 5. **Get Registered Nodes**
```
GET /nodes
```
**Description:**
Returns the list of currently registered nodes.

**Response:**
- `200 OK`
  - `nodes`: List of registered nodes

#### 6. **Post Transaction to Specific Node**
```
POST /post_transaction/<node_nickname>
```
**Description:**
Posts a transaction to a specific node using its nickname.

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
- `200 OK`
  - `message`: "Transaction posted successfully"
- `404 Not Found`
  - `error`: "Node not found"
- `500 Internal Server Error`
  - `error`: "Error message"

### **Example Requests**

#### **Configure Master Controller**

**Request:**
```bash
curl -X POST http://localhost:5000/configure \
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
  "nodes": ["localhost:5001", "localhost:5002"],
  "master_controller": "localhost:5000",
  "difficulty": 4,
  "send_transactions": true,
  "send_blocks": true
}
```

#### **Send Configuration to Nodes**

**Request:**
```bash
curl -X POST http://localhost:5000/send_configuration
```

**Response:**
```json
{
  "message": "Configuration sent to all nodes"
}
```

#### **Log Messages from Nodes**

**Request:**
```bash
curl -X POST http://localhost:5000/log \
     -H "Content-Type: application/json" \
     -d '{
           "message": "[Node1] New block forged with index 2"
         }'
```

**Response:**
```json
{
  "message": "Log received"
}
```

#### **Get Current Configuration**

**Request:**
```bash
curl -X GET http://localhost:5000/configuration
```

**Response:**
```json
{
  "nodes": ["localhost:5001", "localhost:5002"],
  "master_controller": "localhost:5000",
  "difficulty": 4,
  "send_transactions": true,
  "send_blocks": true
}
```

#### **Get Registered Nodes**

**Request:**
```bash
curl -X GET http://localhost:5000/nodes
```

**Response:**
```json
{
  "nodes": ["localhost:5001", "localhost:5002"]
}
```

#### **Post Transaction to Specific Node**

**Request:**
```bash
curl -X POST http://localhost:5000/post_transaction/Node1 \
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
  "message": "Transaction posted successfully"
}
```

