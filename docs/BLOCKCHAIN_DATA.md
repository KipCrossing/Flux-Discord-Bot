# Blockchain data

_This section is under CONSTRUCTION_

This is an explination of

The contense of the block include:

- **Block Hash** - Calculated (see below))
- **BlockNo** - The number of the block, Itteraied starting at 1
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
- **RECEIVER_ID** - The ID to the issue, made up of `"server_id-channel_id-message_id"`
- **TRANSFER_AMOUNT** - 0 - As no PC should be transferred in a simple vote

### NOTE = "NO"

- **SENDER_ID** - The ID of the voter
- **RECEIVER_ID** - The ID to the issue
- **TRANSFER_AMOUNT** - 0

### NOTE =

- **SENDER_ID** -
- **RECEIVER_ID** -
- **TRANSFER_AMOUNT** -

### NOTE =

- **SENDER_ID** -
- **RECEIVER_ID** -
- **TRANSFER_AMOUNT** -

### NOTE =

- **SENDER_ID** -
- **RECEIVER_ID** -
- **TRANSFER_AMOUNT** -

### NOTE =

- **SENDER_ID** -
- **RECEIVER_ID** -
- **TRANSFER_AMOUNT** -
