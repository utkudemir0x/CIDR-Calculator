#!/usr/bin/env python3
"""
CIDR Calculator
===============
A simple command-line IP/CIDR calculation tool.

Menu:
[1] Calculate CIDR            -> Enter IP + CIDR, calculate network info
[2] IP Information            -> Info about a single IP (class, private/public, etc.)
[3] Subnet Mask from CIDR     -> Generate subnet mask from CIDR
[4] Wildcard Mask             -> Generate wildcard mask from CIDR
[5] Binary Converter          -> IP <-> Binary conversion
[6] Help                      -> Usage information
[0] Exit                      -> Quit
"""

import ipaddress
import os
import sys


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"


BANNER = rf"""{C.CYAN}{C.BOLD}
 ██████╗██╗██████╗ ██████╗      ██████╗ █████╗ ██╗      ██████╗██╗   ██╗████████╗ ██████╗ ██████╗ 
██╔════╝██║██╔══██╗██╔══██╗    ██╔════╝██╔══██╗██║     ██╔════╝██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗
██║     ██║██║  ██║██████╔╝    ██║     ███████║██║     ██║     ██║   ██║   ██║   ██║   ██║██████╔╝
██║     ██║██║  ██║██╔══██╗    ██║     ██╔══██║██║     ██║     ██║   ██║   ██║   ██║   ██║██╔══██╗
╚██████╗██║██████╔╝██║  ██║    ╚██████╗██║  ██║███████╗╚██████╗╚██████╔╝   ██║   ╚██████╔╝██║  ██║
 ╚═════╝╚═╝╚═════╝ ╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                                  
{C.RESET}{C.DIM}                 IPv4 / CIDR / Subnet Calculation Tool{C.RESET}
"""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def clear_line():
    print(f"{C.DIM}{'-' * 55}{C.RESET}")


def get_ip_input(prompt="Enter IP address (e.g. 192.168.1.10): "):
    while True:
        raw = input(prompt).strip()
        try:
            return ipaddress.ip_address(raw)
        except ValueError:
            print("Invalid IP address! Try again.\n")


def get_cidr_input(prompt="Enter CIDR / prefix length (0-32): "):
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if 0 <= val <= 32:
                return val
            print("CIDR must be between 0 and 32!\n")
        except ValueError:
            print("Invalid number! Try again.\n")


def ip_class(ip):
    first_octet = int(str(ip).split(".")[0])
    if first_octet < 128:
        return "A"
    elif first_octet < 192:
        return "B"
    elif first_octet < 224:
        return "C"
    elif first_octet < 240:
        return "D (Multicast)"
    else:
        return "E (Experimental)"


def to_binary(ip):
    return ".".join(f"{int(o):08b}" for o in str(ip).split("."))


# ----------------------------------------------------------------------
# Menu functions
# ----------------------------------------------------------------------

def print_field(label, value, color=C.GREEN):
    print(f"{C.DIM}{label:<22}{C.RESET}: {color}{value}{C.RESET}")


def calculate_cidr():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== CIDR Calculation =={C.RESET}")
    ip_raw = input(f"{C.YELLOW}IP address (e.g. 192.168.1.10): {C.RESET}").strip()
    cidr = get_cidr_input()

    try:
        network = ipaddress.ip_network(f"{ip_raw}/{cidr}", strict=False)
    except ValueError as e:
        print(f"{C.RED}Error: {e}{C.RESET}")
        return

    print()
    print_field("Entered IP", ip_raw, C.CYAN)
    print_field("CIDR", f"/{cidr}", C.CYAN)
    print_field("Network Address", network.network_address)
    print_field("Broadcast Address", network.broadcast_address)
    print_field("Subnet Mask", network.netmask)
    print_field("Wildcard Mask", network.hostmask)
    print_field("Total Address Count", network.num_addresses)

    usable = list(network.hosts())
    if usable:
        print_field("Usable Hosts", len(usable))
        print_field("First Usable", usable[0])
        print_field("Last Usable", usable[-1])
    else:
        print_field("Usable Hosts", "0 (No host addresses in this network)", C.RED)

    print_field("Network Class", ip_class(network.network_address), C.YELLOW)
    print_field("Binary Network Address", to_binary(network.network_address), C.BLUE)


def yn(val):
    return (C.GREEN + "Yes" + C.RESET) if val else (C.RED + "No" + C.RESET)


def ip_information():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== IP Information =={C.RESET}")
    ip = get_ip_input()

    print()
    print_field("IP Address", ip, C.CYAN)
    print_field("Version", f"IPv{ip.version}", C.CYAN)
    print_field("Binary", to_binary(ip), C.BLUE)
    print_field("Class", ip_class(ip), C.YELLOW)
    print(f"{C.DIM}{'Private':<22}{C.RESET}: {yn(ip.is_private)}")
    print(f"{C.DIM}{'Loopback':<22}{C.RESET}: {yn(ip.is_loopback)}")
    print(f"{C.DIM}{'Multicast':<22}{C.RESET}: {yn(ip.is_multicast)}")
    print(f"{C.DIM}{'Reserved':<22}{C.RESET}: {yn(ip.is_reserved)}")
    print(f"{C.DIM}{'Link-local':<22}{C.RESET}: {yn(ip.is_link_local)}")
    print(f"{C.DIM}{'Unspecified (0.0.0.0)':<22}{C.RESET}: {yn(ip.is_unspecified)}")


