#!/usr/bin/env python3
"""
CIDR Calculator
===============
Basit bir komut satırı IP/CIDR hesaplama aracı.

Menü:
[1] Calculate CIDR          -> IP + CIDR girilir, ağ bilgileri hesaplanır
[2] IP Information           -> Tek bir IP hakkında bilgi (sınıf, özel/genel vb.)
[3] Subnet Mask from CIDR     -> CIDR'den subnet mask üretir
[4] Wildcard Mask             -> CIDR'den wildcard mask üretir
[5] Binary Converter          -> IP <-> Binary dönüşümü
[6] Help                      -> Kullanım bilgisi
[0] Exit                      -> Çıkış
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
                                                                                                  
{C.RESET}{C.DIM}                 IPv4 / CIDR / Subnet Hesaplama Aracı{C.RESET}
"""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def clear_line():
    print(f"{C.DIM}{'-' * 55}{C.RESET}")


def get_ip_input(prompt="IP adresi girin (örn: 192.168.1.10): "):
    while True:
        raw = input(prompt).strip()
        try:
            return ipaddress.ip_address(raw)
        except ValueError:
            print("Geçersiz IP adresi! Tekrar deneyin.\n")


def get_cidr_input(prompt="CIDR / prefix uzunluğu girin (0-32): "):
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if 0 <= val <= 32:
                return val
            print("CIDR 0 ile 32 arasında olmalı!\n")
        except ValueError:
            print("Geçersiz sayı! Tekrar deneyin.\n")


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
        return "E (Deneysel)"


def to_binary(ip):
    return ".".join(f"{int(o):08b}" for o in str(ip).split("."))


# ----------------------------------------------------------------------
# Menü fonksiyonları
# ----------------------------------------------------------------------

def print_field(label, value, color=C.GREEN):
    print(f"{C.DIM}{label:<22}{C.RESET}: {color}{value}{C.RESET}")


def calculate_cidr():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== CIDR Hesaplama =={C.RESET}")
    ip_raw = input(f"{C.YELLOW}IP adresi (örn: 192.168.1.10): {C.RESET}").strip()
    cidr = get_cidr_input()

    try:
        network = ipaddress.ip_network(f"{ip_raw}/{cidr}", strict=False)
    except ValueError as e:
        print(f"{C.RED}Hata: {e}{C.RESET}")
        return

    print()
    print_field("Girilen IP", ip_raw, C.CYAN)
    print_field("CIDR", f"/{cidr}", C.CYAN)
    print_field("Ağ Adresi (Network)", network.network_address)
    print_field("Broadcast Adresi", network.broadcast_address)
    print_field("Subnet Mask", network.netmask)
    print_field("Wildcard Mask", network.hostmask)
    print_field("Toplam Adres Sayısı", network.num_addresses)

    usable = list(network.hosts())
    if usable:
        print_field("Kullanılabilir Host", len(usable))
        print_field("İlk Kullanılabilir", usable[0])
        print_field("Son Kullanılabilir", usable[-1])
    else:
        print_field("Kullanılabilir Host", "0 (Bu ağda host adresi yok)", C.RED)

    print_field("Ağ Sınıfı", ip_class(network.network_address), C.YELLOW)
    print_field("Binary Ağ Adresi", to_binary(network.network_address), C.BLUE)


def yn(val):
    return (C.GREEN + "Evet" + C.RESET) if val else (C.RED + "Hayır" + C.RESET)


def ip_information():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== IP Bilgisi =={C.RESET}")
    ip = get_ip_input()

    print()
    print_field("IP Adresi", ip, C.CYAN)
    print_field("Versiyon", f"IPv{ip.version}", C.CYAN)
    print_field("Binary", to_binary(ip), C.BLUE)
    print_field("Sınıf", ip_class(ip), C.YELLOW)
    print(f"{C.DIM}{'Özel (Private)':<22}{C.RESET}: {yn(ip.is_private)}")
    print(f"{C.DIM}{'Loopback':<22}{C.RESET}: {yn(ip.is_loopback)}")
    print(f"{C.DIM}{'Multicast':<22}{C.RESET}: {yn(ip.is_multicast)}")
    print(f"{C.DIM}{'Reserved':<22}{C.RESET}: {yn(ip.is_reserved)}")
    print(f"{C.DIM}{'Link-local':<22}{C.RESET}: {yn(ip.is_link_local)}")
    print(f"{C.DIM}{'Unspecified (0.0.0.0)':<22}{C.RESET}: {yn(ip.is_unspecified)}")


