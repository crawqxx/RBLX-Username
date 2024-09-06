import importlib

modules = ["os", "random", "secrets", "string", "time", "selenium", "aiohttp", "asyncio", "colorama"]
not_installed = []

for module in modules:
    if importlib.util.find_spec(module) is None:
        not_installed.append(module)

if not_installed:
    print("The following modules are not installed:")
    for module in not_installed:
        print(module)

import os
import random
import secrets
import string
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
import aiohttp
import asyncio
from colorama import Fore, Style, init

# Initialize colorama with autoreset to ensure colors are reset after each print
init(autoreset=True)

# Global settings
show_taken_usernames = True  # Boolean setting to control whether taken usernames are shown or not
generation_filter = 1        # 1: Random 5 Symbols, 2: 6 Letters, 3: 5 Symbols with 3 Same, 4: 6 Symbols with 3 or 4 Same
generated_usernames_count = 0

# Helper function to clear console and print status
def status(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + text + "\033[0m")

def print_watermark():
    print("""
    ░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██╗░░██╗██╗░░██╗
    ██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔═══██╗╚██╗██╔╝╚██╗██╔╝
    ██║░░╚═╝██████╔╝███████║░╚██╗████╗██╔╝██║██╗██║░╚███╔╝░░╚███╔╝░
    ██║░░██╗██╔══██╗██╔══██║░░████╔═████║░╚██████╔╝░██╔██╗░░██╔██╗░
    ╚█████╔╝██║░░██║██║░░██║░░╚██╔╝░╚██╔╝░░╚═██╔═╝░██╔╝╚██╗██╔╝╚██╗
    ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝
          
                        RBLX-Username v1.1 Beta
    """)

def display_error_message(username, code):
    if code == 0:
        print(f"{Fore.WHITE}{username} - {Fore.RED}Account does not exist (available){Style.RESET_ALL}")
    elif code == 1:
        print(f"{Fore.WHITE}{username} - {Fore.GREEN}Account exists (taken){Style.RESET_ALL}")
    elif code == 2:
        print(f"{Fore.WHITE}{username} - \033[95mUsername is inappropriate for Roblox{Style.RESET_ALL}")
    elif code == 3:
        print(f"{Fore.WHITE}{username} - {Fore.CYAN}Username must be 3 to 20 characters long.{Style.RESET_ALL}")
    elif code == 4:
        print(f"{Fore.WHITE}{username} - {Fore.CYAN}Username cannot start or end with _{Style.RESET_ALL}")
    elif code == 7:
        print(f"{Fore.WHITE}{username} - {Fore.CYAN}Only a-z, A-Z, 0-9, and _ are allowed.{Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}{username} - {Fore.YELLOW}Unknown error occurred. (rare error xd){Style.RESET_ALL}")

# Helper function to generate a random username
def generate_random_username(length=5):
    characters = string.ascii_lowercase + string.digits + "_"
    
    while True:
        username = ''.join(random.choices(characters, k=length))

        # Apply new generation rules:
        if username.startswith('_') or username.endswith('_'):
            continue
        if username.count('_') > 1:
            continue
        if 'kkk' in username:
            continue
        if length == 5 and not any(char.isdigit() for char in username):
            continue  # Ensure at least one number for 5-symbol usernames

        return username

# Other generation strategies
def generate_6_letter_username():
    return ''.join(random.choices(string.ascii_lowercase, k=6))

def generate_5_symbols_with_3_same():
    char = random.choice(string.ascii_lowercase + string.digits + "_")
    other_chars = random.choices(string.ascii_lowercase + string.digits + "_", k=2)
    username = char * 3 + ''.join(other_chars)
    username = ''.join(random.sample(username, len(username)))

    # Apply generation rules
    if username.startswith('_') or username.endswith('_'):
        return generate_5_symbols_with_3_same()  # Regenerate
    if username.count('_') > 1 or 'kkk' in username:
        return generate_5_symbols_with_3_same()

    return username

def generate_6_symbols_with_3_or_4_same():
    char = random.choice(string.ascii_lowercase + string.digits + "_")
    count = random.choice([3, 4])
    other_chars = random.choices(string.ascii_lowercase + string.digits + "_", k=6 - count)
    username = char * count + ''.join(other_chars)
    username = ''.join(random.sample(username, len(username)))

    # Apply generation rules
    if username.startswith('_') or username.endswith('_'):
        return generate_6_symbols_with_3_or_4_same()  # Regenerate
    if username.count('_') > 1 or 'kkk' in username:
        return generate_6_symbols_with_3_or_4_same()

    return username

