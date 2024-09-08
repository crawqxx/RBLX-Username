import os
import random
import string
import asyncio
import aiohttp
from colorama import Fore, Style, init

# Initialize colorama with autoreset to ensure colors are reset after each print
init(autoreset=True)

# Global settings
show_taken_usernames = True  # Control whether taken usernames are shown or not
generation_filter = 1        # 1: Random 5 Symbols, 2: 6 Letters, 3: 5 Symbols with 3 Same, 4: 6 Symbols with 3 or 4 Same
language = "eng"  # Default language is English

# Dictionary for translation (English -> Russian)
translations = {
    "eng": {
        "settings_menu": "Settings Menu:",
        "toggle_taken_usernames": "1) Toggle showing taken usernames (current: {})",
        "filters": "2) Filters (current: {})",
        "enter_choice": "Select an option (or press Enter to return): ",
        "select_filter": "Select a filter:",
        "filter_choice": "Enter your choice (1-8): ",
        "start_generating": "1) Start generating usernames",
        "settings": "2) Settings",
        "exit": "3) Exit",
        "number_of_usernames": "Enter the number of usernames to generate: ",
        "invalid_number": "Invalid number. Please enter a valid positive number.",
        "generated_count": "Generated {}/{} usernames",
        "exiting": "Exiting...",
        "return_main_menu": "Press Enter to return to the main menu...",
        "account_exists": "Account exists (taken)",
        "account_available": "Account does not exist (available)",
        "request_timed_out": "Request timed out",
        "account_banned": "Account is banned",
        "settings_applied": "Settings applied.",
        "filters_applied": "Filter applied.",
        "regenerate": "Regenerating...",
        "filter_options": [
            "1) Random 5 Symbol (default)",
            "2) 6 Letters",
            "3) 5 Symbols with 3 Same Symbols",
            "4) 6 Symbols with 3 or 4 Same Symbols",
            "5) Thin Name (5-6 symbols using only 't, i, l, 1, j')",
            "6) 5 Symbols with 3 Same In a Row",
            "7) 6 Symbols with 4-5 Same In a Row",
            "8) 5 Symbols using only 2 symbols"
        ]
    },
    "rus": {
        "settings_menu": "Меню настроек:",
        "toggle_taken_usernames": "1) Переключить показ занятых имен пользователей (текущие: {})",
        "filters": "2) Фильтры (текущие: {})",
        "enter_choice": "Выберите опцию (или нажмите Enter для возврата): ",
        "select_filter": "Выберите фильтр:",
        "filter_choice": "Введите ваш выбор (1-8): ",
        "start_generating": "1) Начать генерацию имен пользователей",
        "settings": "2) Настройки",
        "exit": "3) Выйти",
        "number_of_usernames": "Введите количество имен пользователей для генерации: ",
        "invalid_number": "Неверное число. Пожалуйста, введите допустимое положительное число.",
        "generated_count": "Сгенерировано {}/{} имен пользователей",
        "exiting": "Выход...",
        "return_main_menu": "Нажмите Enter для возврата в главное меню...",
        "account_exists": "Аккаунт существует (занят)",
        "account_available": "Аккаунт не существует (доступен)",
        "request_timed_out": "Время ожидания запроса истекло",
        "account_banned": "Аккаунт заблокирован",
        "settings_applied": "Настройки применены.",
        "filters_applied": "Фильтр применен.",
        "regenerate": "Регенерация...",
        "filter_options": [
            "1) Случайные 5 символов (по умолчанию)",
            "2) 6 букв",
            "3) 5 символов с 3 одинаковыми символами",
            "4) 6 символов с 3 или 4 одинаковыми символами",
            "5) Узкое имя (5-6 символов, используя только 't, i, l, 1, j')",
            "6) 5 символов с 3 одинаковыми символами подряд",
            "7) 6 символов с 4-5 одинаковыми символами",
            "8) 5 символов с использованием только 2 символов"
        ]
    }
}

