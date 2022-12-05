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

import ipfsApi

if __name__ == '__main__':

     # Connect to local node
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
        print(api)
    except ipfsapi.exceptions.ConnectionError as ce:
        print(str(ce))

    #new_file = api.add('new.txt')
    #print(new_file)

    #node = await IPFS.create()
    #data = 'Hello, :)'