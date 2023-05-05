import argparse
import re
import time
import sys

from web_inspect import WebInspect

from rich import print as printc

if __name__ == "__main__":
    start_time = time.perf_counter()
    parser = argparse.ArgumentParser(prog='main.py', description="Retrieve interesting information from the webpage's source code", epilog='Ping me: 0liverFlow@proton.me')
    parser.add_argument('-v', '--verbose', action="count", help='increase output verbosity', default=0)
    parser.add_argument('-u','--url', metavar="URL", help="target's url (e.g. https://example.com)", required=True)
    args = parser.parse_args()
    url = args.url

    # Banner
    print("""
╔────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╗
|                                                                                                                                    |
| ████████╗██╗  ██╗███████╗    ██╗    ██╗███████╗██████╗     ██╗███╗   ██╗███████╗██████╗ ███████╗ ██████╗████████╗ ██████╗ ██████╗  | 
| ╚══██╔══╝██║  ██║██╔════╝    ██║    ██║██╔════╝██╔══██╗    ██║████╗  ██║██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗ |
|    ██║   ███████║█████╗      ██║ █╗ ██║█████╗  ██████╔╝    ██║██╔██╗ ██║███████╗██████╔╝█████╗  ██║        ██║   ██║   ██║██████╔╝ |
|    ██║   ██╔══██║██╔══╝      ██║███╗██║██╔══╝  ██╔══██╗    ██║██║╚██╗██║╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗ |
|    ██║   ██║  ██║███████╗    ╚███╔███╔╝███████╗██████╔╝    ██║██║ ╚████║███████║██║     ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║ |
|    ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚══╝╚══╝ ╚══════╝╚═════╝     ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ |
|                                                    THE WEB INSPECTOR 1.0                                                           |
|                                                 Coded with <3 by 0LIVERFLOW                                                        |
╚────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╝                                  
""")

    ##############################
    # Check if curl is installed
    #############################
    running_os = WebInspect.get_running_os()
    if running_os:
        is_curl_installed = WebInspect.is_installed('curl', running_os)
        if not is_curl_installed:
            sys.exit(printc("[red3][-][/red3] You need to install curl to run this script!!"))
        elif is_curl_installed is None:
            printc("[red3][-][/red3] Unknown Operating System!!")
            printc("[gold1][!][/gold1] Supported OS are: GNU/Linux, Windows and MacOS")
            sys.exit(printc("[gold1][!][/gold1] If you're sure that you are running one of these systems, thanks to report this issue at https://github.com/0liverFlow/TheWebInspector/issues"))
    
    inspected_webpage = WebInspect(url) # new instance of WebInspect class  

    ###############
    # Target URL
    ##############
    printc(f"\n[bright_blue][*][/bright_blue] Target URL: [red3]{inspected_webpage.url}[/red3]\n{'-'*45}")
    
    ############################
    # Check the webpage response
    ############################
    if inspected_webpage.response == "":
        printc("[red3][-][/red3] No information found!")
        sys.exit(printc("[gold1][!][/gold1] Please make sure that the specified url is not redirected, then retry!"))
                 
    ##############################
    # Checking website language
    ##############################
    printc(f"\n[bright_blue][*][/bright_blue] Language\n{'-'*18}")
    inspected_webpage.get_language()
    if inspected_webpage.language != "N/A":
        printc(f"[spring_green2][+][/spring_green2] {inspected_webpage.language}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.language}")

    #########################
    # Checking website title
    #########################
    inspected_webpage.get_title()
    printc(f"\n[bright_blue][*][/bright_blue] Title\n{'-'*18}")
    if inspected_webpage.title != "N/A":
        printc(f"[spring_green2][+][/spring_green2] {inspected_webpage.title}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.title}")

    #######################
    # Allowed HTTP Methods
    #######################
    inspected_webpage.get_allowed_methods()
    printc(f"\n[bright_blue][*][/bright_blue] Allowed Methods\n{'-'*19}")
    if inspected_webpage.allowed_methods != "N/A":
        printc(f"[spring_green2][+][/spring_green2] {inspected_webpage.allowed_methods}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.allowed_methods}")
    
    ########################            
    # HTTP Response Headers
    ########################
    inspected_webpage.check_secured_http_response_headers()
    printc(f"\n[bright_blue][*][/bright_blue] HTTP Response Headers\n{'-'*25}")
    if len(inspected_webpage.unset_secured_http_response_headers):
        for unset_secured_http_response_header in inspected_webpage.unset_secured_http_response_headers:
            printc(f"[gold1][!][/gold1] {unset_secured_http_response_header} not found!")
    else:
        printc("[red3][-][/red3] N/A")
    if len(inspected_webpage.juicy_headers):
        for juicy_header, juicy_header_value in inspected_webpage.juicy_headers.items():
            printc(f"[gold1][!][/gold1] {juicy_header}: {juicy_header_value}")
    else:
        printc("[red3][-][/red3] N/A")

    #############
    # Comments
    #############
    inspected_webpage.get_comments()
    printc(f"\n[bright_blue][*][/bright_blue] Comments\n{'-'*18}")
    if inspected_webpage.comments != 'N/A':
        for comment_num, comment_tag in enumerate(inspected_webpage.comments, start=1):
            if comment_tag:
                printc(re.sub('\s\s+',' ', str(comment_tag).strip()))
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.comments}")

    ###############
    # Meta Tags
    ###############
    if args.verbose > 1:
        inspected_webpage.get_meta_tags()
        printc(f"\n[bright_blue][*][/bright_blue] Meta Tags\n{'-'*20}")
        if inspected_webpage.meta_tags != 'N/A':
            for meta_tag in inspected_webpage.meta_tags:
                for meta_tag_attr in meta_tag.attrs:
                    if 'name' in meta_tag_attr:
                        printc(f"{meta_tag['name']}: {meta_tag['content']}")
                    elif 'property' in meta_tag_attr:
                        printc(f"{meta_tag['property']}: {meta_tag['content']}")
        else:
            printc(f"[red3][-][/red3] {inspected_webpage.meta_tags}")

    #############
    # Inputs
    #############
    inspected_webpage.get_inputs()
    printc(f"\n[bright_blue][*][/bright_blue] Text Inputs\n{'-'*20}")
    if inspected_webpage.text_inputs != "N/A":
        for text_input in inspected_webpage.text_inputs:
            printc(f"{str(text_input).strip()}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.text_inputs}")
    printc(f"\n[bright_blue][*][/bright_blue] Password Inputs\n{'-'*19}")
    if inspected_webpage.password_inputs != "N/A":
        for password_input in inspected_webpage.password_inputs:
            printc(f"{str(password_input).strip()}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.password_inputs}")
    printc(f"\n[bright_blue][*][/bright_blue] File Inputs\n{'-'*18}")
    if inspected_webpage.file_inputs != "N/A":
        for file_input in inspected_webpage.file_inputs:
            printc(f"{str(file_input).strip()}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.file_inputs}")
    printc(f"\n[bright_blue][*][/bright_blue] Search Inputs\n{'-'*18}")
    if inspected_webpage.search_inputs != "N/A":
        for search_input in inspected_webpage.search_inputs:
            printc(f"{str(search_input).strip()}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.search_inputs}")
    printc(f"\n[bright_blue][*][/bright_blue] Email Inputs\n{'-'*18}")
    if inspected_webpage.email_inputs != "N/A":
        for email_input in inspected_webpage.email_inputs:
            printc(f"{str(email_input).strip()}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.email_inputs}")
    printc(f"\n[bright_blue][*][/bright_blue] Hidden Inputs\n{'-'*20}")
    if inspected_webpage.hidden_inputs != "N/A":
        for hidden_input in inspected_webpage.hidden_inputs:
            printc(f"{str(hidden_input).strip()}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.hidden_inputs}")
    
    #####################
    # Display: None Tags
    #####################
    if args.verbose > 1:
        inspected_webpage.get_display_none_tags()
        printc(f"\n[bright_blue][*][/bright_blue] Display None Tags\n{'-'*22}")
        if inspected_webpage.display_none != "N/A":
            for display_none in inspected_webpage.display_none:
                printc(f"{display_none}")
        else:
            printc(f"[red3][-][/red3] {inspected_webpage.display_none}")

    ##############
    # Forms
    ##############
    if args.verbose > 1:
        inspected_webpage.get_forms()
        printc(f"\n[bright_blue][*][/bright_blue] Forms\n{'-'*20}")
        if inspected_webpage.forms != "N/A":
            for form_num, form_tag in enumerate(inspected_webpage.forms, start=1):
                printc(f"[spring_green2][+][/spring_green2] Form n°{form_num}\n{'-'*12}")
                printc(f"{form_tag}\n{'-'*12}")
        else:
            printc(f"[red3][-][/red3] {inspected_webpage.forms}")

    ################            
    # Robots.txt
    ################
    inspected_webpage.get_robots_txt()
    printc(f"\n[bright_blue][*][/bright_blue] Robots.txt\n{'-'*20}")
    if inspected_webpage.robots_txt not in ["N/A", "Robots.txt file empty!"]:
        for robots_txt_rule in inspected_webpage.robots_txt:
            if args.verbose == 2:
                    printc(f"{robots_txt_rule.strip()}")
            elif args.verbose == 1:
                if not re.search("^(Disallow|User-agent|Allow)", robots_txt_rule.strip(), flags=re.IGNORECASE) is None:
                    printc(f"{robots_txt_rule.strip()}")
            else:   
                if not re.search("^(Disallow|User-agent)", robots_txt_rule.strip(), flags=re.IGNORECASE) is None:
                    printc(f"[spring_green2][+][/spring_green2] {robots_txt_rule.strip()}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.robots_txt}")

    ################            
    # Sitemap.xml
    ################
    inspected_webpage.get_sitemap_xml()
    printc(f"\n[bright_blue][*][/bright_blue] Sitemap.xml\n{'-'*20}")
    if inspected_webpage.sitemap_xml not in ["N/A", "Sitemap file empty!"]:
        printc(f"[spring_green2][+][/spring_green2] {inspected_webpage.url + '/sitemap.xml'} found!")
        if args.verbose > 0:
            for line in inspected_webpage.sitemap_xml:
                printc(f"{str(line).strip()}")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.sitemap_xml}")

    ##################
    # Phpinfo
    ##################
    inspected_webpage.get_phpinfo()
    printc(f"\n[bright_blue][*][/bright_blue] PHP Info\n{'-'*20}")
    if not inspected_webpage.phpinfo.startswith("N/A"):
        printc(f"[spring_green2][+][/spring_green2] {inspected_webpage.phpinfo} found!")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.phpinfo}")

    ##################
    # Cgidir
    ##################
    inspected_webpage.get_cgidir()
    printc(f"\n[bright_blue][*][/bright_blue] CGI Dir\n{'-'*20}")
    if inspected_webpage.cgidir.startswith("N/A"):
        printc(f"[spring_green2][+][/spring_green2] {inspected_webpage.cgidir} found!")
    else:
        printc(f"[red3][-][/red3] {inspected_webpage.cgidir}")

    ##################
    # Elapsed time
    ##################
    end_time = time.perf_counter()
    hours, minutes, seconds = inspected_webpage.determine_elapsed_time(start_time, end_time)
    elapsed_time = inspected_webpage.format_time(hours, minutes, seconds)
    printc(f"\n[bright_blue][*][/bright_blue] THE WEB INSPECTOR: [red3]{inspected_webpage.url}[/red3]'s source code inspected in [gold1]{elapsed_time}[/gold1]!")
