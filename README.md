# 🔐 Zero-Knowledge Proof Concepts - Interactive Demo

A comprehensive educational platform demonstrating multiple Zero-Knowledge Proof (ZKP) concepts through interactive web-based implementations. This project showcases how cryptographic protocols can prove knowledge or properties without revealing sensitive information.

## 🎯 Abstract

Zero-Knowledge Proofs represent a revolutionary approach to privacy-preserving verification where a prover can demonstrate knowledge of secrets or satisfy conditions without revealing the underlying information. This educational platform implements four fundamental ZKP concepts:

1. **Password Authentication** - Prove password knowledge without transmission
2. **Age Verification** - Prove age requirements without revealing exact age  
3. **Range Proofs** - Prove values fall within ranges without disclosure
4. **Membership Proofs** - Prove group membership without revealing identity

Each implementation uses the Schnorr identification protocol and commitment schemes, providing practical demonstrations of cryptographic concepts fundamental to modern privacy-preserving systems.

## ✨ Features

### 🔐 Multiple ZKP Demonstrations
- **Password Authentication**: Schnorr protocol for secure login without password transmission
- **Age Verification**: Range proofs for proving age requirements (18+) without revealing exact age
- **Range Proofs**: Demonstrate values within specified ranges without disclosure
- **Membership Proofs**: Prove group membership without revealing specific identity

### 🎨 Interactive Learning Platform
- **Beautiful Modern UI**: Gradient-based interface with smooth animations
- **Step-by-Step Visualization**: Real-time display of cryptographic protocol execution
- **Educational Theory Section**: Explains completeness, soundness, and zero-knowledge properties
- **Multi-Round Verification**: Configurable rounds for enhanced security demonstration

### 🚀 Technical Excellence
- **Production Ready**: Deployed on Vercel with serverless architecture
- **Responsive Design**: Works seamlessly across all devices and screen sizes
- **Cryptographically Sound**: Based on discrete logarithm problem in finite fields
- **Educational Focus**: Clear explanations of mathematical foundations

## 🏗️ Architecture

### Mathematical Foundation
- **Prime Field**: Operations in Z_p where p = 10007 (demo prime)
- **Generator**: g = 5 (primitive root modulo p)
- **Hash Function**: SHA-256 for password-to-secret conversion
- **Protocol**: Schnorr identification scheme

### System Components
```
┌─────────────────────────────────────────────────────────────┐
│                    ZKP Concept Demonstrations                │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Password      │  Age Verify     │    Range Proof          │
│ Authentication  │   (18+ check)   │  (Value in [a,b])       │
├─────────────────┼─────────────────┼─────────────────────────┤
│  Membership     │   Mathematical  │   Interactive UI        │
│    Proof        │   Foundation    │   & Visualization       │
│ (Group member)  │ (Schnorr + DLP) │  (Step-by-step)         │
└─────────────────┴─────────────────┴─────────────────────────┘

Protocol Flow (for each concept):
┌─────────────────┐    ┌─────────────────┐
│     Prover      │    │    Verifier     │
│   (Client)      │    │    (Server)     │
│                 │    │                 │
│ 1. Commitment   │───▶│ 2. Challenge    │
│ 4. Response     │◀───│ 3. Verification │
│                 │    │                 │
└─────────────────┘    └─────────────────┘
```


**Test Credentials & Scenarios:**
- **Password Demo**: `SecurePassword123`
- **Age Demo**: Birth year 2000 or earlier (for 18+ verification)
- **Range Demo**: Secret number is `3500` (range: 1000-5000)
- **Membership Demo**: Valid member is `Charlie` from group [Alice, Bob, Charlie, Diana, Eve]

Try wrong values first to see how the system detects invalid proofs!

## 📋 Prerequisites

- Python 3.7+
- Flask 2.3.3
- Modern web browser
- Git

## 🛠️ Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/AtharvaLotankar11/Zero-Knowledge-Proofs_CNS.git
   cd Zero-Knowledge-Proofs_CNS
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your secret key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the demo**
   ```
   http://localhost:5000
   ```

### Vercel Deployment

This project is configured for seamless Vercel deployment:

1. **Fork/Clone this repository**
2. **Connect to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Deploy automatically

3. **Configuration**
   - Framework: Other
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`

## 📁 Project Structure

```
Zero-Knowledge-Proofs_CNS/
├── api/
│   └── index.py          # Vercel serverless function
├── templates/
│   └── index.html        # Frontend interface
├── app.py               # Local Flask application
├── main.py              # CLI demonstration
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel configuration
└── README.md           # Project documentation
```

## 🔬 How It Works

### 1. Core ZKP Concepts Demonstrated

#### Password Authentication (Schnorr Protocol)
```
Prover Secret: x = H(password) mod q
Public Key: y = g^x mod p

