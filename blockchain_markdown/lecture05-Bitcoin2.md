COMP4137 Blockchain Technology and Applications
COMP7200 Blockchain and Cryptocurrencies

Lecturer: Dr. Hong-Ning Dai (Henry)

Lecture 5
Bitcoin Details



Outline

• Bitcoin Block Format

• Header
• Body

• Bitcoin Consensus

• Mining
• Target Threshold
• Bitcoin Transactions
• Transaction Format
• Script

• Bitcoin’s variants

COMP4137/COMP7200

Page 2



Cryptocurrency

• Over 2000 cryptocurrencies at the moment

COMP4137/COMP7200

Page 3



What is Bitcoin?

• Cryptocurrency
• Open source
• Decentralized network

COMP4137/COMP7200

Page 4



Cryptocurrency Transaction Workflow

1. Request Bob’s address

2. Send Bob’s address

Alice

Bob

Cryptocurrency Network

COMP4137/COMP7200

Page 5



Decentralization Challenges

• Counterfeiting
• Currency creation rules
• Double spending

• Alice pays Bob n digital coins for a cake
• Alice uses the same n digital coins to pay Charlie for a book

Alice

Bob

Charlie

Solution without a central coordinator?

Page 6



The Blockchain

• Blockchain: A public ledger (database) to store all transactions which

is replicated by many network nodes

• Header and Body

Hash chain of blocks

prev: H(  )

trans: H(  )

prev: H(  )

trans: H(  )

prev: H(  )

trans: H(  )

H(  )   H(  )

Hash tree (Merkle tree) of
transactions in each block

H(  )   H(  )

H(  )   H(  )

How are blocks linked?

transaction

transaction

transaction

transaction

COMP4137/COMP7200

Page 7



Bitcoin Block Format

Version Number

Hash of Previous
Block Header

Hash of
Transactions
Timestamp
Threshold
Nonce

Block Header Fields

Block Header

Number of
Transactions n

Coinbase
Transaction

Regular
Transaction 1

Regular
Transaction 2

…

Regular
Transaction n − 1

• Hash = Output of cryptographic hash function

COMP4137/COMP7200

Page 8



Block Header

nVersion
hashPrevBlock
hashMerkleRoot
nTime
nBits
nNonce

4 bytes
32 bytes
32 bytes
4 bytes
4 bytes
4 bytes

80 bytes

Previous Block Header

Current Block Header

nVersion
hashPrevBlock
hashMerkleRoot
nTime
nBits
nNonce

Double
SHA-256

nVersion
hashPrevBlock
hashMerkleRoot
nTime
nBits
nNonce

SHA256(SHA256(header))

COMP4137/COMP7200

Page 9



Cryptographic Hash Functions (CHF)

• Easy to compute but difficult to invert
• Collision-resistant
• Pseudorandom outputs
• SHA-256 = NIST approved CHF with 256-bit outputs

Input
july0
july1
july2
july3
july4
july5
july6
july7
july8
july9

SHA-256 Output
171c9f5053d5d675d1d1ed477c908e98498e6751ae392a78807c3cd6ad6975fa
7d8033d140d8b8db8324753a25c5e32ee4faa9c4e306bddb317907be51cd8a24
bda0b2ab2c7d654589b32f46a548cba27b7371f27b070ddd7d3b87122a078f06
dfa3569a46b1a13c24c9f385da140f4763a3fbb70f8eebe0f29ba535145d32ca
27d39d26edc54c11cc78d17bf0dd294413300dd004127fa6dcff368ea74bb87c
a0ebd3e23823fc291b090abd2eb1403912be6b72398f3bf4e92c4ec555902d53
dc7d6bcc266af402e53b9fb978b6579940bb97743f6e975a988cb20d903e0c5f
984906fbbaa7dbad2ee01a81df7a237bfdb63aeb06b4cf97a89fc004542c1dab
7be4d491b73a4797304980070d5b5fb5c7fd6921e70efc7ce38023c50664803d
e8c4af8895bcddb9cea3e3e1e8a08e090690bb55fd6617da5aa0873f27e218ee

