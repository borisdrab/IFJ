#include <stdio.h>
#include <string.h>
#include <ctype.h>

enum TokenType {
    TOKEN_UNKNOWN,
    TOKEN_IDENTIFIER,
    TOKEN_INT,
    TOKEN_IF,
    TOKEN_RETURN,
    TOKEN_ELSE,
    TOKEN_WHILE,
    TOKEN_EQ,
    TOKEN_NEQ,
    TOKEN_ASSIGN,
    TOKEN_ADD,
    TOKEN_SUB,
    TOKEN_MUL,
    TOKEN_DIV,
    TOKEN_LT,
    TOKEN_GT,
    TOKEN_LE,
    TOKEN_GE,
    TOKEN_AND,
    TOKEN_OR,
    TOKEN_PLUSEQ,
    TOKEN_MINUSEQ,
    TOKEN_MULEQ,
    TOKEN_DIVEQ,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LBRACE,
    TOKEN_RBRACE,
    TOKEN_SEMICOLON,
    TOKEN_COMMA
};

void print_token(enum TokenType type, const char* value) {
    printf("%s: %s\n", 
        (type == TOKEN_IF) ? "IF" :
        (type == TOKEN_RETURN) ? "RETURN" :
        (type == TOKEN_ELSE) ? "ELSE" :
        (type == TOKEN_WHILE) ? "WHILE" :
        (type == TOKEN_IDENTIFIER) ? "IDENTIFIER" :
        (type == TOKEN_INT) ? "INT" :
        (type == TOKEN_EQ) ? "EQ" :
        (type == TOKEN_NEQ) ? "NEQ" :
        (type == TOKEN_ASSIGN) ? "ASSIGN" :
        (type == TOKEN_ADD) ? "ADD" :
        (type == TOKEN_SUB) ? "SUB" :
        (type == TOKEN_MUL) ? "MUL" :
        (type == TOKEN_DIV) ? "DIV" :
        (type == TOKEN_LT) ? "LT" :
        (type == TOKEN_GT) ? "GT" :
        (type == TOKEN_LE) ? "LE" :
        (type == TOKEN_GE) ? "GE" :
        (type == TOKEN_AND) ? "AND" :
        (type == TOKEN_OR) ? "OR" :
        (type == TOKEN_PLUSEQ) ? "PLUSEQ" :
        (type == TOKEN_MINUSEQ) ? "MINUSEQ" :
        (type == TOKEN_MULEQ) ? "MULEQ" :
        (type == TOKEN_DIVEQ) ? "DIVEQ" :
        (type == TOKEN_LPAREN) ? "LPAREN" :
        (type == TOKEN_RPAREN) ? "RPAREN" :
        (type == TOKEN_LBRACE) ? "LBRACE" :
        (type == TOKEN_RBRACE) ? "RBRACE" :
        (type == TOKEN_SEMICOLON) ? "SEMICOLON" :
        (type == TOKEN_COMMA) ? "COMMA" :
        (type == TOKEN_UNKNOWN) ? "UNKNOWN" :
        "UNKNOWN_TYPE",
        value);
}

int main(int argc, char** argv) {
    const char* input = "if (x == 10) { return x_1 + 5; } else { while (x_1 != 3) { x_1 += 1; } }";
    if (argc == 2) {
        FILE* file = fopen(argv[1], "r");
        if (!file) {
            perror("Nepodarilo sa otvoriť vstupný súbor");
            return 1;
        }
        static char buffer[4096];
        size_t read = fread(buffer, 1, sizeof(buffer) - 1, file);
        buffer[read] = '\0';
        fclose(file);
        input = buffer;
    }

    %%LEXER_TRANSITIONS%%

    return 0;
}
