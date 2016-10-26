from stampery import Stampery

# Sign up and get your secret token at https://api-dashboard.stampery.com
client = Stampery('user-secret')

def on_ready():
    digest = client.hash("Hello, blockchain!")
    client.stamp(digest)

def on_proof(hash, proof):
    print("Received proof for")
    print(hash)
    print("Proof")
    print(proof)

def on_error(err):
    print("Woot: %s" % err)

client.on("error", on_error)
client.on("proof", on_proof)
client.on("ready", on_ready)

client.start()
