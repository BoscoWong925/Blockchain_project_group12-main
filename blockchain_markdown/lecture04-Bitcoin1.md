COMP4137 Blockchain Technology and Applications
COMP7200 Blockchain Technology

Lecturer: Dr. Hong-Ning Dai (Henry)

Lecture 4
Bitcoin Basics



Cryptocurrency

Bitcoin

Ethereum

Satoshi Nakamoto
中本聰

Vitalik Buterin

https://vitalik.ca/index.html

COMP4137/COMP7200

2



Outline

• Hash Function and Merkle Tree
• Elliptic Curve Cryptography (ECC)

COMP4137/COMP7200

3



Hash Functions

• A hash function maps/compresses messages of  arbitrary lengths to

an m-bit output

• Output known as the fingerprint or the message digest

• What is an example of hash functions?

• Given a hash function that maps Strings to integers in [0,232-1]

• A hash function is a many-to-one function, so collisions must happen.
• Hash functions are used in a number of data structures

Long message of
arbitrary length

𝑚

Hash

𝐻(𝑚)

Short message of
fixed length

|𝐻(𝑚)|≪ |𝑚|

|𝐻(𝑚)| = {160, 256, 384, 512} (preferred 256 bits)

4



Hash Functions

• Currently popular Hash algorithms include MD5, SHA-1, and SHA-2.

• MD4 (RFC 1320) was designed by Ronald L. Rivest of MIT in 1990. MD

is an acronym for Message Digest. Its output is 128 bits. MD4 has
proven to be insufficiently secure.

• MD5 (RFC 1321) is an improved version of MD4 by Rivest in 1991. It
still groups the inputs in 512 bits and the output is 128 bits. MD5 is
more complex than MD4 and is slower and safer to calculate. MD5
has proven not to be "strong resistant collision".

COMP4137/COMP7200

5



Hash Functions

• Currently popular Hash algorithms include MD5, SHA-1, and SHA-2.

• SHA (Secure Hash Algorithm) is a family of Hash functions. The first

algorithm was released in 1993 by NIST (National Institute of Standards and
Technology).

• The well-known SHA-1 was introduced in 1995, and its output is a 160-bit

hash value, so it is better against exhaustiveness. The SHA-1 design is based
on the same principle as MD4 and mimics the algorithm. SHA-1 has been
proven not to be "strong resistant collision".

• To improve security, NIST also designed SHA-224, SHA-256, SHA-384, and

SHA-512 algorithms (collectively referred to as SHA-2), similar to the SHA-1
algorithm. SHA-3 related algorithms have also been proposed.

COMP4137/COMP7200

6



Security Requirements for Cryptographic Hash Functions

• Given a function H: m → H(m), then we say that H is:
• One-way property:

• Given H(m), it is computationally infeasible to find a value m
easy

m

hard✕

H(m)

• Weak collision resistant:

• Given an arbitrary m, it is computationally infeasible to find some m’ s.t.

H(m’) = H(m)

• Strong collision resistant:

• It is computationally infeasible to find any two distinct values m1,m2, s.t.

H(m1) = H(m2)

COMP4137/COMP7200

7



Chained Hash

• More general construction than one-way hash chains

• Useful for authenticating a sequence of data values 𝐷0 , 𝐷1 , … , 𝐷 n

• 𝐻∗ authenticates the entire chain

𝐻∗

𝐷0

𝐻0

𝐷n-2

𝐷n- 1

…

𝐻n-2

𝐻n-1
𝐻( 𝐷 n - 1 ||𝐻n-1)

𝐻n-2=

𝐷n

𝐻n-1=𝐻(𝐷n)

COMP4137/COMP7200

Page 8



Merkle Tree

• Introduced by Ralph Merkle, 1979
• “Classic” cryptographic construction
• Involves combining hash functions on binary tree structure

• An authentication scheme

• Using only one-way hash function as building blocks

• An efficient data structure with many practical applications
• Blockchain, privacy protection, integrity check, quick search, …

COMP4137/COMP7200

9



Merkle Tree Data Structure

• A binary tree over data values for authentication purpose
• Verifier stores the root as the commitment of the Merkle tree

COMP4137/COMP7200

10



Merkle Tree Data Structure

• Binary tree, nodes are assigned values (e.g. 160 bits)
• Extra, secret values associated to each leaf

