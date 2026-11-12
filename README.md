- Teleport: https://devops.lrk.si/web/cluster/devops.lrk.si/resources

# TO JE POIZKUS 'DOKUMENTACIJE' - NI SE MI DALO VEČ PISAT

# 1. Vagrant in cloud-init

## Postavitev okolja

```sh
tomy@mac:~> brew tap hashicorp/tap
```

```sh
tomy@mac:~> brew install hashicorp/tap/hashicorp-vagrant
```

```sh
tomy@mac:~> mkdir -p ~Desktop/DevOps/1vagrant/
```

```sh
tomy@mac:~> cd ~Desktop/DevOps/1vagrant/
```

```sh
tomy@mac:1vagrant> vagrant init bento/ubuntu-26.04
```

```sh
tomy@mac:1vagrant> vagrant up --provider=virtualbox
```

```sh
# Do virtualke dostopaš z:
tomy@mac:1vagrant> vagrant ssh
# Da greš ven iz virtualke:
tomy@vagrant:~> exit
```

## Dejanska naloga

```sh
tomy@mac:1vagrant> nano provision.sh
```

```sh
#!/bin/bash
set -e
apt update
DEBIAN_FRONTEND=noninteractive apt-get install -y nginx python3-flask
systemctl enable --now nginx
echo "Najlepša spletna stran" > /var/www/html/index.html
```

```sh
tomy@mac:1vagrant> nano Vagrantfile
```

Pod `grant.configure("2") do |config|` dodaj:
```sh
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.provision "shell", path: "provision.sh"
```

```sh
tomy@mac:1vagrant> vagrant reload --provision
```

## MacOS fix

Če `vagrant reload --provision` faila, dodaj temporary bugfix:
```sh
tomy@mac:~> mkdir -p ~/.vagrant.d
```

```sh
tomy@mac:~> nano ~/.vagrant.d/Vagrantfile
```

Znotraj `Vagrantfile` prilepi:
```python
require "socket"
require "timeout"
require "vagrant/util/is_port_open"

def port_check_bug?
  probe = TCPServer.new("127.0.0.1", 0)
  port = probe.addr[1]
  probe.close
  Socket.tcp("127.0.0.1", port, connect_timeout: 0.1).close
  true
rescue StandardError
  false
end

if port_check_bug?
  module Vagrant
    module Util
      module IsPortOpen
        def is_port_open?(host, port)
          Timeout.timeout(1) do
            TCPSocket.new(host, port).close
          end
          true
        rescue Errno::ETIMEDOUT,
               Errno::ECONNREFUSED,
               Errno::EHOSTUNREACH,
               Errno::ENETUNREACH,
               Errno::EACCES,
               Errno::ENOTCONN,
               Errno::EALREADY,
               Timeout::Error
          false
        end
        extend self
      end
    end
  end
end
```

## Nadaljevanje naloge

Prešaltam iz basic nginx na Flask:
```sh
tomy@mac:1vagrant> mkdir -p app
```

```sh
tomy@mac:1vagrant> nano app/app.py
```

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Najlepša spletna stran v Flasku"

@app.route("/health")
def health():
    return jsonify(status="ok")
```

```sh
tomy@mac:1vagrant> vagrant provision
# če si ugasnil računalnik vmes uporabi vagrant up --provision
```

Probi pognat Flask s Pythonom:
```sh
tomy@mac:1vagrant> vagrant ssh
```

```sh
tomy@vagrant:~> cd /vagrant/app
```

Zalaufi Flask server:
```sh
tomy@vagrant:~> python3 -m flask --app app run --host 127.0.0.1 --port 5000
```

Odpri nov terminal na Macu, prever če dela:
```sh
tomy@mac:~> vagrant ssh -c "curl http://127.0.0.1:5000/health"
```

# Podatkovna baza

Test:
```
devops=> INSERT INTO messages (id, content) VALUES (1, 'Najlepša podatkovna baza');
INSERT 0 1
devops=> SELECT * FROM messages;
 id |         content          
----+--------------------------
  1 | Najlepša podatkovna baza
(1 row)
```
