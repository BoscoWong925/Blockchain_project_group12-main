COMP4137 Blockchain Technology and Applications
COMP7200 Blockchain and Cryptocurrencies

Lecturer: Dr. Hong-Ning Dai (Henry)

Lecture 2
Cryptographic Primitives



Outline

• Introduction to Cryptography

• Classical ciphers

• Computer Cryptography

COMP4137/COMP7200

2



Cryptography  Security

▪ Cryptography may be a component of a secure system

▪ Adding cryptography may not make a system secure

COMP4137/COMP7200

3



Terms

Plaintext (cleartext) is denoted by message M

Encryption is denoted by function E(M)

It then produces ciphertext denoted by C=E(M)

Decryption the ciphertext and obtain original message M=D(C)

Cipher: Cryptographic algorithm

COMP4137/COMP7200

4



Terms: types of ciphers

• Restricted cipher

• Symmetric algorithms

• Public key algorithms

COMP4137/COMP7200

5



Restricted cipher

Secret algorithm
• Leaking
• Reverse engineering

• HD DVD (Dec 2006) and Blu-Ray (Jan 2007)
• RC4
• All digital cellular encryption algorithms
• DVD and DIVX video compression
• Firewire
• Enigma cipher machine
• Every NATO and Warsaw Pact algorithm during Cold War

COMP4137/COMP7200

6



The key

BTW, the above is a bump key. See http://en.wikipedia.org/wiki/Lock_bumping .

7



The key

• Lock without key

Source: en.wikipedia.org/wiki/Pin_tumbler_lock

COMP4137/COMP7200

8



The key

• Insert Key into Lock

Source: en.wikipedia.org/wiki/Pin_tumbler_lock

COMP4137/COMP7200

9



The key

• We understand how it

works:

• Strengths
• Weaknesses

• Based on this

understanding, we can
assess how much to trust
the key & lock.

Source: en.wikipedia.org/wiki/Pin_tumbler_lock

COMP4137/COMP7200

10



Symmetric algorithm

Secret key

C = EK(M )

M = DK(C )

COMP4137/COMP7200

11



Public key algorithm

Public key and private keys

C1 = Epublic(M )
M = Dprivate(C1 )

also:

C2 = Eprivate(M )
M = Dpublic(C2 )

COMP4137/COMP7200

12



McCarthy’s puzzle (1958)

• Two countries are at war
• One country sends spies to the other country
• To return safely, spies must give the border guards a password

• Spies can be trusted
• Guards chat – information given to them may leak

Challenge!

How can a guard authenticate a person without
knowing the password?

Enemies cannot use the guard’s knowledge to
introduce their own spies

COMP4137/COMP7200

13



Solution to McCarthy’s puzzle

Michael Rabin, 1958

Use one-way function, B=f(A)

• Guards get B …

• Enemy cannot compute A
• Spies give A, guards compute f(A)

• If the result is B, the password is correct.

Example function:
Middle squares

• Take a 100-digit number (A), and square it
• Let B = middle 100 digits of 200-digit result

COMP4137/COMP7200

14



McCarthy’s puzzle example

Example with an 18 digit number
A = 289407349786637777
A2 = 83756614110525308948445338203501729
Middle square, B = 110525308948445338

Given A, it is easy to compute B
Given B, it is extremely hard to compute A

COMP4137/COMP7200

15



One-way functions

• Easy to compute in one direction
• Difficult to compute in the other

Examples:

Factoring:
pq = N
find p,q given N

Discrete Log:

EASY
DIFFICULT

ab mod c = N
EASY
find b given a, c, N DIFFICULT

COMP4137/COMP7200

16



More terms

• one-way function

• Rabin, 1958: McCarthy’s puzzle
• middle squares, exponentiation, …

• [one-way] hash function

• message digest, fingerprint, cryptographic checksum, integrity check

• encrypted hash

• message authentication code
• only possessor of key can validate message

COMP4137/COMP7200

17



More terms

• Stream cipher

• Encrypt a message a character at a time

• Block cipher

• Encrypt a message a chunk at a time

• Digital Signature

• Authenticate, not encrypt message
• Use pair of keys (private, public)
• Owner encrypts message with private key
• Sender validates by decrypting with public key
• Generally use hash(message).

COMP4137/COMP7200

18



Outline

• Introduction to Cryptography

