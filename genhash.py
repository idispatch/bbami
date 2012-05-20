#!/usr/bin/python3.2

import sys
import re
import operator

# http://baldur.iti.kit.edu/~falke/kittel/rta-2011/c/hash.c.txt

def unsigned(x):
    return x & 0xFFFFFFFF
    
def DJBHash(key):
    hash = 5381
    for i in key:
        hash = unsigned(unsigned(unsigned(hash << 5) + hash) + ord(i))
    return unsigned(hash)

def SDBMHash(key):
    hash = 0
    for i in key:
        hash = unsigned(unsigned(unsigned(ord(i) + unsigned(hash << 6)) + (hash << 16)) - hash)
    return unsigned(hash)

def LoseHash(key):
    hash = 0
    for c in key:
        hash=unsigned(hash+ord(c))
    return unsigned(hash)

def RSHash(key):
    a = 378551
    b = 63689
    hash = 0
    for i in key:
        hash = unsigned(unsigned(hash * a) + ord(i))
        a = unsigned(a * b)
    return unsigned(hash)

def JSHash(key):
    hash = 1315423911
    for i in key:
        hash ^= unsigned(unsigned((unsigned(hash << 5) + ord(i)) + (hash >> 2)))
    return unsigned(hash)

def PJWHash(key):
    BitsInUnsignedInt = 32
    ThreeQuarters = BitsInUnsignedInt * 3 // 4
    OneEighth = BitsInUnsignedInt // 8
    HighBits = unsigned((0xFFFFFFFF << (BitsInUnsignedInt - OneEighth)))
    hash = 0
    test = 0
    for i in key:
        hash = unsigned(unsigned(hash << OneEighth) + ord(i))
        test = hash & HighBits
        if test:
            hash = (( hash ^ (test >> ThreeQuarters)) & (~HighBits))
    return unsigned(hash)

def ELFHash(key):
    hash = 0
    x = 0
    for i in key:
        hash = unsigned(unsigned(hash << 4) + ord(i))
        x = hash & 0xF0000000
        if x != 0:
            hash ^= (x >> 24)
            hash &= ~x
    return unsigned(hash)
    
def FNVHash(key):
    fnv_prime = 0x811C9DC5
    hash = 0;
    for i in key:
        hash = unsigned(hash * fnv_prime)
        hash ^= ord(i)
    return unsigned(hash)
    
def BPHash(key):
    hash = 0;
    for i in key:
        hash = unsigned(hash << 7) ^ ord(i)
    return hash;

def BKDRHash31(key):
    seed = 31 # 31 131 1313 13131 131313 etc..
    hash = 0
    for i in key:
        hash = unsigned(unsigned(hash * seed) + ord(i))
    return unsigned(hash)

def BKDRHash131(key):
        seed = 131 # 31 131 1313 13131 131313 etc..
        hash = 0
        for i in key:
            hash = unsigned(unsigned(hash * seed) + ord(i))
        return unsigned(hash)

def BKDRHash1313(key):
        seed = 1313 # 31 131 1313 13131 131313 etc..
        hash = 0
        for i in key:
            hash = unsigned(unsigned(hash * seed) + ord(i))
        return unsigned(hash)

def BKDRHash13131(key):
        seed = 13131 # 31 131 1313 13131 131313 etc..
        hash = 0
        for i in key:
            hash = unsigned(unsigned(hash * seed) + ord(i))
        return unsigned(hash)

def BKDRHash131313(key):
        seed = 131313 # 31 131 1313 13131 131313 etc..
        hash = 0
        for i in key:
            hash = unsigned(unsigned(hash * seed) + ord(i))
        return unsigned(hash)

def DEKHash(key):
    hash = len(key);
    for i in key:
        hash = (unsigned(hash << 5) ^ unsigned(hash >>27)) ^ ord(i)
    return unsigned(hash)

def APHash(key):
    hash = 0
    for i in key:
        if ((ord(i) & 1) == 0):
            hash ^= (unsigned(hash << 7) ^ ord(i) ^ (hash >> 3))
        else:
            hash ^= (~(unsigned(hash << 11) ^ ord(i) ^ (hash >> 5)))
    return unsigned(hash)

hash_function_header = """
static unsigned hash_str_impl(const char * str) {"""

hash_function_footer = """}
"""

