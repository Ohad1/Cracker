# Cracker
Cracker is an application that cracks MD5 hashes of phone numbers
# Usage
The default configuration can be found in config.json
### Step 1
Install python 3.10.5
### Step 2
Run application using run_cracker.bat in project root or via CMD:
1. Open CMD in project root
    1. venv\Scripts\activate
    2. cd Cracker
    3. py cracker_app.py
### Step 3
Open a browser/Postman and send a GET HTTP request in the following format:\
http://{server_url}/crack?hashes={h1},{h2},...\
For example:\
http://127.0.0.1:5000/crack?hashes=276ec31f626a9dcf680b4401bd74f705,797d492e314fdf560fb7bf5b3b294356,75585c7f7f50c2dea2c4e0e92aafafcb \
The expected response is:\
{\
&nbsp;&nbsp;&nbsp;&nbsp;"276ec31f626a9dcf680b4401bd74f705": "050-7086178",\
&nbsp;&nbsp;&nbsp;&nbsp;"75585c7f7f50c2dea2c4e0e92aafafcb": "053-6588790",\
&nbsp;&nbsp;&nbsp;&nbsp;"797d492e314fdf560fb7bf5b3b294356": "057-7080167"\
}
# Implemented Features
* Hash Validation
* Parallel decoding of hashes
    * Retry mechanism in case of overload
    * Dynamic stopping of all used minions once decoded string is found
* Logger
* Error Handling
* DB + Cache
* Configuration
* Basic load balancing
# Future Features
* Reuse ongoing calculations
* Algorithm to save more decoded hashes calculated by a minion to DB and cache
