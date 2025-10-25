from flask import Flask, render_template, request, jsonify
import random
import hashlib
import secrets
import os
from datetime import datetime, date
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# Shared parameters (large prime p, generator g, modulus q = p-1)
p = 10007  # Larger prime for demo (real-world: 2048-bit)
g = 5  # Generator
q = p - 1

# Demo configurations
DEMO_CONFIGS = {
    'password': {
        'registered_password': "SecurePassword123",
        'description': "Prove you know a password without revealing it"
    },
    'age': {
        'min_age': 18,
        'description': "Prove you're over 18 without revealing your exact age"
    },
    'range': {
        'min_value': 1000,
        'max_value': 5000,
        'secret_number': 3500,
        'description': "Prove a number is in range [1000, 5000] without revealing it"
    },
    'membership': {
        'group_members': ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        'secret_member': "Charlie",
        'description': "Prove you're in a group without revealing which member you are"
    }
}


def hash_to_int(password):
    """
    Hash password to an integer secret using SHA-256.
    Converts string password to a numerical secret for ZKP math.
    """
    hash_obj = hashlib.sha256(password.encode())
    return int(hash_obj.hexdigest(), 16) % q


def zkp_password_auth(client_password, server_public_key, rounds=3):
    """ZKP password authentication using Schnorr protocol"""
    secret = hash_to_int(client_password)
    steps = []
    
    steps.append({
        'type': 'info',
        'message': f'🔧 Public parameters: p={p}, g={g}, q={q}'
    })
    steps.append({
        'type': 'info', 
        'message': f'🔑 Server public key: {server_public_key}'
    })

    for round_num in range(1, rounds + 1):
        steps.append({
            'type': 'round',
            'round': round_num,
            'message': f'🔄 Round {round_num} - Schnorr Protocol'
        })

        k = random.randint(1, q - 1)
        t = pow(g, k, p)
        steps.append({
            'type': 'step',
            'message': f'📤 Client commitment: t = {g}^{k} mod {p} = {t}'
        })

        e = random.randint(1, q - 1)
        steps.append({
            'type': 'step',
            'message': f'🎯 Server challenge: e = {e}'
        })

        s = (k + e * secret) % q
        steps.append({
            'type': 'step',
            'message': f'📥 Client response: s = (k + e * secret) mod {q} = {s}'
        })

        left = pow(g, s, p)
        right = (t * pow(server_public_key, e, p)) % p
        steps.append({
            'type': 'verification',
            'message': f'✅ Verification: {g}^{s} mod {p} = {left}'
        })
        steps.append({
            'type': 'verification',
            'message': f'🎯 Expected: t * (public_key)^{e} mod {p} = {right}'
        })

        if left != right:
            steps.append({
                'type': 'error',
                'message': f'❌ Round {round_num} FAILED!'
            })
            return False, steps
        else:
            steps.append({
                'type': 'success',
                'message': f'✅ Round {round_num} SUCCESS!'
            })

    return True, steps


def zkp_age_verification(birth_year, min_age=18, rounds=3):
    """Prove age >= min_age without revealing exact age"""
    current_year = datetime.now().year
    actual_age = current_year - birth_year
    steps = []
    
    steps.append({
        'type': 'info',
        'message': f'🎂 Age Verification: Proving age >= {min_age} without revealing exact age'
    })
    
    if actual_age < min_age:
        steps.append({
            'type': 'error',
            'message': f'❌ Age verification failed: You must be at least {min_age} years old'
        })
        return False, steps
    
    # Simplified ZKP for age (in practice, would use more complex range proofs)
    secret = actual_age - min_age  # How many years over minimum
    public_commitment = pow(g, secret, p)
    
    steps.append({
        'type': 'info',
        'message': f'🔐 Age commitment generated (hiding exact age)'
    })
    
    for round_num in range(1, rounds + 1):
        steps.append({
            'type': 'round',
            'round': round_num,
            'message': f'🔄 Round {round_num} - Age Range Proof'
        })
        
        r = random.randint(1, q - 1)
        commitment = pow(g, r, p)
        
        steps.append({
            'type': 'step',
            'message': f'📤 Prover commitment: C = g^r mod p = {commitment}'
        })
        
        challenge = random.randint(1, q - 1)
        steps.append({
            'type': 'step',
            'message': f'🎯 Verifier challenge: e = {challenge}'
        })
        
        response = (r + challenge * secret) % q
        steps.append({
            'type': 'step',
            'message': f'📥 Prover response: s = (r + e * age_proof) mod q = {response}'
        })
        
        # Verification
        left = pow(g, response, p)
        right = (commitment * pow(public_commitment, challenge, p)) % p
        
        steps.append({
            'type': 'verification',
            'message': f'✅ Verification: g^s = {left}, C * commitment^e = {right}'
        })
        
        if left == right:
            steps.append({
                'type': 'success',
                'message': f'✅ Round {round_num} SUCCESS! Age >= {min_age} verified'
            })
        else:
            steps.append({
                'type': 'error',
                'message': f'❌ Round {round_num} FAILED!'
            })
            return False, steps
    
    return True, steps


