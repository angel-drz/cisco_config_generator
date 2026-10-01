# cisco_config_generator

# Cisco CLI Bulk Config Generator

A lightweight, practical Python command-line utility designed for network engineers and CCNA/CCNP students to quickly generate automated Cisco IOS configuration scripts. 

Instead of typing repetitive commands manually in lab environments or production, this tool builds clean, structured configuration blocks and exports them directly into ready-to-use text files.

## 🚀 Features

* **VLAN & Interface Configuration:** Automatically generates VLAN creation blocks, names, access port ranges, and trunk port settings with allowed VLAN filters.
* **OSPF Routing Setup:** Quickly structures OSPF process IDs, custom Router IDs, network statements with wildcard masks, and applies passive interface defaults.
* **Automatic File Export:** Appends proper execution wrappers (`configure terminal`, `end`, `write memory`) and saves the clean output directly into a `.txt` file inside the script's directory.
* **Cross-Platform Path Handling:** Built with native Python libraries (`os`, `sys`, `platform`, `datetime`), making it fully compatible with standalone `.exe` compilation via PyInstaller.

## 📋 Requirements

* Python 3.x installed on your system.
* No external third-party libraries required (uses standard Python libraries only).

## 🎮 How to Use

1. Clone or download the repository.
2. Run the script from your terminal:
   ```bash
   python cisco_config_generator.py
