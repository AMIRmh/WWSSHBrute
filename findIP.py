import requests as req
import re
import sys

def main():

    for i in range(1, len(sys.argv)):
        country = sys.argv[i]
        s = req.session()
        res = s.get("https://lite.ip2location.com/" + country + "-ip-address-ranges")

        i = 0
        result = ""
        for line in res.text.splitlines():
            a = re.search(r'<td>(.*)</td>', line, re.M|re.I)
            if a:
                ip = a.group().replace("<td>","").replace("</td>","")
                if i % 2 == 0:
                    result += ip
                else:
                    result += "," + ip + "\n"
                i += 1
                print(ip)

        file = open(country, "w")
        file.write(result)
        file.close()

if len(sys.argv) == 1:
    print("Usage : python3 findIP.py COUNTRY_LIST")
    print("Example: python3 findIP.py france united-kingdom united-states germany")
    print("For viewing list of countries visit: https://lite.ip2location.com ")
else:
    main()