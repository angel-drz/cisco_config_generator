
import os
import sys
import platform
from datetime import datetime

def get_script_dir():
    """Επιστρέφει τον πραγματικό φάκελο εκτέλεσης (ακόμα και αν γίνει EXE)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def generate_vlan_config():
    print("\n--- VLAN & Interface Config Generator ---")
    vlan_ids = input("Enter VLAN IDs (comma separated, e.g., 10,20,30): ").strip()
    vlan_name_prefix = input("Enter VLAN name prefix (e.g., VLAN): ").strip()
    
    interface_range = input("Enter access interface range (e.g., GigabitEthernet0/1-24): ").strip()
    access_vlan = input("Enter default access VLAN for these ports: ").strip()
    
    trunk_interface = input("Enter trunk interface (leave blank if none, e.g., GigabitEthernet0/24): ").strip()
    allowed_vlans = input("Enter allowed VLANs on trunk (e.g., 10,20,30 or all): ").strip() if trunk_interface else ""

    config = []
    config.append("!\n! --- VLAN CONFIGURATION ---")
    
    # Parse VLANs
    for vid in vlan_ids.split(','):
        vid = vid.strip()
        if vid:
            config.append(f"vlan {vid}")
            config.append(f" name {vlan_name_prefix}_{vid}")
    
    config.append("!\n! --- ACCESS PORTS ---")
    config.append(f"interface range {interface_range}")
    config.append(" switchport mode access")
    config.append(f" switchport access vlan {access_vlan}")
    config.append(" no shutdown")
    
    if trunk_interface:
        config.append("!\n! --- TRUNK PORT ---")
        config.append(f"interface {trunk_interface}")
        config.append(" switchport trunk encapsulation dot1q")
        config.append(" switchport mode trunk")
        if allowed_vlans.lower() != "all" and allowed_vlans.strip() != "":
            config.append(f" switchport trunk allowed vlan {allowed_vlans}")
        config.append(" no shutdown")
        
    return "\n".join(config)

def generate_ospf_config():
    print("\n--- OSPF Routing Config Generator ---")
    process_id = input("Enter OSPF Process ID [Default: 1]: ").strip()
    process_id = process_id if process_id else "1"
    
    router_id = input("Enter Router ID (e.g., 1.1.1.1): ").strip()
    
    networks = []
    print("\nEnter OSPF networks (type 'done' when finished):")
    while True:
        net = input("  Network IP (e.g., 192.168.1.0): ").strip()
        if net.lower() == 'done' or not net:
            break
        wildcard = input(f"  Wildcard mask for {net} (e.g., 0.0.0.255): ").strip()
        area = input(f"  Area ID for {net} (e.g., 0): ").strip()
        networks.append((net, wildcard, area))
        
    config = []
    config.append("!\n! --- OSPF CONFIGURATION ---")
    config.append(f"router ospf {process_id}")
    if router_id:
        config.append(f" router-id {router_id}")
    for net, wildcard, area in networks:
        config.append(f" network {net} {wildcard} area {area}")
    config.append(" passive-interface default")
    
    return "\n".join(config)

def save_to_file(config_text):
    filename_input = input("\nEnter output filename [Default: cisco_config.txt]: ").strip()
    filename = filename_input if filename_input else "cisco_config.txt"
    if not filename.endswith(".txt"):
        filename += ".txt"
        
    filepath = os.path.join(get_script_dir(), filename)
    
    try:
        with open(filepath, "w") as f:
            f.write(f"! ========================================\n")
            f.write(f"! Cisco IOS Bulk Configuration Script\n")
            f.write(f"! Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"! ========================================\n\n")
            f.write("configure terminal\n\n")
            f.write(config_text)
            f.write("\n\nend\nwrite memory\n")
            
        print(f"\n[+] Configuration successfully saved to: \033[92m{filepath}\033[0m")
    except Exception as e:
        print(f"[-] Error saving file: {e}")

def main():
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')
    print("\033[96m========================================")
    print("     Cisco CLI Bulk Config Generator    ")
    print("========================================\033[0m")
    
    print("\nSelect Configuration Type:")
    print("  [1] VLANs & Access/Trunk Interfaces")
    print("  [2] OSPF Routing Protocol")
    print("  [3] Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        cfg = generate_vlan_config()
        print("\n" + "="*45 + "\nGenerated Cisco Configuration:\n" + "="*45)
        print(cfg)
        save_to_file(cfg)
    elif choice == "2":
        cfg = generate_ospf_config()
        print("\n" + "="*45 + "\nGenerated Cisco Configuration:\n" + "="*45)
        print(cfg)
        save_to_file(cfg)
    else:
        print("\nExiting...")

if __name__ == "__main__":
    main()