11



Example

• Binary tree, nodes are assigned values (e.g. 160 bits)
• Extra, secret values associated to each leaf

71ea3409e9a9c749
5d07454cb35bb6c0

2b0e94fb301bedb5
0bb0d5ff0892ec4f

d42e2c85ca55d540
0334757a8503addd

e4da3b7fbbce2345d
7772b0674a318d5

d1fe173d08e95939
7adf34b1d77e88d7

aab3238922bcc25a
6f606eb525ffdc56

37693cfc748049e45
d87b8c7d8b9aacd

5

79

14

23

12



Setup

• Computing the tree and root hash

• Prepare leaf secrets si
• Use hash function to get leaf / interior node values
• Generate root hash P

• Complexity analysis

• Tree of height H has N = 2H leaf nodes
• Nodes at height H will depend on 2H leaf values
• Obtaining P requires calculating all N leaf values plus 2H-1 more hash function

evaluations

COMP4137/COMP7200

13



Authenticating A Secret

• Prover wishes to reveal si to identify herself

• Prover sends i, si
• Additional data required: “sibling node” values

• Verifier checks si against the public root hash P

• Hash first si
• Hash result together with its sibling in tree
• Repeat, moving up tree
• Check result with root

COMP4137/COMP7200

14



Sibling Node Values Required

Sibling nodes required
to authenticate secret

Root value is public

s0

1. Verify secret value by hashing, then hashing together with sibling, etc.
2. Accept if the computed root hash matches with the root value

COMP4137/COMP7200

15



Public Key Infrastructure (PKI) Scenario

• Alice and Bob have public key certificates issued by certificate

authority (CA).

• Alice wishes to perform a transaction with Bob and sends him her

public key certificate.

• Bob is concerned that Alice's private key may have been

compromised, sends a request to CA that contains Alice's certificate
serial number.

COMP4137/COMP7200

16



What can PKI enable?

• Secure Email – sign and/or encrypt messages
• Secure browsing – SSL – authentication and encryption
• Secure code – authenticode
• Secure wireless – PEAP & EAP-TLS
• Secure documents – Rights Management
• Secure networks – segmentation via IPsec
• Secure files – Encrypted File System(EFS)



Public Key Infrastructure Scenario

• Receiving the query, CA checks the revocation status of Alice's

certificate.

• CA maintains the certificate database.
• The database is the only trusted location where a compromise to Alice's

certificate would be recorded.

• CA confirms that Alice's certificate is still OK
• returns a signed, successful 'response' to Bob.

• Bob verifies the signed response using CA's public key.

COMP4137/COMP7200

18



A Large Amount of enquiries?

• When Alice has a large number of certificates that require CA to

respond

• A naive approach requires CA to sign each response
• Bob needs to verify the CA’s signatures in turn

Low
Efficiency!

• Merkle tree can improve efficiency and only requires one signature

on the root hash

• Batch Verification: utilize the root hash to quickly verify the integrity of

a batch of certificates

COMP4137/COMP7200

19



Merkle Tree Scheme

• Construct Merkle hash tree by computing

hashes recursively
• h is hash function
• Ci is certificate i

• Root hash (i.e., h(1,4)) is published

• Root hash is signed by CA to ensure the

value’s integrity

COMP4137/COMP7200

20



Validation

• To validate C1:

• Compute h(1, 1)
• Obtain h(2, 2)
• Compute h(1, 2)
• Obtain h(3, 4)
• Compute h(1,4)
• Compare to known h(1, 4)

• Need to know siblings of nodes on path from

C1 to the root

• The proof from CA consists of these hashes (in

rectangles on the left)

?= h(1, 4)

COMP4137/COMP7200

21



Example

• C1: I
• C2: Love
• C3: E-Payment and
• C4: Cryptocurrency
• Hash Function: SHA-1
• http://www.sha1-online.com/

• h(1,4)?

COMP4137/COMP7200

22



H(1,1) & H(2,2)

COMP4137/COMP7200

23



Example

• h(1,4)?
• h(1,1)=ca73ab65568cd125c2d27a22bbd9e863c10b675d

• h(2,2)=4f61ec4d2d1fd181ec25797e1d8d2400c5b04f24

• h(3,3)=ea049bd6063f621ec4d1ce6fa70a3c9382c59364