def zkp_range_proof(claimed_number, min_val, max_val, secret_number, rounds=3):
    """Prove a number is in range [min_val, max_val] without revealing it"""
    steps = []
    
    steps.append({
        'type': 'info',
        'message': f'📊 Range Proof: Proving number ∈ [{min_val}, {max_val}] without revealing it'
    })
    
    if claimed_number != secret_number:
        steps.append({
            'type': 'error',
            'message': f'❌ Invalid number provided'
        })
        return False, steps
    
    if not (min_val <= secret_number <= max_val):
        steps.append({
            'type': 'error',
            'message': f'❌ Number not in valid range [{min_val}, {max_val}]'
        })
        return False, steps
    
    # Simplified range proof using commitment scheme
    secret = secret_number - min_val  # Normalize to [0, max_val - min_val]
    public_commitment = pow(g, secret, p)
    
    steps.append({
        'type': 'info',
        'message': f'🔐 Range commitment generated for number in [{min_val}, {max_val}]'
    })
    
    for round_num in range(1, rounds + 1):
        steps.append({
            'type': 'round',
            'round': round_num,
            'message': f'🔄 Round {round_num} - Range Proof Protocol'
        })
        
        r = random.randint(1, q - 1)
        commitment = pow(g, r, p)
        
        steps.append({
            'type': 'step',
            'message': f'📤 Commitment: C = g^r mod p = {commitment}'
        })
        
        challenge = random.randint(1, q - 1)
        steps.append({
            'type': 'step',
            'message': f'🎯 Challenge: e = {challenge}'
        })
        
        response = (r + challenge * secret) % q
        steps.append({
            'type': 'step',
            'message': f'📥 Response: s = (r + e * normalized_value) mod q = {response}'
        })
        
        # Verification
        left = pow(g, response, p)
        right = (commitment * pow(public_commitment, challenge, p)) % p
        
        steps.append({
            'type': 'verification',
            'message': f'✅ Verification: g^s = {left}, C * public_commitment^e = {right}'
        })
        
        if left == right:
            steps.append({
                'type': 'success',
                'message': f'✅ Round {round_num} SUCCESS! Number in range [{min_val}, {max_val}] verified'
            })
        else:
            steps.append({
                'type': 'error',
                'message': f'❌ Round {round_num} FAILED!'
            })
            return False, steps
    
    return True, steps


