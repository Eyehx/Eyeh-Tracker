from bs4 import BeautifulSoup
import requests
import argparse

banner = """
----------------------------------------------------------------
 _______               __      _______                   __    
|    ___|.--.--.-----.|  |--. |_     _|.----.---.-.----.|  |--.
|    ___||  |  |  -__||     |   |   |  |   _|  _  |  __||    < 
|_______||___  |_____||__|__|   |___|  |__| |___._|____||__|__|
         |_____|                                                         
----------------------------------------------------------------\n
"""


def show_result(infos):
    show_info = ("IP         {0}\n".format(infos["IP Address"]) +
                 "Longitude: {0}\n".format(infos["Longitude"]) +
                 "Latitude:  {0}\n".format(infos["Latitude"]) +
                 "Estado:    {0}\n".format(infos["Region"]) +
                 "Cidade:    {0}\n".format(infos["City"]) +
                 "País:      {0}\n".format(infos["Country"]))

    show_info = banner + show_info
    print(show_info)


def command_line():
    parse = argparse.ArgumentParser(
        description="Get information's of IP address")
    parse.add_argument("-i", "--ip", help="IP to get information's")
    args = parse.parse_args()
    if args.ip:
        get_data(args.ip)
    else:
        print(banner)
        parse.print_help()


def get_data(ip_address):
    url = "https://www.geodatatool.com/en/?ip=" + ip_address

    resp = requests.get(url)
    if not 200 <= resp.status_code < 299:
        print("failed", resp.status_code, url)
        return

    infos = search_information(resp.text)

    show_result(infos)
    return


def search_information(data):
    if data is not None:
        doc = BeautifulSoup(data, "html.parser")
        data_ip = doc.findAll(
            "div", {"class": "sidebar-data hidden-xs hidden-sm"})
        return take_information(data_ip)


def take_information(bs_data_found):
    data = bs_data_found[0]
    all_information = data.findAll("span")
    dict_data = {}
    i = 0
    while i < len(all_information):
        key = str(all_information[i].string).replace(":", "")
        value = str(all_information[i + 1].string)
        dict_data[key] = value
        i += 2
    return dict_data


command_line()