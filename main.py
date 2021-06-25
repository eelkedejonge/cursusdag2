import requests
import urllib3

# Disable warning for unverified SSL certificates
urllib3.disable_warnings()

host = "10.10.20.48"
port = 443
username = "developer"
password = "C1sco12345"

url = f"https://{host}:{port}/restconf/data/ietf-interfaces:interfaces"

headers = {
       "Content-Type": "application/yang-data+json",
       "Accept": "application/yang-data+json",
}


def get_interfaces():
    response = requests.get(url, headers=headers, auth=(username, password), verify=False)
    if response.status_code != 200:
        print(f"Error {response.status_code}")
    return response.json()


def show_interfaces(data):
    print(data)
    int_list = data["ietf-interfaces:interfaces"]["interface"]
    for interface in int_list:
        name = interface['name']
        description = interface['description']
        print(f"{name}: {description}")

def let_user_pick_interface():
    choice = input("choose an interface: ")
    if choice == "1":
        print(f"please do not choose interface GigabitEthernet{choice}")
        let_user_pick_interface()
    else:
        #print(f"GigabitEthernet{choice}")
        int_of_choice = f"GigabitEthernet{choice}"
        #print(int_of_choice)
        return int_of_choice

def show_int_of_choice(int_of_choice):
    show_int = requests.get(url + f"/interface={int_of_choice}",
                            headers=headers,
                            auth=(username, password),
                            verify=False)
    print(show_int.status_code)
    print(show_int.text)

def change_ip(int_of_choice):
    ip = input("new ip: ")
    netmask = input("new netmask: ")
    data ={"ietf-interfaces:interface": {
        "name": f"{int_of_choice}",
        "description": "To Epacity",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
            {
                "ip": f"{ip}",
                "netmask": f"{netmask}"
            }
            ]
        },
        "ietf-ip:ipv6": {
        }
    }}
    response = requests.put(url + f"/interface={int_of_choice}",
                            headers=headers,
                            auth=(username, password),
                            verify=False, json=data)
    print(response.text)

if __name__ == "__main__":
    data = get_interfaces()
    show_interfaces(data)
    int_of_choice = let_user_pick_interface()
    show_int_of_choice(int_of_choice)
    change_ip(int_of_choice)
    show_int_of_choice(int_of_choice)