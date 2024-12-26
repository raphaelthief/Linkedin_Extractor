import argparse, sys, re, unicodedata, os
from bs4 import BeautifulSoup
from colorama import init, Fore, Style


init() # Init colorama


M = Fore.MAGENTA
R = Fore.RED
Y = Fore.YELLOW
G = Fore.GREEN
C = Fore.CYAN


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


banner = f'''
{R}
▓█████ ▒██   ██▒▄▄▄█████▓ ██▀███   ▄▄▄       ▄████▄  ▄▄▄█████▓ ▒█████   ██▀███  
▓█   ▀ ▒▒ █ █ ▒░▓  ██▒ ▓▒▓██ ▒ ██▒▒████▄    ▒██▀ ▀█  ▓  ██▒ ▓▒▒██▒  ██▒▓██ ▒ ██▒
▒███   ░░  █   ░▒ ▓██░ ▒░▓██ ░▄█ ▒▒██  ▀█▄  ▒▓█    ▄ ▒ ▓██░ ▒░▒██░  ██▒▓██ ░▄█ ▒
▒▓█  ▄  ░ █ █ ▒ ░ ▓██▓ ░ ▒██▀▀█▄  ░██▄▄▄▄██ ▒▓▓▄ ▄██▒░ ▓██▓ ░ ▒██   ██░▒██▀▀█▄  
░▒████▒▒██▒ ▒██▒  ▒██▒ ░ ░██▓ ▒██▒ ▓█   ▓██▒▒ ▓███▀ ░  ▒██▒ ░ ░ ████▓▒░░██▓ ▒██▒
░░ ▒░ ░▒▒ ░ ░▓ ░  ▒ ░░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ░▒ ▒  ░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
 ░ ░  ░░░   ░▒ ░    ░      ░▒ ░ ▒░  ▒   ▒▒ ░  ░  ▒       ░      ░ ▒ ▒░   ░▒ ░ ▒░
   ░    ░    ░    ░        ░░   ░   ░   ▒   ░          ░      ░ ░ ░ ▒    ░░   ░ 
   ░  ░ ░    ░              ░           ░  ░░ ░                   ░ ░     ░     
                                            ░                                   
                                                                  {Y}<{C}raphaelthief{Y}>{G}
'''


def extract_profile_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    profiles = []

    for profile_card in soup.select("li.org-people-profile-card__profile-card-spacing"):
        name = profile_card.select_one("div.lt-line-clamp.lt-line-clamp--single-line")
        profile_link = profile_card.select_one("a[href]")['href'] if profile_card.select_one("a[href]") else None
        title = profile_card.select_one("div.t-14.t-black--light.t-normal")
        relation_common = profile_card.select_one("span.lt-line-clamp")

        profiles.append({
            "Name": name.get_text(strip=True) if name else None,
            "LinkedIn Profile": profile_link,
            "Title": title.get_text(strip=True) if title else None,
            "Common Relation": relation_common.get_text(strip=True) if relation_common else None
        })
    return profiles


def is_valid_name(name):
    if not name:
        return False

    if re.search(r'[^\w\s-]', name):
        return False

    if "Utilisateur LinkedIn" in name or "LinkedIn User" in name:
        return False

    if len(name.split()) != 2:
        return False
    return True


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


def convert_to_email(name, format, domain):
    name = remove_accents(name)
    
    first_name, last_name = name.split()
    initials = first_name[0].lower()
    last_initial = last_name[0].lower()
    first_name = first_name.lower()
    last_name = last_name.lower()

    formats = {
        "nom.prenom": f"{last_name}.{first_name}@{domain}",
        "n.prenom": f"{initials}.{first_name}@{domain}",
        "n.p": f"{initials}.{last_initial}@{domain}",
        "nom.p": f"{last_name}.{last_initial}@{domain}",
        "prenom.nom": f"{first_name}.{last_name}@{domain}",
        "p.nom": f"{first_name[0].lower()}.{last_name}@{domain}",
        "p.n": f"{first_name[0].lower()}.{last_initial}@{domain}",
        "prenom.n": f"{first_name}.{last_initial}@{domain}",
        "nom": f"{last_name}@{domain}",
        "prenom": f"{first_name}@{domain}"
    }
    return formats.get(format, f"{last_name}.{first_name}@{domain}")


def main():
    
    clear_screen()
    print(banner)
    parser = argparse.ArgumentParser(description=f"{M}Linkedin extractor for mass attacks{G}")
    parser.add_argument("--file", help="Select file with webpage data")
    parser.add_argument("--show-all", action="store_true", help="Show name, Linkedin profile, title and common relation")
    parser.add_argument("--names", action="store_true", help="Show names")
    parser.add_argument("--convert", help="""Convert all names extracted to email format with all accents removed from the names.
        Specify domain & format (nom for lastname & prenom for firstname) : nom.prenom@exemple.com (Aviable formats : nom.prenom, n.prenom, n.p, nom.p, prenom.nom, p.nom, p.n, prenom.n)
    """)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        print(Style.RESET_ALL)
        sys.exit(1)

    if not args.file:
        parser.error("You must specify --file args")

    profile_data = extract_profile_info(args.file)

    if args.show_all:
        for profile in profile_data:
            print(f"{G}Name             :{C} {profile['Name']}")
            print(f"{G}LinkedIn Profile :{Y} {profile['LinkedIn Profile']}")
            print(f"{G}Title            :{R} {profile['Title']}")
            print(f"{G}Common Relation  :{Y} {profile['Common Relation']}")
            print("-" * 40)

    if args.names:
        for profile in profile_data:
            print(f"{G}{profile['Name']}")

    if args.convert:
        if '@' not in args.convert:
            print(f"{R}Error : The --convert argument must include a domain (ex : n.p@example.com)")
            print(Style.RESET_ALL)
            sys.exit(1)

        format_part, domain = args.convert.split('@')
        for profile in profile_data:
            if is_valid_name(profile['Name']):
                email = convert_to_email(profile['Name'], format_part, domain)
                print(f"{G}{email}")

    print(Style.RESET_ALL)

if __name__ == "__main__":
    main()
