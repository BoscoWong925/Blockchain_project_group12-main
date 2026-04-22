COMP4137 Blockchain Technology and Applications
COMP7200 Blockchain Technology

Lecturer: Dr. Hong-Ning Dai (Henry)

Lecture 10
Advanced Topics



Outline

• Decentralized Finance (DeFi)

• Scaling blockchain by payment channel

• Decentralized identifiers

• Blockchain applications

COMP4137/COMP7200

Page 2



The Rise of DeFi

• Transforming Traditional Finance with Blockchain Innovation

• Decentralized Finance (DeFi) is revolutionizing the financial landscape

through blockchain technology

COMP4137/COMP7200

Page 3



Difference between traditional finance and DeFi

• Traditional finance

• DeFi

• Asset classes and processes are

managed by companies or people

• Intermediaries are required
• Accessibility is restricted by

location, identity, and financial
status

• Assets are managed by a set of

smart protocols

• No intermediaries are required
• Open to anyone with internet

access

• Low transaction costs due to peer-

• High transaction costs due to fees

to-peer model

and intermediaries

• Transaction speed is fast (near-

• Transaction speed is slow (days for

instantaneous)

cross-border payments)



Advantages of DeFi over traditional finance

Transparency

Accessibility

Security

DeFi provides unparalleled

Unlike traditional financial

With decentralized architecture,

transparency through blockchain

systems, DeFi is open to anyone

DeFi mitigates the risk of single

technology, enabling users to track

with an internet connection,

points of failure and potential data

and verify transactions in real

eliminating barriers to entry.

breaches.

time.

COMP4137/COMP7200

Page 5



Key Components of DeFi

1. Smart Contracts

• Self-executing contracts with the
terms directly written into code,
automating processes without
intermediaries.

2. Decentralized Exchanges (DEX)
• Platforms facilitating peer-to-peer

trading without a central
authority, enhancing liquidity and
security, E.g., CoinBase, UniSwap

3. Lending and Borrowing Protocols

• Smart contracts automate lending and

borrowing on these platforms,
allowing users to collateralize assets
and receive interest on deposits. DeFi
lending techniques include
Compound, Aave, and MakerDAO.

4. Decentralized Autonomous

Organization (DAO)
• Smart contracts and token holders
run decentralized autonomous
organizations (DAOs), enabling
decentralized decision-making and
resource allocation. DAOstack and
Aragon are popular DeFi DAO
frameworks

COMP4137/COMP7200

Page 6



DeFi Protocols: Exploring Decentralized Financial Platforms

Smart Contracts

Automating transactions

Decentralized
Exchange

Liquidity Mining

Governance Token

Incentivizing liquidity

and agreements, reducing

Facilitating peer-to-peer

provision in decentralized

Adds voting rights to the

human error and

intermediaries.

trading without reliance

protocols through reward

ledger platform

on centralized entities.

mechanisms.

COMP4137/COMP7200

Page 7



DeFi Applications: Real-World Implementations
and Success Stories

Decentralized Lending

Enabling borrowers and lenders

Automated Market
Making

Stablecoin Ecosystem

Introduction of stable digital

to interact without

Leveraging smart contracts to

assets to mitigate volatility,

intermediaries, reshaping the

create liquidity pools and

enhancing stability within the

lending landscape.

optimize asset exchanges in a

DeFi ecosystem.

decentralized manner.

COMP4137/COMP7200

Page 8



Outline

• Decentralized Finance (DeFi)

• Scaling blockchain by payment channel

• Decentralized identifiers

• Blockchain applications

COMP4137/COMP7200

Page 9



Bitcoin  Tx per second

≈4200 Tx/block
1 block / 10 mins

⇒ max:  7  Tx/sec

COMP4137/COMP7200

Page 10



Ethereum Tx per second

Ethereum avg Tx per second:

Simple Tx: 21k Gas
max 30M Gas per block
⇒ max 1428 tx/block

1 Block/12s

⇒ max 119 tx/s

≈ 15 Tx/sec

COMP4137/COMP7200

Page 11



In comparison …

• Visa:   up to 24,000 Tx/sec     (regularly 2,000 Tx/sec)

• PayPal:  200 Tx/sec

• Ethereum:  15 Tx/sec

• Bitcoin:  7 Tx/sec

Goal:  scale up blockchain Tx speed

COMP4137/COMP7200

Page 12



How to process more Tx per second

Many approaches:
• Use a faster consensus protocol
• Payment channels, reduce the need to touch the chain

COMP4137/COMP7200

Page 13



Payment Channels: the basic idea

