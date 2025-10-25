import random
import hashlib

# Shared parameters (large prime p, generator g, modulus q = p-1)
p = 10007  # Larger prime for demo (real-world: 2048-bit)
g = 5  # Generator
q = p - 1


def hash_to_int(password):
    """
    Hash password to an integer secret using SHA-256.
    Converts string password to a numerical secret for ZKP math.
    """
    hash_obj = hashlib.sha256(password.encode())
    return int(hash_obj.hexdigest(), 16) % q


def zkp_auth(client_password, server_public_key, rounds=3):
    """
    ZKP authentication simulation.
    Client proves password knowledge without sending it.
    Runs multiple rounds for soundness (cheating odds: 1/2^rounds).
    Returns True if successful, False otherwise.
    """
    secret = hash_to_int(client_password)

    print("\nStarting ZKP Authentication...")
    print(f"Public parameters: p={p}, g={g}, q={q}")
    print(f"Server's public key: {server_public_key}")

    for round_num in range(1, rounds + 1):
        print(f"\n--- Round {round_num} ---")

        # Step 1: Client commitment
        k = random.randint(1, q - 1)
        t = pow(g, k, p)
        print(f"Client sends commitment: t = {g}^{k} mod {p} = {t}")

        # Step 2: Server challenge
        e = random.randint(1, q - 1)
        print(f"Server sends challenge: e = {e}")

        # Step 3: Client response
        s = (k + e * secret) % q
        print(f"Client computes response: s = (k + e * secret) mod {q} = {s}")

        # Step 4: Server verification
        left = pow(g, s, p)
        right = (t * pow(server_public_key, e, p)) % p
        print(f"Server verifies: {g}^{s} mod {p} = {left}")
        print(f"          vs. t * (public_key)^{e} mod {p} = {right}")

        if left != right:
            print("Verification FAILED in this round!")
            return False
        else:
            print("Verification SUCCESS in this round!")

    return True


# Server setup (simulates registration)
registered_password = "SecurePassword123"  # Correct password
server_secret = hash_to_int(registered_password)
server_public_key = pow(g, server_secret, p)

# Interactive demo
print("-------------------------------------------------------------")
print("Welcome to Interactive ZKP Password Authentication Demo!")
print("The server has a registered password hashed to a secret.")
print("You'll try to authenticate without sending the password.")
print("-------------------------------------------------------------")
print("Hint: The correct password is 'SecurePassword123'. Try it after a wrong attempt!\n")

client_password = input("Enter your password to attempt authentication: ")

if zkp_auth(client_password, server_public_key):
    print("\nAuthentication SUCCESS! You proved you know the password.")
else:
    print("\nAuthentication FAILED! Proof invalid.")