def subnet_mask_from_cidr():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== CIDR'den Subnet Mask =={C.RESET}")
    cidr = get_cidr_input()
    mask = ipaddress.IPv4Network(f"0.0.0.0/{cidr}").netmask
    print()
    print_field("CIDR", f"/{cidr}", C.CYAN)
    print_field("Subnet Mask", mask)
    print_field("Binary", to_binary(mask), C.BLUE)


def wildcard_mask():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== CIDR'den Wildcard Mask =={C.RESET}")
    cidr = get_cidr_input()
    wildcard = ipaddress.IPv4Network(f"0.0.0.0/{cidr}").hostmask
    print()
    print_field("CIDR", f"/{cidr}", C.CYAN)
    print_field("Wildcard Mask", wildcard)
    print_field("Binary", to_binary(wildcard), C.BLUE)


def binary_converter():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== Binary Dönüştürücü =={C.RESET}")
    print(f"{C.YELLOW}[1]{C.RESET} IP -> Binary")
    print(f"{C.YELLOW}[2]{C.RESET} Binary -> IP")
    choice = input(f"{C.CYAN}Seçim > {C.RESET}").strip()

    if choice == "1":
        ip = get_ip_input()
        print_field("\nBinary", to_binary(ip), C.BLUE)
    elif choice == "2":
        raw = input(f"{C.YELLOW}Binary IP girin (örn: 11000000.10101000.00000001.00001010): {C.RESET}").strip()
        try:
            octets = raw.split(".")
            if len(octets) != 4:
                raise ValueError("4 oktet olmalı")
            decimal_octets = [str(int(o, 2)) for o in octets]
            ip = ".".join(decimal_octets)
            ipaddress.ip_address(ip)  # doğrulama
            print_field("\nIP Adresi", ip, C.CYAN)
        except ValueError:
            print(f"{C.RED}Geçersiz binary formatı!{C.RESET}")
    else:
        print(f"{C.RED}Geçersiz seçim!{C.RESET}")


def help_menu():
    clear_line()
    print(f"{C.BOLD}{C.MAGENTA}== Yardım =={C.RESET}")
    print(f"""{C.DIM}
Bu araç, IP adresleri ve CIDR (subnet) hesaplamaları yapmanızı sağlar.
{C.RESET}
{C.YELLOW}1) Calculate CIDR{C.RESET}
   Bir IP adresi ve CIDR (/24 gibi) girerek ağ adresi, broadcast,
   subnet mask, kullanılabilir host aralığı gibi bilgileri hesaplar.

{C.YELLOW}2) IP Information{C.RESET}
   Girilen bir IP adresinin sınıfını, özel/genel olup olmadığını,
   binary karşılığını ve diğer özelliklerini gösterir.

{C.YELLOW}3) Subnet Mask from CIDR{C.RESET}
   Sadece CIDR (prefix uzunluğu) girerek subnet mask'i hesaplar.

{C.YELLOW}4) Wildcard Mask{C.RESET}
   CIDR'den wildcard mask (subnet mask'in tersi) hesaplar.

{C.YELLOW}5) Binary Converter{C.RESET}
   IP adresini binary'e, ya da binary'i IP adresine çevirir.

{C.DIM}Örnek CIDR notasyonu: 192.168.1.0/24{C.RESET}
""")


# ----------------------------------------------------------------------
# Ana Menü
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
            print(f"{C.CYAN}Çıkış yapılıyor... Görüşürüz!{C.RESET}")
            sys.exit(0)

        action = actions.get(choice)
        if action:
            try:
                action()
            except KeyboardInterrupt:
                print(f"\n{C.RED}İşlem iptal edildi.{C.RESET}")
        else:
            print(f"{C.RED}Geçersiz seçim! Lütfen menüden bir seçenek girin.{C.RESET}")

        input(f"\n{C.DIM}Devam etmek için Enter'a basın...{C.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.CYAN}Çıkış yapılıyor...{C.RESET}")
        sys.exit(0)