Tx1: 0.01 ETH
Tx2: 0.01 ETH
Tx3: 0.01 ETH

Instead, we can do this:

Alice deposits 1 ETH with Bob.

At the end of the month, Bob
refunds unused deposit to Alice.

☕️
☕️☕️

COMP4137/COMP7200

Tx fee
per purchase!

only two Tx,
hundreds of
coffees

Page 14



Unidirectional Payment Channel

Alice
creates:

Contract A:
1 ETH

Bob does not post on chain

Tx1: send 0.99 to Alice / 0.01 to Bob from Contract A
signed by Alice

Tx2: send 0.98 to Alice / 0.02 to Bob from Contract A
signed by Alice

Post Tx3 on
Blockchain
(close channel)

Tx3: send 0.97 to Alice / 0.03 to Bob from Contract A
signed by Alice

Problem:  Alice could post Tx1 before Bob even though
she bought three coffees.

Page 15



A solution?

Alice
creates:

Contract A:
1 ETH

Only Bob can close the channel

Tx1: send 0.99 to Alice / 0.01 to Bob from Contract A
signed by Alice

Tx2: send 0.98 to Alice / 0.02 to Bob from Contract A
signed by Alice

Post Tx3 on
Blockchain
(close channel)

Tx3: send 0.97 to Alice / 0.03 to Bob from Contract A
signed by Alice

Problem:  What if Bob never publishes Tx3?
⇒ Alice never gets her 0.97 ETH back !!



Unidirectional Payment Channel

Alice needs a way to ensure refund if Bob disappears
Solution:  create a channel that can be closed in one of two ways
• Normal close Tx:  Sends 0.97 to Alice / 0.03 to Bob

… requires signatures by both Alice and Bob.

• Timelock Tx:  Sends 1 ETH to Alice

… requires signature by Alice,

but is accepted 7 days after channel is created

COMP4137/COMP7200

Page 17



Unidirectional Payment Channel

After 6 days:
•

Bob can close channel by signing and posting Tx3.

After 7 days:
• Alice can close channel using timelock Tx, gets back her 1 ETH.

•

Timelock period determines the lifespan of channel

• Once Alice sends the full 1 ETH to Bob, the Channel is

“exhausted”

COMP4137/COMP7200

Page 18



Payment Channel in Solidity

Alice creates contract with funds,
specifies timelock and recipient

verify Alice’s signature on
final amount.
Only Bob can call close() !!

send all funds to sender after timelock

COMP4137/COMP7200

Page 19



Bidirectional Payment Channel

Alice and Bob want to move funds back and forth

Two Unidirectional Channels?

Not as useful because Channels get exhausted

COMP4137/COMP7200

Page 20



Bidirectional Payment Channel

On Ethereum:  create a shared contract, each contributes 0.5 ETH:

channel
state:

A: 0.5 ETH,   B: 0.5 ETH,   Nonce=0

Off chain:  Bob sends 0.1 ETH to Alice by both signing new state:

new
state:

A: 0.6,   Bob: 0.4,  Nonce=1

Alice sig, Bob sig

COMP4137/COMP7200

Page 21



Bidirectional Payment Channel

On chain contract does not change:

balance: 1 ETH,   Nonce=0

Off chain:

Alice and Bob can move funds back and forth

by sending updated state sigs to each other:

A: 0.3,  Bob: 0.7,  Nonce=7

Alice sig, Bob sig

(7th transfer)

COMP4137/COMP7200

Page 22



Eventually: Alice wants to close payment channel

Alice does:  sends latest balances and signatures to contract

⇒ starts challenge period  (say, 3 days)

on chain:

A: 0.3 ETH,   B: 0.7 ETH,   Nonce=7

(pending close)

if Bob does nothing for 3 days:

⇒ funds disbursed according to Alice’s submitted state

if Bob submits signed state with a higher nonce  (e.g., nonce=9)

⇒ funds disbursed according to Bob’s submitted state

COMP4137/COMP7200

Page 23



Watchtowers

• A lightning wallet must be online on a regular basis to track it’s

payment channels for cheating attempts.

• A daily spending wallet, in particular, is offline whenever the user
stops using the app. This means there is a greater risk of cheating
attempts.

• A watchtower service can fix this.

• Watchtowers monitor the payment channels of offline users. If a

counterparty attempts to steal a user’s funds, the watchtower can step in to
help.

• The watchtower can prevent the theft by submitting a justice transaction.

COMP4137/COMP7200

Page 24



Watchtowers

Bidirectional channel requires Bob to
constantly check that Alice did not try to
close the channel with an old stale state

⇒ post latest state if she did

Watchtowers outsource this task

