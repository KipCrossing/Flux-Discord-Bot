# Blockchain data

This is an explanation of how the Block-chain is setup and the Data that is contained within each block. 

The content of the block include:

- **Block Hash** - Calculated (see below))
- **BlockNo** - The number of the block, Iterated starting at 1
- **Block Data** - The voting data (see below)
- **Nonce** - Number of attempts during mining
- **Timestamp** - The time the block was created

## Block Hash

Each block is hashed using the following string:

```python
def hash(self):
    h = hashlib.sha256()
    h.update(
        str(self.previous_hash).encode('utf-8') +
        str(self.blockNo).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.nonce).encode('utf-8') +
        str(self.timestamp).encode('utf-8')
    )
    return h.hexdigest()
```

## Voting Data

The voting data is a _string_ in the form of a list of dictionaries where each dictionaries represents a single voting transaction. each transaction dictionary has 4 fields with the following keys:

- SENDER_ID
- RECEIVER_ID
- TRANSFER_AMOUNT
- NOTE

Depending on the note, the utility of the the first 3 fields varies according to the following:

### NOTE = "YES"

- **SENDER_ID** - The ID of the voter
- **RECEIVER_ID** - The ID of the issue, made up of `"server_id-channel_id-message_id"`
- **TRANSFER_AMOUNT** - 0 - As no PC should be transferred in a simple vote

### NOTE = "NO"

- **SENDER_ID** - The ID of the voter
- **RECEIVER_ID** - The ID of the issue, made up of `"server_id-channel_id-message_id"`
- **TRANSFER_AMOUNT** - 0

### NOTE = "CONVERT"

- **SENDER_ID** - The ID of the voter
- **RECEIVER_ID** - The ID of the issue, made up of `"server_id-channel_id-message_id"`
- **TRANSFER_AMOUNT** - 0

### NOTE = "TRANSFER"

- **SENDER_ID** - The ID of the Server
- **RECEIVER_ID** - The ID of the voter
- **TRANSFER_AMOUNT** - Amount of PC to transfer

### NOTE = "Y-`server_id-channel_id-message_id`

- **SENDER_ID** -
- **RECEIVER_ID** - The ID of the Server
- **TRANSFER_AMOUNT** - Amount of PC to transfer

### NOTE = "N-`server_id-channel_id-message_id`

- **SENDER_ID** - The ID of the voter
- **RECEIVER_ID** - The ID of the Server
- **TRANSFER_AMOUNT** - Amount of PC to transfer

### NOTE = "START"

- **SENDER_ID** - The ID of the issue, made up of `"server_id-channel_id-message_id"`
- **RECEIVER_ID** - The ID of the Server
- **TRANSFER_AMOUNT** - 0

### NOTE = "END"

- **SENDER_ID** - The ID of the issue, made up of `"server_id-channel_id-message_id"`
- **RECEIVER_ID** - The ID of the Server
- **TRANSFER_AMOUNT** - 0