For each round:
1. Prover → Verifier: t = g^k mod p (commitment)
2. Verifier → Prover: e (random challenge)  
3. Prover → Verifier: s = k + ex mod q (response)
4. Verifier checks: g^s ≟ t × y^e mod p
```

#### Age Verification (Range Proof Simplified)
```
Proves: age ≥ min_age without revealing exact age
Secret: age_proof = actual_age - min_age
Uses commitment scheme to hide exact age while proving minimum requirement
```

#### Range Proof
```
Proves: value ∈ [min, max] without revealing value
Normalizes secret to [0, max-min] range
Uses commitment and challenge-response to verify range membership
```

#### Membership Proof  
```
Proves: identity ∈ group without revealing which member
Maps member to index, uses index as secret
Verifies group membership without identity disclosure
```

### 2. Security Properties (All Demos)
- **Completeness**: Honest prover always convinces honest verifier
- **Soundness**: Cheating probability ≤ 1/2^rounds (default: 1/8 for 3 rounds)
- **Zero-Knowledge**: Verifier learns only the proven fact, nothing more

### 3. Implementation Details
- **Mathematical Foundation**: Discrete logarithm problem in finite field Z_p
- **Hash Functions**: SHA-256 for deterministic secret generation
- **Commitment Schemes**: Pedersen-style commitments using modular exponentiation
- **Multi-Round Protocol**: 3 rounds by default for demonstration clarity
- **Finite Field**: Prime p=10007 (educational size; production uses 2048+ bit primes)

## 🎮 Usage Examples

### Web Interface - Multiple Demos
1. **Password Authentication**
   - Enter password: `SecurePassword123`
   - Click "Authenticate with ZKP"
   - Watch Schnorr protocol execution

2. **Age Verification**  
   - Enter birth year: `2000` (or earlier)
   - Click "Verify Age with ZKP"
   - See age range proof without revealing exact age

3. **Range Proof**
   - Enter number: `3500` 
   - Click "Prove Range with ZKP"
   - Verify number is in [1000, 5000] without disclosure

4. **Membership Proof**
   - Select member: `Charlie`
   - Click "Prove Membership with ZKP"  
   - Verify group membership without revealing identity

### Command Line (main.py)
```bash
python main.py
# Interactive password authentication demo
# Enter password when prompted
# Observe the mathematical proof process
```

### API Endpoints
```bash
# Password Authentication
curl -X POST http://localhost:5000/zkp/password \
  -H "Content-Type: application/json" \
  -d '{"password": "SecurePassword123"}'

# Age Verification  
curl -X POST http://localhost:5000/zkp/age \
  -H "Content-Type: application/json" \
  -d '{"birth_year": 2000}'

# Range Proof
curl -X POST http://localhost:5000/zkp/range \
  -H "Content-Type: application/json" \
  -d '{"number": 3500}'

# Membership Proof
curl -X POST http://localhost:5000/zkp/membership \
  -H "Content-Type: application/json" \
  -d '{"member": "Charlie"}'
```

## 🔧 Configuration

### Security Parameters
```python
p = 10007        # Prime modulus (use 2048-bit in production)
g = 5           # Generator
rounds = 3      # Number of verification rounds
```

### Environment Variables
```bash
SECRET_KEY=your-flask-secret-key  # For session management
```

## 🧪 Testing

### Test Cases

#### Password Authentication
1. **Correct Password** (`SecurePassword123`): Should pass all rounds
2. **Incorrect Password**: Should fail verification  
3. **Empty Password**: Should return error message

#### Age Verification
1. **Valid Age** (birth year ≤ 2006): Should pass verification
2. **Invalid Age** (birth year > 2006): Should fail with age requirement message
3. **Invalid Input**: Should handle non-numeric input gracefully

#### Range Proof  
1. **Correct Number** (`3500`): Should pass range verification
2. **Out of Range**: Should fail with range violation message
3. **Wrong Number in Range**: Should fail authentication

#### Membership Proof
1. **Valid Member** (`Charlie`): Should pass membership verification  
2. **Invalid Member** (`Frank`): Should fail with membership error
3. **Empty Selection**: Should return validation error

### Security Testing
- Verify cheating detection across all proof types
- Test with edge cases and boundary values
- Confirm fresh randomness in each protocol round
- Validate mathematical correctness of verification equations

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Add comments for complex mathematical operations
- Test with both valid and invalid inputs
- Update documentation for new features

## 📚 Educational Resources

### Zero-Knowledge Proofs
- [Introduction to Zero-Knowledge Proofs](https://blog.cryptographyengineering.com/2014/11/27/zero-knowledge-proofs-illustrated-primer/)
- [Schnorr Identification Protocol](https://en.wikipedia.org/wiki/Proof_of_knowledge#Schnorr_protocol)
- [Modern Cryptography Textbook](https://toc.cryptobook.us/)

### Implementation References
- [Discrete Logarithm Problem](https://en.wikipedia.org/wiki/Discrete_logarithm)
- [Modular Arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic)
- [Cryptographic Hash Functions](https://en.wikipedia.org/wiki/Cryptographic_hash_function)

## 🛡️ Security Considerations

### Production Deployment
- Use 2048-bit primes for real-world applications
- Implement proper session management
- Add rate limiting for authentication attempts
- Use HTTPS for all communications
- Consider timing attack mitigations

### Known Limitations
- Demo uses small prime (10007) for educational purposes
- No persistent user storage
- Single hardcoded password for demonstration
- Client-side JavaScript handles sensitive operations


## 👥 Authors

- **Atharva Lotankar** - Roll No: 27 - *Developer*
- **Vaishnavi Avhad** - Roll No: 41 - *Developer*


---

**⭐ Star this repository if you found it helpful!**

*Built with ❤️ for educational purposes and practical cryptography learning.*