Bob sends latest state to watchtower.

Trusted for availability

COMP4137/COMP7200

Page 25



Main points:  summary

Payment channel between Alice and Bob:

• One on-chain Tx to create channel (deposit funds);

• Alice & Bob can send funds to each other off-chain
… as many Tx as they want;

• One on-chain Tx to close channel and disburse funds

⇒ only two on-chain Txs

COMP4137/COMP7200

Page 26



A more general concept:  State Channels

Smart contract that implements a game between Alice and Bob.

Begin game & end game: on chain.     All moves are done off-chain.

Page 27



State Channels

Can be used to implement any 2-party contract off chain!

two Txs on-chain:  1) contract creation and 2) termination

Page 28



Multi-hop payments (Bitcoin’s lighting)

Alice has channel
with bank Bob

Carol has channel
with bank Bob

Alice wants to pay Carol 1 BTC through untrusted intermediary Bob

How:   (i) Alice pays Bob 1.01 BTC,   (ii) Bob pays Carol 1 BTC

The challenge:  steps (i) and (ii) need to be atomic (either both (i) (ii) are
done or none of them are done.

COMP4137/COMP7200

Page 29



Multi-hop payments  (briefly)

A

B

send to B:

send to C:

Pay 1.01 BTC to B:

Hashlocked to B with R,
Timelock to A for refund

Pay 1 BTC to C:

Hashlocked to C with R,
Timelock to B for refund

R=H(r)

C

Random r

Alice sig

Bob sig

Then B can claim 1.01 BTC with r

C can claim 1 BTC on-chain with r

⇒ r is publicly known

if Carol never claims, Alice & Bob get funds back after timelock

COMP4137/COMP7200

Page 30



Atomicity of Payment Channel

• The atomicity in the payment channel means that the first payment
and the second payment in a multi-hop payment channel network
must be done as a whole or none.

• The atomicity can be achieved by hashed time-lock contract (HTLC) in

the lightning network (Bitcoin)

OP IF

OP HASH160 <Hash160 (R)> OP EQUALVERIFY
2 <Alice2> <Bob2> OP CHECKMULTISIG

OP ELSE

2 <Alice1> <Bob1> OP CHECKMULTISIG
OP ENDIF 1> <Bob1> OP CHECKMULTISIG
OP ENDIF

COMP4137/COMP7200

Page 31



Multi-hop example

1. Eric generates a secret('R'), hashes that
secret, and sends it to Alice. The secret
is only known by Eric.

2. Alice’s node computes Eric’s payment

(1BTC), and creates an HTLC to pay Bob
1.03BTC if he can provide the secret
within the next 10 blocks, otherwise,
the funds will be refunded to Alice.

3. …
4. Until reaching Eric, he then provides
the secret('R') that he generated and
unlocks the HTLC to get the 1BTC
payment

5. Other parties, Diana, Carol, Bob, and

Alice will eventually retrieve the funds
locked in

COMP4137/COMP7200

Page 32



The lightning network

The network:  lots of open bi-directional payment channels.

Alice wants to pay Bob:  she finds a route to Bob through the graph

Many extensions possible:  multi currency hubs, credit hubs, …

COMP4137/COMP7200

Page 33



Stats

# nodes in lightning network (Nov. 2023)

16,150

Number of channels:   63K

Network capacity:  ≈$205M

COMP4137/COMP7200

Page 34



Outline

• Decentralized Finance (DeFi)

• Scaling blockchain by payment channel

• Decentralized identifiers

• Blockchain applications

COMP4137/COMP7200

Page 35



Decentralized identifiers

• Decentralized identifiers (DIDs) are globally unique identifiers made

up of a string of letters and numbers that act like an identifying
address on a blockchain and are independent of any organization.

• DIDs can be used to digitally sign and issue Verifiable Credentials like

educational certificates, and to verify credentials instantly.

• Decentralized Identifiers contain cryptographic key pairs and are fully

under your control.



Problem with centralized identifiers

• There are many problems with using centralized identifiers like emails

and usernames to access websites and apps.

• Issues include lack of ownership and control of data and increased

risk of data breaches.

Individuals

Organizations

Developers

Data may be collected, stored,
and shared with other parties
without your knowledge

Data collected from these
identifiers are often stored in
centralized storage systems that
can be vulnerable to large-scale
data breaches

Often rely on third party platforms
like Google and Facebook to
authenticate the user, which hurts
users’ privacy

Data is owned and controlled by
providers and identifiers can be
removed anytime

Difficult to authenticate users and
preserve their privacy at the
same time

Inefficient sign-in processes that
creates a bad user experience



Decentralized identifiers

• Decentralized identifiers (DIDs) are a way to identify yourself on the
internet without using a central authority, like a government or a
company.

• With a DID, you can prove who you are online without having to give
your personal information to a bunch of different websites or apps.

• Key features of DIDs:

• Are created and managed completely by the user (individual or organization)

without depending on any third party

• Allow the owner to securely prove control over them
• Don’t contain any personal data or wallet information



Example of DID

• Verifiable educational certificates
• There are rising cases of fake certificates in many HK universities



Example of DID

• A decentralized identifier (DID) example for a university diploma
involves a digital, tamper-proof credential issued directly to a
student's digital wallet, rather than a paper certificate or PDF.

• This system allows employers to verify the degree instantly without

contacting the university.

Scenario: "Alice" Receives a Digital Diploma

1. Creation (University DID): The University of Example creates a DID on a blockchain

(e.g., did:indy:example:123456) to act as the trusted issuer.

2. Issuance (Verifiable Credential): Upon graduation, the university creates a Verifiable

Credential (VC)—a digital diploma containing Alice's name, degree, and graduation date.

3. Signing: The university signs this digital diploma using its private key, which is linked to its

DID.

4. Storage (Holder): Alice receives the signed digital diploma and stores it in her secure digital

wallet app on her phone.

5. Verification (Verifier): When Alice applies for a job, she shares the digital diploma via a QR

code or direct transfer. The employer uses the university's public DID on the blockchain to

verify the signature, confirming the diploma is authentic, untampered, and valid.



Benefits of Decentralized Identifiers

• DIDs enable the following for organizations, individuals, and

developers:

Organizations

Individuals

Developers

Instantly verify credentials
anytime without needing to
contact an issuer like a university

Full ownership of data and no
one can take away your DIDs

Eliminates the need for
passwords and inefficient
authentication processes

Efficiently issue fraud-proof
credentials at lower costs

Prevent device tracking as you
browse websites and apps

Request data directly from users
while maintaining their privacy

Robust data security

Complete control of data and
who views it



Centralized vs. Decentralized Identifiers

Centralized Identifiers

Decentralized Identifiers (DIDs)

Identifiers provided by centralized providers
like Google or Facebook can be taken away
anytime and are owned by the provider

You create your DIDs that no one can take
away from you and you have full ownership of
them

Can be used to track online behavior

Create as many DIDs as you want for
different relationships. Having multiple DIDs
makes it harder for companies to track users
and correlate data.

Less secure and private connections between
parties

Enables unique, private, and secure peer-to-
peer connections between two parties



Outline

• Decentralized Finance (DeFi)

• Scaling blockchain by payment channel

• Decentralized identifiers

• Blockchain applications

COMP4137/COMP7200

Page 43



Blockchain applications

1. Blockchain for Internet of Things
2. Blockchain for mobile crowdsensing

COMP4137/COMP7200

Page 44



2.1 Internet of Things

• Internet of Things (IoT) is a network of intelligent computers, devices,

and objects that collect and share huge amounts of data

• IoT can support a number of industrial applications

Industrial
applications

Communication
layer

Perception layer

COMP4137/COMP7200

45



2.1 Challenges of IoT

• Heterogeneity of IoT systems

• Heterogeneous IoT devices, heterogeneous communication protocols and

heterogeneous IoT data types

• Complexity of networks

• Different types of IoT protocols (NFC, WiFi, 6LoWPAN, NB-IoT, LoRa)

• Poor interoperability

• Due to the decentralization and the heterogeneity of IoT systems

COMP4137/COMP7200

46



2.1 Challenges of IoT (cont.)

• Resource constraints of IoT devices

• IoT devices such as sensors, actuators, RFID tags and smart meters suffer from
limited resources including computing resource, storage resource and battery
power.

• Privacy vulnerability

• Due to the complexity and decentralization of IoT systems
• Uploading data to remote clouds -> risk of privacy exposure

• Security vulnerability

• Authentication, authorization and communication encryption may not be

applicable to distributed IoT

COMP4137/COMP7200

47



2.2 Architecture of Blockchain of Things
• We name such integration of blockchain with IoT as BCoT.

COMP4137/COMP7200

48



2.2 Architecture of Blockchain of Things
• We name such integration of blockchain with IoT as BCoT.

COMP4137/COMP7200

49



P2P overlay network and blockchain node architecture

• Each node in overlay network consists of a number of components

corresponding to the composite blockchain layer

50



Features of BCoT

• Blockchain serves as a middleware between IoT and applications

• offering an abstraction from the lower layers in IoT
• providing users with blockchain-based services

• Hiding complexity of IoT systems

• Offering general interfaces to various IoT applications

COMP4137/COMP7200

51



Opportunities of integrating blockchain with IoT

• Enhanced interoperability of IoT systems

• Transforming various IoT data into blockchain
• Interoperating crossing different types of fragmented networks

• Improved security of IoT systems
• Encryption and digital signature

• Traceability and Reliability of IoT data

• Data in blockchain is traceable and reliable

• Autonomic interactions of IoT systems

• Distributed autonomous Corporations (DACs) to automate transactions

COMP4137/COMP7200

52



Blockchain for computing management

• Cloud servers and edge servers may store the whole blockchain (or

partial blockchain) data and IoT devices only store the partial
blockchain
Orchestration of Cloud and edge computing is a necessity!

53



Acknowledgement

• This is a joint work with Zibin Zheng (Sun Yat-sen University, China)

and Yan Zhang (Oslo University, Norway)

• For more details, please refer to our paper entitled "Blockchain for

Internet of Things: A Survey" in (ESI highly-cited paper) IEEE Internet
of Things Journal, 2019

COMP4137/COMP7200

54



Blockchain applications

1. Blockchain for Internet of Things
2. Blockchain for mobile crowdsensing

COMP4137/COMP7200

55



3.1 Mobile Crowdsensing

• Mobile crowdsensing (MCS) has become a new paradigm which takes
advantages of pervasive mobile devices and sensors to collect data
efficiently, thereby enabling numerous applications.

MCS Applications

Categories

Environmental

Industrial

Social

Natural Environment

Smart factory

Personal information

COMP4137/COMP7200

56



Examples of MCS

Google street map

HealthMap

https://www.healthmap.org/en/

COMP4137/COMP7200

57



Traditional mobile crowdsensing triangular architecture

(2)

(1)

(3)

COMP4137/COMP7200

58



Challenges of MCS

• Reliability of MCS

• Centralized architecture requires mobile devices to communicate with MCS

system -> susceptible to single-point-failure

• Security of MCS

• MCS is exposed to the risk of DDoS and man-in-the-middle attacks
• Data at MCS server to be leaked or falsified

• Data quality of MCS

• Data collected by human being (i.e., behave maliciously or unreliably-> poor

quality of sensing data)

COMP4137/COMP7200

59



3.2 Why blockchain can be used for MCS?

• Sensory data at centralized server of MCS cannot be fully trusted

while blockchain can guarantee decentralized trust (non-tamperable
data)

• Decentralized architecture of blockchain can also improve the system

reliability

• Smart contracts on top of blockchain can prevent malicious behaviors

such as free-riding and false-reporting in MCS

COMP4137/COMP7200

60



Blockchain for MCS (BMCS)

Decentralize conventional centralized MCS architecture!

61



Working procedure of BMCS

Two issues to be solved:
1.

Incentive mechanism to motivate workers to contribute to sensing tasks
(especially on some unpopular regions)

2. Data quality assurance mechanism

COMP4137/COMP7200

62



Incentive mechanism

• Dynamic reward ranking (DR2) incentive mechanism

COMP4137/COMP7200

63



Sensory Data Quality Detection Scheme

• Normal data contributed by

users has the temporal
stability and spatial
correlation

• Abnormal Data due to

hardware faults or fake data
submitted by dishonest
users;

If the data point is in the range of              , it is normal data; it is abnormal otherwise.

64



Experiments

• We implemented a

prototype of BMCS on
Ethereum and
conducted sound
sensing tasks in the
public blockchain test
network.

• We used 6 MI-4 mobile

phones for workers

COMP4137/COMP7200

65



Real testbed

• We conducted

experiments in a factory
workroom

• Test scenario of sound

sensing tasks.

COMP4137/COMP7200

66



Sensory Data Quality Detection Scheme

Proposed data quality detection scheme achieves an excellent performance

COMP4137/COMP7200

67



Acknowledgement

• This is a joint work with Junqin Huang, Linghe Kong (Shangjiao Jiao

Tong University, China), Steve Xue Liu (McGill University, Canada) and
Long Cheng (Clemson University, USA)

• For more details, please refer to our paper entitled "BlockSense:

Towards trustworthy mobile crowdsensing via proof-of-data
blockchain" in IEEE Transactions on Mobile Computing, 2024

COMP4137/COMP7200

68



Summary

• Speed up blockchain by different strategies (e.g., Payment

channel network)

• Decentralized identifiers

• Blockchain applications

• Blockchain for IoT
• Blockchain for mobile crowdsensing

COMP4137/COMP7200

Page 69



Thank you!

