from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64


def generate_key(request):
    rsa = RSA.generate(1024)
    private_pem = rsa.exportKey()
    request.session['key'] = str(private_pem, encoding="utf8")
    public_pem = rsa.publickey().exportKey()
    return str(public_pem, encoding="utf8")


def decrypt(request):
    pk = request.session.get('key')
    if pk:
        rsa_key = RSA.importKey(pk)
        cipher_rsa = PKCS1_v1_5.new(rsa_key)
        content = str(cipher_rsa.decrypt(base64.b64decode(request.data['content']), None), encoding="utf8")
        timestamp = content[0:13]
        # TODO: Check timestamp in time limit
        return content[13:]
