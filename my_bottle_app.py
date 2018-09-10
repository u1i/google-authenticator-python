from bottle import Bottle, request, view
import pyotp, random, qrcode, base64, io

app_name = "My Test App"
user_account = "bob@localhost"
# secret = pyotp.random_base32()
secret = "NZ767ZQKHUIGFA2D"

totp = pyotp.TOTP(secret)

app = Bottle()

@app.get('/code')
def get_home():

	return("current token is: " + str(totp.now()))

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
	return(dict(message="hello!"))
