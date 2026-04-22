COMP4137 Blockchain Technology and Applications
COMP7200 Blockchain Technology

Lecturer: Dr. Hong-Ning Dai (Henry)

Lecture 7
Permissionless blockchain 2



Outline

• Ethereum Block
• Patricia Trie

• Ethereum Consensus
• Ethereum DApps



Ethereum Block

• Block header

• Consensus data: parent hash, difficulty, PoW solution, etc

• Beneficiary: where TX fees will go (address)

• World state root (stateRoot): updated world state

• Merkle Patricia Tree hash of all accounts in the system

• TX Root (transactionRoot): Merkle hash of all TXs

included in block

• TX receipt root (receiptsRoot): Merkle hash of log

messages generated in block

• Gas used: Tells verifier how much work to verify block

Block

Header

List of Transactions

Ethereum block header

parentHash

beneficiary

difficulty

ommersHash

logsBloom

number

gasLimit

gasUsed

timestamp

nonce

mixHash

extraData

stateRoot

transactionsRoot

receiptsRoot

Ethereum account state

balance

storageRoot

nonce

codeHash



Ethereum Block

• Block header contains three Merkle trees for Transactions, Receipts and States

• Enable light clients to conduct various types of queries

• Has this transaction been included in a particular block? (transactionTree)

• Tell me all instances of an event of type X (e.g., a crowdfunding contract reaching its

goal) emitted by this address in the past Y days (ReceiptsTree)

• What is the current balance of my account? (stateTree)

• Does this account exist? (stateTree)



Why Patricia Trie

• A simple Merkle tree is good for proving that an item is part of a

static, ordered set (like the list of transactions in a block).
• However, Ethereum's world state is a massive key-value store
(address -> account data) that is constantly being updated.
• A simple Merkle tree is inefficient for lookups, insertions, and

modifications.

• PATRICIA=“Practical Algorithm To Retrieve Information Coded In

Alphanumeric”

• Patricia Trie* can be regarded as a special case of Radix Trie

* A trie is a specialized type of tree data structure optimized for storing and retrieving sequences, typically strings, based on shared prefixes.



Radix Trie

• How does Ethereum manage the storage with 256-bit address?

• Key-value pair

• Radix Trie: used for key-value pair storage management

do:0
dog:1
data:2
down:3
cat:4
cats:5

One possible child for each letter

Each path spells a key word

Value at end of path

Search time = key length

a

b

z

y

6



Radix Trie

Search for “dog”

do:0
dog:1
data:2
down:3
cat:4
cats:5

a

t

d

c

o

0

w

g

1

a

2

Search
successful,
result is 1

a

n

3

t

4

s

5

7



Radix Trie

Search for “can”

do:0
dog:1
data:2
down:3
cat:4
cats:5

a

2

a

t

d

c

o

0

w

g

1

Search failed,
no value
corresponds
to “can”

a

t

4

s

5

n

3

8



Radix Trie

Search for “to”

do:0
dog:1
data:2
down:3
cat:4
cats:5

a

2

a

t

d

c

o

0

w

g

1

Search failed, no result

a

n

3

t

4

s

5

9



Radix Trie

• Can we optimize the tree?

do:0
dog:1
data:2
down:3
cat:4
cats:5

a

t

d

c

o

0

w

g

1

a

n

3

t

4

s

5

a

2

10



Radix Trie

• Can we optimize the tree?
• Combine some edges

do:0
dog:1
data:2
down:3
cat:4
cats:5

Combine the edges

ata

2

d

o

0

g

1

cat

4

wn

3

s

5

Combine the edges

Combine the edges

11



Patricia Trie

• Patricia Trie

• It is an optimized Trie with lower tree height

• Features

• Efficient look up
• Short membership proof and non-membership proof

13



Patricia Trie

Extension Node

Leaf Node

Branch Node

14



Patricia Trie

Extension Node

Contains two elements:
•
Key: encode path
• Value: path of

following branch
node

0: 0000
1: 0001
2: 0010
3: 0011

15



Patricia Trie

Branch Node

Contain 17-
elements:
•

Point to the
next level

16



Patricia Trie

Leaf Node

Contains two elements:
•
Key: encode path
• Value: data of

account

17



Patricia Trie in Ethereum

• All Merkle Hash Trees in Ethereum use Merkle Patricia Trie
• Three types of tries

• State Trie

• include all accounts in ETH
• balance and storage

• Transaction Trie

• include Txs in this block

• Receipts Trie

• include transaction’s receipts
• such as logs and gas used

Ethereum block header
beneficiary

parentHash

ommersHash

logsBloom

timestamp

nonce

difficulty

number

mixHash

gasLimit

gasUsed

