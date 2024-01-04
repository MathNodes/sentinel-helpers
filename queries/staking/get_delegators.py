#!/bin/env python3

import requests

API      = "https://api.sentinel.mathnodes.com"
ENDPOINT = "/cosmos/staking/v1beta1/validators/%s/delegations"
PAGINATION = "/cosmos/staking/v1beta1/validators/%s/delegations?pagination.key=%s"
SATOSHI = 1000000
if __name__ == "__main__":
    with open("validator.addys", "r") as validator_addys:
        vdata = validator_addys.readlines()
    JSON_array = []    
    pkey = None
    num = 1    
    for a in vdata:
        validator_address = a.rstrip()
        r = requests.get(API + ENDPOINT % validator_address)
        JSON = r.json()
        #print(JSON)
        JSON_array.append(JSON)
        
        if "pagination" in JSON:
            try:
                pkey = JSON['pagination']['next_key'].rstrip().lstrip()
                pkey = pkey.replace('+', '/')
            except:
                pkey = None
            total = int(JSON['pagination']['total'])
            #print(pkey)
        if pkey:
            while pkey is not None and total != 0:
                r = requests.get(API + PAGINATION % (validator_address,pkey))
                JSON = r.json()
                #print(JSON)
                JSON_array.append(JSON)
                if "pagination" in JSON:
                    try:
                        pkey = JSON['pagination']['next_key'].rstrip().lstrip()
                        pkey = pkey.replace('+', '/')
                    except:
                        pkey = None
                    total = int(JSON['pagination']['total'])
                    #print(pkey)
        print("Parsend Validator: %d" % num)
        num += 1
        
    stakers = open("delegators.csv", "w")        
    for j in JSON_array:
        for delegate in j['delegation_responses']:
            balance = float(int(delegate['balance']['amount']) / SATOSHI)
            if balance != 0 and delegate['delegation']['delegator_address'] != "sent1vv8kmwrs24j5emzw8dp7k8satgea62l7knegd7":
                stakers.write(f"{delegate['delegation']['delegator_address']},{balance}\n")
            
    stakers.close()