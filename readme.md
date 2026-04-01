COMP4137/COMP7200 Programming Project:
Implementation of a Mini Blockchain
COMP4137/COMP7200
Henry Hong-Ning Dai
March 5, 2026
Important Milestones:
• Group Registration Deadline: 17:00 Mar. 20, 2026
• Project Phase I Deadline: 17:00 April 3, 2026
• Project Phase II Deadline: 17:00 April 24, 2026
1 Project Overview & Mission
In this project, your goal is to design and implement “MiniChain”, a simplified, functional blockchain
system from the ground up. This hands-on project will take you beyond theory and into the practical
mechanics of how blockchains work. Working in a team, you will complete this project that contains
the components: (1) Transaction generation, (2) Verifiable Merkle tree of transactions, (3) Construc-
tion of blockchain, and (4) Integrity verification of transactions and blocks. Upon completion of this
project, you need to submit a comprehensive technical report written in English. Moreover, you are
also required to present your project in a short video (within 5 minutes).
Programming Languages: You are encouraged to use Python or Java. If you prefer using another
language, please obtain the instructor’s approval first.
2 Learning Objectives
Upon successful completion of this project, you will be able to:
• Implement Core Concepts: Build a working blockchain platform, including transactions,
Merkle trees, blocks, and mining.
• Apply Cryptography: Use public-key cryptography for account creation and digital signatures
to secure transactions.
• Master Data Structures: Understand and implement the crucial data structures of a blockchain,
particularly the linked-list nature of blocks and the efficiency of Merkle trees.
• Develop System Integrity: Design verification systems to detect tampering and ensure the
integrity of your blockchain.
• Collaborate and Document: Gain experience in team-based software development, work dis-
tribution, and professional technical documentation.
1
3 Project Roadmap & Key Deadlines
This project is divided into two phases, each with a specific deadline. Plan your time accordingly.
• Group Registration Deadline: 17:00 Mar. 20, 2026
– Form your groups of 3 to 5 students (detailed in Section 4).
• Phase I: The Building Blocks
– Deadline: 17:00 April 3, 2026
– Tasks:
1. Account & Transaction Generation: Implement cryptographic key pairs for ac-
counts and create signed, single-input-single-output (SISO) transactions.
2. Verifiable Merkle Tree: Construct a Merkle tree from a set of transactions to produce
a single root hash.
• Phase II: Assembling the Chain
– Deadline: 17:00 April 24, 2026
– Tasks:
1. Blockchain Construction: Define the structure of a block and chain them together.
2. Proof-of-Work Mining: Implement a “mining” function that finds a valid nonce to
secure a new block.
3. Integrity Verification: Create a test program to verify the entire chain and detect any
tampering.
• Final Submission Deadline: 17:00 April 24, 2026
– Deliverables:
* Final Project Report (PDF)
* Project Presentation Video (5 min)
* Complete Source Code with README
4 Requirements
Projects should be done in groups, each with THREE to FIVE students. Please specify the work
distribution of each member in the final project report. The deadline for grouping is 17:00 Mar. 20,
2026. For the students who cannot form a group, TAs will help to assign a group manually after the
grouping deadline.
Please write the documents in your own words and make sure that the materials (including codes)
used have been properly referenced. Please notice the HKBU plagiarism booklet: http://ar.hkbu.
edu.hk/curr/avoid plagiarism/.
2
5 Detailed Task Breakdown
A full-fledged blockchain requires multiple technologies, including cryptographic algorithms, data
structures, digital signatures, digital hash, peer-to-peer systems, and incentive mechanisms. Due to the
limited time, you only need to implement the following basic components: (1) Account & Transaction
generation, (2) Verifiable Merkle tree of transactions, (3) Construction of blockchain, and (4) Integrity
verification of transactions and blockchains.
5.1 Account & Transaction Generation
Account Creation. Before transaction generation, you need to create a blockchain account for the
user. The user will own a pair of private key and public key, where the public key will be used as the
user’ account for transactions in the blockchain. You need to consider adopting well-known public
key cryptographic algorithms, such as Elliptic Curve Cryptography (ECC), RSA, EI-Gamal, etc. To
achieve this goal, you may refer to Python cryptography libraries1 or Java cryptography libraries2
.
Defining the Transaction Structure. Your blockchain only generates single-input single-output
(SISO) transactions. Take an SISO transaction as an example, in which a user Alice will make a
transaction to another user Bob.
One transaction consists of a unique transaction ID, data, an input, an output, and signature,
described as follows:
1. Transaction ID: the transaction ID is calculated by taking a hash3 of the transaction contents.
2. Data: You can fill in this field by the amount of virtual coins and a digital signature (the crypto-
hash of the amount of virtual coins).
3. Input: the input consists of the source (sender) address.
4. Output: the output consists of the destination (receiver) address.
5. Signature: A digital signature created by signing the transaction details (e.g., a hash of sender,
recipient, and amount) with the sender’s private key.
The generated transactions will be used for building the verifiable Merkle tree and construction of
the blockchain.
5.2 Verifiable Merkle Tree
After obtaining a number of transactions, you can build a verifiable Merkle tree on top of these trans-
actions. You need to adopt the SHA-256 hash function or other alternative ones in Python4 or Java5
.
Consider Figure 1 as an example, in which you can build the Merkle tree from four transactions. Note
that you can always assume the number of transactions is a power of 2 (e.g., 2, 4, 8, 16) for simplicity.
1https://pypi.org/project/securesystemslib/, https://pypi.org/project/secp256k1/
2https://www.java.com/en/configure crypto.html
3You may choose SHA256 or alternative ones in Python https://docs.python.org/3/library/hashlib.html#
module-hashlib or Java https://commons.apache.org/proper/commons-codec/apidocs/org/apache/commons/
codec/digest/DigestUtils.html
4https://docs.python.org/3/library/hashlib.html#module-hashlib
5https://commons.apache.org/proper/commons-codec/apidocs/org/apache/commons/codec/digest/
DigestUtils.html
3
Merkle Root
H1234 H5678
H12 H34 H56 H78
H1 H2 H3 H4 H5 H6 H7 H8
T1 T2 T3 T4 T5 T6 T7 T8
Figure 1: An example of the Merkle tree of transactions.
Hash a List of Transactions: Start with a list of transactions generated in Task 1. Calculate the
SHA-256 hash of each individual transaction ID.
Build the Tree: Conduct the following steps to build the Merkle tree.
• Pair up the hashes and hash them together (e.g., hash(H(A) + H(B))).
• Repeat this process for each level of the tree until you are left with a single hash: the Merkle
Root.
5.3 Construction of Blockchain
Your blockchain essentially consists of (1) a Header and (2) a number of transactions, where the
transactions are generated in Section 5.1.
The header contains the following information:
1. The previous hash, which is generated by the previous block;
2. The time stamp, which is the time when the block is generated;
3. Nounce (starting with 0), which is used to mine a block (see Section 5.4);
4. The block will also contain the list of transactions it confirms;
5. The Merkle tree of all the transactions in the block in Section 5.2.
Note that you will also need to adopt the SHA-256 hash function to generate hash values. More-
over, you need to design a function to generate the “Genesis Block”, which is the very first block in a
chain (a special block since it has no previous hash).
5.4 Mining a block with Proof-of-Work (PoW)
In this step, you need to implement a Proof-of-Work (PoW) protocol.
To add a block to the chain, a “miner” must solve a computational puzzle according to the follow-
ing Mining Loop:
4
• Define a difficulty level (e.g., a target hash starting with a certain number of zeros, like “0000”).
• Create a function mine block that:
– Takes a new block’s data (previous hash, merkle root, etc.).
– Enters a loop that repeatedly calculates the SHA-256 hash of the entire block header (in-
cluding the current nonce).
– Checks if the resulting hash meets the difficulty target (e.g., a hash value starts with
“0000”)).
– If it doesn’t, increment the nonce by 1 and repeat.
– If it does, the puzzle is solved! The loop ends, and the block (with its valid nonce) is ready
to be added to the chain.
5.5 Integrity Verification
In this step, you need to design and implement a test program, which can simulate the process of
falsifying some transactions or modifying the data (even other fields) in a block. Your implemented
system will report whether the transactions/blocks are falsified.
1. Chain Verification: Write a function is chain valid() that iterates through your entire
blockchain (from the last block to the first) and checks two things for each block:
• The previous hash stored in the block matches the actual calculated hash of the previous
block.
• The block’s own hash is valid according to the PoW difficulty.
If any link is broken, the chain is invalid.
2. Tampering Simulation: Create a test script that simulates an attack:
• Manually change data in a transaction within an early block.
• Re-run your is chain valid() function. It should immediately detect the tampering and
report the chain as invalid. Explain in your report why it was detected.
6 Deliverables & Submission
6.1 Source Code & Reproducibility
Your code must be easy to understand and run. Submit a single compressed file (.zip or .tar.gz)
containing all your source code and a README.md file with the following:
• Project Info: Title, group number, and names/IDs of all members.
• Setup Instructions:
– Hardware/OS requirements (e.g., Windows 10, macOS, 8GB RAM).
– List of all required libraries and dependencies (e.g., pip install cryptography).
– Clear, step-by-step instructions to compile and run your project.
5
• Execution Guide:
– How to run your main program or test scripts.
– An explanation of the expected output and how it demonstrates your working system.
6.2 Final Project Report
This is a professional technical document detailing your project (Maximum 10 pages) with appen-
dices excluded. It must include:
• Introduction: Project overview and a clear description of each group member's contributions.
• System Architecture: A high-level diagram and description of how your components (ac-
counts, transactions, blocks, chain) fit together.
• Design & Implementation: Detailed explanation of your key algorithms and data structures.
Use pseudocode or flowcharts, but do not paste large blocks of code.
• Testing & Results: Show how you tested your system. Include screenshots of your program
running (e.g., creating a block, verifying the chain, detecting an attack) and explain the results.
• Conclusion: Summarize your work and discuss potential future improvements.
• References: Properly cite any external libraries, articles, or resources used.
6.3 Project Presentation Video (5 minutes)
Create a short video to showcase your project.
• Content: Briefly introduce your team, explain the project’s goal, demonstrate its core features
running, and highlight your key achievements.
• Format: MP4, 16:9 landscape, 720p resolution, max 500MB.
Requirements of your report:
• Your report should be fully written in English.
• You should write the report in your own words - DO NOT directly copy words/texts from other
papers or technical blogs.
• You should properly cite references or other related studies if necessary.
• You should explicitly explain figures or tables when you refer to them.
Any violation of the above rules may lead to a penalty for your score.
6
6.4 Submission
Please submit the completed project report and source codes in the course Moodle according to the
given deadline. The implemented methods (codes) that you have used are also suggested to be sub-
mitted though they should be in limited size (e.g., 50 MB) due to the limitation of the course Moodle.
You also need to specify the compile and execution methods for your codes (i.e., a README file). If
your codes are larger than 50 MB, you may offer a URL link to let us download your codes. Details
about the source codes and the data can be referred to Section 7.
The deadline for submitting the completed codes of Tasks 1 and 2 (Sections 5.2) is 17:00 April 3,
2026.
2026.
The deadline for submitting the completed codes of Tasks 3, 4, 5 (Sections 5.5) is 17:00 April 24,
Note: Late submission will be penalized.
7 Evaluation of Reproducibility Artifacts
Artifacts comprise software, datasets, environment configuration, mechanized proofs, benchmarks,
test suites with scripts, etc. A complete artifact package must contain (1) the computational artifacts
and (2) instructions/documentation describing the contents and how to use them. Regarding the ar-
tifact, in particular the code and the datasets, scripts should be provided to support the compilation,
deployment, and execution to support the reproducibility of experiments.
The artifact description must be included in a README file along with the artifact, and it must
include the following aspects:
• Artifact Identification: (i) the report’s title, (ii) the group No, the student names, and student
IDs, and (iii) an abstract describing the main contributions of the project and how the role of the
artifact in these contributions. The abstract may include a software architecture or data models
and its description to help to understand the artifact and a clear description on to what extent
the artifact contributes to the reproducibility of the experiments in the report.
• Artifact Dependencies and Requirements: (i) a description of the hardware resources required,
(ii) a description of the operating systems required, (iii) the software libraries needed, (iv) the
input dataset needed to execute the code or when the input data is generated, and (v) optionally,
any other dependencies or requirements. Best practices to facilitate the understanding of the
descriptions indicate that unnecessary dependencies and requirements should be suppressed
from the artifact.
• Artifact Installation and Deployment Process: (i) the process description to install and compile
the libraries and the code, and (ii) the process description to deploy the code in the resources.
The description of these processes should include an estimation of the installation, compilation,
and deployment times.
• Reproducibility of Experiments: (i) a complete description of the experiment workflow that the
code can execute, (ii) an estimation of the execution time to execute the experiment workflow,
(iii) a complete description of the expected results and an evaluation of them, and most impor-
tantly (iv) how the expected results from the experiment workflow relate to the results found
in the report. Best practices indicate that the expected results from the artifact should be in the
same format as the ones in the submitted report to facilitate the understanding of the scope of
7
the reproducibility. For instance, when the results in the report are depicted in a graph figure,
ideally, the execution of the code should provide a (similar) figure (there are open-source tools
that can be used for that purpose such as gnuplot and Matplotlib).
8 Grading Criteria
Your project will be graded primarily based on the following weighting scheme:
• Project Phase I (30%): Correct implementation of Tasks 1 & 2.
• Project Phase II (30%): Correct implementation of Tasks 3, 4, & 5.
• Project Report (20%): Quality, clarity, and completeness of your technical report.
• Evaluation of reproducibility artifacts on executable program codes (10%): Clarity of your
README.md and ease of running your code.
• Presentation and demonstration (10%): Quality and effectiveness of your project demonstration
Academic Integrity: All work must be your own. Please familiarize yourself with HKBU’s
policy on plagiarism. Properly cite any code or ideas that are not your own.
8