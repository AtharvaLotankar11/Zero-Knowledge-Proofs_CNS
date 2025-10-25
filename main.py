import random
import hashlib
from datetime import datetime

# Shared parameters (large prime p, generator g, modulus q = p-1)
p = 10007  # Larger prime for demo (real-world: 2048-bit)
g = 5  # Generator
q = p - 1

# Demo configurations
DEMO_CONFIGS = {
    'password': "SecurePassword123",
    'min_age': 18,
    'range_min': 1000,
    'range_max': 5000,
    'secret_number': 3500,
    'group_members': ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    'secret_member': "Charlie"
}


def hash_to_int(password):
    """Hash password to an integer secret using SHA-256."""
    hash_obj = hashlib.sha256(password.encode())
    return int(hash_obj.hexdigest(), 16) % q


def zkp_password_demo():
    """Password authentication ZKP demonstration"""
    print("\n" + "="*60)
    print("🔑 DEMO 1: PASSWORD AUTHENTICATION")
    print("="*60)
    print("Prove you know a password without revealing it!")
    print(f"Hint: The correct password is '{DEMO_CONFIGS['password']}'")
    
    client_password = input("\nEnter password: ")
    
    # Server setup
    server_secret = hash_to_int(DEMO_CONFIGS['password'])
    server_public_key = pow(g, server_secret, p)
    
    print(f"\n🔧 Public parameters: p={p}, g={g}, q={q}")
    print(f"🔑 Server public key: {server_public_key}")
    
    # ZKP Protocol
    secret = hash_to_int(client_password)
    
    for round_num in range(1, 4):
        print(f"\n🔄 Round {round_num} - Schnorr Protocol")
        
        k = random.randint(1, q - 1)
        t = pow(g, k, p)
        print(f"📤 Client commitment: t = {g}^{k} mod {p} = {t}")
        
        e = random.randint(1, q - 1)
        print(f"🎯 Server challenge: e = {e}")
        
        s = (k + e * secret) % q
        print(f"📥 Client response: s = (k + e * secret) mod {q} = {s}")
        
        left = pow(g, s, p)
        right = (t * pow(server_public_key, e, p)) % p
        print(f"✅ Verification: {g}^{s} mod {p} = {left}")
        print(f"🎯 Expected: t * (public_key)^{e} mod {p} = {right}")
        
        if left != right:
            print(f"❌ Round {round_num} FAILED!")
            return False
        else:
            print(f"✅ Round {round_num} SUCCESS!")
    
    return True


def zkp_age_demo():
    """Age verification ZKP demonstration"""
    print("\n" + "="*60)
    print("🎂 DEMO 2: AGE VERIFICATION")
    print("="*60)
    print(f"Prove you're over {DEMO_CONFIGS['min_age']} without revealing exact age!")
    
    try:
        birth_year = int(input("\nEnter your birth year: "))
    except ValueError:
        print("❌ Invalid birth year!")
        return False
    
    current_year = datetime.now().year
    actual_age = current_year - birth_year
    
    print(f"\n🎂 Age Verification: Proving age >= {DEMO_CONFIGS['min_age']}")
    
    if actual_age < DEMO_CONFIGS['min_age']:
        print(f"❌ Age verification failed: You must be at least {DEMO_CONFIGS['min_age']} years old")
        return False
    
    secret = actual_age - DEMO_CONFIGS['min_age']
    public_commitment = pow(g, secret, p)
    
    print(f"🔐 Age commitment generated (hiding exact age)")
    
    for round_num in range(1, 4):
        print(f"\n🔄 Round {round_num} - Age Range Proof")
        
        r = random.randint(1, q - 1)
        commitment = pow(g, r, p)
        print(f"📤 Prover commitment: C = g^r mod p = {commitment}")
        
        challenge = random.randint(1, q - 1)
        print(f"🎯 Verifier challenge: e = {challenge}")
        
        response = (r + challenge * secret) % q
        print(f"📥 Prover response: s = (r + e * age_proof) mod q = {response}")
        
        left = pow(g, response, p)
        right = (commitment * pow(public_commitment, challenge, p)) % p
        print(f"✅ Verification: g^s = {left}, C * commitment^e = {right}")
        
        if left == right:
            print(f"✅ Round {round_num} SUCCESS! Age >= {DEMO_CONFIGS['min_age']} verified")
        else:
            print(f"❌ Round {round_num} FAILED!")
            return False
    
    return True


