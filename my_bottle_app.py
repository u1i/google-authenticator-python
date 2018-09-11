from bottle import Bottle, request, view
import pyotp, random, qrcode, base64, io, os

# secret = pyotp.random_base32()
# secret = "NZ767ZQKHUIGFA2D"

# Get the secret from an environment variable
try:
	secret = os.environ['secret']
except:
	exit("ERROR: Please set the 'secret' environment variable that contains the 16 character base32 secret")

# Get the app_id from an environment variable
try:
	app_id = os.environ['app_id']
except:
	exit("ERROR: Please set the 'app_id' environment variable")

app_name = "My Test App " + str(app_id)
user_account = "bob@localhost"


totp = pyotp.TOTP(secret)

app = Bottle()

# Show the current PIN
@app.get('/code')
def get_home():

	return(str(totp.now()))

# Reveal the secret
@app.get('/secret')
def get_secret():

	return(str(secret))


@app.get('/qr')
def do_qr():

	# construct URL for Google Authenticator
	url = pyotp.totp.TOTP(secret).provisioning_uri(user_account, issuer_name=app_name)

	# Turn it into a QR Code (PNG)
	img = qrcode.make(url)

	# Get the content of the image
	with io.BytesIO() as output:
		img.save(output, format="PNG")
		contents = output.getvalue()

	# Return a base64 encoded image with an HTML wrapper
	out = '<img alt="Avatar" src="data:image/jpeg;base64,' + base64.b64encode(contents) + '">'
	return(out)

@app.get('/')
@view('my')
def do_templ():
	return(dict(message="", app_name=app_name))
