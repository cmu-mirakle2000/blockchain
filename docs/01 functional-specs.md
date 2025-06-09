### Blockchain Project Functional Requirements Document

#### Introduction

This document outlines the functionality of a blockchain project designed to implement a simple, distributed blockchain network. The network consists of nodes that can mine blocks, process transactions, and communicate with each other to maintain a consistent blockchain.

#### Functional Overview

The project includes the following key component:

1. **Blockchain Node**

#### 1. Blockchain Node

Each node in the network has the following functionalities:

- **Mining Blocks**
  - Nodes can perform proof-of-work calculations to mine new blocks.
  - The first block (genesis block) can be created by a designated node upon request.
  - Nodes broadcast newly mined blocks to other nodes.

- **Transaction Processing**
  - Nodes process transactions by verifying the sender's balance and signature.
  - Nodes can receive new transactions and add them to a pool of current transactions.
  - Nodes broadcast new transactions to other nodes.
  - Reward transactions from mining are exempt from signature verification and are sent by a special user called "Bank".

- **Communication**
  - Nodes can register with each other to form a network.
  - Nodes receive and validate blocks from other nodes.
  - Nodes receive and validate transactions from other nodes.
  - Nodes reset their blockchain and configuration based on commands from the master controller.

#### Detailed Functional Requirements

**1. Mining Blocks**

- **Proof-of-Work**
  - Each node can mine blocks by performing proof-of-work calculations.
  - The proof-of-work algorithm involves finding a nonce such that the hash of the block's data (including the nonce) has a certain number of leading zeros, determined by the difficulty level.
  - Upon finding a valid nonce, the node creates a new block and broadcasts it to the network.
  - The node is rewarded with a transaction from "Bank" to itself for successfully mining the block.

- **Genesis Block Creation**
  - The genesis block is the first block in the blockchain and is created by a designated node upon request.
  - The genesis block has a predefined previous hash and proof value.

**2. Transaction Processing**

- **Transaction Structure**
  - Each transaction includes the sender, recipient, amount, and a signature to verify authenticity.
  - The sender's public key is used to verify the signature.

- **Transaction Verification**
  - Nodes verify that the sender has sufficient balance before processing a transaction.
  - Nodes verify the transaction signature using the sender's public key.
  - Reward transactions from mining are exempt from signature verification and are sent by the "Bank" user.

- **Transaction Handling**
  - Nodes add valid transactions to the pool of current transactions.
  - Transactions are included in the next block to be mined.
  - Nodes broadcast new transactions to other nodes.

**3. Communication**

- **Node Registration**
  - Nodes can register with each other to form a network.
  - Each node maintains a list of registered nodes.

- **Block Broadcasting**
  - When a node mines a new block, it broadcasts the block to all registered nodes.
  - Nodes receiving a new block validate the block and add it to their blockchain if valid.
  - Nodes stop their mining process upon receiving a valid new block from another node.

- **Transaction Broadcasting**
  - When a node receives a new transaction, it broadcasts the transaction to all registered nodes.
  - Nodes validate and add the transaction to their current transaction pool if valid.

- **Blockchain and Configuration Reset**
  - Nodes can reset their blockchain and configuration based on commands from the master controller.
  - The reset includes clearing the current blockchain and transactions, and reconfiguring the node network and difficulty level.

**4. Configurability**

- **Node Configuration**
  - Nodes can be configured with a list of other nodes, the master controller address, and the mining difficulty level.
  - Configuration can be updated dynamically based on commands from the master controller.

- **Mining Difficulty**
  - The mining difficulty level determines the number of leading zeros required in the hash of the block's data.
  - Higher difficulty levels make mining more computationally intensive.

- **Master Controller Integration**
  - Nodes can receive configurations from a master controller, including the list of other nodes and the mining difficulty level.
  - Nodes can send log messages and status updates to the master controller.

**Blockchain Node API Endpoints**

1. **GET /mine**
   - Mines a new block if the proof-of-work is successful.
   - Creates a reward transaction from "Bank" to the node.

2. **POST /transactions/new**
   - Receives a new transaction, validates it, and adds it to the current transaction pool.

3. **GET /chain**
   - Returns the full blockchain.

4. **GET /users**
   - Returns the list of users and their balances.

5. **POST /configure**
   - Configures the node with a new list of nodes, master controller address, and mining difficulty.
   - Resets the blockchain.

6. **POST /blocks/new**
   - Receives a new block from another node and validates it.

7. **POST /create_genesis**
   - Creates the genesis block and broadcasts it to other nodes.

**Behavioral Details**

- **Genesis Block Handling**
  - The genesis block is created by a designated node upon request.
  - It is the first block in the blockchain with a predefined previous hash and proof value.
  - The creation of the genesis block is a one-time event that initializes the blockchain.

- **Transaction Flow**
  - Transactions are initiated by users and include the sender, recipient, amount, and signature.
  - Nodes verify transactions by checking the sender's balance and validating the signature.
  - Valid transactions are added to the current transaction pool and broadcasted to other nodes.
  - Transactions are included in the next mined block and removed from the pool.

- **Block Mining and Broadcasting**
  - Nodes mine blocks by performing proof-of-work calculations.
  - Upon successfully mining a block, a reward transaction from "Bank" to the node is created.
  - The mined block is broadcasted to all registered nodes.
  - Nodes receiving a new block validate it, add it to their blockchain, and stop their mining process if it was active.

- **Network Communication**
  - Nodes register with each other to form a network.
  - Nodes exchange blocks and transactions to maintain a consistent blockchain.
  - Nodes can dynamically update their configuration based on commands from the master controller.

- **Configurability**
  - Nodes can be configured with a new list of nodes, master controller address, and mining difficulty level.
  - Configuration updates reset the blockchain and current transactions.
  - Nodes can adapt to changes in the network and maintain consistent operations.

#### Conclusion

This document provides a detailed description of the functionality required to implement the described blockchain project. Each component, endpoint, and behavior has been outlined to facilitate the development of similar projects.