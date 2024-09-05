import os
import random
import string
import asyncio
import aiohttp
from colorama import Fore, Style, init

# Initialize colorama with autoreset to ensure colors are reset after each print
init(autoreset=True)

# Global setting to control whether taken usernames are shown or not
show_taken_usernames = True  # Boolean setting to control whether taken usernames are shown or not

def print_watermark():
    print("""
    ░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██╗░░██╗██╗░░██╗
    ██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔═══██╗╚██╗██╔╝╚██╗██╔╝
    ██║░░╚═╝██████╔╝███████║░╚██╗████╗██╔╝██║██╗██║░╚███╔╝░░╚███╔╝░
    ██║░░██╗██╔══██╗██╔══██║░░████╔═████║░╚██████╔╝░██╔██╗░░██╔██╗░
    ╚█████╔╝██║░░██║██║░░██║░░╚██╔╝░╚██╔╝░░╚═██╔═╝░██╔╝╚██╗██╔╝╚██╗
    ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝
          
    RBLX-Username v1.0 Beta
    """)

def generate_random_username(length=5):
    while True:
        characters = string.ascii_lowercase + string.digits + "_"
        username = ''.join(random.choices(characters, k=length))
        
        if (any(char.isdigit() for char in username) or '_' in username) and not (username.startswith('_') or username.endswith('_')):
            return username

async def check_roblox_username_exists(session, username, timeout=4):
    url = f"https://www.roblox.com/users/profile?username={username}"
    
    try:
        async with session.get(url, timeout=timeout) as response:
            if response.status == 200:
                # Assuming a 200 status means account exists (could be taken or banned)
                page_content = await response.text()
                if "banned" in page_content.lower():
                    return "banned"
                return True  # Account exists (taken)
            else:
                return False  # Account does not exist (available)
    except asyncio.TimeoutError:
        print(f"{Fore.WHITE}{username} - {Fore.YELLOW}Request timed out{Style.RESET_ALL}")
        return None  # Timeout

async def check_usernames_concurrently(usernames):
    async with aiohttp.ClientSession() as session:
        tasks = [check_roblox_username_exists(session, username) for username in usernames]
        return await asyncio.gather(*tasks)

async def check_username(username):
    async with aiohttp.ClientSession() as session:
        result = await check_roblox_username_exists(session, username)
        if result is None:
            print(f"{Fore.WHITE}{username} - {Fore.YELLOW}Request timed out{Style.RESET_ALL}")
        elif result == "banned":
            print(f"{Fore.WHITE}{username} - {Fore.MAGENTA}Account is banned{Style.RESET_ALL}")
        elif result:
            print(f"{Fore.WHITE}{username} - {Fore.GREEN}Account exists (taken){Style.RESET_ALL}")
        else:
            print(f"{Fore.WHITE}{username} - {Fore.RED}Account does not exist (available){Style.RESET_ALL}")

def display_username(username, is_taken):
    global show_taken_usernames
    if is_taken:
        if show_taken_usernames:
            print(f"{Fore.WHITE}{username} - {Fore.GREEN}Account exists (taken){Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}{username} - {Fore.RED}Account does not exist (available){Style.RESET_ALL}")

def generate_usernames(number_of_usernames):
    usernames = []
    while len(usernames) < number_of_usernames:
        username = generate_random_username()
        if show_taken_usernames:
            usernames.append(username)
        else:
            async def check_and_append(username):
                async with aiohttp.ClientSession() as session:
                    result = await check_roblox_username_exists(session, username)
                    if result is None:
                        print(f"{Fore.WHITE}{username} - {Fore.YELLOW}Request timed out{Style.RESET_ALL}")
                    elif not result:  # If the username is not taken
                        usernames.append(username)
                    else:
                        print(f"{Fore.WHITE}{username} - {Fore.GREEN}Account exists (taken), regenerating...{Style.RESET_ALL}")

            asyncio.run(check_and_append(username))

    # Display results
    if usernames:
        results = asyncio.run(check_usernames_concurrently(usernames))
        for username, status in zip(usernames, results):
            if status == "banned":
                print(f"{Fore.WHITE}{username} - {Fore.MAGENTA}Account is banned{Style.RESET_ALL}")
            elif status:
                display_username(username, True)
            else:
                display_username(username, False)

def generation_page():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_watermark()
        try:
            number_of_usernames = input("Enter how many usernames you want to generate (or press Enter to return): ")
            if number_of_usernames == '':
                break
            number_of_usernames = int(number_of_usernames)
            if number_of_usernames > 0:
                generate_usernames(number_of_usernames)
            else:
                print("Invalid number. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        input("Enter a number to generate more or press Enter to return to the generation page...")

def username_checker():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_watermark()
        username = input("Enter a username to check (or press Enter to return): ")

        if username == '':
            break
        elif len(username) < 3 or len(username) > 20:
            print(f"{Fore.WHITE}Error: Username must be between 3 and 20 characters.{Style.RESET_ALL}")
        else:
            asyncio.run(check_username(username))
        input("Enter a username to check more or press Enter to return to the username checker...")

def update_settings():
    global show_taken_usernames
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_watermark()
        print("Settings Menu:")
        print(f"1) Toggle showing taken usernames (current: {'On' if show_taken_usernames else 'Off'})")
        print("2) Back to main menu")
        
        choice = input("Select an option: ")

        if choice == '1':
            show_taken_usernames = not show_taken_usernames
            print(f"Show taken usernames set to {'On' if show_taken_usernames else 'Off'}.")
        elif choice == '2':
            break
        input("Press Enter to return to the settings menu...")
        os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_watermark()
        print("1) Start generating usernames")
        print("2) Username Checker")
        print("3) Settings")
        print("4) Exit")
        choice = input("Select an option: ")

        if choice == '1':
            generation_page()
        elif choice == '2':
            username_checker()
        elif choice == '3':
            update_settings()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')

# Uncomment this line to run the program
if __name__ == "__main__":
    print_watermark()
    main_menu()
