# Chef Commands
- chef-server-ctl: Utility in Chef Server to interact with Chef Server directly from the chef-server-node.
- knife: Chef client utility that can be run from any client that has connectivity to the chef-server. Please remember to export the corresponding CHEF_ENV before running the ```knife``` commands.

## Create new Chef Organisation
```
chef-server-ctl org-create <new-org-name> '<org-short-desc>' --association_user <org-owner-username> --filename <chef-validator.pem>
```

## Create new Org user

### New User
```
chef-server-ctl org-user-add <org-name> <chef-user-name> 
```

### New Admin User
```
chef-server-ctl org-user-add <org-name> <chef-user-name> --admin
```

## List users
```
chef-server-ctl user-list
```

## Delete user
```
chef-server-ctl user-delete <chef-user-name>
```

## Upload Cookbook
```
knife upload /cookbooks/<cookbook-name>
```

## Upload Databags
```
knife upload /data_bags
```

## Bootstrap
### Add a new Ubuntu node to Chef
```
knife bootstrap -N <node-name> --ssh-user <ssh-user> --sudo --ssh-identity-file <ssh-key> -r <chef-role-name> -E <chef-env> -V -y --color --bootstrap-version <chef-version> --server-url <chef-org-env-url> <hostname/ip>
```

Example:
```
knife bootstrap -N test-app1 --ssh-user ubuntu --sudo --ssh-identity-file ~/.ssh/chef-key.pem -r 'role[app]' -E test -V -y --color --bootstrap-version 14.8.12 --server-url https://chef.example.com/organizations/test test-app1.example.com
```

### Add a new Ubuntu node to Chef, with databag secret:
```
knife bootstrap -N <node-name> --ssh-user <ssh-user> --sudo --ssh-identity-file <ssh-key> -r <chef-role-name> -E <chef-env> -V -y --color --bootstrap-version <chef-version> --secret-file <chef-secret-file> --server-url <chef-org-env-url> <hostname/ip>
```

Example:
```
knife bootstrap -N test-app1 --ssh-user ubuntu --sudo --ssh-identity-file ~/.ssh/chef-key.pem -r 'role[app]' -E test -V -y --color --bootstrap-version 14.8.12 --secret-file ~/.chef/chef_secret_key --server-url https://chef.example.com/organizations/test test-app1.example.com
```

## Environment Config
### Download
```
knife download /environments/<env-name>.json 
```

### Upload
```
knife upload /environments/<env-name>.json
```

## Roles
```
#Download all roles
knife download /roles/

#Download specific-role
knife upload /roles/<env-role>.json
```

## Chef-client dry-run
The chef-client can be run separately, but in some cases we want to dry-run it to debug new chef-code (cookbook/role/env/etc.) changes:
```
chef-client -W
```