# Watermark helper function
def get_watermark():
    columns, _ = os.get_terminal_size()
    if columns < 71:
        return """
█▀▀ █▀▀█ █▀▀█ █───█ █▀▀█ █─█ █─█ 
█── █▄▄▀ █▄▄█ █▄█▄█ █──█ ▄▀▄ ▄▀▄ 
▀▀▀ ▀─▀▀ ▀──▀ ─▀─▀─ ▀▀▀█ ▀─▀ ▀─▀
     RBLX-Username Lite
        """
    else:
        return """
        ░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██╗░░██╗██╗░░██╗
        ██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔═══██╗╚██╗██╔╝╚██╗██╔╝
        ██║░░╚═╝██████╔╝███████║░╚██╗████╗██╔╝██║██╗██║░╚███╔╝░░╚███╔╝░
        ██║░░██╗██╔══██╗██╔══██║░░████╔═████║░╚██████╔╝░██╔██╗░░██╔██╗░
        ╚█████╔╝██║░░██║██║░░██║░░╚██╔╝░╚██╔╝░░╚═██╔═╝░██╔╝╚██╗██╔╝╚██╗
        ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝
                  
                            RBLX-Username Lite
        """

# Helper function to print the watermark with the specified color
def print_watermark(color=Fore.WHITE):
    watermark = get_watermark()
    print(color + watermark + Style.RESET_ALL)

# Helper function to retrieve the translated text
def t(key):
    return translations[language][key]

# Display the username check result
def display_username(username, status):
    if status is None:
        print(f"{Fore.YELLOW}{username} - {Fore.RED}{t('request_timed_out')}{Style.RESET_ALL}")
    elif status == "banned":
        print(f"{Fore.YELLOW}{username} - {Fore.RED}{t('account_banned')}{Style.RESET_ALL}")
    elif status:
        print(f"{Fore.WHITE}{username} - {Fore.GREEN}{t('account_exists')}{Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}{username} - {Fore.RED}{t('account_available')}{Style.RESET_ALL}")

# Settings update
def update_settings():
    global show_taken_usernames, generation_filter
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_watermark(Fore.GREEN)
        print(t("settings_menu"))
        print(t("toggle_taken_usernames").format("On" if show_taken_usernames else "Off"))
        print(t("filters").format(generation_filter))
        
        choice = input(t("enter_choice"))
        if choice == '1':
            show_taken_usernames = not show_taken_usernames
            print(f"{Fore.GREEN}{t('settings_applied')}{Style.RESET_ALL}")
        elif choice == '2':
            update_filters()
        else:
            break

# Filters update (Stay in settings after filter applied)
def update_filters():
    global generation_filter
    os.system('cls' if os.name == 'nt' else 'clear')
    print_watermark(Fore.GREEN)
    print(t("select_filter"))
    for option in t("filter_options"):
        print(option)

    filter_choice = input(t("filter_choice"))
    if filter_choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
        generation_filter = int(filter_choice)
        print(f"{Fore.GREEN}{t('filters_applied')}{Style.RESET_ALL}")
        update_settings()  # Stay in settings after applying the filter

# Generate usernames based on the selected filter
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
    elif generation_filter == 6:
        return generate_5_symbols_with_3_same_in_a_row()
    elif generation_filter == 7:
        return generate_6_symbols_with_4_or_5_same()
    elif generation_filter == 8:
        return generate_5_symbols_using_2_symbols()

# Main menu
def main_menu():
    global language
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_watermark(Fore.WHITE)
        print(t("start_generating"))
        print(t("settings"))
        print(t("exit"))
        choice = input(t("enter_choice"))
        
        if choice == "rus":
            language = "rus"
        elif choice == "eng":
            language = "eng"
        elif choice == '1':
            generation_page()
        elif choice == '2':
            update_settings()
        elif choice == '3':
            print(t("exiting"))
            break

# Main generation page (restored and translated)
def generation_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_watermark(Fore.RED)
    try:
        number_of_usernames = int(input(t("number_of_usernames")))
        asyncio.run(generate_usernames(number_of_usernames))
        input(t("return_main_menu"))
    except ValueError:
        print(t("invalid_number"))

# Generate random username with specific filters
def generate_random_username(length=5):
    characters = string.ascii_lowercase + string.digits + "_"
    
    while True:
        username = ''.join(random.choices(characters, k=length))
        if username.startswith('_') or username.endswith('_') or username.count('_') > 1 or 'kkk' in username:
            continue
        if length == 5 and not any(char.isdigit() for char in username):
            continue
        return username

# Add the remaining username generation functions (unchanged)
def generate_6_letter_username():
    return ''.join(random.choices(string.ascii_lowercase, k=6))

def generate_5_symbols_with_3_same():
    char = random.choice(string.ascii_lowercase + string.digits + "_")
    other_chars = random.choices(string.ascii_lowercase + string.digits + "_", k=2)
    username = ''.join(random.sample(char * 3 + ''.join(other_chars), 5))
    return username if not username.startswith('_') and username.count('_') <= 1 else generate_5_symbols_with_3_same()

