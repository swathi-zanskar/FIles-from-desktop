import re

def clean_binary_file(input_file, output_file):
    # Read the binary file
    with open(input_file, 'rb') as file:
        binary_content = file.read()
    
    # Decode using utf-8 with 'ignore' to skip undecodable bytes
    text_content = binary_content.decode('utf-8', errors='ignore')
    
    # Remove non-printable ASCII characters
    cleaned_content = re.sub(r'[^\x20-\x7E\n\r\t]', '', text_content)
    
    # Write the cleaned content to the output file
    with open(output_file, 'w', encoding='utf-8', newline='\n') as file:
        file.write(cleaned_content.strip() + '\n')

    print(f"Cleaned text saved to {output_file}")

# Example usage
clean_binary_file('/home/swathi/Downloads/mock/PROD15/cm/NSE_CM_Pro(ZS)_mock_connection', 'NSE_CM_Pro(ZS)_mock_connection.txt')
