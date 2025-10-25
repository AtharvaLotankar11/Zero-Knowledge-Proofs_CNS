from flask import Flask, render_template, request, jsonify
import random
import hashlib
import secrets
import os

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# Shared parameters (large prime p, generator g, modulus q = p-1)
p = 10007  # Larger prime for demo (real-world: 2048-bit)
g = 5  # Generator
q = p - 1

# Server setup (simulates registration)
registered_password = "SecurePassword123"  # Correct password


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
    Returns (success, steps) where steps contains the verification process.
    """
    secret = hash_to_int(client_password)
    steps = []
    
    steps.append({
        'type': 'info',
        'message': f'Public parameters: p={p}, g={g}, q={q}'
    })
    steps.append({
        'type': 'info', 
        'message': f'Server public key: {server_public_key}'
    })

    for round_num in range(1, rounds + 1):
        steps.append({
            'type': 'round',
            'round': round_num,
            'message': f'Round {round_num}'
        })

        # Step 1: Client commitment
        k = random.randint(1, q - 1)
        t = pow(g, k, p)
        steps.append({
            'type': 'step',
            'message': f'Client commitment: t = {g}^{k} mod {p} = {t}'
        })

        # Step 2: Server challenge
        e = random.randint(1, q - 1)
        steps.append({
            'type': 'step',
            'message': f'Server challenge: e = {e}'
        })

        # Step 3: Client response
        s = (k + e * secret) % q
        steps.append({
            'type': 'step',
            'message': f'Client response: s = (k + e * secret) mod {q} = {s}'
        })

        # Step 4: Server verification
        left = pow(g, s, p)
        right = (t * pow(server_public_key, e, p)) % p
        steps.append({
            'type': 'verification',
            'message': f'Verification: {g}^{s} mod {p} = {left}'
        })
        steps.append({
            'type': 'verification',
            'message': f'Expected: t * (public_key)^{e} mod {p} = {right}'
        })

        if left != right:
            steps.append({
                'type': 'error',
                'message': f'Round {round_num} FAILED!'
            })
            return False, steps
        else:
            steps.append({
                'type': 'success',
                'message': f'Round {round_num} SUCCESS!'
            })

    return True, steps


# Calculate server public key
server_secret = hash_to_int(registered_password)
server_public_key = pow(g, server_secret, p)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    client_password = data.get('password', '')
    
    if not client_password:
        return jsonify({
            'success': False,
            'message': 'Password is required',
            'steps': []
        })
    
    success, steps = zkp_auth(client_password, server_public_key)
    
    return jsonify({
        'success': success,
        'message': 'Authentication SUCCESS! You proved you know the password.' if success else 'Authentication FAILED! Proof invalid.',
        'steps': steps
    })


# Export the Flask app for Vercel
app = app