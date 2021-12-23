import sys
import colorama
import time
import argparse
import json
import httpx
import hmac
import hashlib
import urllib
import requests
from httpx import get
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style, init

colorama.init(autoreset=True)


def banner():
    print("                _ _   _                ")
    print("  _  _ ___ ___ (_) |_( )___  _ __  ___ ")
    print(" | || / -_|_-< | |  _|/(_-< | '  \/ -_)")
    print("  \_, \___/__/ |_|\__| /__/ |_|_|_\___|")
    print("  |__/                                 ")
    print("\n\tTwitter: " + Fore.MAGENTA + "@blackeko5")


def getUserId(username, sessionsId):
    cookies = {'sessionid': sessionsId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96', }
    r = get('https://www.instagram.com/{}/?__a=1'.format(username),
            headers=headers, cookies=cookies)
    try:
        info = json.loads(r.text)
        id = info["logging_page_id"].strip("profilePage_")
        return({"id": id, "error": None})
    except:
        return({"id": None, "error": "User not found or rate limit"})


def getInfo(username, sessionId):
    userId = getUserId(username, sessionId)
    if userId["error"] != None:
        return({"user": None, "error": "User not found or rate limit"})
    else:
        cookies = {'sessionid': sessionId}
        headers = {'User-Agent': 'Instagram 64.0.0.14.96', }
        response = get('https://i.instagram.com/api/v1/users/' +
                       userId["id"]+'/info/', headers=headers, cookies=cookies)
        info = json.loads(response.text)
        infoUser = info["user"]
        infoUser["userID"] = userId["id"]
        return({"user": infoUser, "error": None})


def advanced_lookup(username):
    USERS_LOOKUP_URL = 'https://i.instagram.com/api/v1/users/lookup/'
    SIG_KEY_VERSION = '4'
    IG_SIG_KEY = 'e6358aeede676184b9fe702b30f4fd35e71744605e39d2181a34cede076b3c33'

    def generate_signature(data):
        return 'ig_sig_key_version=' + SIG_KEY_VERSION + '&signed_body=' + hmac.new(IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + urllib.parse.quote_plus(data)

    def generate_data(phone_number_raw):
        data = {'login_attempt_count': '0',
                'directly_sign_in': 'true',
                'source': 'default',
                'q': phone_number_raw,
                'ig_sig_key_version': SIG_KEY_VERSION
                }
        return data

    data = generate_signature(json.dumps(generate_data(username)))
    headers = {
        "Accept-Language": "en-US",
        "User-Agent": "Instagram 101.0.0.15.120",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate",
        "X-FB-HTTP-Engine": "Liger",
        "Connection": "close"}
    try:
        r = httpx.post(USERS_LOOKUP_URL, headers=headers, data=data)
        rep = r.json()
        return({"user": rep, "error": None})
    except:
        return({"user": None, "error": "rate limit"})


def dumpor(name):
    url = "https://dumpor.com/search?query="
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    req = url + name.replace(" ", "+")

    try:
        account_list = []
        response = requests.get(req, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        accounts = soup.findAll('a', {"class": "profile-name-link"})
        for account in accounts:
            account_list.append(account.text)
        return({"user": account_list, "error": None})
    except:
        return({"user": None, "error": "rate limit"})


def main():
    banner()
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    parser.add_argument('-s', '--sessionid',
                        help="Instagram session ID", required=True)
    parser.add_argument(
        '-n', '--name', help="Target name & surname", required=True)
    parser.add_argument('-e', '--email', help="Target email", required=True)
    parser.add_argument(
        '-p', '--phone', help="Target phone number", required=True)
    parser.add_argument('-t', '--timeout',
                        help="Timeout between requests", required=False)

    args = parser.parse_args()

    sessionsId = args.sessionid
    name = args.name
    email = args.email
    phone = args.phone
    timeout = args.timeout

    accounts = dumpor(name)

    if accounts["user"] == None:
        print(accounts["error"])
    else:
        for account in accounts["user"]:
            name_f, email_f, phone_f = 0, 0, 0
            infos = getInfo(account[1:], sessionsId)
            if infos["user"] == None:
                print(infos["error"])
            else:
                infos = infos["user"]

                print("\nInformation about      : " + infos["username"])
                if(infos["full_name"].lower() == name.lower()):
                    print(Fore.GREEN + "Full Name              : " +
                          infos["full_name"] + " \u2713")
                    name_f = 1
                else:
                    print("Full Name              : " + infos["full_name"])
                print("User ID                : " + infos["userID"])
                print("Verified               : " + str(infos['is_verified']))
                print("Is business Account    : " + str(infos["is_business"]))
                print("Is private Account     : " + str(infos["is_private"]))
                print("Followers              : " +
                      str(infos["follower_count"]))
                print("Following              : " +
                      str(infos["following_count"]))
                print("Number of posts        : " + str(infos["media_count"]))
                print("External URL           : " + infos["external_url"])
                print("Biography              : " + infos["biography"])
                if "public_email" in infos.keys():
                    if infos["public_email"] != '':
                        if(email != ' ' and infos["public_email"][0] == email[0] and infos["public_email"].split('@')[0][-1] == email.split('@')[0][-1]
                                    and infos["public_email"].split('@')[1] == email.split('@')[1]):
                            print(Fore.GREEN + "Public email           : " +
                                  infos["public_email"] + " \u2713")
                            email_f = 1
                        else:
                            print("Public email           : " +
                                  infos["public_email"])

                if "public_phone_number" in infos.keys():
                    if str(infos["public_phone_number"]) != '':
                        if(phone != ' ' and str(infos["public_phone_number"]).split()[0] == phone.split()[0] and str(infos["public_phone_number"])[-2:] == phone[-2:]):
                            print(Fore.GREEN + "Public phone number    : " +
                                  str(infos["public_phone_number"]) + " \u2713")
                            phone_f = 1
                        else:
                            print("Public phone    : " +
                                  str(infos["public_phone_number"]))

                other_infos = advanced_lookup(account[1:])
                if other_infos["error"] == "rate limit":
                    print("Rate limit please wait a few minutes before you try again")
                elif "message" in other_infos["user"].keys():
                    if other_infos["user"]["message"] == "No users found":
                        print("The lookup did not work on this account")
                    else:
                        sys.exit(
                            Fore.RED + "Rate limit! Please, wait a few minutes before running the script again.")
                else:
                    if "obfuscated_email" in other_infos["user"].keys():
                        if other_infos["user"]["obfuscated_email"] != '':
                            if(email != ' ' and other_infos["user"]["obfuscated_email"][0] == email[0] and other_infos["user"]["obfuscated_email"][8] == email.split('@')[0][-1]
                                    and other_infos["user"]["obfuscated_email"].split('@')[1] == email.split('@')[1]):
                                print(Fore.GREEN + "Obfuscated email       : " +
                                      other_infos["user"]["obfuscated_email"] + " \u2713")
                                email_f = 1
                            else:
                                print("Obfuscated email       : " +
                                      other_infos["user"]["obfuscated_email"])

                        else:
                            print("No obfuscated email found")

                    if "obfuscated_phone" in other_infos["user"].keys():
                        if str(other_infos["user"]["obfuscated_phone"]) != '':
                            if(phone != ' ' and str(other_infos["user"]["obfuscated_phone"].split()[0]) == phone.split()[0] and str(other_infos["user"]["obfuscated_phone"])[-2:] == phone[-2:]):
                                print(Fore.GREEN + "Obfuscated phone       : " +
                                      str(other_infos["user"]["obfuscated_phone"]) + " \u2713")
                                phone_f = 1
                            else:
                                print("Obfuscated phone       : " +
                                      str(other_infos["user"]["obfuscated_phone"]))
                        else:
                            print("No obfuscated phone found")

                print("Profile Picture        : " +
                      infos["hd_profile_pic_url_info"]["url"] + "\n")

            if(name_f + email_f + phone_f == 3):
                print(Fore.CYAN + "[*] " + Fore.GREEN + "Profile ID " +
                      infos["userID"] + " match level: HIGH\n")
                usr_choice = input("Stop searching? Y/n ")
                if(usr_choice.lower() == 'y'):
                    sys.exit(0)
                else:
                    pass

            elif(name_f + email_f + phone_f == 2):
                print(Fore.CYAN + "[*] " + Fore.YELLOW + "Profile ID " +
                      infos["userID"] + " match level: MEDIUM\n")

            elif(name_f + email_f + phone_f == 1):
                print(Fore.CYAN + "[*] " + Fore.RED + "Profile with ID " +
                      infos["userID"] + " match level: LOW\n")

            print("-"*30)

            if(timeout):
                time.sleep(int(timeout))


if __name__ == "__main__":
    main()
