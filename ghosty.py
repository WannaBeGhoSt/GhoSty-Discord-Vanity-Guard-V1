import requests
import time

vanityopghosty = '' # Force Vanity Code
serverid = '' # Add Server Id 
token = ''  # Account Token 

base_url = 'https://discord.com/api/v9'
invite_url = f'{base_url}/invites/{vanityopghosty}'
settings_url = f'{base_url}/guilds/{serverid}/vanity-url'                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
audit_log_url = f'{base_url}/guilds/{serverid}/audit-logs'                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
guild_url = f'{base_url}/guilds/{serverid}'
dm_url = f'{base_url}/users/@me/channels'                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
user_url = f'{base_url}/users/'
headers = {
    'Authorization': f'{token}',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
}

def print_success(message):
    print(f'\033[92m[+] {message}\033[0m')

def print_error(message):
    print(f'\033[91m[-] {message}\033[0m')

def vanitycodecd():
    response = requests.get(settings_url, headers=headers)
    if response.status_code == 200:
        return response.json().get('code')                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
    else:                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
        print_error(f'Failed to get current vanity URL: {response.text}')
        return None

def setvanityopghosty():
    start_time = time.time()
    patch_response = requests.patch(
        settings_url,
        headers=headers,
        json={'code': vanityopghosty}
    )
    end_time = time.time()

    if patch_response.status_code == 200:
        duration = end_time - start_time
        print_success(f'Vanity URL "{vanityopghosty}" has been set for the server [in {duration:.2f} seconds].')                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
    else:
        print_error(f'Failed to set vanity URL: {patch_response.text}')

def kick_user(user_id):
    kick_url = f'{base_url}/guilds/{serverid}/members/{user_id}'
    response = requests.delete(kick_url, headers=headers)
    if response.status_code == 204:
        print_success(f'User {user_id} has been kicked from the server.')
    else:
        print_error(f'Unable to kick user {user_id} due to {response.text}')

def lastlogaudit():
    response = requests.get(audit_log_url, headers=headers, params={'limit': 1, 'action_type': 60})                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
    if response.status_code == 200:
        logs = response.json().get('audit_log_entries')
        if logs:
            return logs[0]
    else:
        print_error(f'Failed to get audit log: {response.text}')
    return None

def get_user_info(user_id):
    response = requests.get(f'{user_url}{user_id}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print_error(f'Failed to get user info: {response.text}')                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
        return None

def send_dm(user_id, message):
    payload = {'recipient_id': user_id}
    response = requests.post(dm_url, headers=headers, json=payload)
    if response.status_code == 200:
        dm_channel_id = response.json().get('id')
        message_url = f'{base_url}/channels/{dm_channel_id}/messages'
        message_payload = {'content': message}
        response = requests.post(message_url, headers=headers, json=message_payload)                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
        if response.status_code != 200:
            print_error(f'Failed to send DM: {response.text}')
    else:
        print_error(f'Failed to create DM channel: {response.text}')

def owneridfetch():
    response = requests.get(guild_url, headers=headers)
    if response.status_code == 200:
        return response.json().get('owner_id')
    else:
        print_error(f'Failed to get owner ID: {response.text}')
        return None

owner_id = owneridfetch()                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija

while True:                                                                                                                                                                                                                                                         # Made By GhoSty @ghostyjija
    try:
        current_code = vanitycodecd()
        if current_code != vanityopghosty:
            start_time = time.time()
            print_error(f'Unauthorized vanity URL change detected: {current_code}')
            
            
            setvanityopghosty()

            last_log_entry = lastlogaudit()
            if last_log_entry:
                user_id = last_log_entry.get('user_id')
                user_info = get_user_info(user_id)
                if user_info:
                    username = user_info.get('username')
                    discriminator = user_info.get('discriminator')
                    print_error(f'Unauthorized vanity URL change by {username}#{discriminator} detected: {current_code}.')                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija

                    message = f'Unauthorized vanity URL change by {username}#{discriminator} detected. Vanity URL reset to "{vanityopghosty}".'                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
                    if owner_id:
                        send_dm(owner_id, message)

                    kick_user(user_id)

            end_time = time.time()                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
            duration = end_time - start_time                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
            print_success(f'Action completed in {duration:.2f} seconds.')                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija

        time.sleep(10)                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija

    except requests.RequestException as e:
        print_error(f'Error occurred: {e}')                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
        time.sleep(60)                                                                                                                                                                                                                                                          # Made By GhoSty @ghostyjija