# Function to generate "Thin Name" usernames
def generate_thin_name():
    thin_chars = "til1j"
    length = random.choice([5, 6])
    return ''.join(random.choices(thin_chars, k=length))


def generate_username_by_filter():
    if generation_filter == 1:
        return generate_random_username(5)
    elif generation_filter == 2:
        return generate_6_letter_username()
    elif generation_filter == 3:
        return generate_5_symbols_with_3_same()
    elif generation_filter == 4:
        return generate_6_symbols_with_3_or_4_same()
    elif generation_filter == 5:
        return generate_thin_name() 

# Check if the Roblox username exists
async def check_roblox_username_exists(session, username, timeout=4):
    url_1 = f"https://www.roblox.com/users/profile?username={username}"
    url_2 = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"

    try:
        # Check the first URL (Roblox profile check)
        async with session.get(url_1, timeout=timeout) as response_1:
            if response_1.status == 200:
                page_content = await response_1.text()
                if "banned" in page_content.lower():
                    return "banned"
                # If the profile page loads, the account exists (taken)
                return True
            else:
                # If profile not found, check the second URL (username validation)
                async with session.get(url_2, timeout=timeout) as response_2:
                    if response_2.status == 200:
                        validation_data = await response_2.json()
                        if validation_data.get("code") == 0:
                            return False  # Username is available
                        elif validation_data.get("code") == 1:
                            return True  # Account exists (taken)
                        else:
                            return validation_data.get("code")  # Return the validation code
                    else:
                        return False  # Assume username is available or validation failed
    except asyncio.TimeoutError:
        print(f"{Fore.WHITE}{username} - {Fore.YELLOW}Request timed out{Style.RESET_ALL}")
        return None  # Timeout


# Check multiple usernames concurrently
async def check_usernames_concurrently(usernames, session, max_concurrent_requests=10):
    semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def throttled_check(username):
        async with semaphore:
            return await check_roblox_username_exists(session, username)

    tasks = [throttled_check(username) for username in usernames]
    return await asyncio.gather(*tasks)

# Check a single username
async def check_username(username):
    async with aiohttp.ClientSession() as session:
        result = await check_roblox_username_exists(session, username)
        if result is None:
            print(f"{Fore.WHITE}{username} - {Fore.YELLOW}Request timed out{Style.RESET_ALL}")
        else:
            display_username(username, result)

# Display the generated username
def display_username(username, status):
    if status == "banned":
        print(f"{Fore.WHITE}{username} - {Fore.MAGENTA}Account is banned{Style.RESET_ALL}")
    elif isinstance(status, int):
        display_error_message(username, status)
    elif status is True:
        print(f"{Fore.WHITE}{username} - {Fore.GREEN}Account exists (taken){Style.RESET_ALL}")
    elif status is False:
        print(f"{Fore.WHITE}{username} - {Fore.RED}Account does not exist (available){Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}{username} - {Fore.YELLOW}Unknown status received.{Style.RESET_ALL}")


# Generate usernames
async def generate_usernames(number_of_usernames):
    global generated_usernames_count
    usernames = []
    session = aiohttp.ClientSession()

    try:
        generated_usernames_count = 0  # Reset count before generating

        for _ in range(number_of_usernames):
            username = generate_username_by_filter()

            if not show_taken_usernames:
                while True:
                    result = await check_roblox_username_exists(session, username)
                    if result is False:
                        usernames.append(username)
                        break
                    else:
                        print(f"{Fore.WHITE}{username} - {Fore.GREEN}Account exists (taken), regenerating...{Style.RESET_ALL}")
                        username = generate_username_by_filter()
            else:
                usernames.append(username)

            generated_usernames_count += 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print_watermark()
            print(f"Generated {generated_usernames_count} usernames so far")

        results = await check_usernames_concurrently(usernames, session)
        for username, status in zip(usernames, results):
            display_username(username, status)

    finally:
        await session.close()

