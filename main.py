# main.py

from config import Transition, DFA

def load_dka(filepath):
    transitions = []
    outputs = {}
    keyword_map = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("?"):
                parts = line[1:].split("->")
                keyword = parts[0].strip()
                token = parts[1].strip()
                keyword_map[keyword] = token

            elif line.startswith("{") and line.endswith("}"):
                content = line[1:-1]
                state, token = map(str.strip, content.split('='))
                outputs[state] = token

            elif '->' in line:
                parts = line.split('->')
                left = parts[0].strip()
                right = parts[1].strip()

                # Správne rozparsuj (FROM, SYMBOLY...) -> TO
                if left.startswith("(") and left.endswith(")"):
                    inside = left[1:-1]
                    parts_inside = inside.split(",", 1)
                    from_state = parts_inside[0].strip()
                    symbol = parts_inside[1].strip()
                    transitions.append(Transition(from_state, symbol, right))
                else:
                    raise ValueError(f"Nesprávny formát riadku: {line}")

    return DFA(transitions, outputs, keyword_map)


def tokenize(dfa, text):
    tokens = []
    i = 0

    while i < len(text):
        dfa.reset()
        j = i
        last_final = -1
        last_token = None

        while j < len(text) and dfa.step(text[j]):
            if dfa.is_final():
                last_final = j
                last_token = dfa.get_token()
            j += 1

        if last_final != -1:
            value = text[i:last_final + 1]
            if last_token != "IGNORE":
                keyword_token = dfa.check_keyword(value)
                if keyword_token:
                    tokens.append((keyword_token, value))
                else:
                    tokens.append((last_token, value))
            i = last_final + 1
        else:
            print(f"Chyba: neplatný token pri znaku '{text[i]}' (pozícia {i})")
            i += 1

    return tokens


if __name__ == "__main__":
    dfa = load_dka("mylexer.dka")

    with open("test_input.code", "r", encoding='utf-8') as f:
        code = f.read()

    tokens = tokenize(dfa, code)

    for tok in tokens:
        print(f"{tok[0]}: {tok[1]}")
