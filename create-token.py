import pyotp
import sys
secret = pyotp.random_base32()
sys.stdout.write(secret)
sys.stdout.flush()


