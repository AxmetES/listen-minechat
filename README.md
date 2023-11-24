### Description

For listening special server.
For reply to server.

### Get started

Clone project:
```bash
git clone https://github.com/AxmetES/listen-minechat.git
```
```bash 
cd listen-minechat/
```
Create virtual environment:
```bash
python3 -m venv venv
```
Activate a virtual environment:
```bash
source venv/bin/activate
```
Install requirements:
```bash
pip install -r requirements.txt
```
### Usage
Start script:

For listening chat:
```bash
python3 listen-minechat.py --host minechat.dvmn.org --port 5000 --path chat_log.txt
```
For write to chat:
```bash
python3 write-minechat.py
```
All chat history recoding in file ```chat_log.txt```