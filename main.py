from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# Rate limiting storage
request_counter = {}

@app.route("/")
def home():
    return """
    <h1>CyberShield Security Scanner</h1>

    <form action="/scan">
        <input name="payload" placeholder="Enter text">
        <button type="submit">Scan</button>
    </form>
    """

@app.route("/scan")
def scan():

    payload = request.args.get("payload", "")
    ip = request.remote_addr

    # Count requests from each IP
    request_counter[ip] = request_counter.get(ip, 0) + 1

    if request_counter[ip] > 5:
        result = "Rate Limit Exceeded"

    elif "or 1=1" in payload.lower():
        result = "SQL Injection Detected"

    elif "<script>" in payload.lower():
        result = "XSS Attack Detected"

    elif "../" in payload:
        result = "Directory Traversal Detected"

    elif ";" in payload or "&&" in payload:
        result = "Command Injection Detected"

    else:
        result = "Safe Request"

    # Logging
    with open("security_log.txt", "a") as log:
        log.write(
            f"{datetime.now()} | "
            f"IP: {ip} | "
            f"Payload: {payload} | "
            f"Result: {result}\n"
        )

    return f"""
    <h2>Scan Result</h2>

    <p><b>Input:</b> {payload}</p>

    <p><b>Status:</b> {result}</p>

    <p><b>Requests from your IP:</b> {request_counter[ip]}</p>
    """
@app.route("/dashboard")
def dashboard():

    return """
    <h1>CyberShield Dashboard</h1>

    <ul>
        <li>SQL Injection Attacks: 1</li>
        <li>XSS Attacks: 1</li>
        <li>Command Injection Attacks: 2</li>
        <li>Rate Limit Violations: 2</li>
    </ul>
    """

if __name__ == "__main__":
    app.run(debug=True)