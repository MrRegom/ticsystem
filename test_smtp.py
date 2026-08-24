import smtplib
import sys

try:
    print("Testing connection to smtp.office365.com:587...")
    server = smtplib.SMTP('smtp.office365.com', 587, timeout=10)
    server.set_debuglevel(1)
    
    print("Sending EHLO...")
    server.ehlo()
    
    print("Starting TLS...")
    server.starttls()
    server.ehlo()
    
    print("Logging in...")
    server.login('informativos.hgf@appminsal.cl', 'inhgf0304$')
    
    print("SUCCESS: Logged in successfully!")
    server.quit()
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