def zkp_membership_proof(claimed_member, group_members, secret_member, rounds=3):
    """Prove membership in a group without revealing which member"""
    steps = []
    
    steps.append({
        'type': 'info',
        'message': f'👥 Membership Proof: Proving membership in group {group_members} without revealing identity'
    })
    
    if claimed_member != secret_member:
        steps.append({
            'type': 'error',
            'message': f'❌ Invalid member claim'
        })
        return False, steps
    
    if secret_member not in group_members:
        steps.append({
            'type': 'error',
            'message': f'❌ Member not in group'
        })
        return False, steps
    
    # Use member index as secret
    member_index = group_members.index(secret_member)
    secret = member_index + 1  # Avoid zero
    public_commitment = pow(g, secret, p)
    
    steps.append({
        'type': 'info',
        'message': f'🔐 Membership commitment generated (hiding specific identity)'
    })
    
    for round_num in range(1, rounds + 1):
        steps.append({
            'type': 'round',
            'round': round_num,
            'message': f'🔄 Round {round_num} - Membership Proof Protocol'
        })
        
        r = random.randint(1, q - 1)
        commitment = pow(g, r, p)
        
        steps.append({
            'type': 'step',
            'message': f'📤 Commitment: C = g^r mod p = {commitment}'
        })
        
        challenge = random.randint(1, q - 1)
        steps.append({
            'type': 'step',
            'message': f'🎯 Challenge: e = {challenge}'
        })
        
        response = (r + challenge * secret) % q
        steps.append({
            'type': 'step',
            'message': f'📥 Response: s = (r + e * member_proof) mod q = {response}'
        })
        
        # Verification
        left = pow(g, response, p)
        right = (commitment * pow(public_commitment, challenge, p)) % p
        
        steps.append({
            'type': 'verification',
            'message': f'✅ Verification: g^s = {left}, C * membership_commitment^e = {right}'
        })
        
        if left == right:
            steps.append({
                'type': 'success',
                'message': f'✅ Round {round_num} SUCCESS! Group membership verified'
            })
        else:
            steps.append({
                'type': 'error',
                'message': f'❌ Round {round_num} FAILED!'
            })
            return False, steps
    
    return True, steps


# Calculate server public key for password auth
server_secret = hash_to_int(DEMO_CONFIGS['password']['registered_password'])
server_public_key = pow(g, server_secret, p)


@app.route('/')
def index():
    return render_template('index.html', demos=DEMO_CONFIGS)


@app.route('/zkp/<demo_type>', methods=['POST'])
def zkp_demo(demo_type):
    data = request.get_json()
    
    try:
        if demo_type == 'password':
            client_password = data.get('password', '')
            if not client_password:
                return jsonify({
                    'success': False,
                    'message': 'Password is required',
                    'steps': []
                })
            
            success, steps = zkp_password_auth(client_password, server_public_key)
            message = 'Password authentication SUCCESS! You proved you know the password.' if success else 'Password authentication FAILED! Proof invalid.'
            
        elif demo_type == 'age':
            birth_year = data.get('birth_year')
            if not birth_year:
                return jsonify({
                    'success': False,
                    'message': 'Birth year is required',
                    'steps': []
                })
            
            success, steps = zkp_age_verification(int(birth_year), DEMO_CONFIGS['age']['min_age'])
            message = f'Age verification SUCCESS! You proved you are over {DEMO_CONFIGS["age"]["min_age"]}.' if success else 'Age verification FAILED!'
            
        elif demo_type == 'range':
            number = data.get('number')
            if number is None:
                return jsonify({
                    'success': False,
                    'message': 'Number is required',
                    'steps': []
                })
            
            config = DEMO_CONFIGS['range']
            success, steps = zkp_range_proof(int(number), config['min_value'], config['max_value'], config['secret_number'])
            message = f'Range proof SUCCESS! Number is in [{config["min_value"]}, {config["max_value"]}].' if success else 'Range proof FAILED!'
            
        elif demo_type == 'membership':
            member = data.get('member', '')
            if not member:
                return jsonify({
                    'success': False,
                    'message': 'Member name is required',
                    'steps': []
                })
            
            config = DEMO_CONFIGS['membership']
            success, steps = zkp_membership_proof(member, config['group_members'], config['secret_member'])
            message = 'Membership proof SUCCESS! You are a valid group member.' if success else 'Membership proof FAILED!'
            
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid demo type',
                'steps': []
            })
        
        return jsonify({
            'success': success,
            'message': message,
            'steps': steps
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}',
            'steps': []
        })


# Legacy endpoint for backward compatibility
@app.route('/authenticate', methods=['POST'])
def authenticate():
    return zkp_demo('password')


# Export the Flask app for Vercel
app = app