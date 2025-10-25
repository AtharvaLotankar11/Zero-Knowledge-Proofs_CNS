# 🔐 Zero-Knowledge Proof Authentication Demo

A comprehensive implementation of Zero-Knowledge Proof (ZKP) based password authentication system using Flask and modern web technologies. This project demonstrates how users can prove they know a password without actually transmitting it over the network.

## 🎯 Abstract

Zero-Knowledge Proofs represent a revolutionary approach to authentication where a prover can demonstrate knowledge of a secret (password) to a verifier without revealing the secret itself. This implementation showcases the Schnorr identification protocol, providing a practical demonstration of cryptographic concepts that are fundamental to modern security systems.

The system implements a multi-round challenge-response protocol where:
- **Prover (Client)**: Demonstrates knowledge of password without revealing it
- **Verifier (Server)**: Validates the proof without learning the password
- **Security**: Achieves soundness with cheating probability of 1/2^n for n rounds

## ✨ Features

- **🔒 Zero-Knowledge Authentication**: Prove password knowledge without transmission
- **🎨 Beautiful UI**: Modern gradient-based interface with animations
- **📊 Step-by-Step Visualization**: Real-time display of ZKP protocol execution
- **🔄 Multi-Round Verification**: Configurable rounds for enhanced security
- **🚀 Production Ready**: Deployed on Vercel with serverless architecture
- **📱 Responsive Design**: Works seamlessly across all devices
- **🛡️ Cryptographically Sound**: Based on discrete logarithm problem

## 🏗️ Architecture

### Mathematical Foundation
- **Prime Field**: Operations in Z_p where p = 10007 (demo prime)
- **Generator**: g = 5 (primitive root modulo p)
- **Hash Function**: SHA-256 for password-to-secret conversion
- **Protocol**: Schnorr identification scheme

### System Components
```
┌─────────────────┐    ┌─────────────────┐
│     Client      │    │     Server      │
│                 │    │                 │
│ 1. Commitment   │───▶│ 2. Challenge    │
│ 4. Response     │◀───│ 3. Verification │
│                 │    │                 │
└─────────────────┘    └─────────────────┘
```

## 🚀 Live Demo

**🌐 [Try the Live Demo](https://your-vercel-deployment-url.vercel.app)**

**Test Credentials:**
- Password: `SecurePassword123`
- Try wrong passwords first to see failure cases!

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

3. **Run the application**
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

### 1. Protocol Overview
The system implements the Schnorr identification protocol:

```
Client Secret: x = H(password) mod q
Server Public Key: y = g^x mod p

For each round:
1. Client → Server: t = g^k mod p (commitment)
2. Server → Client: e (random challenge)
3. Client → Server: s = k + ex mod q (response)
4. Server verifies: g^s ≟ t × y^e mod p
```

### 2. Security Properties
- **Completeness**: Honest prover always convinces honest verifier
- **Soundness**: Cheating probability ≤ 1/2^rounds
- **Zero-Knowledge**: Verifier learns nothing about the password

### 3. Implementation Details
- **Password Hashing**: SHA-256 converts passwords to mathematical secrets
- **Modular Arithmetic**: All operations in finite field Z_p
- **Random Generation**: Cryptographically secure random numbers
- **Multi-Round**: 3 rounds by default (1/8 cheating probability)

## 🎮 Usage Examples

### Web Interface
1. Open the application in your browser
2. Enter password: `SecurePassword123`
3. Click "Authenticate with ZKP"
4. Watch the step-by-step proof verification

### Command Line (main.py)
```bash
python main.py
# Enter password when prompted
# Observe the mathematical proof process
```

### API Endpoint
```bash
curl -X POST http://localhost:5000/authenticate \
  -H "Content-Type: application/json" \
  -d '{"password": "SecurePassword123"}'
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
1. **Correct Password**: Should pass all rounds
2. **Incorrect Password**: Should fail verification
3. **Empty Password**: Should return error message
4. **Multiple Attempts**: Each attempt uses fresh randomness

### Security Testing
- Verify cheating detection works
- Test with various password lengths
- Confirm randomness in each round

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Atharva Lotankar** - Roll No: 27 - *Lead Developer*
- **Vaishnavi Avhad** - Roll No: 41 - *Co-Developer*

## 🙏 Acknowledgments

- Computer Networks and Security Course
- Flask Framework Community
- Cryptography Research Community
- Vercel for hosting platform

## 📞 Support

For questions, issues, or contributions:
- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/AtharvaLotankar11/Zero-Knowledge-Proofs_CNS/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/AtharvaLotankar11/Zero-Knowledge-Proofs_CNS/discussions)

---

**⭐ Star this repository if you found it helpful!**

*Built with ❤️ for educational purposes and practical cryptography learning.*