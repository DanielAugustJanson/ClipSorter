import os
import datetime
from collections import defaultdict

def get_file_modification_time(path):
    """Get file modification time"""
    return os.path.getmtime(path)

def generate_alphabetical_index(index):
    """Generate alphabetical sequence (AA, AB, AC...)"""
    first_char = chr(ord('A') + (index // 26))
    second_char = chr(ord('A') + (index % 26))
    return f"{first_char}{second_char}"

def generate_mixed_index(index):
    """Generate mixed alphanumeric sequence (A0, A1... A9, B0...)"""
    letter = chr(ord('A') + (index // 10))
    number = index % 10
    return f"{letter}{number}"

def main():
    print("=== Video Clip Renaming Tool ===")
    
    # User inputs
    prefix = input("Enter prefix for files (e.g., 'DayZ'): ").strip()
    
    print("\nSelect naming scheme:")
    print("1. Numerical (1, 2, 3...)")
    print("2. Alphabetical (AA, AB, AC...)")
    print("3. Mixed alphanumeric (A0, A1... A9, B0...)")
    scheme_choice = input("Enter choice (1-3): ").strip()
    
    date_specific = input("\nUse date-specific naming? (y/n): ").strip().lower() == 'y'
    include_year = False
    if date_specific:
        include_year = input("Include year in date format? (y/n): ").strip().lower() == 'y'
    
    # File processing
    folder = os.getcwd()
    print(f"\nUsing current directory: {folder}")
    
    files = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if not os.path.isfile(filepath):
            continue
        if os.path.splitext(filename)[1].lower() in ['.py', '.txt']:
            continue
            
        try:
            mod_time = get_file_modification_time(filepath)
            mod_date = datetime.datetime.fromtimestamp(mod_time)
            files.append({
                'original': filename,
                'path': filepath,
                'mod_time': mod_time,
                'datetime': mod_date
            })
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    if not files:
        print("No files found in directory!")
        return
    
    files.sort(key=lambda x: x['mod_time'])
    
    # Grouping and naming
    name_groups = defaultdict(list)
    for file in files:
        if date_specific:
            if include_year:
                date_str = file['datetime'].strftime("%Y-%d-%m")
            else:
                date_str = file['datetime'].strftime("%d-%m")
            name_groups[date_str].append(file)
        else:
            name_groups["all"].append(file)
    
    for group, group_files in name_groups.items():
        for idx, file in enumerate(group_files, start=1):
            if scheme_choice == '1':
                seq = f"{idx}"
            elif scheme_choice == '2':
                seq = generate_alphabetical_index(idx-1)
            else:
                seq = generate_mixed_index(idx-1)
            
            new_name = f"{prefix}-{group}-{seq}" if date_specific else f"{prefix}-{seq}"
            file['new_name'] = f"{new_name}{os.path.splitext(file['original'])[1]}"
    
    # Preview and confirmation
    print("\n=== Renaming Preview ===")
    for file in files:
        print(f"{file['original']} -> {file['new_name']}")
    
    if input("\nProceed with renaming? (y/n): ").lower() != 'y':
        print("Cancelled.")
        return
    
    # Execution and logging
    log_entries = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(folder, f"rename_log_{timestamp}.txt")
    
    for file in files:
        try:
            os.rename(file['path'], os.path.join(folder, file['new_name']))
            log_entries.append(f"Success: {file['original']} -> {file['new_name']}")
        except Exception as e:
            log_entries.append(f"Failed: {file['original']} - {str(e)}")
    
    with open(log_file, 'w') as f:
        f.write("\n".join([
            "Rename Log:",
            f"Timestamp: {timestamp}",
            f"Prefix: {prefix}",
            f"Scheme: {['Numerical','Alphabetical','Mixed'][int(scheme_choice)-1]}",
            f"Date Format: {['N/A','Day-Month','Year-Day-Month'][include_year + date_specific]}",
            "\nOperations:",
            *log_entries
        ]))
    
    print(f"\nRenaming complete! Log saved to {log_file}")

if __name__ == "__main__":
    main()