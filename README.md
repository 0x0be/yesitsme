<p align="center">
    <img src="https://github.com/blackeko/yesitsme/blob/media/logo.png" alt="yesitsme logo">
</p>

<h3 align="center">Yes, it's me!</h3>
<p align="center">
   Simple OSINT script to find Instagram profiles by name and e-mail/phone 
</p>

# 💬 Description
**yesitsme** is a simple Python script which tries to find Instagram account associated with a specific name, e-mail and phone number.
Leveraging dumpor.com indexing capabilities, it retrieves all usernames associated with a certain name and automatically compares the fetched toutatis obfuscated e-mail/phone with the given one, saving time and energy while doing online investigations.  



# ⚙️ Installation
```console
eva@paradise:~$ git clone https://github.com/blackeko/yesitsme/
eva@paradise:~$ cd yesitsme
eva@paradise:~$ pip3 install -r requirements.txt
eva@paradise:~$ python3 yesitsme.py -s SESSION_ID -n NAME -e EMAIL -p PHONE -t TIMEOUT 
```

# 🕹️ Usage
## Argument description
- ```-s``` "SESSION_ID"
  - *sessionid* cookie of your Instagram account (i.e. sockpuppet);
- ```-n``` "Name Surname"
  - Target *name* and *surname* (case insensitive);
- ```-e``` "a****z<span>@</span>domain.tld"
  - *First* and *last letter* of target e-mail;
- ```-p``` "+39 ** 09"
  - *Area code* and *last two digits* of target phone number;
- ```-t``` "10"
  - *Timeout* between each request (default = 0).

## Example
```console
eva@paradise:~$ python3 yesitsme.py -s 5t3El3650d4Z7A3jA2%Y1R70vnYn%36U3 -n "John Doe" -e "j*****e@gmail.com" -p "+39 *** *** **09" -t 10
```

## Output
<img src="https://github.com/blackeko/yesitsme/blob/media/screenshot_1.png">

Three levels of match:
- **HIGH**: name, e-mail and phone number (obfuscated) match; 
- **MEDIUM**: name and/or e-mail and/or phone match;
- **LOW**: only one of them matches.

# 📝 Notes
- Name and e-mail (or phone number) are **mandatory**;
- To leave e-mail/phone empty, simply set ```-e/-p " "```;
- E-mail/phone asterisks are just for show and **can be omitted**;
- If omitted, timeout is zero; it's recommended to set at least 10 seconds to avoid being detected;
- Phone number must be in the **same format** as in the example, i.e. it must contain the area code (including plus symbol) and the whitespace;
- When the match level is HIGH, it will prompt whether to stop or continue searching.

# 🍪 Retrieve Instagram sessionid
While logged in your Instagram account:
  1. Right-click and click on Inspect Element to open the developer console;
  2. Go to the Storage tab;
  3. Expand the Cookies menu and check "sessionid" cookie.

<img src="https://github.com/blackeko/yesitsme/blob/media/screenshot_2.png">


# 🙏🏻 Credits
Thanks to: 
* [Toutatis](https://github.com/megadose/toutatis)
* [Dumpor](https://dumpor.com/)