• h(4,4)=3f9b3fd3271d34c9b292f15cd52d0e3b71499428

• h(1,2)=eb42ab5639880ef199cbf4e86d9ec4fad2891023

• h(3,4)=362121ce0c2a5d3a5a37463fbb0f17eb7edc47c5

• h(1,4)=7039ef1cb6974943aab0c1d79b016c4410377bbe

h(1,2)
=hash(h(1,1)||h(2,2))
=hash(ca73ab65568cd125c2d27a22bbd9e863c10b67
5d4f61ec4d2d1fd181ec25797e1d8d2400c5b04f24)
=eb42ab5639880ef199cbf4e86d9ec4fad2891023

COMP4137/COMP7200

24



Merkle Tree in Blockchain

• We build a Merkle Tree for many transactions, and store the root in

the block header.

• Can easily check whether transactions stored in a block have been modified
• Enable efficient membership proofs for transactions in a block, which are

necessary for Simple Payment Verification (SPV) nodes that only store block
headers and not block contents.

• Just concatenate all TXs and store the hash in header?
• Not efficient for membership proof – O(n) complexity
• Efficient with Merkle tree – O(log(n)) complexity

COMP4137/COMP7200

25



Merkle Hash Tree in Blockchain

Hash chain of blocks

prev: H( )

trans: H( )

prev: H( )

trans: H( )

prev: H( )

trans: H( )

Hash tree (Merkle tree) of
transactions in each block

H( ) H( )

H( ) H( )

H( ) H( )

transaction

transaction

transaction

transaction

COMP4137/COMP7200

Page 26



Outline

• Merkle Tree
• Elliptic Curve Cryptography (ECC)

COMP4137/COMP7200

27



Public key cryptography

• Recall

• RSA algorithm
• Diffie-Hellman key exchange algorithm

• What you need for a public key cryptographic system to work is a set of
algorithms that is easy to process in one direction, but difficult to undo.

• These algorithms serve as trap door functions

• Finding a good Trapdoor Function is critical for a secure public key

cryptographic system.

COMP4137/COMP7200

Page 28



Motivation

▪ Problem:

Asymmetric schemes like RSA and El Gamal require exponentiations
in integer rings and fields with parameters of more than 1,000 bits.

▪ High computational effort on CPUs with 32-bit or 64-bit arithmetic
▪ Large parameter sizes critical for storage on small and embedded device

▪ Motivation:

Smaller field sizes providing equivalent security are desirable

▪ Solution:

Elliptic Curve Cryptography (ECC) uses a group of points (instead of
integers) for cryptographic schemes with coefficient sizes of 160-256
bits, reducing significantly the computational effort.

COMP4137/COMP7200

Page 29



What is an Elliptic Curve?

• An Elliptic Curve E is a curve given by an equation

E : y2 = f(x),

where f(x) is a square-free (no double roots) cubic (x3)

or a quartic polynomial (x4).

After a change of variables, it takes a simpler form:

E : y2 = x3 + Ax + B

So, y2 = x3 is not an elliptic curve but y2 = x3-1 is

COMP4137/COMP7200

Page 30



What exactly is an elliptic curve?

• Let A∈ℝ, B∈ℝ, be constants such that 4A³ + 27B² ≠ 0. A non-singular
elliptic curve is the set E of points (x, y) ∈ℝ x ℝ described by the
equation:

y² = x³ + Ax + B

together with a special point O called the point
at infinity.

COMP4137/COMP7200

31



Computations on Elliptic Curves

• In cryptography, we are interested in elliptic curves module a prime p:

Definition: Elliptic Curves over prime fields

The elliptic curve over Zp, p>3 is the set of all
pairs (x,y) ∈ Zp which fulfill

y2 = x3 + Ax + B mod p

together with an imaginary point of infinity O,
where A,B ∈ Zp fulfill the condition

4A3+27B2 ≠ 0 mod p.

• Note that Zp = {0,1,…, p -1} is a set of integers

with modulo p arithmetic

COMP4137/COMP7200

Page 32



Computations on Elliptic Curves

▪Some special considerations are required to convert elliptic

curves into a group of points

• In any group, a special element is required to allow for the identity operation,

i.e., given P ∈ E: P + O = P = O + P

• This identity point (which is not on the curve) is additionally added to the

