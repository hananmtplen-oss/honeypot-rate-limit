from flask import Flask, request, jsonify
import time

app = Flask(__name__)
failed_attempts = {}

@app.route('/login', methods=['POST'])
def login():
    ip = request.remote_addr
    if ip not in failed_attempts:
        failed_attempts[ip] = {'count': 0, 'time': time.time()}
    
    data = request.get_json()
    if check_credentials(data['username'], data['password']):
        failed_attempts[ip] = {'count': 0, 'time': time.time()}
        return jsonify({'token': generate_token(data['username'])})
    else:
        failed_attempts[ip]['count'] += 1
        return jsonify({'error': 'Invalid credentials'}), 401
