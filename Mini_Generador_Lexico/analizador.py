import re

# Define the token types
TOKEN_TYPES = {
    'NUMBER': 'Number',          
    'FLOAT': 'Float',            
    'STRING': 'String',          
    'ERROR': 'Error',            
}

# Function to check if the token is a valid integer
def is_integer(value):
    return value.isdigit()

# Function to check if the token is a valid float
def is_valid_float(value):
    # Check if there's a dot and if the parts before and after the dot are valid
    if '.' in value:
        parts = value.split('.')
        if len(parts) == 2 and (parts[0] == '' or parts[1] == ''):  # Incomplete float
            return False
        elif len(parts) == 2 and not parts[1].isdigit():  # Invalid float, e.g., '80.' or '.'
            return False
        return True
    return False

# Function to check if the token is a valid string (alphanumeric or underscore)
def is_valid_string(value):
    # Must be alphanumeric or contain underscores, and must not be empty
    return value.isalnum() 

# Lexical analyzer function
def lexical_analyzer(input_text):
    # Split input into individual tokens by spaces or punctuation
    tokens = input_text.split() 

    analyzed_tokens = []

    for token in tokens:
        if is_integer(token):
            analyzed_tokens.append((token, TOKEN_TYPES['NUMBER']))
        elif is_valid_float(token):
            analyzed_tokens.append((token, TOKEN_TYPES['FLOAT']))
        elif is_valid_string(token):
            analyzed_tokens.append((token, TOKEN_TYPES['STRING']))
        else:
            analyzed_tokens.append((token, TOKEN_TYPES['ERROR']))
    
    return analyzed_tokens

# Function to print the results
def print_token_analysis(input_text):
    print(f"Input: {input_text}")
    print("Tokenized Output:")
    tokens = lexical_analyzer(input_text)
    
    for token, token_type in tokens:
        print(f"Token: '{token}', Type: {token_type}")

# Example run
input_text = input("Enter values separated by spaces: ")
print_token_analysis(input_text)