group definition

• This (infinite) identity point is denoted by O

▪Elliptic Curve are symmetric along the x-axis

• Up to two solutions y and -y exist for each quadratic residue x of the elliptic

curve

• For each point P =(x,y), the inverse or negative point is defined as -P =(x,-y)

y

O

P

-P

x

COMP4137/COMP7200

Page 33



Computations on Elliptic Curves

▪ Generating a group of points on elliptic curves
based on point addition operation P+Q = R, i.e.,
(xP,yP)+(xQ,yQ) = (xR,yR)

▪ Geometric Interpretation of point addition operation

y

▪ Draw straight line through P and Q; if P=Q use

tangent line instead

▪ Mirror third intersection point of drawn line with

the elliptic curve along the x-axis

P

Point Addition

R=P+Q

▪ Elliptic Curve Point Addition and Doubling Formulas

x

Q

-R

COMP4137/COMP7200

Page 34



Computations on Elliptic Curves

▪ Generating a group of points on elliptic curves
based on point addition operation P+Q = R, i.e.,
(xP,yP)+(xQ,yQ) = (xR,yR)

▪ Geometric Interpretation of point addition operation

y

▪ Draw straight line through P and Q; if P=Q use

tangent line instead

▪ Mirror third intersection point of drawn line with

the elliptic curve along the x-axis

tangent line

P (Q)

▪ Elliptic Curve Point Addition and Doubling Formulas

Point Doubling

x

2P=P+P

COMP4137/COMP7200

Page 35



Computations on Elliptic Curves

▪ Elliptic Curve Point Addition and Doubling Formulas

x3 = s2 −x1−x2 mod p  and y3 = s(x1 −x3)−y1 mod p

where

s =

; if P ≠ Q (point addition)

; if P = Q (point doubling)

Example: Given E: y2 = x3+2x+2 mod 17 and point P=(5,1)
Goal: Compute 2P = P+P = (5,1)+(5,1)= (x3,y3)

[2]

s =               (mod 17) = (2 · 1)−1(3 · 52 + 2) (mod 17) = 2−1 · 9 ≡ 217-2 9 (mod 17) ≡ 9 · 9 ≡ 13 (mod 17)

x3 = s2 − x1 − x2 = 132 − 5 − 5 = 159 ≡ 6 (mod 17)
y3 = s(x1−x3) − y1 = 13(5 − 6) − 1= −14 ≡ 3 (mod 17)

[1] https://en.wikipedia.org/wiki/Modular_arithmetic
[2] https://en.wikipedia.org/wiki/Modular_multiplicative_inverse

COMP4137/COMP7200

Finally 2P = (5,1) + (5,1) = (6,3)

Page 36

pxxyymod1212−−pyaxmod23121+12123yax+

Addition of Points on E

1. Commutativity.  P1 + P2 = P2 + P1

2. Existence of identity. P + O = P

3. Existence of inverses.  P + (-P) = O

4. Associativity. (P1+P2) + P3 = P1+(P2+P3)

The point at infinity O, is the identity element.

• Online visual tool for elliptic curve: https://andrea.corbellini.name/ecc/interactive/reals-add.html

COMP4137/COMP7200

Page 37



ECC’s trapdoor function

• We start with an arbitrary point on the
curve. Next, we use the dot function to
find a new point. Finally, we keep
repeating the dot function to hop around
the curve until we finally end up at our
last point.

-C

Starting at A:
• A dot B = -C (Draw a line from A to B and it intersects at -C)
• Reflect across the X-axis from -C to C
• A dot C = -D (Draw a line from A to C and it intersects -D)
• Reflect across the X-axis from -D to D
• A dot D = -E (Draw a line from A to D and it intersects -E)
• Reflect across the X-axis from -E to E

COMP4137/COMP7200

Page 38



ECC’s trapdoor function

• This is a great trapdoor function because if
you know where the starting point (A) is
and how many hops are required to get to
the ending point (E).

• It’s very easy to find the ending point.
• If all you know is where the starting point

and ending point are, it’s nearly
impossible to find how many hops it took
to get there.

Public Key: Starting Point A, Ending Point E
Private Key: Number of hops from A to E

COMP4137/COMP7200

Page 39



Elliptic Curve Cryptography