def subnet_mask_from_cidr():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== Subnet Mask from CIDR =={C.RESET}")
    cidr = get_cidr_input()
    mask = ipaddress.IPv4Network(f"0.0.0.0/{cidr}").netmask
    print()
    print_field("CIDR", f"/{cidr}", C.CYAN)
    print_field("Subnet Mask", mask)
    print_field("Binary", to_binary(mask), C.BLUE)


def wildcard_mask():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== Wildcard Mask from CIDR =={C.RESET}")
    cidr = get_cidr_input()
    wildcard = ipaddress.IPv4Network(f"0.0.0.0/{cidr}").hostmask
    print()
    print_field("CIDR", f"/{cidr}", C.CYAN)
    print_field("Wildcard Mask", wildcard)
    print_field("Binary", to_binary(wildcard), C.BLUE)


def binary_converter():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== Binary Converter =={C.RESET}")
    print(f"{C.YELLOW}[1]{C.RESET} IP -> Binary")
    print(f"{C.YELLOW}[2]{C.RESET} Binary -> IP")
    choice = input(f"{C.CYAN}Choice > {C.RESET}").strip()

    if choice == "1":
        ip = get_ip_input()
        print_field("\nBinary", to_binary(ip), C.BLUE)
    elif choice == "2":
        raw = input(f"{C.YELLOW}Enter binary IP (e.g. 11000000.10101000.00000001.00001010): {C.RESET}").strip()
        try:
            octets = raw.split(".")
            if len(octets) != 4:
                raise ValueError("Must have 4 octets")
            decimal_octets = [str(int(o, 2)) for o in octets]
            ip = ".".join(decimal_octets)
            ipaddress.ip_address(ip)  # validation
            print_field("\nIP Address", ip, C.CYAN)
        except ValueError:
            print(f"{C.RED}Invalid binary format!{C.RESET}")
    else:
        print(f"{C.RED}Invalid choice!{C.RESET}")


def help_menu():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== Help =={C.RESET}")
    print(f"""{C.DIM}
This tool lets you perform IP address and CIDR (subnet) calculations.
{C.RESET}
{C.YELLOW}1) Calculate CIDR{C.RESET}
   Enter an IP address and CIDR (e.g. /24) to calculate the network address,
   broadcast address, subnet mask, usable host range, and more.

{C.YELLOW}2) IP Information{C.RESET}
   Shows the class of the entered IP address, whether it's private/public,
   its binary representation, and other properties.

{C.YELLOW}3) Subnet Mask from CIDR{C.RESET}
   Calculates the subnet mask from just the CIDR (prefix length).

{C.YELLOW}4) Wildcard Mask{C.RESET}
   Calculates the wildcard mask (the inverse of the subnet mask) from CIDR.

{C.YELLOW}5) Binary Converter{C.RESET}
   Converts an IP address to binary, or binary to an IP address.

{C.DIM}Example CIDR notation: 192.168.1.0/24{C.RESET}
""")


# ----------------------------------------------------------------------
# Main Menu
# ----------------------------------------------------------------------

def print_menu():
    print(BANNER)
    print(f"{C.CYAN}{'═' * 55}{C.RESET}")
    print(f" {C.YELLOW}[1]{C.RESET} Calculate CIDR")
    print(f" {C.YELLOW}[2]{C.RESET} IP Information")
    print(f" {C.YELLOW}[3]{C.RESET} Subnet Mask from CIDR")
    print(f" {C.YELLOW}[4]{C.RESET} Wildcard Mask")
    print(f" {C.YELLOW}[5]{C.RESET} Binary Converter")
    print(f" {C.YELLOW}[6]{C.RESET} Help")
    print(f" {C.RED}[0]{C.RESET} Exit")
    print(f"{C.CYAN}{'═' * 55}{C.RESET}")


def main():
    actions = {
        "1": calculate_cidr,
        "2": ip_information,
        "3": subnet_mask_from_cidr,
        "4": wildcard_mask,
        "5": binary_converter,
        "6": help_menu,
    }

    while True:
        clear_screen()
        print_menu()
        choice = input(f"{C.BOLD}{C.GREEN}Choice > {C.RESET}").strip()

        if choice == "0":
            print(f"{C.CYAN}Exiting... Goodbye!{C.RESET}")
            sys.exit(0)

        action = actions.get(choice)
        if action:
            try:
                action()
            except KeyboardInterrupt:
                print(f"\n{C.RED}Operation cancelled.{C.RESET}")
        else:
            print(f"{C.RED}Invalid choice! Please select an option from the menu.{C.RESET}")

        input(f"\n{C.DIM}Press Enter to continue...{C.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.CYAN}Exiting...{C.RESET}")
        sys.exit(0)
