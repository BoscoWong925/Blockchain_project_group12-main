COMP4137 Blockchain Technology and Applications
COMP7200 Blockchain Technology

Lecturer: Dr. Hong-Ning Dai (Henry)

Lecture 3
Distributed System and Consensus



Outline

• Definition and Characteristics

• Architecture Models

• Distributed Algorithms

COMP 4137/COMP 7200

Page 2



Centralized Systems

• All tasks completed by a single entity

✓Simple

✓Easy to design and implement

✓Efficient (with small # of users)

X

Server

Server is down?

A lot of users?

COMP 4137/COMP 7200

Page 3



Distributed Systems

▪ A group of independent entities communicated with one

another in a coordinated manner

▪ Collaboratively enable a service (computing, data sharing and storage)

▪ Goal: Address inherent limitations of centralized systems

• Robustness
•
Scalability
• Reliability

COMP 4137/COMP 7200

Page 4



Distributed Systems

Distributed server

Appeared as a single entity

Message-based communication

Each entity has separate resource (data,
memory, processor, OS)

COMP 4137/COMP 7200

Page 5



Key Characteristics

• Transparency

• Most important feature

• Illusion of a single system

• Hide all internal organization, communication details

• Uniform interface

• Access transparency, location transparency, relocation transparency,

migration transparency, replication transparency, concurrency
transparency, failure transparency, scaling transparency, performance
transparency

COMP 4137/COMP 7200

Page 6



Key Characteristics

• Openness

• Heterogeneity

• Variety and differences in hardware and software components

• Resource Sharing

• Resources (hardware, software, data) accessed across multiple entities

• Concurrency

• Parallel executions of activities
• Reduce latency, increase throughput

COMP 4137/COMP 7200

Page 7



Key Characteristics

• Scalability

• Add/remove components to/from the system

• Fault Tolerance

• Continuous availability

COMP 4137/COMP 7200

Page 8



Design Goals

• High Performance

• Low latency, high throughput

• Reliability

• Preserve correctness and integrity in the presence of

faulty/malicious nodes

• Failure detection, self-stabilization

• Scalability

• Adapt with flexible number of users in the system

COMP 4137/COMP 7200

Page 9



Design Goals

• Consistency

• Update consistency, replication consistency, cache consistency,
failure consistency, clock consistency, user interface consistency

• Synchronization between concurrent tasks

• Security

• Malicious adversaries, secure communication, resource protection

COMP 4137/COMP 7200

Page 10



CAP Theorem

▪ Consistency
• All nodes see the same data at the same time

“Any  distributed  system  cannot  achieve  Consistency,  Availability  and
Partition tolerance concurrently.”                                   -- Gilbert and Lynch

▪   Availability

• If the node in the system does not fail, it must always respond to the

user’s request.

▪ Partition tolerance

• The network will be allowed to lose arbitrarily many messages sent

from one node to another

Choose 2 out of 3: Generally, between consistency & availability under partition!

COMP 4137/COMP 7200

Page 11



Distributed System Applications

• Distributed systems are everywhere

• Mobile systems
• Sensor networks IoT

• Ubiquitous and Pervasive computing WWW

• P2P computing

Page 12



Peer-oriented Systems

Client/server

Server

Search
engine/grid

Content Delivery Networks

e.g., Netflix
Cloudflare

Server

Duplicated
Server

Pure P2P

Hybrid P2P

directory

e.g.,
WhatsApp,
Napster

e.g., BitTorrent, Freenet & Gnutella

COMP 4137/COMP 7200

Page 13



Outline

• Definition and Characteristics

• Architecture Models

• Distributed Algorithms

COMP 4137/COMP 7200

Page 14



Client-Server Architecture

• Basic model

• Two types of node: client (slave) and server

(master)

• All tasks accomplished by server

• Server is resource-powerful

• Client is resource-limited

Internet

COMP 4137/COMP 7200

Page 15



Client-Server Architecture

• Asymmetric, partially distributed

• Examples:

• Cloud services (Amazon, MicroSoft,

Internet

Facebook, Google)

• Internet of Things (IoTs)

• Advantage
• Easy to maintain security and reliability
• Enable a wide range of services

• Easy to design and implement

COMP 4137/COMP 7200

Page 16



Client-Server Architecture

• Disadvantages

• Central point of failure and compromise

• Attacks targeting to server nodes (e.g., DoS, data-breach)

• Resource management and administration

• Central point of trust: Server has more control and authority in the

system

• Not so scalable: more clients join -> more server demands

COMP 4137/COMP 7200

Page 17



Peer-to-Peer Architecture

• A network of nodes (peers) sharing resources directly with each other

• Symmetric: All nodes are equal participants and play both roles:

• provider and consumer of resource

• No *server* node

• Fully distributed, no centralized data and resource
• “The ultimate form of democracy on the Internet”

• Examples: blockchains, file-sharing software

COMP 4137/COMP 7200

Page 18



Peer-to-Peer Architecture

• Advantage
• Distributed trust
• Balanced resource load
• High resource capacity and high scalability

• More clients, more servers

• High fault-tolerance and resiliency against DoS attacks

Node

Node

Node

Node

COMP 4137/COMP 7200

Page 19



Peer-to-Peer Architecture

• Disadvantage
• Costly backup, high bandwidth consumption
• Hard to control
• Hard to maintain security and consistency

Node

Node

• Vulnerable to network partitions, byzantine behavior

Node

Node

• Unstable

COMP 4137/COMP 7200

Page 20



Distributed vs. Decentralized

• P2P is distributed, but offers various degrees of decentralization

• Some P2P still need central authorities to make decision (e.g.,
network control, resource load) efficiently

• Somewhat centralized

• Decentralized is NOT all-or-nothing

COMP 4137/COMP 7200

Page 21



Distributed vs. Decentralized

• In fact, no system is purely decentralized, or purely
centralized

• Blockchain can be centralized or decentralized under certain
degrees

• Depend on the design and application requirements

COMP 4137/COMP 7200

Page 22



Unstructured P2P network

• Easy to build

• Loose restriction on overlay structure, data location and
resource distribution

• Nodes communicate randomly, perform arbitrary tasks

• High resiliency to churn

• Nodes leave and join frequently

• Nodes and resources are loosely-coupled

• Data navigation issue

• High resource (CPU, memory, network) usage

• Examples: Napster, Gnutella, KaZaA

COMP 4137/COMP 7200

Page 23



Directory-based P2P of Sharing Music: Napster

join

query

answer

central index

get

file

...

24



Unstructured P2P: Gnutella

flooding query

25



Super Node based P2P: KaZaA (Morpheus)

...

...

...

super peer

...

file

get

...

query

answer

...



Super Node based P2P: KaZaA (Morpheus)

...

...

flooding query

...

...

super peer

...

...



Structured P2P network

• Structured overlay network, restriction on content placement and
resource distribution
• Nodes and resources are tightly-coupled, everyone has their own task

• Each node is responsible for a specific role in the network

• Distributed Hash Table (DHT) for node-task assignment

Peers

•

Simplifying content location

Harder to build

Low resiliency against churn

Fox

The red fox
runs across
the ice

The red fox
walks across
the ice

Hash
function

Hash
function

Hash
function

ABCDE213

DEF21234

FFE78682

COMP 4137/COMP 7200

Page 28



DHT: Example - Chord

• Associate to each node and file a unique id in a uni-dimensional space (a

Ring)

• E.g., pick from the range [0...2m]
• Usually, the hash of the file or  IP address

• Properties:

• Routing table size is O(log N) , where N is the total number of nodes
• Guarantees that a file is found in O(log N) hops



Consistent Hashing

• The main idea: map both keys and nodes (node IPs) to the same (metric) ID

space

David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine, and Daniel Lewin “Consistent
hashing and random trees: distributed caching protocols for relieving hot spots on the World Wide
Web”, In Proceedings of the twenty-ninth annual ACM symposium on Theory of computing (STOC '97)



Consistent Hashing

• The main idea: map both keys and nodes (node IPs) to the same (metric) ID

space

The ring is just a possibility.
Any metric space will do



Consistent Hashing

• The main idea: map both keys and nodes (node IPs) to the same (metric) ID space
• Each key is assigned to the node with ID closest to the key ID

▪ uniformly distributed
▪ at most logarithmic number of keys assigned to each node

Problem: Starting from a node, how do we locate the node responsible for a
key, while maintaining as little information about other nodes as possible?



Chord [MIT]

• Consistent hashing (SHA-1) assigns each node and object an m-bit ID
• IDs are ordered in an ID circle ranging from 0 – (2m-1).
• New nodes assume slots in ID circle according to their ID
• Key k is assigned to first node whose ID ≥ k

→ successor(k)

* All Chord figures from “Chord: A Scalable Peer-to-peer Lookup Protocol for Internet Applications”,
Ion Stoica et al., IEEE/ACM Transactions on Networking, Feb. 2003.
MIIS01 Distributed Systems

33



Consistent Hashing - Successor Nodes

identifier

node

X key

1

successor(1) = 1

2

2

successor(2) = 3

6

0

7

5

identifier
circle

1

3

4

2

successor(6) = 0

6

6

34



DHT: Chord Basic Lookup

N120

N105

N10

“Where is key 80?”

“N90 has K80”

N32

K80

N90

* All Chord figures from “Chord: A Scalable Peer-to-peer Lookup Protocol for Internet Applications”,
Ion Stoica et al., IEEE/ACM Transactions on Networking, Feb. 2003.
MIIS01 Distributed Systems

35

N60

How about lookup
efficiency?



Consistent Hashing – Join and Departure

• When a node n joins the network, certain keys previously assigned to

n’s successor now become assigned to n.

• When node n leaves the network, all of its assigned keys are

reassigned to n’s successor.

36



Consistent Hashing – Node Join

keys

5

7

keys
1

keys
2

1

3

2

0

4

keys

6

7

5



Consistent Hashing – Node Departure

keys
7

keys
6

6

7

5

0

4

keys
1

keys
2

1

3

2



Scalable Key Location – Finger Tables

• To accelerate lookups, Chord maintains additional routing

information.

• This additional information is not essential for correctness, which is

achieved as long as each node knows its correct successor.

• Each node n’ maintains a routing table with up to m entries (which is

in fact the number of bits in identifiers), called finger table.

• The ith entry in the table at node n contains the identity of the first

node s that succeeds n by at least 2i-1 on the identifier circle.

• s = successor(n+2i-1).
• s is called the ith finger of node n, denoted by n.finger(i)



Scalable Key Location – Finger Tables

keys
6

finger table

For.
0+20
0+21
0+22

start

succ.

1
2
4

1
3
0

6

7

5

0

4

1

3

2

keys
1

finger table

For.
1+20
1+21
1+22

start

succ.

2
3
5

3
3
0

keys
2

finger table

For.
3+20
3+21
3+22

start

succ.

4
5
7

0
0
0



Chord Key Location

• Lookup in finger table
the furthest node that
precedes key

• Query homes in on

target in O(logN) hops



Chord Key Location

• Lookup in finger table

the furthest node
that precedes key

• -> O(log n) hops



Hybrid P2P network

• Central authorities to help nodes navigate each other

• Combine client-server with P2P models

• Tend to improve overall performance

• Trade-off b/w centralization vs. node equality

•

Inherit the best of both worlds

•

Efficiency in C-S setting, and decentralization in P2P setting

COMP 4137/COMP 7200

Page 43



Objectives and Benefits of P2P

• As long as there no physical break in the network, the target file will

always be found.

• Adding more contents to P2P will not affect its performance.

(information scalability).

• Adding and removed nodes from P2P will not affect its performance.

(system scalability).

COMP 4137/COMP 7200

44



Peer-oriented Applications

• File Sharing: document sharing among peers with no or limited

central controls.

• Instant Messaging (IM): Immediate voice and file exchanges among

peers.

• Distributed Processing: One can widely utilize resources available in

other remote peers.

COMP 4137/COMP 7200

45



Outline

• Definition and Characteristics

• Architecture Models

• Distributed Algorithms

COMP 4137/COMP 7200

Page 46



What is Consensus?

Consensus is an agreement among a group of people on
an idea, statement, or plan of action

▪ Majority: 51%
▪ Supermajority: 66% (sometimes higher)
▪ Unanimous: 100%
▪ Weighted: not all votes weighed equally

COMP 4137/COMP 7200

Page 47



Consensus Mechanism

• Main Motivation: Reliability and Fault-Tolerance in distributed system

• Correct operation in the presence of corrupted nodes

• Reach a common agreement in a distributed/ decentralized

system

• Nodes propose values

• All nodes must agree on one of these values

COMP 4137/COMP 7200

Page 48



Consensus Mechanism

▪ Key to solving many problems in distributed computing

• Atomic commit of database transaction

• Clock synchronization

• Dynamic group membership

COMP 4137/COMP 7200

Page 49



Consensus Protocol: Definition

• A consensus protocol comprises two algorithms:
▪

𝑣i  ← Propose(): Each node 𝑛i  proposes a value 𝑣i  and broadcasts 𝑣i  to the network
𝑣  ←  Decide(𝑣1, 𝑣2 , … , 𝑣n): All nodes agree on a common value 𝑣  ∈ {𝑣1, 𝑣2 , … , 𝑣n}

▪

▪

▪

The protocol terminates when all correct nodes decide on the same value

The agreed value cannot be arbitrary: it must come from some correct nodes

P1

v1

P1

d1

Consensus
algorithm

P2

v 2

P3
v3

P2

d 2

P3
d3

1. Propose

COMP 4137/COMP 7200

2. Decide

Page 50



Consensus Protocol

• Example: Find max value among all values

P1

5

5

15

15

P3

10

5

20

5

20

15

P2

10

10

20

20

P5

COMP 4137/COMP 7200

Page 51



Consensus Properties

• Validity

• Value agreed is a value proposed

• Agreement

• All correct nodes agree on the same value

• Integrity

• Every correct node decides at most once

COMP 4137/COMP 7200

Page 52



Consensus Properties

• Termination

• Every correct node must decide at the end of protocol

• Safety

• Every correct node must not agree on incorrect value

• Liveness

• Every correct value must be accepted

COMP 4137/COMP 7200

Page 53



When Failure Happens

• If no failure or malice, easy to reach a consensus

▪

Individuals broadcast their values to all nodes

▪ Values received with a pre-defined timeframe

(synchronous)

• What if there are failures or malicious activities in the network?

COMP 4137/COMP 7200

Page 54



When Failure Happens

• Common types of failure

• Crash Fault: Node crashed, offline during communication

• Network Fault: Not all pairs of nodes well- connected (partitioned

network), latency (no notion of global time)

• Byzantine Fault: Nodes may be malicious

• Achieving consensus in the faulty (yet realistic) environment is
hard

COMP 4137/COMP 7200

Page 55



Synchronous vs. Asynchronous Systems

▪   Synchronous system

• Defined maximum waiting time for message transmission
• Easy to reach a consensus

▪ Asynchronous system

• Undefined waiting time

• Hard to achieve a consensus

COMP 4137/COMP 7200

Page 56



Single Server Architecture

State Machine Replication

COMP 4137/COMP 7200

Page 57



Single Server Architecture

• A single point of failure!

State Machine Replication

COMP 4137/COMP 7200

Page 58



State Machine Replication (SMR)

State Machine Replication

• Interactive protocol among servers

• State machine replication gives safety and liveness.

COMP 4137/COMP 7200

Page 59



State Machine Replication (SMR)

State Machine Replication

• Replicas maintain the same state
• Replicas start in the same state
• Operations are deterministic
• Replicas execute operations in the same order (i.e., total

order)

• Replicas send replies to clients
• Clients vote on replica replies

COMP 4137/COMP 7200

Page 60



Roughly, Consensus: All About Achieving “Total Order”

• Blockchains (modeled as state machine replication)

[Lamport, ACM TOPLAS 1984]

$100

$100

$100

COMP 4137/COMP 7200

Page 61



The “Total Order” Requirement

Client 1:
“Deposit $100”

Client 1:
“Deposit $100”

$200

$200

$100

$100

$100

COMP 4137/COMP 7200

Page 62



The “Total Order” Requirement

Client 1:
“Deposit $100”

Chase:
“Charge 10%”

$200

$180

Client 1:
“Deposit $100”

Chase:
“Charge 10%”

$180

$200

$100

$100

$100

COMP 4137/COMP 7200

Page 63



The “Total Order” Requirement

Client 1:
“Deposit $100”

Chase:
“Charge 10%”

$200

$180

Client 1:
“Deposit $100”

Chase:
“Charge 10%”

$180

$200

$100

$100

$100

COMP 4137/COMP 7200

Page 64



The “Total Order” Requirement

Chase:
“Charge 10%”

Client 1:
“Deposit $100”

Chase:
“Charge 10%”

$90

$90

Client 1:
“Deposit $100”

$190

$190

$100

$100

$100

COMP 4137/COMP 7200

Page 65



The “Total Order” Requirement

Chase:
“Charge 10%”

Client 1:
“Deposit $100”

$90

$190

Client 1:
“Deposit $100”

Chase:
“Charge 10%”

$180

$200

$100

$100

$100

COMP 4137/COMP 7200

Page 66



The two generals paradox

• Two armies have surrounded a city
• Their generals must decide together whether to attack or retreat
• Communication through messengers, must pass through the city and

might be intercepted

• Both must take the same decision

General A

General B

Page 67



Easy enough… or not?

We attack tomorrow at dawn.

Did they get my message? I can’t attack just yet.

Agreed, we attack tomorrow at dawn.

Did they get the confirmation? If not, they won’t
attack…

Confirmation has been received.

General A

Did they get my confirmation? If not, they won’t
attack…

COMP 4137/COMP 7200

General B

Page 68



Probably not…

I confirm receiving the confirmation.

Did they get my last message? If not, they won’t
attack…

I confirm receiving the confirmation.

Did they get my last message? If not, they won’t
attack…

General A

…

COMP 4137/COMP 7200

General B

Page 69



The two generals paradox

• No protocol exists that guarantees both generals are 100% certain of

the decision of the other

▪ Proofs exist

• After 500 confirmations, both would be pretty sure the other will

attack

• But “pretty sure” is not guaranteed 100% certainty

COMP 4137/COMP 7200

70



The two generals paradox

Simplified impossibility proof:

▪ Let’s assume a protocol that exchanges N messages exists, which

guarantees certainty

▪ The Nth message could be lost… meaning, the first N-1 messages

must be sufficient to guarantee certainty

▪ Therefore, there exists such a protocol which exchanges N-1

messages

▪ Absurd conclusion: there exists such a protocol that exchanges 0

messages

COMP 4137/COMP 7200

71



The odd conclusion

• Through an unreliable network, two nodes cannot 100% agree even

on a single bit

• Perfect state consistency is not achievable over unreliable networks –

but in practice, that’s not required

• Protocols exist that mitigate message delivery uncertainty, typically

using retries, ACKs, and timeouts

▪ TCP though it does not really solve the problem…

COMP 4137/COMP 7200

72



TCP does not solve two generals paradox

Untrusted communication channel

A

B

FIN

ACK

FIN

ACK

This solution leads to a half-open
connection.

TCP does not solve two generals
problem!

COMP 4137/COMP 7200

73



The problem of Byzantine Generals

• Generalization of Two Generals

• N generals, decision to attack or retreat based on majority vote

• Some generals might be secretly traitors, and try to manipulate the

vote…

• Goal: achieve consensus between honest nodes

COMP 4137/COMP 7200

74



The problem of Byzantine Generals

• #1 wants to attack
• #3 wants to retreat

I vote that we retreat

I vote that we attack

1

2

3

• #1 receives retreat votes from #2 and #3
• #3 receives attack votes from #1 and #2

• Result: #3 attacks alone, #1 retreats

COMP 4137/COMP 7200

75



Consensus Algorithms

• Paxos

• Majority rule, asynchronous setting
• Consistency, fault-tolerance, but may get stuck (2 out of 3 rule) Byzantine-fault

intolerance

• Raft

• Leader-Follower model
• Choose 2 in 3: Safety, Liveness, Fault-Tolerance Byzantine-fault

intolerance

• http://thesecretlivesofdata.com/raft/ (animated example)

• BFT

• Byzantine-fault tolerance

COMP 4137/COMP 7200

Page 76



Paxos

[Lamport, ACM TOCS 1998]; going
back to 1989

[Lamport. Paxos made simple.
ACM SIGACT News 2001]

“For fundamental contributions to the theory and practice of
distributed and concurrent systems, notably the invention of
concepts such as causality and logical clocks, safety and liveness,
replicated state machines, and sequential consistency.”

Turing Award 2013

COMP 4137/COMP 7200

Page 77



Byzantine Fault-Tolerant SMR (BFT Protocols)
• Traditionally important

• Powerful: Byzantine/arbitrary failures & attacks
• Systems, distributed systems, theory, crypto, security, …

• Recently gain prominence
• Real threats to real systems
• Blockchains
• Mission-critical systems (SpaceX)
• …

COMP 4137/COMP 7200

Page 78



Consensus in Public Blockchain

• Traditional consensus works on closed environment

• Nodes know addresses of their peers Every node accesses a

shared memory

• Public blockchain is an open P2P system
• Where to keep shared memory in P2P?
• Anyone can join and leave the network at anytime How to enable

consensus in an open system?

Signed by Bob

Pay to pkBob: H ()

Alice is offline

All nodes must agree on the validity of the Bob’s transaction

COMP 4137/COMP 7200

Page 79



Consensus in Public Blockchain

• At any given time:
• All nodes have a sequence of blocks of transactions
• they have reached a consensus on (block of committed transactions)

• Each node has a set of outstanding transactions
• that need to be validated against block of committed transactions
outstanding transactions

block of committed transactions

Tx
Tx
…
Tx

Tx
Tx
…
Tx

Tx
Tx
…
Tx

Validate

Tx
Tx
…
Tx

Tx
Tx
…
Tx

Tx
Tx
…
Tx

COMP 4137/COMP 7200

Page 80

Block-based consensus



Consensus in Public Blockchain

▪ Bitcoin introduces incentive concept for honest actions

• Possible as Bitcoin is a digital currency

▪   Embrace randomness

• Does away with the notion of a specific end-point
• Consensus happens over long-time scales – approx. 1 hour
▪   Blockchain consensus works better in practice than in theory

• Theory is catching up
• Theory is still very important as It can help predict unforeseen attacks

COMP 4137/COMP 7200

Page 81



Summary

• Centralized systems vs distributed systems

• Architectures: client/server model, peer-to-peer models

• Distributed Algorithms: consensus, fault-tolerance