• Classical ciphers

• Computer Cryptography

COMP4137/COMP7200

19



Cryptography: what is it good for?

• Authentication

• determine origin of message

• Integrity

• verify that message has not been modified

• Nonrepudiation

• sender should not be able to falsely deny that a message was sent

• Confidentiality

• others cannot read contents of the message

COMP4137/COMP7200

20



Cæsar cipher

Earliest documented military use of cryptography

Julius Caesar  c. 60 BC

•
• shift cipher: simple variant of a substitution cipher
• each letter replaced by one n positions away

modulo alphabet size

n = shift value = key

Similar scheme used in India

• early Indians also used substitutions based on phonetics

similar to pig latin

Last seen as ROT13 on usenet to keep the reader from seeing offensive messages

unwillingly

COMP4137/COMP7200

21



Cæsar cipher

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

COMP4137/COMP7200

22



Cæsar cipher

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z A B C D E F G H I J K L M N O P Q R S T

shift alphabet by n (6)

COMP4137/COMP7200

23



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

COMP4137/COMP7200

24



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

G

COMP4137/COMP7200

25



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GS

COMP4137/COMP7200

26



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSW

COMP4137/COMP7200

27



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWU

COMP4137/COMP7200

28



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWUN

COMP4137/COMP7200

29



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWUNB

COMP4137/COMP7200

30



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWUNBU

COMP4137/COMP7200

31



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWUNBUM

COMP4137/COMP7200

32



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWUNBUMZ

COMP4137/COMP7200

33



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWUNBUMZF

COMP4137/COMP7200

34



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWUNBUMZFY

COMP4137/COMP7200

35



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWUNBUMZFYU

COMP4137/COMP7200

36



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWUNBUMZFYUM

COMP4137/COMP7200

37



Cæsar cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

U V W X Y Z

A B C D E F G H I J K L M N O P Q R S T

GSWUNBUMZFYUM

• Convey one piece of information for decryption: shift value

• trivially easy to crack (26 possibilities for a 26 character alphabet)

COMP4137/COMP7200

38



Ancient Hebrew variant (ATBASH)

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

Z Y X W V U

T S R Q P O N M L K J I H G F E D C B A

NBXZGSZHUOVZH

• c. 600 BC
• No information (key) needs to be conveyed!

COMP4137/COMP7200

39



Substitution cipher

MY CAT HAS FLEAS

A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

M P S R L Q

E A J T N C I F Z WO Y B X G K U D V H

IVSMXAMBQCLMB

• General case: arbitrary mapping
• both sides must have substitution alphabet

COMP4137/COMP7200

40



Substitution cipher

Easy to decode:

• vulnerable to frequency analysis

Moby Dick
(1.2M chars)

Shakespeare
(55.8M chars)

e  12.300%
o   7.282%
d   4.015%
b   1.773%
x   0.108%

e  11.797%
o   8.299%
d   3.943%
b   1.634%
x   0.140%

COMP4137/COMP7200

41



Statistical Analysis

Letter frequencies
E: 12%
A, H, I, N, O, R, S, T: 6 – 9%
D, L: 4%
B, C, F, G, M, P, U, W, Y: 1.5 – 2.8%
J, K, Q, V, X, Z: < 1%

Common digrams:

TH, HE, IN, ER, AN, RE, …

Common trigrams

THE, ING, AND, HER, ERE, …

Strong password:
• At least 12 characters long but 14 or more is

better.

• A combination of uppercase letters,

lowercase letters, numbers, and symbols.

COMP4137/COMP7200

42



Outline

• Introduction to Cryptography

• Classical ciphers

• Computer Cryptography

COMP4137/COMP7200

43



Popular symmetric algorithms

DES - Data Encryption Standard

• 1976

IDEA - International Data Encryption Algorithm

• 1992
• 128-bit keys, operates on 8-byte blocks (like DES)
• algorithm is more secure than DES

RC4, by Ron Rivest

• 1995
• key size up to 2048 bits
• not secure against multiple messages encrypted with the same key

AES - Advanced Encryption Standard

• NIST proposed successor to DES, chosen in October 2000
• based on Rigndael cipher
• 128, 192, and 256-bit keys

COMP4137/COMP7200

44



DES

• Data Encryption Standard

• adopted as a federal standard in 1976

• block cipher, 64-bit blocks
• 56 bit key

