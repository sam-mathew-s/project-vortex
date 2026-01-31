import sys
import time
from vortex import crawl_website 
from search import search_vortex 

def print_menu():
    print("\n" + "="*40)
    print("PROJECT VORTEX: COMMAND CENTER")
    print("="*40)
    print(" [1]  CRAWL NEW INTEL (Add Website)")
    print(" [2]  SEARCH ARCHIVES (Query Database)")
    print("="*40)
    
def main():
    while True:
        print_menu()
        choice = input("\n ENTER COMMAND: ")

        if choice == '1':
            url = input("PASTE URL TO CRAWL: ")
            print("\n--- INITIATING CRAWLER PROTOCOL ---")
            crawl_website(url)
            time.sleep(1)  # read the result time

        elif choice == '2':
            query = input("ENTER SEARCH TERM: ")
            print("\n--- ACCESSING DATABASE ---")
            search_vortex(query)
            input("\n(Press Enter to continue...)") #Pause for read 
            
        elif choice == '3':
            print("\n SHUTTING DOWN SYSTEM. GOODBYE COMMANDER.")
            break
        else:
            print("INVALID COMMAND. TRY AGAIN.")

if __name__ == "__main__":
    main()