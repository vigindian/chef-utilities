#!/usr/bin/python3

#################################################
# Chef Server API: get env-details in json format
# 
# VN
#################################################

#prereq modules
import base64
import hashlib
import datetime
import requests
import os
from collections import OrderedDict

#X-Ops-Authorization-N prereq
import rsa
from rsa import common, transform, core
from rsa.pkcs1 import _pad_for_signing

#handle script arguments
import argparse

####################

#############
# FUNCTIONS
#############

def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

#sign the given message using private-key and openssl bash-cli - this method works too
def via_openssl(message, private_key_loc):
    import subprocess
    import tempfile

    p = subprocess.Popen("openssl rsautl -sign -inkey " + private_key_loc,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input=message.encode())
    if stderr or p.returncode != 0:
        print(stderr)
    return stdout

#sign the given message using private-key
def pure_sign(message, priv_key):
    '''Signs the message with the private key.

    :param message: the message to sign. Can be an 8-bit string or a file-like
        object. If ``message`` has a ``read()`` method, it is assumed to be a
        file-like object.
    :param priv_key: the :py:class:`rsa.PrivateKey` to sign with
    :return: a message signature block.
    :raise OverflowError: if the private key is too small to contain the
        requested hash.

    '''

    keylength = common.byte_size(priv_key.n)
    padded = _pad_for_signing(message, keylength)

    payload = transform.bytes2int(padded)
    encrypted = core.encrypt_int(payload, priv_key.d, priv_key.n)
    block = transform.int2bytes(encrypted, keylength)

    return block

def chefgetenv(env):
  environment = env

  regionenv = environment

  path = "/organizations/"+environment+"/environments/"+regionenv

  #chef-api prereqs ref: https://docs.chef.io/server/api_chef_server/
  hashed_body = base64.b64encode(hashlib.sha1(body.encode()).digest()).decode("ASCII")
  hashed_path = base64.b64encode(hashlib.sha1(path.encode()).digest()).decode("ASCII")
  timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

  #X-Ops-Authorization-N needs canonical headers in specific format
  canonical_request = 'Method:GET\nHashed Path:{hashed_path}\nX-Ops-Content-Hash:{hashed_body}\nX-Ops-Timestamp:{timestamp}\nX-Ops-UserId:{client_name}'
  canonical_request = canonical_request.format(hashed_body=hashed_body, hashed_path=hashed_path, timestamp=timestamp, client_name=client_name)
  ##print("DEBUG canonical: "+canonical_request)

  headers = "X-Ops-Timestamp:{timestamp}\nX-Ops-Userid:{client_name}\nX-Chef-Version:{chefversion}\nAccept:application/json\nX-Ops-Content-Hash:{hashed_body}\nX-Ops-Sign:version=1.0"
  headers = headers.format(hashed_body=hashed_body, timestamp=timestamp, client_name=client_name, hashed_path=hashed_path, chefversion=chefversion)
  headers = OrderedDict((a.split(":", 2)[0], a.split(":", 2)[1]) for a in headers.split("\n"))
  headers["X-Ops-Timestamp"] = timestamp

  #load the chef private-key
  with open(client_key, 'r') as privatefile:
    keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)

  #X-Ops-Authorization-N: sign the canonical-headers with private-key
  signed_request = base64.b64encode(pure_sign(canonical_request.encode(), privkey)).decode('utf-8')

  #X-Ops-Authorization-N: separate into multiple 60-character segments
  auth_headers = OrderedDict(("X-Ops-Authorization-{0}".format(i+1), chunk) for i, chunk in enumerate(chunks(signed_request, 60)))

  ##print("DEBUG: "+auth_headers)

  #append X-Ops-Authorization-N to headers
  all_headers = OrderedDict(headers)
  all_headers.update(auth_headers)

  ##print(requests.get(url+path, headers=all_headers, timeout=timeout).text)

  apicall=requests.get(url+path, headers=all_headers, timeout=timeout)
  apicallRC=apicall.status_code
  if apicallRC == 200:
    return apicall.text
  else:
    print("ERR HTTP_CODE: " +str(apicall.status_code)+ " HTTP_ERR_MESSAGE: "+str(apicall.text))
    return None

