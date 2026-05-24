import asyncio
import sys
import os

from utils.terminal import clear_screen, print_banner, display_menu, C_RESET, C_RED, C_GREEN, C_YELLOW, C_BOLD
from utils.config import load_config, CONFIG_FILE, IP_RANGES_FILE, PORTS_FILE, FINGERPRINTS_FILE, FILTER_FILE
from core.engine import ScannerEngine

async def run_scan(custom_filter_enabled=False):
    config = load_config()
    engine = ScannerEngine(config, custom_filter_enabled=custom_filter_enabled)
    await engine.init()
    
    scan_task = asyncio.create_task(engine.run())
    
    try:
        await scan_task
    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] CTRL+C detected! Shutting down gracefully...{C_RESET}")
        engine.stop()
        await scan_task
    except Exception as e:
        print(f"\n{C_RED}[!] Scan error: {e}{C_RESET}")
        engine.stop()
    finally:
        input("\nPress Enter to return to menu...")

def edit_config():
    clear_screen()
    print_banner()
    print("[*] Configuration Files:\n")
    print(f"1. {CONFIG_FILE} (Main Config)")
    print(f"2. {IP_RANGES_FILE} (Targets)")
    print(f"3. {PORTS_FILE} (Ports)")
    print(f"4. {FINGERPRINTS_FILE} (Signatures)")
    print(f"5. {FILTER_FILE} (Custom Search Terms)")
    print("\n[*] To edit these, please open them in your preferred text editor.")
    print(f"[*] They are located in the '{os.path.abspath('config')}' directory.")
    input("\nPress Enter to return to menu...")

def show_statistics():
    clear_screen()
    print_banner()
    print("[*] Global Statistics")
    print("Reports are saved in the 'reports' directory.")
    
    if os.path.exists("reports/report.txt"):
        size = os.path.getsize("reports/report.txt")
        print(f"\nTXT Report Size: {size} bytes")
    
    if os.path.exists("reports/report.db"):
        size = os.path.getsize("reports/report.db")
        print(f"SQLite DB Size: {size} bytes")
        
    input("\nPress Enter to return to menu...")

async def main():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        os.system("") # Enable ANSI colors in Windows terminal

    # Ensure files exist
    load_config()

    while True:
        clear_screen()
        print_banner()
        choice = display_menu()

        if choice == "1":
            clear_screen()
            print_banner()
            print(f"{C_BOLD}Select Scan Mode:{C_RESET}")
            print(f"[{C_GREEN}1{C_RESET}] Full Scan (Save all open ports and services)")
            print(f"[{C_YELLOW}2{C_RESET}] Custom Scan (Only save results matching terms in {FILTER_FILE})")
            mode = input(f"\n{C_BOLD}SPECTRE > {C_RESET}").strip()
            
            if mode == "1":
                await run_scan(custom_filter_enabled=False)
            elif mode == "2":
                await run_scan(custom_filter_enabled=True)
            else:
                print(f"{C_RED}Invalid choice.{C_RESET}")
                await asyncio.sleep(1)
        elif choice == "2":
            edit_config()
        elif choice == "3":
            show_statistics()
        elif choice == "4":
            clear_screen()
            print("Exiting SPECTRE. Goodbye!")
            break
        else:
            print(f"{C_RED}Invalid choice.{C_RESET}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        clear_screen()
        print("Exiting SPECTRE. Goodbye!")
        sys.exit(0)