• Hex digits: 0 = 0000,1 = 0001,2 = 0010,..., a = 1010, b = 1011, c = 1100,...,

e = 1110, f = 1111

• At a billion outputs per second, 78 billion years required to calculate 2100 outputs

COMP4137/COMP7200

Page 10



Merkle Root in Block Header

• hashMerkleRoot contains root hash of transaction Merkle tree
• Modifying any transaction will modify the block header

nVersion
hashPrevBlock
hashMerkleRoot
nTime
nBits
nNonce

h = H (h0 || h1)

h0 = H (h00 || h01)

h1 = H (h10 || h10)

h00 = H (t0)

h01 = H (t1)

h10 = H (t2)

h11

t0

t1

t2

COMP4137/COMP7200

Page 11



Hashcash

• A database you own where anyone in the world can add entries?

• Your email inbox

• Hashcash was proposed in 1997 to prevent spam
• Protocol

1. Suppose an email client wants to send email to an email server
Client and server agree upon a cryptographic hash function H

2. Server sends the client a challenge string c and an integer k
3. Client needs to find a string r s.t. H(c||r) begins with k zeros

Email Client

1. Request to send an email

Email Server

2. Send challenge c and integer k

3. Search for r

4. Send response r and an email

5. Verify that H(c||r)
begins with k zeros

• The r is considered proof-of-work (PoW)
• Difficult to generate but easy to verify

COMP4137/COMP7200

Page 12



Hashcash Proof of Work

• Public Challenge: c

SHA256

• Goal: Find nonce r s.t. H(c||r) =

00 ⋯ 00
𝑘

1 ⋯ ⋯ ⋯

• The probability to find such nonce

Pr first 𝑘 bits of H(c||r) are zeros =

1
2𝑘



Outline

• Bitcoin Block Format

• Header
• Body

• Bitcoin Consensus

• Mining
• Target Threshold
• Bitcoin Transactions
• Transaction Format
• Script

• Bitcoin’s variants

COMP4137/COMP7200

Page 14



Bitcoin Mining

• Mining = Process of adding new blocks to the blockchain
• Nodes perform transactions and broadcast them
• Miners collect some of these transactions into a candidate block

Block Header
Number of

Transactions n

Coinbase Transaction

Regular

Transaction 1
Regular

Transaction 2
…

Regular

Transaction n − 1

Version Number

Hash of Previous

Block Header

Hash of

Transactions

Timestamp

Threshold

Nonce

Block Header Fields

• Threshold encodes a 256-bit value like
• Miner who can find Nonce such that
can add a new block.

0x 00 ⋯ 00

FFFF … FFFFF
48
SHA256(SHA256(VersionNumer ∥ ⋯ ∥ Nonce

16

Candidate Block Header

)) ≤ Threshold

COMP4137/COMP7200

Page 15



Mining is Hard

Target value T

Fraction of Double SHA256’s output ≤ T

0x7 FFFF … FFFFF

63

0x0 FFFF … FFFFF

63

0x 00 ⋯ 00

16

FFFF … FFFFF
48

1
2
1
16
1
264

[0 … 7] → 8
16
1
24
1
24∗16

Pr[DoubleSHA256′s output ≤ T)] ≈

𝑇 + 1
2256

COMP4137/COMP7200

Page 16



Genesis Block (Raw Hex Version)

