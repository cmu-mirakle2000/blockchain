
# CLI for Master Controller

This documentation provides information on how to use the command line interface (CLI) to interact with the master controller in the blockchain network.

## Usage

```
python cli.py <command> [arguments]
```

## Commands

### 1. Post Log

**Command**: `post_log`  
**Description**: Sends a log message to the master controller.

**Arguments**:
- `message` (str): The log message to send.

**Example**:
```sh
python cli.py post_log "This is a log message"
```

### 2. Add Node

**Command**: `add_node`  
**Description**: Adds a node to the configuration.

**Arguments**:
- `node` (str): The URL of the node to add.

**Example**:
```sh
python cli.py add_node "http://localhost:5001"
```

### 3. Set Difficulty

**Command**: `set_difficulty`  
**Description**: Sets the mining difficulty for the nodes.

**Arguments**:
- `difficulty` (int): The difficulty level for mining.

**Example**:
```sh
python cli.py set_difficulty 4
```

### 4. Configure

**Command**: `configure`  
**Description**: Sends the configuration to all nodes.

**Example**:
```sh
python cli.py configure
```

### 5. Post Transaction

**Command**: `post_transaction`  
**Description**: Posts a transaction to a specific node using its nickname.

**Arguments**:
- `nickname` (str): The nickname of the node.
- `sender` (str): The sender of the transaction.
- `recipient` (str): The recipient of the transaction.
- `amount` (int): The amount of the transaction.
- `signature` (str): The signature of the transaction.

**Example**:
```sh
python cli.py post_transaction Node1 Alice Bob 100 signature_hex
```

### 6. Get Users

**Command**: `get_users`  
**Description**: Retrieves the list of users from a specific node using its nickname.

**Arguments**:
- `nickname` (str): The nickname of the node.

**Example**:
```sh
python cli.py get_users Node1
```

### 7. Get Blockchain

**Command**: `get_chain`  
**Description**: Retrieves the full blockchain from a specific node using its nickname.

**Arguments**:
- `nickname` (str): The nickname of the node.

**Example**:
```sh
python cli.py get_chain Node1
```

### 8. Get Configuration

**Command**: `get_configuration`  
**Description**: Retrieves the current configuration of the master controller.

**Example**:
```sh
python cli.py get_configuration
```