hash_functions = {
    "DJBHash": """
    unsigned hash = 5381;
    unsigned c;
    while((c = *str++)!=0)
        hash = (hash << 5) + hash + c;
    return hash;
""",
    "SDBMHash": """
    unsigned hash = 0;
    unsigned c;
    while((c = *str++)!=0)
        hash = c + (hash << 6) + (hash << 16) - hash;
    return hash;
""",
    "LoseHash": """
    unsigned hash = 0;
    unsigned c;
    while((c = *str++)!=0)
        hash = hash + c;
    return hash;
""",
    "RSHash": """
    unsigned a = 378551;
    unsigned b = 63689;
    unsigned hash = 0;
    unsigned c;
    while((c = *str++)!=0)
        hash = hash * a + c;
        a = a * b;
    }
    return hash;
""",
    "JSHash": """
    unsigned c;
    unsigned hash = 1315423911;
    while((c = *str++)!=0)
        hash ^= (hash << 5) + c + (hash >> 2);
    return hash;
""",
    "PJWHash": """
    const unsigned BitsInUnsignedInt = (unsigned int)(sizeof(unsigned int) * 8);
    const unsigned ThreeQuarters     = (unsigned int)((BitsInUnsignedInt  * 3) / 4);
    const unsigned OneEighth         = (unsigned int)(BitsInUnsignedInt / 8);
    const unsigned HighBits          = (unsigned int)(0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth);
    unsigned int hash              = 0;
    unsigned int test              = 0;
    unsigned c;
    while((c = *str++)!=0)
       hash = (hash << OneEighth) + c;
       if((test = hash & HighBits)!= 0)
          hash = (( hash ^ (test >> ThreeQuarters)) & (~HighBits));
    }
    return hash;
""",
    "ELFHash": """
    unsigned hash = 0;
    while(*str) {
        hash = (hash << 4) + *str++;
        unsigned g = hash & 0xF0000000;
        if (g) 
            hash ^= g >> 24;
        hash &= ~g;
    }
    return hash;
""",
    "BKDRHash31": """
    unsigned seed = 31;
    unsigned hash = 0;
    while((c = *str++)!=0)
        hash = hash * seed + c;
    return hash;
""",
    "BKDRHash131": """
    unsigned seed = 131;
    unsigned hash = 0;
    while((c = *str++)!=0)
        hash = hash * seed + c;
    return hash;
""",   
    "BKDRHash1313": """
    unsigned seed = 1313;
    unsigned hash = 0;
    while((c = *str++)!=0)
        hash = hash * seed + c;
    return hash;
""",
    "BKDRHash13131": """
    unsigned seed = 13131;
    unsigned hash = 0;
    while((c = *str++)!=0)
        hash = hash * seed + c;
    return hash;
""",
    "BKDRHash131313": """
    unsigned seed = 131313;
    unsigned hash = 0;
    while((c = *str++)!=0)
        hash = hash * seed + c;
    return hash;
""",
    "DEKHash": """
    unsigned hash = strlen(str);
    unsigned c;
    while((c = *str++)!=0)
        hash = ((hash << 5) ^ (hash >> 27)) ^ c;
    return hash;
""",
    "FNVHash": """
    const unsigned fnv_prime = 0x811C9DC5;
    unsigned int hash = 0;
    unsigned c;
    while((c = *str++)!=0)
        hash *= fnv_prime;
        hash ^= (*str);
    }
    return hash;
""",
    "BPHash": """
    unsigned int hash = 0;
    unsigned c;
    while((c = *str++)!=0)
        hash = hash << 7 ^ c;
    return hash;
""",
    "APHash": """
    unsigned hash = 0;
    unsigned c;
    while((c = *str++)!=0) {
        if (c & 1 == 0)
            hash ^= (hash << 7) ^ c ^ (hash >> 3);
        else
            hash ^= ~((hash << 11) ^ c ^ (hash >> 5));
    }
    return hash;
"""
}

if len(sys.argv) < 2:
    sys.exit(-1)

with open(sys.argv[1]) as f:
    h={}
    for i in f.readlines():
        m=re.search(r'\[([^]]+)\]\s*=\s*"([^"]+)"',i)
        if m:
            id, value = m.group(1,2)
            h[id] = value

    #print("Number of strings: %s\n" % len(h))
    stat = {}
    for name in hash_functions:  # vary hash algorithm
        for table_size in range(len(h), 10*len(h)): # vary hash table size
            table = [0] * table_size
            fn = globals()[name]
            for i in h:
                hash = fn(h[i]) % table_size
                table[hash] += 1
            num_collisions=0
            max_collisions=0
            for i,collisions in enumerate(table):
                if collisions > 1:
                    num_collisions += collisions - 1
                    max_collisions = max(max_collisions, collisions)
            if num_collisions == 0:
                stat[name] = table_size
                break

    sorted_stat = list(sorted(stat.items(), key = operator.itemgetter(1)))
    #for entry in sorted_stat:
    #    print("%-20s: %s" % (entry[0], entry[1]))

    name, table_size = sorted_stat[0]
    #print("\nUsing %s" % name)
    
    table = {}
    fn = globals()[name]
    for i in h:
        hash = fn(h[i]) % table_size
        table[hash] = i
    
    print("#ifndef __hash_table_definition_included__")
    print("#define __hash_table_definition_included__")
    print("")
    print("static const unsigned attr_hash_table[] = {")
    for i in range(table_size):
        if i in table:
            print('    %-38s, /* %-8s%s */' % (table[i], i, h[table[i]]))
        else:
            print("    %s," % "~0")
    print("};")
    print("")
    print("#define HASH_TABLE_SIZE (sizeof(attr_hash_table) / sizeof(attr_hash_table[0]))")
    print(hash_function_header, end="")
    print(hash_functions[name], end="")
    print(hash_function_footer, end="")
    print("""
static unsigned hash_str(const char * str) {
    return hash_str_impl(str) % HASH_TABLE_SIZE;
}

static int hash_lookup(const char * str, bbami_attribute_id * attribute_id) {
    if(!str || !attribute_id)
        return EINVAL;
    if(!*str)
        return ENOENT;
    unsigned hash = hash_str(str);
    if (hash < HASH_TABLE_SIZE &&       /* hash value must not exceed table size */
        ~0 != attr_hash_table[hash] &&  /* hash value must map to the defined value */
        0 == strcmp(str, attr_names[attr_hash_table[hash]])) {
        *attribute_id = (bbami_attribute_id)attr_hash_table[hash];
        return EOK;
    }
    return ENOENT;
}

#endif /* __hash_table_definition_included__ */
""")
