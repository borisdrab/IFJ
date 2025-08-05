import re

class Transition:
    def __init__(self, from_state, symbol, to_state):
        self.from_state = from_state
        self.symbol = symbol
        self.to_state = to_state
        self.matchers = self._compile_symbol(symbol)

    def _unescape(self, s):
        """Prevedie escape sekvencie ako \\t na tabuľátor atď."""
        return bytes(s, "utf-8").decode("unicode_escape")

    def _compile_symbol(self, symbol):
        # Extrahuje všetky časti: "a", "a"-"z", "\t", _, atď.
        parts = re.findall(r'"[^"]+"(?:-"[^"]+")?|[^,\s]+', symbol)
        matchers = []

        for part in parts:
            part = part.strip()
            if '-' in part and part.count('"') == 4:
                # Napr. '"a"-"z"' alebo '"\t"-"\n"'
                match = re.match(r'"(.*)"-"(.*)"', part)
                if match:
                    a, b = self._unescape(match.group(1)), self._unescape(match.group(2))
                    matchers.append(lambda c, a=a, b=b: a <= c <= b)
                else:
                    raise ValueError(f"Nesprávny rozsah alebo symbol: {part}")
            elif part.startswith('"') and part.endswith('"'):
                ch = self._unescape(part[1:-1])
                matchers.append(lambda c, ch=ch: c == ch)
            elif len(part) == 1:
                matchers.append(lambda c, ch=part: c == ch)
            else:
                raise ValueError(f"Nesprávny rozsah alebo symbol: {part}")

        return matchers

    def matches(self, char):
        return any(m(char) for m in self.matchers)


class DFA:
    def __init__(self, transitions, outputs, keyword_map=None):
        self.transitions = transitions
        self.outputs = outputs
        self.keyword_map = keyword_map or {}
        self.reset()

    def reset(self):
        self.current_state = "START"
        self.current_token = None

    def step(self, char):
        for t in self.transitions:
            if t.from_state == self.current_state and t.matches(char):
                self.current_state = t.to_state
                if self.current_state in self.outputs:
                    self.current_token = self.outputs[self.current_state]
                return True
        return False

    def is_final(self):
        return self.current_token is not None

    def get_token(self):
        return self.current_token

    def check_keyword(self, value):
        return self.keyword_map.get(value)

