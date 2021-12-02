# Alpha Beta Discord Bot

# How to run it
1. create a `virtualenv` and install packages and create `.env` file
    + if you use windows 
        ```powershell
        python -m venv .venv
        .\.venv\Script\activate
        pip install -r requirements.txt
        ```
        rename `.env-sample` to `.env` and put your `discord ID` to `USER_ID` variable must be an integer
    + if you use linux
        ```bash
        sudo apt install virtualenv
        virtualenv -p py3 .venv
        source .venv/bin/activate
        pip3 install -r requirements.txt
        mv .env-sample .env
        ```
        ```python
        # open .env file and put this on it
        USER_ID = # your discord ID must be an integer
        ```
    + if you use mac
        ```bash
        sudo brew install virtualenv
        virtualrnv -p py3 .venv
        source .venv/bin/activate
        pip3 install -r requirements.txt
        mv .env-sample .env
        ```
        ```python
        # open .env file and put this on it
        USER_ID = # your discord ID must be an integer
        ```
2. run bot
    ```bash
    python3 happy.py
    python3 sad.py
    ```
# bot commands
## feels
1. `feels` => if on sad bot => `Add your sad feels to database` , 
if on happy bot `Add your happy feels to database`

2.`time`, `much` => if on sad bot => `show your sad feels`, if on happy bot `show your happy feels`

3. `clear` => `clear your feels`

## notes
4. `note`, `notes`, `add-note` => `add your notes to database`

5.`show-note`, `see-note`, `find-note` => `add your notes to database`

6. `delete-note`, `del-note` => `delete your notes from database`

## codes
7. `code`, `codes`, `add-code` => `add your codes to database`

8.`show-code`, `see-code`, `find-code` => `add your codes to database`

9. `delete-code`, `del-code` => `delete your codes from database`

## help
10. `help` => `help command`

----
## i hope you enjoy that
## writed by metidotpy