00000000   01 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ................
00000010   00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00 ................
00000020   00 00 00 00 3B A3 ED FD 7A 7B 12 B2 7A C7 2C 3E ....;£íýz{.²zÇ,>
00000030   67 76 8F 61 7F C8 1B C3  88 8A 51 32 3A 9F B8 AA gv.a.È.ÃˆŠQ2:Ÿ¸ª
00000040   4B 1E 5E 4A 29 AB 5F 49  FF FF 00 1D 1D AC 2B 7C  K.^J)«_Iÿÿ...¬+|
00000050   01 01 00 00 00 01 00 00  00 00 00 00 00 00 00 00   ................
00000060   00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ................
00000070   00 00 00 00 00 00 FF FF FF FF 4D 04 FF FF 00 1D   ......ÿÿÿÿM.ÿÿ..
00000080   01 04 45 54 68 65 20 54  69 6D 65 73 20 30 33 2F   ..EThe Times 03/
00000090   4A 61 6E 2F 32 30 30 39  20 43 68 61 6E 63 65 6C   Jan/2009 Chancel
000000A0   6C 6F 72 20 6F 6E 20 62  72 69 6E 6B 20 6F 66 20   lor on brink of
000000B0   73 65 63 6F 6E 64 20 62  61 69 6C 6F 75 74 20 66   second bailout f
000000C0   6F 72 20 62 61 6E 6B 73  FF FF FF FF 01 00 F2 05   or banksÿÿÿÿ..ò.
000000D0   2A 01 00 00 00 43 41 04  67 8A FD B0 FE 55 48 27   *....CA.gŠý°þUH'
000000E0   19 67 F1 A6 71 30 B7 10  5C D6 A8 28 E0 39 09 A6   .gñ¦q0·.\Ö¨(à9.¦
000000F0   79 62 E0 EA 1F 61 DE B6  49 F6 BC 3F 4C EF 38 C4   ybàê.aÞ¶Iö¼?Lï8Ä
00000100   F3 55 04 E5 1E C1 12 DE  5C 38 4D F7 BA 0B 8D 57   óU.å.Á.Þ\8M÷º..W

header

body

Explanation (in the next page)

COMP4137/COMP7200

Page 17



Genesis Block Header Explained

• nVersion: 01 00 00 00 (= 00 00 00 01, little endian)
• hashPrevBlock:

00000000000000000000000000000000000000000
00000000000000000000000 (why?)

• hashMerkleRoot:

3BA3EDFD7A7B12B27AC72C3E67768F617FC81B
C3888A51323A9FB8AA4B1E5E4A

• nTime: 29 AB 5F 49

• (= 49 5F AB 29 = 123100650510, little endian)

• nBits: FF FF 00 1D
• nNonce: 1D AC 2B 7C (= 208323689310, little endian)

COMP4137/COMP7200

Page 18



Big Endian vs Little Endian

• Endian-ness is about byte ordering.

• It means the way that a machine (we mean the entire computer architecture)

orders the bytes.

E.g., Intel

little endian

Small value in
small address

A 4-byte integer with
hex. value:
89ABCDEF

E.g., SPARC

big endian

Small value in
large address

0

EF

1

CD

2

AB

3

89

0

89

1

AB

2

CD

3

EF

small address

large address

small address

large address

COMP4137/COMP7200

Page 19



Miner’s Incentive

• Block Reward

1. Block Subsidy: each block contains a coinbase transaction,

which creates 6.25 BTC
• Each miner specifies his own address as the destination of the new coins
• Every miner is competing to solve their own PoW puzzle

2. Transaction fee: miners also collect transaction fees in the block

COMP4137/COMP7200

Page 20



Mining Farms

• Mining farms have thousands of mining rigs
• Each mining rig has dozens of mining chips
• Each chip has dozens of SHA256 mining cores
• Farms are located in places with cheap power and cooling

COMP4137/COMP7200

Page 21



Block Addition Workflow

• Nodes broadcast transactions
• Miners accept valid transactions and reject invalid ones (solves double spending)
• Miners try to extend the latest block

· · ·

Block
A

Block
B

Candidate
Block C1

Candidate
Block C2

Candidate
Block C3

• Miners compete to solve the search puzzle and broadcast solutions
• Unsuccessful miners abandon their current candidate blocks and start work on

new ones

· · ·

Block
A

Block
B

Candidate
Block C1

Candidate
Block C2

Candidate
Block C3

Candidate
Block D1

Candidate
Block D2

Candidate
Block D3

COMP4137/COMP7200

Page 22



What if two miners solve the puzzle at the same time?

• Both miners will broadcast their solutions on the network
• Nodes will accept the first solution they hear and reject others

A

A

MA

A

A

A

A

B

B

B

B

B

MB

···

Block
N − 1

Block
N

B

B

Block
N + 2

Block
N + 1

Block
B

Blockchain fork

COMP4137/COMP7200

Page 23



What if two miners solve the puzzle at the same time?

Block
N + 1

Block
N + 2

Block
N + 3

Switch to
this branch

···

Block
N − 1

Block
N

Block
B

Block
B’

Stale blocks

• Nodes always switch to the longest branch they become aware of
• Eventually the network will converge and achieve consensus
• This is called proof-of-work (PoW) consensus

COMP4137/COMP7200

Page 24



How often are new blocks created?

• Once every 10 minutes

nVersion
hashPrevBlock
hashMerkleRoot
nTime
nBits
nNonce

• Every 2016 blocks, the target T is recalculated
• Let tsum = Number of seconds taken to mine last 2016 blocks, then the target 𝑇new

𝑇new =

𝑡sum
2016 × 10 × 60

× 𝑇

• Recall that probability of success in single try is  𝑇+1
2256
4
• If tsum = 2016 × 8 × 60, then  𝑇new =
× 𝑇
5
6
• If tsum = 2016 × 12 × 60, then 𝑇new =
5

× 𝑇

COMP4137/COMP7200

Page 25



The Bitcoin P2P Network

• Three types of nodes

• Full Node

• A full node stores a copy of blockchain on their local storage

• Miner

• A miner is a full node that takes part in adding blocks to the

blockchain

• Simple Payment Verification (SPV) Node
• A SPV node only stores the block header
• They contact full nodes when additional information about

transactions is required

COMP4137/COMP7200

Page 26



Bitcoin Blockchain Explorers

• Web interfaces to view current blockchain state

• https://www.blockstream.info
• https://www.blockchain.com/explorer
• https://btc.com/

• Demo checklist

• Address generation at https://www.bitaddress.org
• Brainwallet generation at https://brainwalletx.github.io

COMP4137/COMP7200

Page 27



Bitcoin Supply

• The block subsidy was initially 50 BTC per block
• Halves every 210,000 blocks ≈ 4 years

• 25 BTC in Nov 2012, 12.5 BTC in July 2016, and 6.25 BTC in May 2020

• Total Bitcoin supply is 21 million

15,000,000

10,000,000

i

d
e
n
m
s
n
o
c
t
i
b

i

f
o

r
e
b
m
u
N

5,000,000

• The last bitcoin will be mined in 2140

0
9
0
0
2
n
a
J

0
1
0
2
y
a
M

1
1
0
2
t
p
e
S

3
1
0
2
b
e
F

4
1
0
2
n
u
J

5
1
0
2
v
o
N

7
1
0
2
r
a
M

8
1
0
2
g
u
A

COMP4137/COMP7200

Page 28



Blockchain – A High-level View

A

C

B

D

Distributed ledger

Alice pays Bob 3 BTC

Bob pays Chris 2 BTC

Eve pays Alice 5 BTC
…

Applications

Data structure

Consensus

COMP4137/COMP7200

Page 29



Bitcoin Testnet Transactions

• Each cryptocurrency has a mainnet and one or more testnets
• Bitcoin Testnet

• https://live.blockcypher.com/btc-testnet/

• Testnet Address Generator

• https://bitcoinpaperwallet.com/bitcoinpaperwallet/generate-

wallet.html?design=alt-testnet

• Testnet faucet 1

• https://coinfaucet.eu/en/btc-testnet/

• Testnet faucet 2

• https://bitcoinfaucet.uo1.net

• Mycelium Testnet Wallet Mobile APP

COMP4137/COMP7200

Page 30



Bitcoin P2P network

• Ad-hoc protocol (runs on TCP port 8333)
• Ad-hoc network with random topology
• All nodes are equal
• New nodes can join at any time
• Forget non-responding nodes after 3 hr

COMP4137/COMP7200

Page 31



Joining the Bitcoin P2P network

1

Hello World! I’m
ready to Bitcoin!

5

6

8

4

3

7

2

COMP4137/COMP7200

Page 32



Transaction propagation (flooding)

1

A→B

6
A→B

8

4
A→B

5

Already
heard that!

7
A→B

A→B

A→B

New tx!
A→B

3
A→B

A→B

A→B

2
A→B

COMP4137/COMP7200

Page 33



Should I relay a proposed transaction?

• Transaction valid with current block chain (default)
• Run script for each previous output being redeemed

•

and ensure that script returns true!
Script matches a whitelist
• Avoid unusual scripts
• Haven’t seen before
• Avoid infinite loops

Sanity checks only...
Well-behaving nodes implement them!
Some nodes may ignore them!

• Doesn’t conflict with others I’ve relayed

• Avoid double-spends

COMP4137/COMP7200

Page 34



Nodes may differ on transaction pool

New tx!
A→C

A→C

5
A→C

A→B

7
A→B

2
A→B

3
A→B

1
A→C

A→B

A→C

8
A→B

A→C

6
A→B

4
A→B

COMP4137/COMP7200

Page 35



Outline

• Bitcoin Block Format

• Header
• Body

• Bitcoin Consensus

• Mining
• Target Threshold
• Bitcoin Transactions
• Transaction Format
• Script

• Bitcoin’s variants

COMP4137/COMP7200

Page 36



Bitcoin Payment Workflow

• Merchant Bob shares address out of band (not using Bitcoin P2P)
• Customer Alice broadcasts transaction tx, which pays the address
• Miners collect broadcasted transactions into a candidate block
• One of the candidate blocks containing tx is mined
• Bob waits for confirmations on t before providing goods

1. Request Bob’s address

2. Send Bob’s address

Bob

Alice
3. Construct
tx

Bitcoin network

Page 37



Block Format

Block Header

80 bytes

VarInt (1-9 bytes)

List of Transactions

Number of
Transactions n

Coinbase
Transaction

Regular
Transaction 1

Regular
Transaction 2

…

Regular
Transaction n − 1

Value of n

0 - 252

253 – 216 - 1

216 – 232 - 1

232 – 264 - 1

Size of
VarInt (byte)

Encoding

1

3

5

9

n

253||n

254||n

255||n

COMP4137/COMP7200

Page 38



Bitcoin Transactions

• A Bitcoin transaction (Tx) encodes a transfer of bitcoins between

entities.

• A destination of the transfer is called an output

• A single Tx can have several outputs
• Each output can serve as a source of bitcoins in a later Tx

• When previous Tx outputs are specified as the source of bitcoins in a

transaction, they are called inputs

• A coinbase transaction has no input and at least one output.

• There is no input because the source of bitcoins is not from a previous

transaction, rather, it is from the block reward.

COMP4137/COMP7200

Page 39



Examples

https://www.blockchain.com/explorer/ (and many other sites)

Page 40



Examples (coinbase)

• https://www.blockchain.com/explorer/transactions/btc/04f535a736834ce1b711fd1fb94ca418e470d65b98bd8b3dfd163b8fc

8bac026

COMP4137/COMP7200

Page 41



Examples

A

UTxO

• An output contains the value to be transferred and the recipient's address (or public key)

• Multiple outputs are allowed in a transaction

• An input refers to a previous unspent transaction output (UTxO)
• Multiple inputs are allowed in a transaction



Bitcoin Ownership (1)

• When an output of a previous transaction is “unlocked” by the input
of a later transaction, all the bitcoins in this output need to be spent
• A transaction output can be in only one of the two states, namely, spent or

unspent

• Unspent transaction outputs (UTXOs)

• Refers to outputs in Tx which have not been referred by the inputs of later

transactions

txID_3

TxID_1,0

20K,G
20K,G

10K,G

txID_4

TxID_3,0

COMP4137/COMP7200

Page 43



Bitcoin Ownership (2)

• When a new block is added, the output of the coinbase transaction is

a UTXO

• Every regular transaction in the new block unlocks UTXOs from the

previous blocks and creates new UTXOs

• The unlocked outputs in the previous Tx are not UTXOs

• The set of UTXOs changes with every new block

• UTXO model is different from the traditional account model in the

bank

• Provide anonymity

COMP4137/COMP7200

Page 44



Bitcoin Ownership (3)

• The set of all UTXOs that an entity can unlock can be thought of as bitcoins

owned by that entity

• During a fork, different nodes may consider different branches and thus the UTXO

set will differ across nodes with different local copies

• The UTXO set will be the same when the local copies become the same (after the

fork is resolved)

COMP4137/COMP7200

Page 45



Coinbase Transaction

• Each output in the coinbase transaction contains two items:

• Amount of bitcoins
• A script which specifies the conditions under which the bitcoins associated

with this output can be spent

• The script in an output can be viewed as a challenge.

• An entity which provides a satisfactory response can transfer the bitcoins

associated with the output

Coinbase Transaction

Amount x1
Challenge Script C1

Output 0

Amount x2
Challenge Script C2

Output 1

COMP4137/COMP7200

Page 46



Coinbase Transaction

• The sum of the amounts in all outputs of the coinbase transaction

must be less than or equal to the block reward

• If less, some of the bitcoin is not spendable

• So, usually the sum of amounts of all outputs of a coinbase

transaction is equal to the block reward

• Coinbase Transaction demo

• https://andersbrownworth.com/blockchain/coinbase

COMP4137/COMP7200

Page 47



Regular Transaction

• A regular transaction spends the bitcoins earned in a coinbase

transaction or received from a regular transaction.

• Each regular transaction must have at least one input and one output.
• The outputs in a regular transaction have the same format as the

outputs in a coinbase transaction

COMP4137/COMP7200

Page 48



Regular Transaction Input

• One input includes following information:

• Transaction Identifier (TxID) of a previous transaction on    the blockchain. TxID is the double

SHA-256 hash of the transaction

• The index of an output in the previous transaction, starting from 0.
• A response script which satisfies the condition required to spend the bitcoins in the output

• The inputs don’t specify the amount of Bitcoins to be spent.
• If an input refers to an output of a previous Tx, all BTCs associated with that

output must be spent in the Tx.

COMP4137/COMP7200

Page 49



Regular Transaction Fee

• Suppose a regular transaction has N inputs and M outputs
• Let x1, x2, …, xN be the bitcoins associated with the N inputs (i.e., N

outputs of previous transactions)

• Let y1, y2, …, yM be the bitcoin associated with the M outputs
• Then, the transaction fee denoted by R is defined as

where σ𝑖=1

𝑁 𝑥𝑖 ≥ σ𝑗=1

𝑀 𝑦𝑗.

𝑅 = ෍
𝑖=1

𝑁

𝑀
𝑥𝑖 − ෍
𝑗=1

𝑦𝑗

COMP4137/COMP7200

Page 50



Regular Transaction Fee Rate

• Miners aim to maximize their block reward
• Block subsidy is fixed
• Transaction fee depends on the transaction miner chooses to include

in the block

• High transaction fee
• Small transaction size
• Transaction fee per byte (or fee rate) is the factor for them to be considered

COMP4137/COMP7200

Page 51



Example of writing a new transaction

Input: 0.1
Output: 0.015+0.0845=0.0995

Fee: 0.0005 = Input - Output



Bitcoin Script

COMP4137/COMP7200

Page 53



Bitcoin Script

• Response and Challenge scripts are encoded using a special scripting

language developed by Bitcoin

• Stored in scriptSig and scriptPubkey fields of a transaction

• This language is simply called Script

• It is a stack-based language.
• It is not a general-purpose language and its goal is to support bitcoin

transactions.

COMP4137/COMP7200

Page 54



Standard Transactions

• To prevent a Denial-of-Service (DoS) attack, nodes in the Bitcoin

network will only relay transactions containing challenge scripts of
some pre-defined forms.

• They are called standard transactions.

COMP4137/COMP7200

Page 55



Standard Transactions

• Pay to Public Key (P2PK)

• Public key as payment destination
• Pay to Public Key Hash (P2PKH)

• Hash of public key as payment destination

• M-of-N multi-signature

• Response script provides signatures created using any m out of the n private

keys

• Pay to Script Hash (P2SH)

• Hash of a script as payment destination

• Null Data

• Mainly used to timestamp data

COMP4137/COMP7200

Page 56



Outline

• Bitcoin Block Format

• Header
• Body

• Bitcoin Consensus

• Mining
• Target Threshold
• Bitcoin Transactions
• Transaction Format
• Script

• Bitcoin’s variants

COMP4137/COMP7200

Page 57



Bitcoin’s variants

• Network forks (new coins split from Bitcoin’s history)

• Bitcoin Cash (BCH): Aug 2017 hard fork; larger blocks, different signature
scheme (SIGHASH_FORKID), CashAddr format; altcoin focuses on on-chain
transactions.

• Bitcoin Gold (BTG): Oct 2017; changed proof-of-work to Equihash to target GPU

mining.

• Bitcoin SV (BSV): Nov 2018 fork from BCH; very large blocks, many opcodes re-

enabled; different economic/governance assumptions.

• Others (less prominent): Bitcoin Diamond (BCD), Bitcoin Private (BTCP), etc.

These typically tweak block size, PoW, or script rules.



Bitcoin’s variants

• Protocol upgrades (feature variants within Bitcoin, not new coins)

• SegWit (2017): fixes malleability, enables Lightning, reduces fees.
• Taproot (2021): improves privacy and flexibility for complex transactions.
• Other soft forks: various consensus and policy refinements over time

• Networks for development/testing (variants of the Bitcoin

environment)

• mainnet (real BTC), testnet/signet (public testing), regtest (local testing)



Bitcoin’s variants

• Layer-2 and sidechains (use BTC but change how it’s transacted)
• Lightning Network: off-chain payment channels for fast, cheap micro-

payments; settles back to Bitcoin (to be addressed in our future
lectures).

To be covered in our future lectures.

• Liquid Network: federated sidechain by Blockstream; fast finality,

Confidential Transactions; asset is LBTC pegged to BTC.

• Rootstock (RSK): smart-contract sidechain (Solidity), two-way peg

(RBTC), merge-mined with Bitcoin.



Summary

• Bitcoin’s blockchain prevents double spending and tampering
• Secure only if nobody controls 50% or more of network hashrate
• Mining difficulty adjusted to regulate coin supply
• Miners incentivized by block reward
• Block subsidy halves every four years to limit total coin supply
• Bitcoin addresses are shared over the Internet
• Transactions paying these addresses are broadcasted on the Bitcoin

network

COMP4137/COMP7200

Page 61



References

• Saravanan Vijayakumaran, “An Introduction to Bitcoin”
• Arvind Narayanan, Joseph Bonneau, Edward Felten, Andrew Miller,

Steven Goldfeder, “Bitcoin and Cryptocurrency Technologies”

• Satoshi Nakamoto, “Bitcoin: A Peer-to-Peer Electronic Cash System”
• Bitcoin Charts

• https://www.blockchain.com/charts

• Bitmain Mining Rigs

• https://shop.bitmain.com

COMP4137/COMP7200

Page 62

