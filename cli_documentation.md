
# CLI for Master Controller

This documentation provides information on how to use the command line interface (CLI) to interact with the master controller in the blockchain network.

## Usage

```
python cli.py <command> [arguments]
```

## Commands


### 1 Set Difficulty

**Command**: `difficulty`  
**Description**: Sets the mining difficulty for the nodes the blockchain.

**Arguments**:
- `difficulty` (int): The difficulty level for mining.

**Example**:
```sh
python mcli.py difficulty 4
```

### 2 Reset

**Command**: `reset`  
**Description**: Resets the blockchain with the existing difficulty.

**Example**:
```sh
python mcli.py reset
```

### 3 Post Transaction

**Command**: `transaction`  
**Description**: Posts a transaction to a specific node using its nickname.

**Arguments**:
- `sender` (str): The sender of the transaction.
- `recipient` (str): The recipient of the transaction.
- `amount` (int): The amount of the transaction.

**Example**:
```sh
python mcli.py transaction Alice Bob 100
```

### 4 Get Users

**Command**: `users`  
**Description**: Retrieves the list of users from the node.


**Example**:
```sh
python mcli.py users
```

### 5 Get Blockchain

**Command**: `chain`  
**Description**: Retrieves the full blockchain from the node.

**Example**:
```sh
python mcli.py chain
```

    