'''
    brew update
    brew upgrade
    brew install node
    node -v                 # verify node installed
    npm -v                  # verify npm installed 
    npm install ipfs-core

    brew install ipfs       
    ipfs                    # or 'ipfs --version' verify that ipfs installed 
    pip3 install ipfsapi

    ipfs init
    ipfs daemon
    # now can run all the files using ipfs


'''

'''
import * as IPFS from 'ipfs-core'

const ipfs = await IPFS.create()
const { cid } = await ipfs.add('Hello world')
console.info(cid)
'''

import ipfshttpclient

# Share TCP connections using a context manager
with ipfshttpclient.connect() as client:
	hash = client.add('test.txt')['Hash']
	print(client.stat(hash))

# Share TCP connections until the client session is closed
class SomeObject:
	def __init__(self):
		self._client = ipfshttpclient.connect(session=True)

	def do_something(self):
		hash = self._client.add('test.txt')['Hash']
		print(self._client.stat(hash))

	def close(self):  # Call this when your done
		self._client.close()