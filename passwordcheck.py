import requests 
import hashlib
import sys

#password hash generator - https://www.md5hashgenerator.com/sha1-generator.php (sha1 as the API uses this)
#k - anonimity: first 5 hash characters sending to the API
# API GET https://api.pwnedpasswords.com/range/{first 5 hash chars}
#Idempotent - the input will always gives the same output. like MD5 hash


#send request to API 
def request_api(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res  #sample is response 200. 

def get_password_leaks_count(response, tail): #response contains all the passwords matched and count; tail - our password >5chars
    #split the response with : count
    hashes = (line.split(':') for line in response.text.splitlines())
#    for line in response.text.splitlines():
 #       print(line.split(':'))
    for h, count in hashes:
        if h == tail:
            print(count)
            return count
    return 0

#get first 5 hash chars
def send_APIHash(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
  #  print(first5_char)
    response = request_api(first5_char)
   # print(response.text)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = send_APIHash(password)
        if count:
            print(f'{password} is found {count} times. See if you want to change it')
        else: 
            print(f'{password} not found. Carry on!')


main(sys.argv[1:])





