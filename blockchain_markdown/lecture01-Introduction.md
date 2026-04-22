COMP4137 Blockchain Technology and Applications
COMP7200 Blockchain and Cryptocurrencies

Lecturer: Dr. Hong-Ning Dai (Henry)

Lecture 1
Introduction to Blockchain



Outline

• Cryptocurrency

• Blockchain

• Blockchain Applications

COMP4137/COMP7200

Page 2



Cryptocurrency

Bitcoin

Ethereum

Satoshi Nakamoto
中本聰

Vitalik Buterin

https://vitalik.ca/index.html

COMP4137/COMP7200

Page 3



Cryptocurrency

• Historical price of Bitcoin

https://www.statista.com/statistics/326707/bitcoin-price-index/

COMP4137/COMP7200

Page 4



Cryptocurrency

• Over 2000 cryptocurrencies at this moment

Page 5



Cryptocurrency

• Cryptocurrencies have different features.

System

Concept

Tx details

Tx example

Market cap

Release date

Release method

Mining algorithm

Support

Total Amount

Time

Block size

Bitcoin (BTC)

Zcash (ZEC)

Homology Difference: Zcash code is modified based on Bitcoin V.0.11.2 code

Digital currency

Publicly viewable

Private digital currency

Hidden (readable with key)

addr. X sent 1 BTC to addr. Y

? sent ? ZEC to ?

~ $800 billion

Jan. 2009

Mining

SHA256

~ $2 billion

Oct. 2016

Mining / founders’ reward

Equihash

Web-based wallet

Zcash: only linux, command line without GUI

21 million

10 mins

1 M

21 million

2.5 mins

2 M

COMP4137/COMP7200

Page 6



Cryptocurrency

Advantages
• Fast, safe and cheap
• Ease of use and high portable
• Pseudonymity
• Decentralization
• Active involvement of users
• Transparent and neutral

COMP4137/COMP7200

Page 7



Cryptocurrency

Disadvantages
• Unrecoverable once lost
• High market volatility
• Malicious activities (money

laundering, scam)

Challenges
• Lack of auditability
• Complex mathematical

calculations
• Data privacy
• Performance (high latency, low

throughput)

• Communication between

different blockchains

COMP4137/COMP7200

Page 8



Data analysis on Cryptocurrency

• Software (such as Chainalysis, Elliptic) can infer your address if you
have transacted with other addresses that are not anonymous.

Visualization of blockchain networks

COMP4137/COMP7200

Page 9



Non-Fungible Token (NFT)

• NFT is a unit of data stored on blockchain to represent the ownership

of an object (a virtual asset)

• Each NFT represents something unique, not interchangeable, and not divisible
• Can be photos, videos, audio, and other types of digital files

• Platforms and Standards

• Ethereum
• ERC-721
• ERC-1155

• FLOW
• Tezos
• Solana

Community: Projects and Brands

COMP4137/COMP7200

Page 10



NFT

• NFTs are unique and non-interchangeable assets (data) stored on

blockchains

• Fungibility – the ability of an asset to be exchanged or substituted

with similar assets of the same value.

Fungible

Non-Fungible

Alice

Bob

The lack of interchangeability (fungibility) distinguishes NFTs from blockchain cryptocurrencies.

COMP4137/COMP7200

Page 11

Lebron James

Paul George

NBA Top shot



Outline

• Cryptocurrency

• Blockchain

• Blockchain Applications

COMP4137/COMP7200

Page 12



Blockchain - A High-level View

• Cryptocurrency  != Blockchain
• Blockchain: a kind of data structure
• A blockchain consists of a number of consecutively-connected blocks.
• Each block points to its immediately-previous block (called parent block) via
an inverse reference that is essentially the hash  value of the parent block.

the hash value of the root of a Merkel tree with concatenating
the hash values of all the transactions in the block

COMP4137/COMP7200

Page 13



Blockchain

• Bitcoin Genesis Block

“The Times 03/Jan/2009 Chancellor on brink of second bailout for banks”

*hypotheses…

https://btc.com/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b

COMP4137/COMP7200

Page 14



Blockchain - A High-level View

• Blockchain System: a decentralized system
• The construction of a blockchain system requires diverse ICT technologies:

• Cryptographic algorithms
• Computer networks
• Distributed systems and consensus
• Smart contracts (software technology)
• Reward and transaction cost (economics)

COMP4137/COMP7200

Page 15



Working flow of blockchain

• Consider a single transaction

COMP4137/COMP7200

Page 16



Blockchain Transactions

• Smallest element
• Record every decision and action taken
• Proof of history, provides provenance

Image from https://evrythng.com/

COMP4137/COMP7200

Page 17



Blockchain “Block”

■ Contain multiple transactions

• The transaction is immutable/indelible

■ Write and Read-Only

■ Once a block is chained, it is extremely difficult to change

• If modification possible, need to rework on all the
subsequent blocks and consensus for each block

TX1

TX2

…

TXn

COMP4137/COMP7200

Page 18



Chain of Blocks

• Contain multiple blocks
• Blocks linked using cryptography
• An instance of distributed ledger

TX1

TX2

…

TXn

COMP4137/COMP7200

Page 19



Distributed Network

■ Blockchain operates on a decentralized/distributed P2P network

■ Each node stores a copy of the ledger

• Distributed Ledger

Centralized Network

Distributed Network

Decentralized Network

Nodes interact with a single central node

Nodes interact with some central nodes

Nodes interact with each other directly

COMP4137/COMP7200

Page 20



Distributed Ledger

Blockchain is a distributed ledger
■ Centralized ledger: stored by a central node

■ Distributed ledger: stored in every node

• All nodes agree on the true state of the ledger (via a consensus protocol)

Centralized ledger

Distributed ledger

A

C

B

D

A

C

B

D

Alice pays Bob 3 BTC

Bob pays Chris 2 BTC

Eve pays Alice 5 BTC

…

COMP4137/COMP7200

Page 21



Distributed Ledger

■ Keep track of all transactions performed in the network

■ Can be encrypted for confidentiality

■ Can be used by individuals without a central authority

■ Immutable: Ledger records are very difficult to be altered

• Changing a record in the ledger requires a consensus from all

participants

• Rework on all subsequent records

COMP4137/COMP7200

Page 22



Demo of blockchain

• https://andersbrownworth.com/blockchain/



Distributed Consensus

■ Ensure the blocks in blockchain are valid and truthful

■ Prevent malicious adversaries from system compromise and chain-

forking

■ Many consensus protocols, each with different pros and cons

• Proof of Work (PoW), Proof of Stake (PoS), Proof of Elapsed Time (PoET),

Proof of Activity (PoA), Proof of Burn (PoB)

• Paxos, BFT, Streamlet

■ We will explore many of blockchain consensus protocols later

COMP4137/COMP7200

Page 24



Smart Contract

• A program running in a secure environment that controls the transfer

of digital assets between parties under certain conditions

• Contract encoded into blockchain
• Enable broader blockchain applications beyond cryptocurrencies

pragma solidity 0.5.8;

contract SimpleBank {

mapping(address => uint) balances;

function deposit(uint amount) payable public {
balances[msg.sender] += amount;

}

}

}

