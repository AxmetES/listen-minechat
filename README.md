### Description

For listening special server.

### Get started

Clone project:
```bash
git clone https://github.com/AxmetES/listen-minechat.git
```
Activate a virtual environment.

```bash 
cd ./project rep
```
```bash
source venv/var/activate
```
Install requirements:
```bash
pip install -r requirements.txt
```

### Usage

Start script:

```bash
python3 listen-minechat.py --host minechat.dvmn.org --port 5000 --path chat_log.txt
```

All chat history recoding in file ```chat_log.txt```