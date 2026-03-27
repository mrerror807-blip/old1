#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SIZAN OLD ID CHECKER - EDUCATIONAL DEMO

import os
import sys
import time
import random
import string
import requests
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
WHITE = '\033[97m'
RESET = '\033[0m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    clear()
    print(f"""{GREEN}
    ███████╗██╗███████╗ █████╗ ███╗   ██╗
    ██╔════╝██║╚══███╔╝██╔══██╗████╗  ██║
    ███████╗██║  ███╔╝ ███████║██╔██╗ ██║
    ╚════██║██║ ███╔╝  ██╔══██║██║╚██╗██║
    ███████║██║███████╗██║  ██║██║ ╚████║
    ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    {RESET}
    {YELLOW}╔════════════════════════════════════════╗{RESET}
    {YELLOW}║ {WHITE}OLD ID CHECKER - EDUCATIONAL DEMO{RESET}{YELLOW}      ║{RESET}
    {YELLOW}║ {WHITE}Created by: SIZAN{RESET}{YELLOW}                         ║{RESET}
    {YELLOW}╚════════════════════════════════════════╝{RESET}
    """)

def get_user_agent():
    """Random User Agent"""
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/131.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1',
    ]
    return random.choice(agents)

def check_id_exists(user_id):
    """Check if Facebook ID exists (Educational Only)"""
    try:
        session = requests.Session()
        headers = {'User-Agent': get_user_agent()}
        
        # Try mbasic.facebook.com
        response = session.get(f'https://mbasic.facebook.com/profile.php?id={user_id}', headers=headers, timeout=10)
        
        if response.status_code == 200:
            text = response.text.lower()
            if 'content not found' not in text and 'page not found' not in text:
                return True, "Active"
            return False, "Not Found"
        return False, "Error"
    except:
        return False, "Connection Error"

def estimate_year(user_id):
    """Estimate account creation year from ID"""
    uid_str = str(user_id)
    if len(uid_str) == 15:
        if uid_str.startswith('1000000'):
            return '2009-2010'
        elif uid_str.startswith('100001'):
            return '2010-2011'
        elif uid_str.startswith('100002'):
            return '2011-2012'
        elif uid_str.startswith('100003'):
            return '2012-2013'
        elif uid_str.startswith('100004'):
            return '2013-2014'
        elif uid_str.startswith('100005'):
            return '2014-2015'
        elif uid_str.startswith('100006'):
            return '2015-2016'
        elif uid_str.startswith('100007'):
            return '2016-2017'
        elif uid_str.startswith('100008'):
            return '2017-2018'
        elif uid_str.startswith('100009'):
            return '2018-2019'
    elif len(uid_str) in (9, 10):
        return '2008-2009'
    elif len(uid_str) == 8:
        return '2007-2008'
    elif len(uid_str) == 7:
        return '2006-2007'
    return 'Unknown'

def generate_old_ids(count, year_type='all'):
    """Generate old Facebook IDs"""
    ids = []
    prefixes = {
        '2006-2007': ['10000', '10001'],
        '2007-2008': ['100000', '100001'],
        '2008-2009': ['1000000', '1000001'],
        '2009-2010': ['10000000', '10000001'],
        '2010-2011': ['100000000', '100000001'],
        '2011-2012': ['1000000000', '1000000001'],
        'all': ['10000', '100000', '1000000', '10000000', '100000000', '1000000000']
    }
    
    for _ in range(count):
        if year_type in prefixes:
            prefix = random.choice(prefixes[year_type])
        else:
            prefix = random.choice(prefixes['all'])
        
        suffix = ''.join(random.choices(string.digits, k=10 - len(prefix)))
        ids.append(prefix + suffix)
    
    return ids

def check_batch(ids):
    """Check multiple IDs"""
    results = []
    total = len(ids)
    
    for i, uid in enumerate(ids):
        exists, status = check_id_exists(uid)
        year = estimate_year(uid)
        
        results.append({
            'id': uid,
            'exists': exists,
            'status': status,
            'year': year
        })
        
        # Show progress
        percent = ((i+1)/total)*100
        bar = '█' * int(percent/5) + '░' * (20 - int(percent/5))
        sys.stdout.write(f'\r{YELLOW}[{bar}] {i+1}/{total} ({percent:.0f}%){RESET}')
        sys.stdout.flush()
        time.sleep(0.5)  # Delay to avoid rate limiting
    
    print()
    return results

def main():
    """Main function"""
    banner()
    
    print(f"\n{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{GREEN}[1] Check Single ID{RESET}")
    print(f"{GREEN}[2] Generate & Check IDs{RESET}")
    print(f"{GREEN}[3] Check from File{RESET}")
    print(f"{RED}[0] Exit{RESET}")
    print(f"{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    
    choice = input(f"\n{BLUE}[?] Select: {RESET}")
    
    if choice == '1':
        # Single ID
        uid = input(f"{BLUE}[?] Enter Facebook ID: {RESET}")
        print(f"\n{YELLOW}[!] Checking...{RESET}")
        exists, status = check_id_exists(uid)
        year = estimate_year(uid)
        
        if exists:
            print(f"{GREEN}[✓] ID: {uid}{RESET}")
            print(f"{GREEN}[✓] Status: Active{RESET}")
            print(f"{GREEN}[✓] Estimated Year: {year}{RESET}")
        else:
            print(f"{RED}[✗] ID: {uid}{RESET}")
            print(f"{RED}[✗] Status: {status}{RESET}")
    
    elif choice == '2':
        # Generate and check
        try:
            count = int(input(f"{BLUE}[?] How many IDs to check? (max 100): {RESET}"))
            if count > 100:
                count = 100
                print(f"{YELLOW}[!] Limiting to 100{RESET}")
            
            print(f"\n{YELLOW}[!] Generating {count} IDs...{RESET}")
            ids = generate_old_ids(count)
            
            print(f"{YELLOW}[!] Checking IDs...{RESET}\n")
            results = check_batch(ids)
            
            # Show results
            print(f"\n{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
            print(f"{GREEN}RESULTS:{RESET}")
            print(f"{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
            
            active = [r for r in results if r['exists']]
            for r in active:
                print(f"{GREEN}[✓] {r['id']} | Year: {r['year']}{RESET}")
            
            if not active:
                print(f"{RED}[✗] No active IDs found{RESET}")
            
            print(f"\n{YELLOW}Total Checked: {len(results)}{RESET}")
            print(f"{GREEN}Active Found: {len(active)}{RESET}")
            
    elif choice == '3':
        # Check from file
        filename = input(f"{BLUE}[?] Enter filename (ids.txt): {RESET}")
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                ids = [line.strip() for line in f if line.strip()]
            print(f"{YELLOW}[!] Found {len(ids)} IDs{RESET}")
            results = check_batch(ids)
            
            print(f"\n{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
            print(f"{GREEN}RESULTS:{RESET}")
            print(f"{WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
            
            for r in results:
                if r['exists']:
                    print(f"{GREEN}[✓] {r['id']} | Year: {r['year']}{RESET}")
                else:
                    print(f"{RED}[✗] {r['id']} | {r['status']}{RESET}")
        else:
            print(f"{RED}[✗] File not found!{RESET}")
    
    elif choice == '0':
        print(f"\n{GREEN}Goodbye! 👋{RESET}")
        sys.exit(0)
    
    input(f"\n{BLUE}Press Enter to continue...{RESET}")
    main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{GREEN}Goodbye! 👋{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}[!] Error: {e}{RESET}")
        sys.exit(1)