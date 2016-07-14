# Gitlab Webhook
Webhook for resolve issues automatically when users push code in default branch,
with commit message like:
"Some text
Resolve: TASK 123"

* Install virtualenv is a tool to create isolated Python environments


```bash
pip install virtualenv
```

* Creates a virtual environment is the following:

```bash
virtualenv flask
```

* Download modules:

```bash
./flask/bin/pip install -r modules.txt 
```

* Set host, user data in config.py

* Run webhook:

```bash
./run.py
```
