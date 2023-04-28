# Chef Utilities

## Chef Get Nodes via Chef API
[chefGetNodes](./chefGetNodes.py): Get node details via Chef API. The same concept can be used for different operations via the Chef API.

### Pre-requisites:
```pip3 install -r requirements.txt```

### Usage
```
$ ./chefGetNodes.py -h
usage: chefGetNodes.py [-h] -u USER -k KEY -e ENV [-n NODE]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Specify the chef-username
  -k KEY, --key KEY     Specify the chef private-key full-path. Eg: /home/johndoe/.chef/jdoe.pem
  -e ENV, --env ENV     Specify environment name
  -n NODE, --node NODE  Specify node name
```

## Chef Commands
[chef-commands](chef-commands.md): A set of frequently used Chef commands, from chef-server, chef-development-clients, and chef-client
