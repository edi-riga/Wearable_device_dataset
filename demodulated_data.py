import os
import json

def count_total_packets(metadata):
    return len(metadata)

def select_json_file(json_files):
    print("Select a JSON file to load:")
    for idx, file_path in enumerate(json_files):
        print(f"{idx + 1}. {file_path}")
    selection = int(input("Enter the number corresponding to the file you want to load: ")) - 1
    if selection < 0 or selection >= len(json_files):
        print("Invalid selection.")
        return None
    return json_files[selection]

def find_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

# Function to prompt user to select a packet and print its metadata entries
def select_and_print_packet_metadata(metadata):
    while True:
        packet_num = input("Enter the packet number you want to load (or 'q' to quit): ")
        if packet_num.lower() == 'q':
            break
        try:
            packet_idx = int(packet_num) - 1
            if 0 <= packet_idx < len(metadata):
                packet = metadata[packet_idx]
                print(f"Packet {packet_idx + 1}:")
                for key, value in packet.items():
                    print(f"{key}: {value}")
                print("\n")
            else:
                print("Invalid packet number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

# Main function
def main():
    # Directory to search for JSON files
    directory_to_search = '.'  # You can specify the directory path here

    # Find JSON files in the directory
    json_files = find_json_files(directory_to_search)

    # Check if any JSON files were found
    if not json_files:
        print("No JSON files found in the directory.")
        return

    # Prompt user to select a JSON file
    selected_file = select_json_file(json_files)
    if not selected_file:
        return

    # Load the selected JSON file into memory
    with open(selected_file, 'r') as file:
        json_data = json.load(file)

    # Process the loaded JSON data
    num_total_packets = count_total_packets(json_data)
    print(f"Number of all packets: {num_total_packets}")

    # Prompt user to select a packet and print its metadata entries
    if num_total_packets > 0:
        select_and_print_packet_metadata(json_data)

if __name__ == "__main__":
    main()