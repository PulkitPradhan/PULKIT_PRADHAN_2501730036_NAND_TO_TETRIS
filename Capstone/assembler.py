import os
import sys

DEST = {"": "000", "M": "001", "D": "010", "MD": "011", "DM": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111", "ADM": "111"}

JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "A+D": "0000010",
    "D+M": "1000010", "M+D": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "A&D": "0000000",
    "D&M": "1000000", "M&D": "1000000",
    "D|A": "0010101", "A|D": "0010101",
    "D|M": "1010101", "M|D": "1010101",
}

PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
              "SCREEN": 16384, "KBD": 24576}
PREDEFINED.update({f"R{i}": i for i in range(16)})

def assemble(asm_path):
    symbols = dict(PREDEFINED)
    user_symbols = {}
    program = []
    with open(asm_path) as f:
        for line in f:
            text = "".join(line.split("//")[0].split())
            if not text:
                continue
            if text.startswith("(") and text.endswith(")"):
                label = text[1:-1]
                symbols[label] = len(program)
                user_symbols[label] = len(program)
            else:
                program.append(text)
    binary = []
    next_var = 16
    for text in program:
        if text.startswith("@"):
            val = text[1:]
            if val.isdigit():
                addr = int(val)
            else:
                if val not in symbols:
                    symbols[val] = next_var
                    user_symbols[val] = next_var
                    next_var += 1
                addr = symbols[val]
            binary.append(format(addr, "016b"))
        else:
            dest, comp, jump = "", text, ""
            if "=" in comp:
                dest, comp = comp.split("=")
            if ";" in comp:
                comp, jump = comp.split(";")
            binary.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
    return binary, user_symbols

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    asm_path = sys.argv[1]
    binary, user_symbols = assemble(asm_path)
    out_hack = os.path.splitext(asm_path)[0] + ".hack"
    with open(out_hack, "w") as f:
        f.write("\n".join(binary) + "\n")
    sym_dir = os.path.dirname(asm_path)
    sym_path = os.path.join(sym_dir, "symbols.txt") if sym_dir else "symbols.txt"
    with open(sym_path, "w") as f:
        for sym, addr in user_symbols.items():
            f.write(f"{sym} {addr}\n")

if __name__ == "__main__":
    main()
