# generate_output.py

def generate_lexer_code():
    return """
    // Lexer loop
    const char* ptr = input;
    FILE* fout = fopen("tokens.txt", "w");
    if (!fout) {
        perror("Nepodarilo sa otvoriť výstupný súbor");
        return 1;
    }

    while (*ptr) {
        if (strncmp(ptr, "if", 2) == 0 && !isalnum(ptr[2]) && ptr[2] != '_') {
            fprintf(fout, "IF: if\\n");
            ptr += 2;
        }
        else if (strncmp(ptr, "return", 6) == 0 && !isalnum(ptr[6]) && ptr[6] != '_') {
            fprintf(fout, "RETURN: return\\n");
            ptr += 6;
        }
        else if (strncmp(ptr, "else", 4) == 0 && !isalnum(ptr[4]) && ptr[4] != '_') {
            fprintf(fout, "ELSE: else\\n");
            ptr += 4;
        }
        else if (strncmp(ptr, "while", 5) == 0 && !isalnum(ptr[5]) && ptr[5] != '_') {
            fprintf(fout, "WHILE: while\\n");
            ptr += 5;
        }
        else if (isdigit(*ptr)) {
            const char* start = ptr;
            while (isdigit(*ptr)) ptr++;
            char buffer[64];
            strncpy(buffer, start, ptr - start);
            buffer[ptr - start] = '\\0';
            fprintf(fout, "INT: %s\\n", buffer);
        }
        else if (isalpha(*ptr) || *ptr == '_') {
            const char* start = ptr;
            while (isalnum(*ptr) || *ptr == '_') ptr++;
            char buffer[64];
            strncpy(buffer, start, ptr - start);
            buffer[ptr - start] = '\\0';
            fprintf(fout, "IDENTIFIER: %s\\n", buffer);
        }
        else if (*ptr == '=' && ptr[1] == '=') {
            fprintf(fout, "EQ: ==\\n"); ptr += 2;
        }
        else if (*ptr == '!' && ptr[1] == '=') {
            fprintf(fout, "NEQ: !=\\n"); ptr += 2;
        }
        else if (*ptr == '<' && ptr[1] == '=') {
            fprintf(fout, "LE: <=\\n"); ptr += 2;
        }
        else if (*ptr == '>' && ptr[1] == '=') {
            fprintf(fout, "GE: >=\\n"); ptr += 2;
        }
        else if (*ptr == '<') {
            fprintf(fout, "LT: <\\n"); ptr++;
        }
        else if (*ptr == '>') {
            fprintf(fout, "GT: >\\n"); ptr++;
        }
        else if (*ptr == '&' && ptr[1] == '&') {
            fprintf(fout, "AND: &&\\n"); ptr += 2;
        }
        else if (*ptr == '|' && ptr[1] == '|') {
            fprintf(fout, "OR: ||\\n"); ptr += 2;
        }
        else if (*ptr == '+' && ptr[1] == '=') {
            fprintf(fout, "PLUSEQ: +=\\n"); ptr += 2;
        }
        else if (*ptr == '-' && ptr[1] == '=') {
            fprintf(fout, "MINUSEQ: -=\\n"); ptr += 2;
        }
        else if (*ptr == '*' && ptr[1] == '=') {
            fprintf(fout, "MULEQ: *=\\n"); ptr += 2;
        }
        else if (*ptr == '/' && ptr[1] == '=') {
            fprintf(fout, "DIVEQ: /=\\n"); ptr += 2;
        }
        else if (*ptr == '=') {
            fprintf(fout, "ASSIGN: =\\n"); ptr++;
        }
        else if (*ptr == '+') {
            fprintf(fout, "ADD: +\\n"); ptr++;
        }
        else if (*ptr == '-') {
            fprintf(fout, "SUB: -\\n"); ptr++;
        }
        else if (*ptr == '*') {
            fprintf(fout, "MUL: *\\n"); ptr++;
        }
        else if (*ptr == '/') {
            fprintf(fout, "DIV: /\\n"); ptr++;
        }
        else if (*ptr == '(') {
            fprintf(fout, "LPAREN: (\\n"); ptr++;
        }
        else if (*ptr == ')') {
            fprintf(fout, "RPAREN: )\\n"); ptr++;
        }
        else if (*ptr == '{') {
            fprintf(fout, "LBRACE: {\\n"); ptr++;
        }
        else if (*ptr == '}') {
            fprintf(fout, "RBRACE: }\\n"); ptr++;
        }
        else if (*ptr == ';') {
            fprintf(fout, "SEMICOLON: ;\\n"); ptr++;
        }
        else if (*ptr == ',') {
            fprintf(fout, "COMMA: ,\\n"); ptr++;
        }
        else if (isspace(*ptr)) {
            ptr++;
        }
        else {
            char unknown[2] = {*ptr, '\\0'};
            fprintf(fout, "UNKNOWN: %s\\n", unknown);
            ptr++;
        }
    }

    fclose(fout);
    """


def main():
    with open("template/template.c", "r", encoding="utf-8") as f:
        template = f.read()

    lexer_code = generate_lexer_code()
    output_code = template.replace("%%LEXER_TRANSITIONS%%", lexer_code)

    with open("output_lexer.c", "w", encoding="utf-8") as f:
        f.write(output_code)

    print("✅ Súbor 'output_lexer.c' bol vygenerovaný.")


if __name__ == "__main__":
    main()
