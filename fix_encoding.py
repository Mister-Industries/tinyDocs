import os

def fix_encoding(file_path):
    """
    Fix encoding issues in a single file by converting non-ASCII characters to ASCII equivalents
    or removing them entirely.
    """
    print(f"Processing {file_path}")
    
    # Try reading with different encodings
    for encoding in ['utf-8', 'cp1252', 'latin1']:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                print(f"  Successfully read with {encoding} encoding")
                break
        except UnicodeDecodeError:
            print(f"  Failed to read with {encoding} encoding")
            content = None
            continue
    
    if content is None:
        print(f"  ERROR: Unable to read {file_path} with any encoding")
        return False
    
    # Find and report problematic characters
    problematic_chars = set()
    for char in content:
        if ord(char) >= 128:
            problematic_chars.add(char)
    
    if problematic_chars:
        print(f"  Found {len(problematic_chars)} non-ASCII characters:")
        for char in problematic_chars:
            print(f"    '{char}' (Unicode U+{ord(char):04X})")
    else:
        print("  No non-ASCII characters found.")
        return True
    
    # Replace or remove problematic characters
    cleaned_content = ''
    replacements = {
        '—': '--',    # em dash
        '–': '-',     # en dash
        ''': "'",     # curly single quote (left)
        ''': "'",     # curly single quote (right)
        '"': '"',     # curly double quote (left)
        '"': '"',     # curly double quote (right)
        '…': '...',   # ellipsis
        '•': '*',     # bullet
        '·': '.',     # middle dot
        '©': '(c)',   # copyright
        '®': '(R)',   # registered trademark
        '™': '(TM)',  # trademark
        '£': 'GBP',   # pound
        '€': 'EUR',   # euro
        '×': 'x',     # multiplication sign
        '÷': '/',     # division sign
        '≤': '<=',    # less than or equal
        '≥': '>=',    # greater than or equal
        '≠': '!=',    # not equal
        '≈': '~=',    # approximately equal
        '°': ' degrees', # degree sign
        '±': '+/-',   # plus-minus sign
        '💫': '*',    # sparkle emoji
        '\u2584': '_' # lower half block
    }
    
    char_count = 0
    for char in content:
        if ord(char) < 128:  # Keep ASCII characters
            cleaned_content += char
        else:
            char_count += 1
            # Replace with closest ASCII equivalent or remove
            if char in replacements:
                cleaned_content += replacements[char]
            else:
                # Remove other non-ASCII characters
                cleaned_content += '?'
    
    # Write the cleaned content back
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)
    
    print(f"  Replaced {char_count} characters and saved with UTF-8 encoding")
    return True

def process_directory(directory_path):
    """
    Process all markdown and text files in the specified directory.
    """
    print(f"Scanning directory: {directory_path}")
    
    # Count successes and failures
    success_count = 0
    failure_count = 0
    
    # Process each file with a markdown or text extension
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(('.md', '.markdown', '.txt')):
                file_path = os.path.join(root, filename)
                if fix_encoding(file_path):
                    success_count += 1
                else:
                    failure_count += 1
    
    print("\nProcessing complete!")
    print(f"Successfully processed: {success_count} files")
    print(f"Failed to process: {failure_count} files")

if __name__ == "__main__":
    # Get directory from user input
    print("Fix Encoding for Markdown Files\n")
    directory = input("Enter the full path to your markdown directory: ")
    
    # Remove quotes if the user included them
    directory = directory.strip('"\'')
    
    if os.path.isdir(directory):
        process_directory(directory)
    else:
        print(f"Error: '{directory}' is not a valid directory.")