def generate_6_symbols_with_3_or_4_same():
    char = random.choice(string.ascii_lowercase + string.digits + "_")
    count = random.choice([3, 4])
    other_chars = random.choices(string.ascii_lowercase + string.digits + "_", k=6 - count)
    username = ''.join(random.sample(char * count + ''.join(other_chars), 6))
    return username if not username.startswith('_') and username.count('_') <= 1 else generate_6_symbols_with_3_or_4_same()

def generate_thin_name():
    thin_chars = "til1j"
    length = random.choice([5, 6])
    return ''.join(random.choices(thin_chars, k=length))

def generate_5_symbols_with_3_same_in_a_row():
    chars = string.ascii_lowercase
    required_characters = string.digits + "_"

    while True:
        position = random.choice([0, 1, 2])
        char = random.choice(chars + required_characters)
        username = list("#####")  # Start with placeholders
        for i in range(3):
            username[position + i] = char
        remaining_chars = random.choices(chars + string.digits + "_", k=2)
        if not any(c in required_characters for c in remaining_chars):
            remaining_chars[random.randrange(len(remaining_chars))] = random.choice(required_characters)
        j = 0
        for i in range(5):
            if username[i] == '#':
                username[i] = remaining_chars[j]
                j += 1
        username = ''.join(username)
        
        if username.startswith('_') or username.endswith('_'):
            continue
        if username.count('_') > 1 or 'kkk' in username:
            continue
        
        return username

def generate_6_symbols_with_4_or_5_same():
    chars = string.ascii_lowercase + string.digits
    count = random.choice([4, 5])
    char = random.choice(chars)
    username = char * count
    remaining_chars = random.choices(string.ascii_lowercase + string.digits + "_", k=6 - count)

    if '_' in remaining_chars:
        remaining_chars = [c for c in remaining_chars if c != '_']
        remaining_chars.append('_')

    username += ''.join(remaining_chars)

    if username.startswith('_') or username.endswith('_'):
        return generate_6_symbols_with_4_or_5_same()
    if username.count('_') > 1 or 'kkk' in username:
        return generate_6_symbols_with_4_or_5_same()

    return username

def generate_5_symbols_using_2_symbols():
    while True:
        letter = random.choice(string.ascii_lowercase)
        number = random.choice(string.digits)
        pattern = random.sample([letter, number] * 5, 5)
        username = ''.join(pattern)

        if username.startswith('_') or username.endswith('_'):
            continue
        if username.count('_') > 1 or 'kkk' in username:
            continue

        return username

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
        print(f"{Fore.WHITE}{username} - {Fore.YELLOW}{t('request_timed_out')}{Style.RESET_ALL}")
        return None  # Timeout

# Check multiple usernames concurrently
async def check_usernames_concurrently(usernames, session, max_concurrent_requests=10):
    semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def throttled_check(username):
        async with semaphore:
            return await check_roblox_username_exists(session, username)

    tasks = [throttled_check(username) for username in usernames]
    return await asyncio.gather(*tasks)

# Generate usernames and check if they are available
async def generate_usernames(number_of_usernames):
    global generated_usernames_count
    usernames = []
    
    async with aiohttp.ClientSession() as session:
        try:
            generated_usernames_count = 0  # Reset count before generating

            for _ in range(number_of_usernames):
                username = generate_username_by_filter()

                # Check for the taken username condition
                if not show_taken_usernames:
                    while True:
                        result = await check_roblox_username_exists(session, username)
                        if result is False:
                            usernames.append(username)
                            break
                        else:
                            print(f"{Fore.WHITE}{username} - {Fore.GREEN}{t('account_exists')}, {t('regenerate')}...{Style.RESET_ALL}")
                            username = generate_username_by_filter()
                else:
                    usernames.append(username)

                generated_usernames_count += 1
                os.system('cls' if os.name == 'nt' else 'clear')
                print_watermark(Fore.RED)
                print(t("generated_count").format(generated_usernames_count, number_of_usernames))

            # Using throttled concurrent checks for better performance
            results = await check_usernames_concurrently(usernames, session, max_concurrent_requests=15)

            # Immediately display the results as soon as they are ready
            for username, status in zip(usernames, results):
                display_username(username, status)

        except Exception as e:
            print(f"{Fore.RED}An error occurred during username generation: {str(e)}{Style.RESET_ALL}")
        finally:
            await session.close()

# Run the main menu
if __name__ == "__main__":
    main_menu()