Suppose that you are given two points P and Q in E(Fp).
The Elliptic Curve Discrete Logarithm Problem (ECDLP)
is to find an integer m satisfying

m summands

Q = P + P + … + P = mP.
▪ Cryptosystems are based on the idea that m is large and kept secret

and attackers cannot compute it easily

• If m is known, an efficient method to compute the point

multiplication mP is required to create a reasonable cryptosystem

• The extreme difficulty of the ECDLP yields highly efficient

cryptosystems.

COMP4137/COMP7200

Page 40



Elliptic Curve Diffie-Hellman Key Exchange

Public Knowledge: A group E(Fp) and a point P of order n.

BOB                                                            ALICE

Choose secret 0 < b < n                 Choose secret 0 < a < n

Compute QAlice = aP
to Alice

Compute QBob = bP
Send QBob
to Bob                                                Send QAlice
Compute bQAlice
Bob and Alice have the shared value bQAlice = abP = aQBob

Compute aQBob

COMP4137/COMP7200

Page 41



Curve secp256k1

• The curve used by Bitcoin is secp256k1
• The curve is y2 = x3 + 7 mod p, where p is a 256-bit prime number:

Note that because secp256k1
is actually defined over the
field Zp, its graph will in reality
look like random scattered
points, not anything like this.

https://en.bitcoin.it/wiki/Secp256k1

COMP4137/COMP7200

42



Curve secp256k1

• p = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF
(hex version)

FFFFFFFF FFFFFC2F

• The base point is P = (x, y) where

• x = 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D 59F2815B

16F81798

• y = 483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419

9C47D08F FB10D4B

• The order n of P is a 256-bit prime (s.t. nP = O), where

• n = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF BAAEDCE6 AF48A03B BFD25E8C

D0364141

COMP4137/COMP7200

43



ECDSA in Bitcoin

• ECDSA - Elliptic Curve Digital Signature Algorithm

• Private Key: k in {1, …, n-1}
• Public Key:
• U = kP
• An elliptic curve (i.e., secp256k1)
• P, elliptic curve base point
• n, integer order of P, means that n*P = O, where O is the identity

element.

COMP4137/COMP7200

44



Signature Generation

• To Sign message m

1. Compute e = Hash(m)
2. Pick a random j from

{1, …, n-1}

3. Compute jP = (x, y), and

r = x mod n

4. Compute s = j-1(e + kr)

mod n

5. Output (r, s) as the
signature on m

COMP4137/COMP7200

45



Signature Verification

• Given message m, signature (r, s), public key U, verification consists of

the following steps:

1. Compute e = Hash(m)
2. Compute u = es-1 mod n, and v = rs-1 mod n
3. Compute Q = uP + vU := (x, y)
// remember, Q is a point

4. Accept if and only if r = x mod n

• Proof:

Q = uP + vU = es-1P + rs-1U = es-1P + rs-1kP = s-1(e+rk)P,  s-1 = j(e + kr)-1
So, Q = jP := (x, y)
(We are calculating the same point Q=jP, just with a different set of equations.)

COMP4137/COMP7200

46



Implementations in Hardware and Software

▪ Elliptic curve computations usually regarded as consisting of four

layers:

▪ Basic modular arithmetic operations are computationally most expensive
▪ Group operation implements point doubling

and point addition

▪ Point multiplication can be implemented using the Double-and-Add

method

▪ Upper layer protocols like ECDH and ECDSA

▪ Most efforts should go in optimizations of the modular arithmetic

operations, such as

▪ Modular addition and subtraction
▪ Modular multiplication
▪ Modular inversion

COMP4137/COMP7200

Page 47

Protocol(ECDSA)Point Multiplication (k·P)Group OperationP+Q, 2·PModular Arithmetic( +, -, x , ÷  )

Summary

• Merkle Tree is based on Tree and Hash
• Merkle Tree Root is public for verification (integrity, membership)
• In blockchain, we build a Merkle Tree for transactions, and store the root in the

block header

• The non-singular elliptic curve is the set of points and the point at infinity O
• The point at infinity O is the identity element
• Elliptic Curve Cryptography is based on elliptic curve logarithm problem
• In Bitcoin, we use Elliptic Curves Modulo p (secp256k1)
• Bitcoin uses Elliptic Curve Digital Signature Algorithm (ECDSA)

COMP4137/COMP7200

48