def zkp_range_demo():
    """Range proof ZKP demonstration"""
    print("\n" + "="*60)
    print("📊 DEMO 3: RANGE PROOF")
    print("="*60)
    print(f"Prove a number is in range [{DEMO_CONFIGS['range_min']}, {DEMO_CONFIGS['range_max']}]!")
    print(f"Hint: The secret number is {DEMO_CONFIGS['secret_number']}")
    
    try:
        number = int(input(f"\nEnter a number: "))
    except ValueError:
        print("❌ Invalid number!")
        return False
    
    print(f"\n📊 Range Proof: Proving number ∈ [{DEMO_CONFIGS['range_min']}, {DEMO_CONFIGS['range_max']}]")
    
    if number != DEMO_CONFIGS['secret_number']:
        print("❌ Invalid number provided")
        return False
    
    if not (DEMO_CONFIGS['range_min'] <= number <= DEMO_CONFIGS['range_max']):
        print(f"❌ Number not in valid range [{DEMO_CONFIGS['range_min']}, {DEMO_CONFIGS['range_max']}]")
        return False
    
    secret = number - DEMO_CONFIGS['range_min']
    public_commitment = pow(g, secret, p)
    
    print(f"🔐 Range commitment generated")
    
    for round_num in range(1, 4):
        print(f"\n🔄 Round {round_num} - Range Proof Protocol")
        
        r = random.randint(1, q - 1)
        commitment = pow(g, r, p)
        print(f"📤 Commitment: C = g^r mod p = {commitment}")
        
        challenge = random.randint(1, q - 1)
        print(f"🎯 Challenge: e = {challenge}")
        
        response = (r + challenge * secret) % q
        print(f"📥 Response: s = (r + e * normalized_value) mod q = {response}")
        
        left = pow(g, response, p)
        right = (commitment * pow(public_commitment, challenge, p)) % p
        print(f"✅ Verification: g^s = {left}, C * public_commitment^e = {right}")
        
        if left == right:
            print(f"✅ Round {round_num} SUCCESS! Number in range verified")
        else:
            print(f"❌ Round {round_num} FAILED!")
            return False
    
    return True


def zkp_membership_demo():
    """Membership proof ZKP demonstration"""
    print("\n" + "="*60)
    print("👥 DEMO 4: GROUP MEMBERSHIP PROOF")
    print("="*60)
    print(f"Prove you're in group {DEMO_CONFIGS['group_members']} without revealing identity!")
    print(f"Hint: The secret member is '{DEMO_CONFIGS['secret_member']}'")
    
    member = input(f"\nEnter member name: ")
    
    print(f"\n👥 Membership Proof: Proving membership in group {DEMO_CONFIGS['group_members']}")
    
    if member != DEMO_CONFIGS['secret_member']:
        print("❌ Invalid member claim")
        return False
    
    if member not in DEMO_CONFIGS['group_members']:
        print("❌ Member not in group")
        return False
    
    member_index = DEMO_CONFIGS['group_members'].index(member)
    secret = member_index + 1
    public_commitment = pow(g, secret, p)
    
    print(f"🔐 Membership commitment generated (hiding specific identity)")
    
    for round_num in range(1, 4):
        print(f"\n🔄 Round {round_num} - Membership Proof Protocol")
        
        r = random.randint(1, q - 1)
        commitment = pow(g, r, p)
        print(f"📤 Commitment: C = g^r mod p = {commitment}")
        
        challenge = random.randint(1, q - 1)
        print(f"🎯 Challenge: e = {challenge}")
        
        response = (r + challenge * secret) % q
        print(f"📥 Response: s = (r + e * member_proof) mod q = {response}")
        
        left = pow(g, response, p)
        right = (commitment * pow(public_commitment, challenge, p)) % p
        print(f"✅ Verification: g^s = {left}, C * membership_commitment^e = {right}")
        
        if left == right:
            print(f"✅ Round {round_num} SUCCESS! Group membership verified")
        else:
            print(f"❌ Round {round_num} FAILED!")
            return False
    
    return True


def main():
    """Main interactive demo"""
    print("🔐" + "="*58 + "🔐")
    print("   ZERO KNOWLEDGE PROOF CONCEPTS - INTERACTIVE DEMO")
    print("🔐" + "="*58 + "🔐")
    print("\nExplore different ZKP concepts through hands-on demonstrations!")
    print("Each demo proves knowledge/properties without revealing secrets.")
    
    demos = [
        ("Password Authentication", zkp_password_demo),
        ("Age Verification", zkp_age_demo), 
        ("Range Proof", zkp_range_demo),
        ("Group Membership", zkp_membership_demo)
    ]
    
    while True:
        print("\n" + "="*60)
        print("📋 AVAILABLE DEMONSTRATIONS:")
        print("="*60)
        for i, (name, _) in enumerate(demos, 1):
            print(f"{i}. {name}")
        print("5. Exit")
        
        try:
            choice = int(input("\nSelect demo (1-5): "))
            
            if choice == 5:
                print("\n🎉 Thanks for exploring Zero Knowledge Proofs!")
                print("Remember: ZKPs enable privacy-preserving verification!")
                break
            elif 1 <= choice <= 4:
                name, demo_func = demos[choice - 1]
                success = demo_func()
                
                if success:
                    print(f"\n🎉 {name} SUCCESS! Proof verified without revealing secrets!")
                else:
                    print(f"\n💥 {name} FAILED! Invalid proof detected!")
                
                input("\nPress Enter to continue...")
            else:
                print("❌ Invalid choice! Please select 1-5.")
                
        except ValueError:
            print("❌ Invalid input! Please enter a number.")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()