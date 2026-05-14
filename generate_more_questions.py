from __future__ import annotations

import json
import random
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
QUESTIONS_DIR = ROOT / "questions"

GENERIC_STEMS = [
    "Which statement about {keyword} is correct?",
    "What is the main purpose of {keyword} in {topic}?",
    "Which option best describes {keyword}?",
    "In {topic}, {keyword} refers to:",
    "What does {keyword} primarily do?",
    "Choose the best description of {keyword}.",
    "Which is true about {keyword}?",
    "How is {keyword} best explained?",
    "Which answer matches {keyword} most closely?",
    "For {topic}, {keyword} is:",
]

CODE_STEMS = [
    "What is the output of the following code?",
    "What will this code print?",
    "Choose the correct output for this snippet.",
    "What does the program display?",
    "After execution, what appears on screen?",
    "What is printed when the code runs?",
    "Select the output produced by this code.",
    "What is the final output?",
    "Which option matches the code output?",
    "What value is shown by the program?",
]

DIFFICULTIES = [
    "easy",
    "easy",
    "easy",
    "medium",
    "easy",
    "medium",
    "medium",
    "easy",
    "medium",
    "hard",
]


TOPIC_SPECS = {
    "c": {
        "label": "C Programming",
        "concepts": [
            ("pointer", "A variable storing an address", ["A loop statement", "A compiler directive", "A function return type"], "Pointers store memory addresses."),
            ("malloc", "Allocates dynamic memory without initialization", ["Reads input from keyboard", "Frees memory blocks", "Copies strings into arrays"], "malloc reserves heap memory and leaves it uninitialized."),
            ("struct", "A user-defined type that groups different members", ["A loop keyword", "A file handle type", "A pointer alias"], "struct groups related data under one name."),
            ("switch", "A multi-way selection statement", ["A recursion mechanism", "A memory allocator", "A pointer operator"], "switch selects one branch from several cases."),
            ("recursion", "A function calling itself until a base case", ["A compile-time macro", "An array indexing rule", "A storage class"], "Recursion repeats a function call until a base case stops it."),
        ],
    },
    "cout": {
        "label": "C Output",
        "concepts": [
            ("pre-increment", "3", ["2", "4", "5"], "Pre-increment updates the value before printing.", "int x = 2;\nprintf(\"%d\", ++x);"),
            ("post-increment", "2", ["1", "3", "4"], "Post-increment prints the current value first.", "int x = 2;\nprintf(\"%d\", x++);"),
            ("for loop", "012", ["210", "123", "001"], "The loop prints the sequence as the counter increases.", "for(int i = 0; i < 3; i++) {\n    printf(\"%d\", i);\n}"),
            ("array access", "30", ["03", "33", "20"], "Array indexing reads the stored value at the selected position.", "int a[] = {10, 20, 30};\nprintf(\"%d\", a[2]);"),
            ("pointer dereference", "7", ["0", "5", "9"], "Dereferencing a pointer prints the value stored at the pointed address.", "int x = 7;\nint *p = &x;\nprintf(\"%d\", *p);"),
        ],
    },
    "ds": {
        "label": "Data Structures",
        "concepts": [
            ("stack", "A LIFO data structure", ["A FIFO data structure", "A tree traversal rule", "A hashing method"], "A stack removes the most recently inserted item first."),
            ("queue", "A FIFO data structure", ["A LIFO data structure", "A binary search tree", "A graph edge"], "A queue removes the earliest inserted item first."),
            ("linked list", "Nodes connected by pointers", ["A contiguous array only", "A heap algorithm", "A sorting rule"], "Linked lists store items in nodes linked by references."),
            ("tree", "A hierarchical data structure with root and children", ["A linear sequence", "A queue discipline", "A hash table only"], "Trees organize data in parent-child levels."),
            ("hash table", "A key-value structure using hashing for fast lookup", ["A recursion tree", "A stack frame", "An adjacency matrix"], "Hash tables map keys to buckets or slots for fast access."),
        ],
    },
    "algo": {
        "label": "Algorithms",
        "concepts": [
            ("binary search", "Search on sorted data by halving the range", ["Always linear scan", "Bubble sort", "DFS traversal"], "Binary search repeatedly halves the search interval."),
            ("merge sort", "A divide and conquer sorting algorithm", ["A greedy scheduling method", "A heap allocation step", "A string encoding format"], "Merge sort splits and merges sorted halves."),
            ("quick sort", "A pivot-based divide and conquer sort", ["A breadth-first search", "A stack overflow check", "A hashing method"], "Quick sort partitions around a pivot and sorts recursively."),
            ("dynamic programming", "Solving overlapping subproblems with memoization or tabulation", ["Random search", "String concatenation", "Encryption step"], "Dynamic programming stores results to avoid repeated work."),
            ("greedy", "Chooses the locally optimal choice at each step", ["Exhaustive backtracking", "Recursion base case", "Matrix transpose"], "Greedy algorithms make the best immediate choice."),
        ],
    },
    "net": {
        "label": "Networking",
        "concepts": [
            ("IP address", "A logical address used to identify a device on a network", ["A physical cable", "An encryption key", "A disk sector"], "An IP address identifies a host on an IP network."),
            ("TCP", "A connection-oriented reliable transport protocol", ["An unreliable datagram protocol", "A file system", "A switch port"], "TCP provides reliable, ordered delivery."),
            ("UDP", "A connectionless lightweight transport protocol", ["A routing table", "An encrypted file", "A kernel service"], "UDP sends datagrams without connection setup."),
            ("DNS", "Translates domain names to IP addresses", ["Compresses packets", "Encrypts emails", "Assigns MAC addresses"], "DNS maps human-readable names to network addresses."),
            ("subnet mask", "Separates network and host portions of an IP address", ["Identifies browser cache", "Stores passwords", "Checks file integrity"], "A subnet mask helps split the IP address into network and host parts."),
        ],
    },
    "subnet": {
        "label": "Subnetting",
        "concepts": [
            ("CIDR", "Classless notation using prefix length", ["Routing cable standard", "MAC numbering", "Application layer rule"], "CIDR expresses networks as prefix lengths like /24."),
            ("network address", "The first address representing the subnet", ["The last usable host", "Broadcast only", "DNS alias"], "The network address identifies the subnet itself."),
            ("broadcast address", "The last address used to reach all hosts", ["Gateway IP", "Loopback address", "Private key"], "The broadcast address targets all hosts in a subnet."),
            ("VLSM", "Variable Length Subnet Masking", ["Fixed-size encryption", "Wireless standard", "File encoding"], "VLSM allows different subnet sizes inside the same network."),
            ("host count", "The number of usable addresses in a subnet", ["Number of routers", "Number of cables", "Number of switches"], "Host count tells how many devices fit in the subnet."),
        ],
    },
    "sec": {
        "label": "Security",
        "concepts": [
            ("confidentiality", "Preventing unauthorized disclosure", ["Data duplication", "Packet loss", "Disk formatting"], "Confidentiality keeps information private."),
            ("integrity", "Preventing unauthorized modification", ["Hiding filenames", "Adding users", "Sorting records"], "Integrity keeps data accurate and unaltered."),
            ("authentication", "Verifying user or system identity", ["Compressing data", "Balancing load", "Allocating memory"], "Authentication confirms who a user is."),
            ("encryption", "Converting plaintext into unreadable ciphertext", ["Deleting passwords", "Changing clock speed", "Indexing data"], "Encryption protects information by encoding it."),
            ("firewall", "Filters network traffic based on rules", ["Stores backups", "Allocates RAM", "Compiles code"], "A firewall allows or blocks network packets based on policy."),
        ],
    },
    "crypto": {
        "label": "Cryptography",
        "concepts": [
            ("AES", "A symmetric block cipher standard", ["A routing protocol", "A hash table", "A text editor"], "AES is a widely used symmetric encryption algorithm."),
            ("RSA", "A public-key cryptosystem based on number theory", ["A symmetric stream cipher", "A file format", "A SQL clause"], "RSA uses a public and private key pair."),
            ("hash function", "Produces a fixed-length digest from input", ["Reversibly encrypts messages", "Schedules tasks", "Manages memory"], "A hash function maps input data to a digest."),
            ("public key", "A key shared openly in asymmetric cryptography", ["A secret file", "A broadcast address", "A password reset token"], "The public key can be shared with everyone."),
            ("digital signature", "Provides authenticity and nonrepudiation", ["File compression", "Video encoding", "Routing metric"], "A digital signature proves origin and integrity."),
        ],
    },
    "db": {
        "label": "Database & SQL",
        "concepts": [
            ("primary key", "Uniquely identifies each row", ["A duplicate column", "A temporary table", "A join condition"], "A primary key must be unique for every row."),
            ("foreign key", "References a key in another table", ["A text index", "A view name", "A trigger body"], "A foreign key creates a relationship between tables."),
            ("normalization", "Organizing data to reduce redundancy", ["Encrypting tables", "Backing up files", "Creating indexes only"], "Normalization reduces duplication and improves structure."),
            ("join", "Combines rows from tables using related columns", ["Deletes rows", "Sorts rows", "Closes transactions"], "A join merges matching rows across tables."),
            ("transaction", "A unit of work with ACID properties", ["A random query", "A stored image", "A view-only rule"], "Transactions group SQL operations into one logical unit."),
        ],
    },
    "relalg": {
        "label": "Relational Algebra",
        "concepts": [
            ("selection", "Filters rows based on a condition", ["Combines columns", "Renames relation", "Duplicates tuples"], "Selection keeps only rows that satisfy a condition."),
            ("projection", "Selects specific columns", ["Filters by rows", "Unions relations", "Sorts tuples"], "Projection reduces a relation to selected attributes."),
            ("join", "Combines relations using a condition", ["Removes attributes", "Scans disk", "Encrypts tuples"], "Join connects related tuples from two relations."),
            ("union", "Returns tuples present in either relation", ["Only common tuples", "Only one column", "Only sorted tuples"], "Union combines all tuples from both relations."),
            ("difference", "Returns tuples in first relation but not second", ["Merges all tuples", "Duplicates columns", "Joins on keys"], "Difference subtracts the second relation from the first."),
        ],
    },
    "virt": {
        "label": "Virtualization",
        "concepts": [
            ("hypervisor", "Software that manages virtual machines", ["Packet sniffer", "File editor", "Compiler backend"], "A hypervisor creates and controls virtual machines."),
            ("VM", "A virtual machine isolated from the host", ["A physical CPU core", "A disk partition", "A network cable"], "A VM is a software-based computer environment."),
            ("container", "A lightweight isolated runtime sharing the host kernel", ["Full hardware emulator", "BIOS replacement", "Checksum function"], "Containers isolate apps while sharing the host kernel."),
            ("snapshot", "A saved state of a VM at a point in time", ["A password hash", "A DNS record", "A kernel driver"], "Snapshots capture the current VM state."),
            ("live migration", "Moving a running VM to another host", ["Shutting down a server", "Deleting a snapshot", "Changing file permissions"], "Live migration moves a running VM with minimal downtime."),
        ],
    },
    "digital": {
        "label": "Digital Systems",
        "concepts": [
            ("logic gate", "A basic digital circuit performing a boolean operation", ["Memory disk", "Routing rule", "Compiler directive"], "Logic gates implement boolean logic."),
            ("flip-flop", "A bistable memory element storing one bit", ["Network switch", "Hard drive platter", "Font style"], "Flip-flops store a single binary state."),
            ("register", "A group of flip-flops storing binary data", ["Text file", "Bus cable", "Opcode only"], "Registers temporarily hold binary data inside digital circuits."),
            ("multiplexer", "Selects one input from many", ["Adds two bits", "Stores one byte", "Encrypts data"], "A mux chooses one of several inputs."),
            ("decoder", "Converts binary code to one of many outputs", ["Compresses data", "Sorts arrays", "Manages threads"], "A decoder activates a unique output line."),
        ],
    },
    "arch": {
        "label": "Computer Architecture",
        "concepts": [
            ("ALU", "Performs arithmetic and logic operations", ["Stores files", "Sends packets", "Draws graphics"], "The ALU executes calculations and logic operations."),
            ("pipeline", "Executes stages overlapped for throughput", ["Compresses data", "Converts fonts", "Encrypts disks"], "Pipelining overlaps instruction stages."),
            ("cache", "Small fast memory for frequently used data", ["Permanent archive", "Keyboard buffer", "Database table"], "Cache reduces average memory access time."),
            ("instruction set", "The set of machine instructions a CPU understands", ["File format", "Browser plugin", "Network card"], "The ISA defines the CPU's available instructions."),
            ("register file", "A collection of CPU registers", ["Disk sector map", "Routing table", "Image buffer"], "The register file stores CPU registers for fast access."),
        ],
    },
    "se": {
        "label": "Software Engineering",
        "concepts": [
            ("requirements", "What software must do or provide", ["Source code list", "CPU clock", "File path"], "Requirements describe desired system behavior."),
            ("SDLC", "Software development life cycle", ["Database index", "Network protocol", "Memory page"], "SDLC covers the process of building software."),
            ("testing", "Checking software for defects", ["Code obfuscation", "File compression", "Hardware repair"], "Testing finds bugs and verifies behavior."),
            ("agile", "An iterative and adaptive development approach", ["One-shot build only", "Hardware encryption", "Static typing"], "Agile develops software in small iterations."),
            ("maintenance", "Modifying software after delivery", ["Compiling the kernel", "Drawing diagrams", "Installing RAM"], "Maintenance keeps software useful after release."),
        ],
    },
    "oop": {
        "label": "OOP",
        "concepts": [
            ("polymorphism", "Same interface, different implementations", ["Access control", "Object destruction", "File hiding"], "Polymorphism lets one interface work with many types."),
            ("encapsulation", "Bundling data with methods and hiding internal state", ["Multiple inheritance", "Loop reuse", "Compile-time optimization"], "Encapsulation protects an object's internal state."),
            ("inheritance", "Creating a new class from an existing class", ["Hiding variables", "Deleting objects", "Creating arrays"], "Inheritance lets a class reuse another class's features."),
            ("abstraction", "Showing essential features and hiding details", ["Copying objects", "Changing access levels", "Recompiling code"], "Abstraction focuses on what an object does, not how."),
            ("composition", "Has-a relationship between objects", ["Is-a relationship", "Runtime dispatch", "Static binding"], "Composition builds complex objects from simpler ones."),
        ],
    },
    "os": {
        "label": "Operating System",
        "concepts": [
            ("process", "A program in execution", ["A file on disk", "A hardware device", "A compiler"], "A process is a running program."),
            ("thread", "A lightweight unit of execution", ["A disk partition", "A network protocol", "A memory block"], "Threads are execution units within a process."),
            ("deadlock", "Processes waiting forever for resources", ["CPU cache miss", "File compression", "Kernel panic"], "Deadlock occurs when processes block each other indefinitely."),
            ("paging", "Divides memory into fixed-size pages", ["Encrypts files", "Schedules CPU", "Formats disks"], "Paging helps manage memory in page-sized blocks."),
            ("system call", "A request from a program to the operating system", ["A compiler warning", "A browser API", "A file permission"], "System calls let programs request OS services."),
        ],
    },
    "bangla": {
        "label": "বাংলা",
        "concepts": [
            ("বিশেষ্য", "যে শব্দ দ্বারা নাম বোঝায়", ["যে শব্দ কাজ বোঝায়", "যে শব্দ গুণ বোঝায়", "যে শব্দ সংখ্যা বোঝায়"], "বিশেষ্য ব্যক্তি, বস্তু, স্থান বা ভাবের নাম বোঝায়।"),
            ("ক্রিয়া", "যে শব্দ কাজ বোঝায়", ["যে শব্দ নাম বোঝায়", "যে শব্দ গুণ বোঝায়", "যে শব্দ সম্পর্ক বোঝায়"], "ক্রিয়া কোনো কাজ বা অবস্থা বোঝায়।"),
            ("বিশেষণ", "যে শব্দ বিশেষ্যকে বর্ণনা করে", ["ক্রিয়া", "সর্বনাম", "অব্যয়"], "বিশেষণ বিশেষ্যের গুণ বা দোষ প্রকাশ করে।"),
            ("সর্বনাম", "নামের পরিবর্তে ব্যবহৃত শব্দ", ["বিশেষণ", "অব্যয়", "সংযোজক"], "সর্বনাম বিশেষ্যের পরিবর্তে ব্যবহৃত হয়।"),
            ("প্রবাদ", "প্রচলিত ও উপদেশমূলক বাক্য", ["অনুপ্রাস", "উপমা", "রূপক"], "প্রবাদ বাক্য লোকমুখে প্রচলিত বচন।"),
        ],
    },
    "english": {
        "label": "English",
        "concepts": [
            ("tense", "Shows the time of an action", ["A noun form", "An article", "A conjunction"], "Tense tells whether an action is past, present, or future."),
            ("article", "A word used before a noun to show definiteness", ["A verb", "An adverb", "A preposition"], "Articles include a, an, and the."),
            ("preposition", "Shows relation between words", ["A verb", "A pronoun", "An exclamation"], "Prepositions show relationships like place or time."),
            ("synonym", "A word with a similar meaning", ["Opposite meaning", "Plural form", "Passive voice"], "Synonyms are words with near the same meaning."),
            ("antonym", "A word with an opposite meaning", ["Similar meaning", "Common noun", "Prefix rule"], "Antonyms have opposite meanings."),
        ],
    },
    "math": {
        "label": "Mathematics",
        "concepts": [
            ("permutation", "Arrangements where order matters", ["Order does not matter", "Odd numbers only", "Prime factors only"], "Permutation counts ordered arrangements."),
            ("combination", "Selections where order does not matter", ["Order matters", "Vector sum", "Equation solving"], "Combination counts unordered selections."),
            ("probability", "The likelihood of an event", ["Average value", "Product rule", "Derivative"], "Probability measures chance."),
            ("matrix", "A rectangular array of numbers", ["A line segment", "A scalar constant", "A polynomial term"], "A matrix arranges numbers in rows and columns."),
            ("logarithm", "The inverse operation of exponentiation", ["Square root", "Factorial", "Modulus"], "Logarithms undo exponentiation."),
        ],
    },
    "gk": {
        "label": "General Knowledge",
        "concepts": [
            ("capital city", "The official city where government is located", ["Largest city always", "Seaport only", "Mountain peak"], "A capital city hosts a country's central government."),
            ("planet", "A celestial body orbiting a star", ["An asteroid only", "A comet only", "A satellite only"], "Planets orbit stars and are massive enough to be rounded by gravity."),
            ("Nobel Prize", "An international award in categories like peace and literature", ["A sports trophy", "A local medal", "An exam grade"], "The Nobel Prize honors major achievements."),
            ("constitution", "The fundamental law of a country", ["A newspaper article", "A tax receipt", "A court verdict"], "A constitution defines the framework of government."),
            ("organization", "A group formed for a purpose", ["A random number", "A single machine", "A file extension"], "Organizations are structured groups working toward goals."),
        ],
    },
    "trans": {
        "label": "Translation",
        "concepts": [
            ("idiom", "A figurative expression whose meaning is not literal", ["A direct sentence", "A question mark", "A noun phrase"], "Idioms mean something different from the literal words."),
            ("one-word substitution", "A single word replacing a phrase", ["A punctuation mark", "A verb tense", "An article rule"], "One-word substitution compresses a phrase into one word."),
            ("direct speech", "Quoting the exact words spoken", ["Reporting indirectly", "Changing tense only", "Adding punctuation only"], "Direct speech keeps the speaker's original words."),
            ("indirect speech", "Reporting speech without exact quotation", ["Copying the exact sentence", "Using only one word", "Writing a title"], "Indirect speech reports meaning without direct quotes."),
            ("translation", "Converting meaning from one language to another", ["Spelling correction", "Grammar rule", "Punctuation mark"], "Translation conveys meaning across languages."),
        ],
    },
}


