# Chef Utilities

## Chef Get Nodes via Chef API
[chefGetNodes](./chefGetNodes.py): Get node details via Chef API. The same concept can be used for different operations via the Chef API.

### Pre-requisites:
```pip3 install -r requirements.txt```

### Usage
```
$ ./chefGetNodes.py -h
usage: chefGetNodes.py [-h] -u USER -k KEY -e ENV -s URL [-v VERSION] [-n NODE]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Specify the chef-username
  -k KEY, --key KEY     Specify the chef private-key full-path. Eg: /home/johndoe/.chef/jdoe.pem
  -e ENV, --env ENV     Specify environment name
  -s URL, --url URL     Specify chef-server URL. Eg: https://chef.example.com
  -v VERSION, --version VERSION
                        Specify chef-server version. Eg: 12.18.14
  -n NODE, --node NODE  Specify node name
```

## Chef Get Environment Details via Chef API
[chefGetEnv](chefGetEnv.py): Get chef environment details in json format via Chef API.
### Pre-requisites:
```pip3 install -r requirements.txt```

### Usage
```
$ ./chefGetEnv.py -h
usage: chefGetEnv.py [-h] -u USER -k KEY -e ENV -s URL [-v VERSION]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Specify the chef-username
  -k KEY, --key KEY     Specify the chef private-key full-path. Eg: /home/johndoe/.chef/jdoe.pem
  -e ENV, --env ENV     Specify chef-environment name
  -s URL, --url URL     Specify chef-server URL. Eg: https://chef.example.com
  -v VERSION, --version VERSION
                        Specify chef-server version. Eg: 12.18.14
```

## Chef Commands
[chef-commands](chef-commands.md): A set of frequently used Chef commands, from chef-server, chef-development-clients, and chef-client