# Selenium-based account creator with headless mode
def create_account(username):
    try:
        status("Starting to create an account...")
        
        # Define days, months, and years for birthday selection
        days = [str(i + 1) for i in range(10, 28)]  # Days between 10 and 28
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        years = [str(i) for i in range(1980, 2004)]  # Years between 1980 and 2004

        # Configure Selenium to run in headless mode (no visible window)
        options = Options()
        options.add_argument('--headless')  # Headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1200x800')
        
        driver = webdriver.Edge(options=options)  # Using Edge WebDriver
        driver.get("https://www.roblox.com/")
        time.sleep(2)

        # Locate elements for filling out the form
        status("Searching for elements on the page...")
        username_input = driver.find_element("id", "signup-username")
        username_error = driver.find_element("id", "signup-usernameInputValidation")
        password_input = driver.find_element("id", "signup-password")
        day_dropdown = driver.find_element("id", "DayDropdown")
        month_dropdown = driver.find_element("id", "MonthDropdown")
        year_dropdown = driver.find_element("id", "YearDropdown")
        male_button = driver.find_element("id", "MaleButton")
        female_button = driver.find_element("id", "FemaleButton")
        register_button = driver.find_element("id", "signup-button")

        # Fill out the form with a random birthday
        status("Filling out birthday...")
        Select(day_dropdown).select_by_value(str(secrets.choice(days)))
        Select(month_dropdown).select_by_value(str(secrets.choice(months)))
        Select(year_dropdown).select_by_value(str(secrets.choice(years)))

        # Input the username
        status(f"Entering username: {username}")
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(1)

        # Check for username validation error
        if username_error.text.strip() != "":
            status(f"Error: Username '{username}' is taken or invalid")
            driver.quit()
            return False

        # Input the password
        status("Entering password: generated21")
        password_input.send_keys("generated21")

        # Register the account
        status("Registering account...")
        register_button.click()
        time.sleep(3)

        status(f"Account with username '{username}' has been successfully created!")
        driver.quit()
        return True

    except Exception as e:
        status(f"An error occurred during account creation: {str(e)}")
        driver.quit()
        return False


# Main menu integration
def account_creator():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_watermark()
        username = input("With what username should we create your account? (or press Enter to return): ")

        if username == '':
            break
        elif len(username) < 3 or len(username) > 20:
            print(f"{Fore.WHITE}Error: Username must be between 3 and 20 characters.{Style.RESET_ALL}")
        else:
            success = create_account(username)
            if success:
                print(f"Account created! Username: {username}, Password: generated21")
            input("Press Enter to continue...")

# Generation page
def generation_page():
    global generated_usernames_count
    generated_usernames_count = 0  # Reset count before generating
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_watermark()
        try:
            number_of_usernames = input("Enter how many usernames you want to generate (or press Enter to return): ")
            if number_of_usernames == '':
                break
            number_of_usernames = int(number_of_usernames)
            if number_of_usernames > 0:
                asyncio.run(generate_usernames(number_of_usernames))
            else:
                print("Invalid number. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        input("Enter a number to generate more or press Enter to return to the generation page...")

# Username checker
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
        input("Press Enter to check another username or press Enter to return to the username checker...")


# Settings update
def update_settings():
    global show_taken_usernames, generation_filter
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_watermark()
        print("Settings Menu:")
        print(f"1) Toggle showing taken usernames (current: {'On' if show_taken_usernames else 'Off'})")
        print(f"2) Filters (current: {'Random 5 Symbol' if generation_filter == 1 else '6 Letters' if generation_filter == 2 else '5 Symbols with 3 Same' if generation_filter == 3 else '6 Symbols with 3 or 4 Same' if generation_filter == 4 else 'Thin Name'})")

        choice = input("Select an option (or press Enter to return): ")

        if choice == '1':
            show_taken_usernames = not show_taken_usernames
        elif choice == '2':
            print("Select a filter:")
            print("1) Random 5 Symbol (default)")
            print("2) 6 Letters")
            print("3) 5 Symbols with 3 Same Symbols")
            print("4) 6 Symbols with 3 or 4 Same Symbols")
            print("5) Thin Name (5-6 symbols using only 't, i, l, 1, j')")
            filter_choice = input("Enter your choice (1-5): ")
            if filter_choice in ['1', '2', '3', '4', '5']:
                generation_filter = int(filter_choice)
            os.system('cls' if os.name == 'nt' else 'clear')
            print_watermark()
        elif choice == '':
            break


# Main menu
def main_menu():
    print_watermark()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_watermark()
        print("1) Start generating usernames")
        print("2) Username Checker")
        print("3) Account Creator (Windows only)")
        print("4) Settings")
        print("5) Exit")
        choice = input("Select an option: ")

        if choice == '1':
            generation_page()
        elif choice == '2':
            username_checker()
        elif choice == '3':
            account_creator()
        elif choice == '4':
            update_settings()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')

# Run the main menu
if __name__ == "__main__":
    print_watermark()
    main_menu()
