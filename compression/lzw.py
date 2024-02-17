import time


def encoding(s1):
    print("Encoding")
    table = {chr(i): i for i in range(256)}

    p = s1[0]
    code = 256
    output_code = []

    print("String\tOutput_Code\tAddition")
    start_time = time.time()
    i = 0
    while i < len(s1) - 1:
        c = s1[i + 1]

        if p + c in table:
            p = p + c
        else:
            print(f"{p}\t{table[p]}\t\t{p + c}\t{code}")
            output_code.append(table[p])
            table[p + c] = code
            code += 1
            p = c
        i += 1

    print(f"{p}\t{table[p]}")
    output_code.append(table[p])
    end_time = time.time()
    compression_time = end_time - start_time
    return output_code, compression_time


def decoding(op):
    print("\nDecoding")
    table = {i: chr(i) for i in range(256)}

    old = op[0]
    s = table[old]
    print(s, end="")

    count = 256
    i = 0
    while i < len(op) - 1:
        n = op[i + 1]

        if n not in table:
            s = table[old] + table[old][0]
        else:
            s = table[n]

        print(s, end="")
        table[count] = table[old] + s[0]
        count += 1
        old = n
        i += 1


def decode_data(encoded_data):
    table = {i: chr(i) for i in range(256)}

    decoded_data = []
    old = encoded_data[0]

    for n in encoded_data[1:]:
        if n not in table:
            s = table[old] + table[old][0]
        else:
            s = table[n]

        decoded_data.append(s)
        table[len(table)] = table[old] + s[0]
        old = n

    return ''.join(decoded_data)


if __name__ == "__main__":
    choice = input("Choose an option (1 for encoding, 2 for decoding): ")

    if choice == "1":
        file_path = input("Enter the path of the file: ")
        try:
            with open(file_path, "r") as file:
                content = file.read()
                output_code, compression_time = encoding(content)
                print("Output Codes are:", end=" ")
                for code in output_code:
                    print(code, end=" ")
                print()
                decoding(output_code)

                # Print compression time
                print(f"\nCompression Time: {compression_time:.6f} seconds")

        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif choice == "2":
        encoded_data = input("Enter the encoded data (space-separated integers): ")
        try:
            encoded_data = list(map(int, encoded_data.split()))
            decoded_data = decode_data(encoded_data)
            print("Decoded data:", decoded_data)
        except ValueError:
            print("Invalid input. Please provide space-separated integers.")
    else:
        print("Invalid choice. Please choose 1 or 2.")
