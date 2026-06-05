import json

input_file = r"D:\Portswigger_Python_Scripts\BSCP_PREP\Authentication\passwd.txt"
output_file = r"D:\Portswigger_Python_Scripts\BSCP_PREP\Authentication\passwdd.json"

with open(input_file, "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(words, f, indent=4)

print(f"Saved {len(words)} entries to {output_file}")