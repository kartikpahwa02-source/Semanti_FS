# cli_app.py - Unified Command-Line Interface for SemantiFS

import os
import database
from embedder import process_and_store_file
from search import semantic_search


def main():
    database.init_db()

    while True:
        print("\n==============================")
        print("      SEMANTIFS CLI      ")
        print("==============================")
        print("1. Index a File Manually")
        print("2. Run Natural Language Search")
        print("3. Exit")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == '1':
            file_path = input("Enter absolute file path to index: ").strip().strip('"')
            if os.path.exists(file_path):
                process_and_store_file(file_path)
            else:
                print("[Error] File path does not exist.")

        elif choice == '2':
            query = input("Enter your search query: ").strip()
            if query:
                print("\nSelect Filter Option:")
                print("1. All Files (Default)")
                print("2. Text Documents Only")
                print("3. Images Only")
                print("4. Audio Transcripts Only")
                print("5. PDFs Only")
                filter_choice = input("Enter option (1-5): ").strip()

                filter_map = {'2': 'text', '3': 'image', '4': 'audio', '5': 'pdf'}
                selected_filter = filter_map.get(filter_choice)

                results = semantic_search(query, filter_type=selected_filter)
                print(f"\n=== Search Results ({len(results)} matches) ===")
                for idx, res in enumerate(results, 1):
                    flag = " (weak)" if res.get('weak') else ""
                    print(f"[{idx}] ({res['type']}) Score: {res['score']:.4f}{flag}")
                    print(f"    Path: {res['file_path']}")
                    print(f"    Snippet: {res['content'][:200]}...\n")

        elif choice == '3':
            print("Exiting SemantiFS. Goodbye!")
            break
        else:
            print("Invalid option. Choose 1, 2, or 3.")


if __name__ == "__main__":
    main()