extraData

stateRoot

transactionsRoot

receiptsRoot

Ethereum account state

balance

storageRoot

nonce

codeHash

18



Outline

• Ethereum Block
• Patricia Trie

• Ethereum Consensus
• Ethereum DApps



Ethereum Consensus

• Initially, use PoW with faster block generation rate (~14s)
• In 2022, switch to PoS
• Faster block generation rate incurs more forks!

Which chain should
we choose?

20



Ethereum’s Main Chain Selection

• Greedy Heaviest Observed Sub-Tree (GHOST) protocol proposed by

Sompolinsky and Zohar in December 2013
• Ethereum uses a simpler version of GHOST

2D

1B

2C

2B

2A

1A

3F

3E

3D

3C

3B

3A

0

4C

4C

4B

Main chain according to
GHOST including Uncle
blocks (10 blocks)

4A

5A

6A

Main chain according
to the “longest” rule
(7 blocks)

21



Canonical chain

• A canonical chain is the primary, agreed-upon sequence of blocks in a

blockchain, recognized by nodes as the legitimate, authoritative
history.

• In Bitcoin, a canonical chain is determined by the "longest chain

rule"—the chain with the most accumulated Proof-of-Work
(cumulative difficulty)

• In Ethereum, , a canonical chain is determined from all potential forks

via its Proof-of-Stake (PoS) consensus mechanism

• Ethereum adopts the LMD-GHOST (Last Message Driven - Greedy

Heaviest Observed SubTree)



Canonical chain

• Ethereum adopts the LMD-GHOST to select the canonical chain

2D

1B

2C

2B

2A

1A

3F

3E

3D

3C

3B

3A

0

4C

4C

4B

Canonical chain

4A

5A

6A

Why?



Ethereum Block Reward

• Recall: Bitcoin only rewards the new block mined in the main chain

• Orphan blocks in Bitcoin don’t contribute to longest chain rule-based consensus
• In GHOST, orphan blocks (“uncles”) are counted when determining the

heaviest sub-tree

• Incentivize the honest-but-not-luck works

• Reward stale block miners and also miners who include stale block headers

• Rewarded stale blocks are called uncles or ommers
• Transactions in uncle blocks are invalid
• Only a fraction of block reward goes to uncle creator; no transaction fees

• Block = (Block Header, Transaction List, Uncle Header List)

• ommersHash in block header is hash of uncle header list

24



Example: Uncle Incentive in Ethereum

Block
Height 0

Block
Height 1

Block
Height 0

Block
Height 1

Block
Height 2

Stale Block in
Bitcoin

No reward

Block
Height 2

Block
Height 3

Block
Height 2

Uncle Block
in Ethereum

A fraction
of reward

Block
Height 2

Block
Height 3

More
reward

25



Ethereum Block Reward

• Normal Block Reward

• Intrinsic reward: 5 ETH (now reduced to 2 ETH)
• All transaction fees in the block
• If include uncle blocks, (5 ETH / 32 = 0.15625 ETH) for each uncle block

• Uncle Block Reward

• (Uncle height + 8 – height of block including this uncle) * intrinsic reward (5

ETH) / 8

26



Block Reward Examples

All transaction fees

Intrinsic reward
5 ETH

Include 2 uncles
(2*0.15625)

27



Block Reward Examples

Uncle height

Height of block including this uncle

(4222271 + 8 - 4222272) * 5 / 8 = 4.375 ETH

28



Ethereum Mining

• Ethash Proof of Work

• Keccak-256 (SHA3 variant)

• Memory-hard computation

• Memory-easy validation

• Cannot exploit ASIC

• Mining similar to Bitcoin

nonce = rand()

