# TECHNIQUES-TO-IMPLEMENT-WEB-CRAWLERS-USING-MULTI-THREADING
We aim to implement multithread management and synchronization techniques for web crawlers. The key concepts we will focus on are process, thread, and synchronization. To implement synchronization, we will apply mutual exclusion and some locking techniques. These topics are all important components in operating systems

## Introduction
It is difficult to profile a webcrawler on external servers as they always have some sort of *api rate limiting* in place to avoid (DoS) denial of service attacks.
We hosted a local server using fastapi to *remove the server api-rate-limiting random bias* from different multithreading based webcrawler runs.
This server is based on two of the fastest growing Python libs  
1. [fastapi](https://fastapi.tiangolo.com/) and 
2. [uvicorn](https://www.uvicorn.org/).

### How to create a setup for the project
1. Update links to be crawled in file ...TECHNIQUES-TO-IMPLEMENT-WEB-CRAWLERS-USING-MULTI-THREADING\TestFiles\TestURL.txt
1. Make sure you have python3 and pip3 installed.
2. Open the terminal and Go to the director of downloaded project file ...\TECHNIQUES-TO-IMPLEMENT-WEB-CRAWLERS-USING-MULTI-THREADING\setup_startup
#### Windows
1. Set up virtual linux environment - To execute Shell Script File Using Windows Subsystem For Linux, download Ubuntu From The Microsoft Store, Integrate With WSL and initialize the newly installed Linux distro
2. follow steps for linux in Ubuntu
2. Open command promt or PowerShell Window, Type Bash and Click enter
3. run sh ./quick-setup.sh

#### Linux or macOS
1. Clone the git code: `git clone https://github.com/divaamahajan/TECHNIQUES-TO-IMPLEMENT-WEB-CRAWLERS-USING-MULTI-THREADING.git`
2. Navigate into TECHNIQUES-TO-IMPLEMENT-WEB-CRAWLERS-USING-MULTI-THREADING/setup_startup `cd TECHNIQUES-TO-IMPLEMENT-WEB-CRAWLERS-USING-MULTI-THREADING/setup_startup`
2. Run quick-setup.sh script `bash +x quick-setup.sh`.
3. Make sure you have virtual env installed. `sudo apt install python3.8-venv`
4. Activate the python virtual env with command printed between # lines.
```
########################################################################
Activate dev profile by running following command
source /home/divyamahajan/.serv-coder/bin/activate
########################################################################
```
I ran `source /home/divyamahajan/.serv-coder/bin/activate`
5. 





1. Set the script executable permission by running chmod command in Linux: chmod +x quick-setup.sh
2. Execute a shell script in Linux: ./quick-setup.sh
3




### driver.py - to maximize localserver throughput.
1. The local server also has limits
2. During testing, we found, we needed to restart the server on subsequent webcrawler runs.
3. We automated with that with a simple script called `driver.py`
4. `driver.py` script run shell commands via python `subprocess` to restart the local server in consecutive webcrawler runs to maximize throughput.

### How to run driver script
1. `driver.py` script can be copied into the `TECHNIQUES-TO-IMPLEMENT-WEB-CRAWLERS-USING-MULTI-THREADING/SourceCode` folder 
2. Run to make sure that the localserver provides maximum throughput to webcrawler.