def build_question(prefix: str, start_index: int, topic_label: str, concept, stem: str, stem_index: int):
    keyword, correct, wrongs, explanation, *rest = concept
    code = rest[0] if rest else None
    rng = random.Random(f"{prefix}:{keyword}:{stem_index}")
    options = [correct, *wrongs[:3]]
    rng.shuffle(options)
    answer = options.index(correct)
    q_text = stem.format(topic=topic_label, keyword=keyword)
    if code:
        q_text = stem
    difficulty = DIFFICULTIES[stem_index % len(DIFFICULTIES)]
    return {
        "id": f"{prefix}_{start_index:03d}",
        "question": q_text,
        "code": code,
        "options": options,
        "answer": answer,
        "difficulty": difficulty,
        "explanation": explanation,
    }


def next_question_index(items):
    max_index = 0
    for item in items:
        match = re.match(r"^[a-z]+_(\d+)$", str(item.get("id", "")))
        if match:
            max_index = max(max_index, int(match.group(1)))
    return max_index + 1


def main():
    for prefix, spec in TOPIC_SPECS.items():
        path = QUESTIONS_DIR / f"{prefix}.json"
        items = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(items, list):
            raise ValueError(f"{path} does not contain a JSON array")

        start = next_question_index(items)
        generated = []
        stems = CODE_STEMS if any(len(concept) > 4 for concept in spec["concepts"]) else GENERIC_STEMS

        for concept in spec["concepts"]:
            for stem_index, stem in enumerate(stems):
                generated.append(build_question(prefix, start, spec["label"], concept, stem, stem_index))
                start += 1

        if len(generated) != 50:
            raise AssertionError(f"Expected 50 generated questions for {prefix}, got {len(generated)}")

        items.extend(generated)
        path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {path.name}: {len(items)} questions total")


if __name__ == "__main__":
    main()