while (SHA3(block,nonce) * difficult > threshold

nonce++

return nonce

29



Ethereum Mining

• Difficulty adjustment

• After every block (vs. after 2016 blocks in bitcoin)

Block_diff = parent_diff +

parent_diff / 2048 *
max(1 - (block_timestamp - parent_timestamp) / 10,-99) +
int(2**((block.number / 100000) - 2))

•

If the difference (block_timestamp - parent_timestamp) is

■ < 10 secs, adjust upwards by parent_diff / 2048 * 1

■ 10 - 19 secs, unchanged

■ >= 20 seconds, adjust downwards from parent_diff/ 2048 *-1 to

parent_diff / 2048 * -99

30



Ethereum PoS Transition

•

Ethereum is moving to Proof of Stake (PoS) consensus (ETH 2.0 phase 1)

PoS does not incur huge computation resource and energy consumption

• Also reduce 51% attack and fast TX validation

Disadvantage: may be more centralized

• Miners become “validators” and deposit to an escrow account

• The more escrow a miner deposit, the higher chance it will be chosen to

mint next block

• Lose deposit if minting a block with invalid transactions

31



Outline

• Ethereum Block
• Patricia Trie

• Ethereum Consensus
• Ethereum DApps



DApp vs. Smart Contract

• DApp is a complete application containing

•

Front-end (e.g., GUI)

• Back-end (e.g., blockchain)

• Smart contract is only a part of DApp that interacts

with the blockchain

DApp

Smart
Contract



Dapp vs. Centralized App

Internet

Ethereum

Decentralized Web Application

Traditional Web Application

Client

Client

Front-end (HTML, CSS, JavaScript)

Execute

Smart Contract

EVM

Load/store state

Internet

Web
server

Front-end (HTML, CSS, JavaScript)

Interact

Back-end (JSP/ASP/PHP)

Load/store state

blockchain

DB



Building DApp

• Main principles to develop a DApp

• Develop Front-end: create app’s user interface

• Add library: to connect front-end with wallet and

blockchain
and send TXs

User’s wallet connect to the network

Front-end

library

• Write smart contract: contains your app’s core functions,
including anything that modifies user’s wallet “contents”

Smart
contract

• Deploy: deploy smart contract to the blockchain

•

Submit TX containing compiled smart contract without
specifying any recipients

Blockchain



Off-chain Storage

■ Sometime data is too large to store directly on blockchain

•

Increase block size, computation (validation) and storage overhead on blockchain
nodes

■ Solution: store data content off chain, and its hash and address on chain

• Example: IPFS, Swarm, Filecoin

1. upload

5. notification

DAPP

t
c
a
r
t
n
o
C
t
r
a
m
S

2. store
encrypted file

(hash, url)

TX

3. submit

4. validation &
confirmation

TX



Ethereum Smart Contract

• Programming language: Solidity

• Contract-oriented
• Syntax similar to Javascript

• A contract is similar to a class in Object Oriented Programming

• State variables
• Functions (methods)
• Events

• Types

• Integer
• String
• Array
• Mapping
• …

37



Example

• Let’s write a simplest form of a cryptocurrency using Solidity
• Requirement

• Anyone can transfer money to each other
• The minter can mint some money and transfer to others
• A sender cannot transfer money that exceeds the owned one (double

spending)

• There should be an event mechanism to notify the state changes

38



Example

• Components

• Public storage

• minter with address type
• balances with mapping (address => uint) type

• Function

• constructor: initialize the minter address
• mint(receiver, amount): minter mints some money

The require function call
defines conditions that reverts
all changes if not met

and transfers it to the receiver

• send(receiver, amount): the sender sends some

money to the receiver

• Event

This ensures that the sender
has enough money to transfer
to the receiver

• Sent(from, to, amount): log elements of from, to, and

amount

Emit an event after the
successful money transfer

39



Ethereum Smart Contract

• Solidity Documentation

• https://solidity.readthedocs.io/en/develop/index.html

• IDE

• A web-based IDE: https://remix.ethereum.org/

40



Applications Built on Ethereum

https://www.augur.net/

https://ethlance.com/

http://www.4g-capital.com/

https://golem.network/

http://www.ampliativeart.org/

41



Companies are starting to accept Ethers

42



Summary

• In Permissionless Blockchains, participation is open to the public with

a fully decentralized network.

• Ethereum is a decentralized platform that runs smart contracts or

dApps, without downtime, censorship, fraud or third party
interference.

• Smart contracts are executed on Ethereum Virtual Machine (EVM).
• Uncle Incentive: reward stale block miners and also miners who

include stale block headers

• Rewards for normal block and uncle block are different

• Each operation in a transaction execution costs some gas
• Main chain selection via GHOST protocol

43



Summary

• Ethereum accounts: Externally owned accounts and Contract

accounts

• Ethereum transactions: Contract creation transaction and Message

call transaction

• Altcoins are digital money created using encryption techniques with

public blockchain.

• Tokens are blockchain-based abstractions that can be owned and

represent assets, currency, or access rights.

• A company can raise funds to create a new coin, app, or service

through ICO.

44



References

• Mastering Ethereum, by Gavin Wood, Andreas M. Antonopoulos
• Ethereum White paper:

https://github.com/ethereum/wiki/wiki/White-Paper

• Ethereum Yellow paper:

https://ethereum.github.io/yellowpaper/paper.pdf

• Ethereum Wikipedia Article: https://en.wikipedia.org/wiki/Ethereum
• A Prehistory of the Ethereum Protocol:

https://vitalik.ca/general/2017/09/14/prehistory.html

• Ethereum announcement on Bitcointalk:

https://bitcointalk.org/index.php?topic=428589.0

45