####################

########
# MAIN
########

#api-request: other prereqs
timeout=3
body = ""

if __name__ == '__main__':

  #parse input arguments
  parser = argparse.ArgumentParser()

  parser.add_argument(
        "-u",
        "--user",
        type = str,
        required = True,
        default = None,
        help = "Specify the chef-username")

  parser.add_argument(
        "-k",
        "--key",
        type = str,
        required = True,
        default = None,
        help = "Specify the chef private-key full-path. Eg: /home/johndoe/.chef/jdoe.pem")

  parser.add_argument(
        "-e",
        "--env",
        type = str,
        required = True,
        default = None,
        help = "Specify chef-environment name")

  parser.add_argument(
        "-s",
        "--url",
        required = True,
        default = None,
        type = str,
        help = "Specify chef-server URL. Eg: https://chef.example.com")

  parser.add_argument(
        "-v",
        "--version",
        #required = True,
        default = "12.18.14",
        type = str,
        help = "Specify chef-server version. Eg: 12.18.14")

  options = parser.parse_args()

  environment = options.env
  client_name = options.user
  client_key = options.key
  url = options.url
  chefversion = options.version

  path = "/organizations/"+environment+"/environments/"+environment

  #chef-api prereqs ref: https://docs.chef.io/server/api_chef_server/
  hashed_body = base64.b64encode(hashlib.sha1(body.encode()).digest()).decode("ASCII")
  hashed_path = base64.b64encode(hashlib.sha1(path.encode()).digest()).decode("ASCII")
  timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

  #X-Ops-Authorization-N needs canonical headers in specific format
  canonical_request = 'Method:GET\nHashed Path:{hashed_path}\nX-Ops-Content-Hash:{hashed_body}\nX-Ops-Timestamp:{timestamp}\nX-Ops-UserId:{client_name}'
  canonical_request = canonical_request.format(hashed_body=hashed_body, hashed_path=hashed_path, timestamp=timestamp, client_name=client_name)
  ##print("DEBUG canonical: "+canonical_request)

  headers = "X-Ops-Timestamp:{timestamp}\nX-Ops-Userid:{client_name}\nX-Chef-Version:{chefversion}\nAccept:application/json\nX-Ops-Content-Hash:{hashed_body}\nX-Ops-Sign:version=1.0"
  headers = headers.format(hashed_body=hashed_body, timestamp=timestamp, client_name=client_name, hashed_path=hashed_path, chefversion=chefversion)
  headers = OrderedDict((a.split(":", 2)[0], a.split(":", 2)[1]) for a in headers.split("\n"))
  headers["X-Ops-Timestamp"] = timestamp

  #load the chef private-key
  with open(client_key, 'r') as privatefile:
    keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)

  #X-Ops-Authorization-N: sign the canonical-headers with private-key
  signed_request = base64.b64encode(pure_sign(canonical_request.encode(), privkey)).decode('utf-8')

  #X-Ops-Authorization-N: separate into multiple 60-character segments
  auth_headers = OrderedDict(("X-Ops-Authorization-{0}".format(i+1), chunk) for i, chunk in enumerate(chunks(signed_request, 60)))

  ##print("DEBUG: "+auth_headers)

  #append X-Ops-Authorization-N to headers
  all_headers = OrderedDict(headers)
  all_headers.update(auth_headers)

  ##print(requests.get(url+path, headers=all_headers, timeout=timeout).text)

  apicall=requests.get(url+path, headers=all_headers, timeout=timeout)
  apicallRC=apicall.status_code
  if apicallRC == 200:
    print(apicall.text)
  else:
    print("ERR HTTP_CODE: " +str(apicall.status_code)+ " HTTP_ERR_MESSAGE: "+str(apicall.text))