• all security rests with the key

• substitution followed by a permutation (transposition)

• same combination of techniques is applied on the plaintext block 16 times

COMP4137/COMP7200

45



DES

64-bit plaintext block

initial permutation, IP

48-bit subkey
permuted from key

left half, L0

right half, R0

16 rounds

L1= R0

L15= R14

f

f

K1

R1 = L0  f(R0, K1)

R15 = L14  f(R14, K15)

K16

R16 = L15  f(R15, K16)

L16 = R15

final permutation, IP-1

64-bit ciphertext block

COMP4137/COMP7200

46



DES: f

DATA: right 32 bits

KEY: 56 bits

48 bits

48 bits

S

S

S

S

S

S

S

S

DATA: left 32 bits

New DATA:
right 32 bits

COMP4137/COMP7200

47



DES: S-boxes

• After compressed key is XORed with expanded block

• 48-bit result moves to substitution operation via 8 substitution boxes (s-boxes)

• Each S-box has
• 6-bit input
• 4-bit output

• 48 bits divided into eight 6-bit sub-blocks
• Each block is operated by a separate S-box
• key components of DES’s security
• net result: 48-bit input generates 32-bit output

COMP4137/COMP7200

48



Is DES secure?

56-bit key makes DES relatively weak

• 7.2×1016 keys
• Brute-force attack

Late 1990’s:

• DES cracker machines built to crack DES keys in a few hours
• DES Deep Crack: 90 billion keys/second
• Distributed.net: test 250 billion keys/second

COMP4137/COMP7200

49



The power of 2

Adding an extra bit to a key doubles the search space.

Suppose it takes 1 second to attack a 20-bit key:

•21-bit key: 2 seconds
•32-bit key: 1 hour
•40-bit key: 12 days
•56-bit key: 2,178 years
•64-bit key: >557,000 years!

COMP4137/COMP7200

50



Increasing The Key

Can double encryption work for DES?

• Useless if we could find a key K such that:

EK(P) = EK2(EK1(P))

• This does not hold for DES

COMP4137/COMP7200

51



AES

From NIST:

Assuming that one could build a machine that could recover a DES key in a
second (i.e., try 256 keys per second), then it would take that machine
approximately 149 trillion years to crack a 128-bit AES key. To put that into
perspective, the universe is believed to be less than 20 billion years old.

http://csrc.nist.gov/encryption/aes/

COMP4137/COMP7200

55



AES Structure

Data block of 4 columns of 4 bytes is state

Key is expanded to array of words

Has 9/11/13 rounds in which state undergoes:
• byte substitution (1 S-box used on every byte)
• shift rows (permute bytes between groups/columns)
• mix columns (subs using matrix multiply of groups)
• add round key (XOR state with key material)
• view as alternating XOR key & scramble data bytes

Initial XOR key material & incomplete last round

Fast XOR & table lookup implementation

COMP4137/COMP7200

Page 56



Symmetric cryptography

• Both parties must agree on a secret key, K
• message is encrypted, sent, decrypted at other side

EK(P)

Bob

DK(C)

Alice

• Key distribution must be secret

• Otherwise, messages can be decrypted
• Users can be impersonated

COMP4137/COMP7200

57



Key explosion

Each pair of users needs a separate key for secure communication

Alice

Bob

Alice

Bob

KAB

2 users: 1 key

KAB

KBC

KA
C

Charles

3 users: 3 keys

4 users: 6 keys

6 users: 15 keys

100 users: 4950 keys

1000 users: 399500 keys

n users:

keys

COMP4137/COMP7200

58