function withdraw() public {
msg.sender.transfer(balances[msg.sender]);
balances[msg.sender] = 0;

COMP4137/COMP7200

Page 25



Smart Contract

■ Smart contract is a computer program that

• Defines rules

• Enforces obligations and penalties

• Executes actions required by clauses

• Autonomous without ownership

• Secure

■ Written in a high-level programming language (e.g., Solidity)

Blockchain Techniques

Smart Contracts?

Language

Bitcoin

Ethereum

Hyperledger

✗

✓

✓

C++

Solidity

GoLang, C++, etc

COMP4137/COMP7200

Page 26



Smart contract

COMP4137/COMP7200

Page 27



Smart contract

COMP4137/COMP7200

Page 28



Smart contract

COMP4137/COMP7200

Page 29



Merits of smart contract

• Reducing risks. Due to the immutability, traceability and auditability

of blockchain data

• Cutting down administration and service costs. Blockchains assure

the trust without going through a central broker or a mediator. Smart
contracts can be automatically triggered in a decentralized way.
• Improving the efficiency of business processes. The elimination of
the dependence on the intermediary can significantly improve the
efficiency of business process.

COMP4137/COMP7200

Page 30



Smart Contract

• Blockchains are enabling smart contracts.

• Essentially, smart contracts are implemented on top of blockchains.

• Life cycle of smart contracts

Write to
blockchain

Write to
blockchain

Write to
blockchain

COMP4137/COMP7200

Page 31



Outline

• Cryptocurrency

• Blockchain

• Blockchain Applications

COMP4137/COMP7200

Page 32



Development of Blockchain

• Blockchain 1.0
• Bitcoin
• Programmable Money

• Blockchain 2.0
• Ethereum
• Smart Contract

• Blockchain 3.0

• Fix problems in current blockchain industry
• Scalability
• Inter-operability
• Privacy
• …

COMP4137/COMP7200

Page 33



Blockchain Applications

• Key industries with blockchain

• Banking and investment

• improve decades old operations and processes

• Gaming and artwork

• trade of virtual goods with token

• Retail

• track & trace, counterfeit prevention, inventory management and auditing

COMP4137/COMP7200

Page 34



Blockchain network in food industry

• Blockchain can be used in food

industry to achieve the
traceability of food supply
chain

• Information in each procedure
will be stored in the blockchain

Source: Thume et al., “Blockchain-based traceability in the food industry: requirements analysis along the food supply chain”, DOI: 10.31219/osf.io/uyb64

COMP4137/COMP7200

Page 35



Blockchain in Medical records

▪ You enter a health facility (not your home facility)
▪ You provide proof of identity verified with a

blockchain

▪ Your “private key” unlocks encrypted data related

only your health records

•

▪ Also provides a much stronger privacy protection
Instead of a medical database being encrypted with one
key (which might be lost or discovered), each patient’s
record has its own key.

• Hence, to compromise the database, you would need to

guess potentially millions of keys

COMP4137/COMP7200

Page 36



Blockchain in Medical Prescriptions

• Widespread fraud
• Blank scripts are stolen from doctors’ offices

or forged

• Some doctors abuse the system
• Token issued to patient: it cannot be resold

and has an expiration

• Patient presents token to pharamacist and
blockchain is checked to make sure patient
owns the token (and has not already spent it)

COMP4137/COMP7200

Page 37



Internet of Medical Things

e
r
a
c
h
t
l
a
e
H

s
r
e
n
o
i
t
i
t
c
a
r
p

a
t
a
D

T
M
o
I

t
n
e
m
e
g
a
n
a
m

i

s
n
o
i
t
a
c
n
u
m
m
o
c

Computing facilities

IoMT data

Data analytics

IoT Gateway

Base station

Sensor/IoT device
COMP4137/COMP7200

Wireless link

Wired link

Page 38



Challenges of IoMT

• Absence of interoperability across different IoMT sectors

• Different IoMT devices (body sensors, medical devices)
• Diverse IoMT protocols

• Privacy and security vulnerabilities of IoMT devices and systems

• Difficult to deploy cryptographic algorithms
• Outsourcing data to clouds (untrusted, e.g., icloud instrusion)

COMP4137/COMP7200

Page 39



Architecture of blockchain-enabled IoMT

COMP4137/COMP7200

Page 40



Solutions of Blockchain-enabled IoMT to COVID-19

COMP4137/COMP7200

Page 41



Summary

■ Blockchain is interdisciplinary

■ Cryptography and Distributed Systems are fundamental building

blocks

O p e r a t i o n
Init & Broadcast
Transactions
Transaction
Validation

C r y p t o Te c h n i q u e s
• Digital Signature
• Private/Public Keys

• Proof-of-Work

Chaining blocks

• Hash Function

A l g o r i t h m s &
D a t a S t r u c t u r e s

h
p
a
r
g
o
t
p
y
r

C

y
t

i
r
u
c
e
S

&

y

s
m
e
t
s
y
S

d

e
t
u
b

i

r

t
s

i

D

COMP4137/COMP7200

Page 42



References

• Satoshi Nakamoto, “Bitcoin: A Peer-to-Peer Electronic Cash System”
• Zibin Zheng, Shaoan Xie, Hong-Ning Dai, Xiangping Chen, Huaimin
Wang, “Blockchain challenges and opportunities: A survey”, 2018

COMP4137/COMP7200

Page 43

