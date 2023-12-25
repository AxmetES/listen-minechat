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
Install requirements:
```bash
poetry install
```
### Usage
Start script:

For listening chat:
```bash
poetry run python listen-minechat.py --host minechat.dvmn.org --port 5000 --filename chat_log.txt
```
For write to chat:
```bash
poetry run python write-minechat.py --host minechat.dvmn.org --port 5050 --nickname "Hopeful Hardcore Pop"

(NOTICE): Use nickname stronly from nicknames.json file.
```
All chat history recoding in file ```chat_log.txt```