21)(−nn

Key distribution

Secure key distribution is the biggest problem with symmetric
cryptography

How can you communicate securely with someone you’ve never met?

Whit Diffie: idea for a public key algorithm

Challenge: can this be done securely?

Knowledge of public key should not allow derivation of private key

COMP4137/COMP7200

59



Diffie-Hellman exponential key exchange

Key distribution algorithm

• first algorithm to use public/private keys
• not public key encryption
• based on difficulty of computing discrete logarithms in a finite

field compared with ease of calculating exponentiation

Allows us to negotiate a secret session key without fear of

eavesdroppers

COMP4137/COMP7200

60



Diffie-Hellman exponential key exchange

• All arithmetic performed in

field of integers modulo some large number

• Both parties agree on

• a large prime number p
• and a number  < p

• Each party generates a public/private key pair

private key for user i:  Xi

public key for user i:  Yi

COMP4137/COMP7200

61



Diffie-Hellman exponential key exchange

• Alice has secret key XA
• Alice has public key YA
• Alice computes

• Bob has secret key XB
• Bob has public key YB

K = (Bob’s public key) (Alice’s private key) mod p

COMP4137/COMP7200

62



Diffie-Hellman exponential key exchange

• Alice has secret key XA
• Alice has public key YA
• Alice computes

• Bob has secret key XB
• Bob has public key YB
• Bob computes

K’ = (Alice’s public key) (Bob’s private key) mod p

COMP4137/COMP7200

63



Diffie-Hellman exponential key exchange

• Alice has secret key XA
• Alice has public key YA
• Alice computes

• Bob has secret key XB
• Bob has public key YB
• Bob computes

• expanding:

• expanding:

K = K’
K is a common key, known only to Bob and Alice

COMP4137/COMP7200

64



Diffie-Hellman example

Suppose  p = 31667,  = 7

Alice picks
XA = 18

Alice’s public key is:

YA = 718 mod 31667 = 6780

Bob picks
XB = 27

Bob’s public key is:

YB = 727 mod 31667 = 22184

K = 2218418 mod 31667
K = 14265

K = 678027 mod 31667
K = 14265

COMP4137/COMP7200

65



Key distribution problem is solved!

• User maintains private key
• Publishes public key in database (“phonebook”)

• Communication begins with key exchange to establish a common key
• Common key can be used to encrypt a session key

• increase difficulty of breaking common key by reducing the amount of data

we encrypt with it

• session key is valid only for one communication session

COMP4137/COMP7200

66



RSA: Public Key Cryptography

• Ron Rivest, Adi Shamir, Leonard Adleman created a true public key

encryption algorithm in 1977

• Each user generates two keys
• private key (kept secret)
• public key

• Difficulty of algorithm based on the difficulty of factoring large

numbers

• keys are functions of a pair of large (~200 digits) prime numbers

COMP4137/COMP7200

67



RSA algorithm

Generate keys:

• choose two random large prime numbers p, q
• Compute the product   n = pq
• randomly choose the encryption key, e,

such that:

e and (p - 1)(q - 1) are relatively prime

• use the extended Euclidean algorithm to compute the decryption key, d:

ed = 1 mod ((p - 1) (q - 1))
d  = e-1 mod ((p - 1) (q - 1))

• discard p, q

COMP4137/COMP7200

68



RSA algorithm

Encrypt:

• divide data into numerical blocks < n
• encrypt each block:
c = me mod n

Decrypt:

m = cd mod n

COMP4137/COMP7200

69



Elliptic Curve Cryptography (ECC)

◼ Why Elliptic Curve Cryptography (ECC)?

 ECC is an encryption technique based on elliptic curve theory that can be used as faster,

smaller, and more efficient cryptosystems

◼ Who introduced it and when?

 Miller and Koblitz in mid 1980s and Lenstra showed how to use elliptic curves to factor

integers

◼ What is the basic principle?

 Obtain same level of security as conventional cryptosystems but with much smaller key

sizes

◼ Bitcoin adopts Elliptic Curve Digital Signature Algorithm (ECDSA), which will be

introduced later



Communication with public key algorithms

Different keys for encrypting and decrypting
• no need to worry about key distribution

COMP4137/COMP7200

71



Communication with public key algorithms

Alice

Alice’s public key: KA

Bob

Bob’s public
key: KB

exchange public keys
(or look up in a directory/DB)

COMP4137/COMP7200

72



Communication with public key algorithms

Alice
Alice’s public key: KA

Bob

Bob’s public key: KB

EB(P)

Db(C)

encrypt message with
Bob’s public key

decrypt message with
Bob’s private key

COMP4137/COMP7200

73



Communication with public key algorithms

Alice

Alice’s public key: KA

Bob

Bob’s public key: KB

EB(P)

Db(C)

encrypt message with
Bob’s public key

Da(C)

decrypt message with
Alice’s private key

decrypt message with
Bob’s private key

EA(P)

encrypt message with
Alice’s public key

COMP4137/COMP7200

74



Public key woes

Public key cryptography is great but:

• RSA about 100 times slower than DES in software, 1000 times slower in HW

• Vulnerable to chosen plaintext attack

• if you know the data is one of n messages, just encrypt each message with the recipient’s

public key and compare

• It’s a good idea to reduce the amount of data encrypted with any given key

• but generating RSA keys is computationally very time consuming

COMP4137/COMP7200

75



Signatures

We use signatures because a signature is

Authentic
Not reusable
Renders document unalterable

Unforgeable

Non repudiatable

COMP4137/COMP7200

Source: http://www.archives.gov/exhibits/charters/declaration.html

76



Signatures

We use signatures because a signature is

Authentic
Not reusable
Renders document unalterable

Unforgeable

Non repudiatable

ALL UNTRUE!

Can we do better with digital signatures?

COMP4137/COMP7200

77



Arbitrated protocol

Arbitrated protocol using symmetric encryption

• turn to trusted third party (arbiter) to authenticate messages

Trent

Trent is trusted
and has everyone’s keys

C=EA(P)

Alice

Bob

Alice encrypts message for herself and sends it to Trent

COMP4137/COMP7200

78



Arbitrated protocol

Trent
P= DA(C)

Alice

Bob

Trent receives Alice’s message and decrypts it with Alice’s key

- this authenticates that it came from Alice
- he may choose to log a hash of the message to

create a record of the transmission

COMP4137/COMP7200

79



Arbitrated protocol

Trent

C’= EB(P)

Alice

Bob

Trent now encrypts the message for Bob and sends it to Bob

COMP4137/COMP7200

80



Arbitrated protocol

Trent

Alice

Bob

P’= DB(C’)

Bob receives the message and decrypts it

- it must have come from Trent

since only Trent and Bob have Bob’s key

- if the message says it’s from Alice, it must be - we trust Trent

COMP4137/COMP7200

81



Digital signatures - public key cryptography

Encrypting a message with a private key is the same as signing!

Alice

Ea(P)

Bob

DA(C)

encrypt message with
Alice’s private key

decrypt message with
Alice’s public key

COMP4137/COMP7200

82



Digital signatures - public key cryptography

• What if Alice was sending Bob binary data?

• Bob might have a hard time knowing whether the decryption was successful or not

• Public key encryption is considerably slower than symmetric encryption

• what if the message is very large?

• What if we don’t want to hide the message, yet want a valid signature?

COMP4137/COMP7200

83



Digital signatures - public key cryptography

• Create a hash of the message

• Encrypt the hash and send it with the message

• Validate the hash by decrypting it and comparing it with the hash of the

received message

• The signature is now a distinct entity from the message

COMP4137/COMP7200

84



Digital signatures - public key cryptography

Alice

H(P)

Bob

Alice generates a hash of the message

COMP4137/COMP7200

85



Digital signatures - public key cryptography

Alice

H(P)

Ea(H(P))

Bob

Alice encrypts the hash with her private key

COMP4137/COMP7200

86



Digital signatures - public key cryptography

Alice

H(P)

Ea(H(P))

Bob

Alice sends Bob the message and the encrypted hash

COMP4137/COMP7200

87



Digital signatures - public key cryptography

Alice

H(P)

C = Ea(H(P))

Bob

H(P)

H’ = DA(C)

1. Bob decrypts the hash using Alice’s public key
2. Bob computes the hash of the message sent by Alice

COMP4137/COMP7200

88



Digital signatures - public key cryptography

Alice

H(P)

C = Ea(H(P))

Bob

H(P)

H’ = DA(C)

If  the hashes match

- the encrypted hash must have been generated by Alice
- the signature is valid

COMP4137/COMP7200

89



Demo of public/privacy keys and digital signature

• Public / Private Key Pairs

• https://andersbrownworth.com/blockchain/public-private-keys/keys

• Digital signatures

• https://andersbrownworth.com/blockchain/public-private-keys/signatures

COMP4137/COMP7200

Page 90



Cryptographic toolbox

• Symmetric encryption
• Public key encryption
• One-way hash functions
• Random number generators

• Nonces, session keys

COMP4137/COMP7200

91



Examples

• Key exchange

• Public key cryptography

• Key exchange + secure communication
• Public key + symmetric cryptography

• Authentication

• Nonce + encryption

• Message authentication codes

• Hashes

• Digital signature

• Hash + encryption

COMP4137/COMP7200

92

