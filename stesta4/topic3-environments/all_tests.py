from stTokenizer import test_simple_tokens, test_identifier_tokens
from stParser import test_parse_simple_expression, test_parse_factor, test_parse_term, test_parse_arithmetic_expression, test_parse_comparison_expression, test_parse_boolean_term, test_parse_boolean_expression, test_parse_expression, test_parse_print_statement, test_parse_assignment_statement, test_parse_statement, test_parse, test_parse_statement_list,test_parse_program
from stEvaluator import test_evaluate_single_value, test_evaluate_addition, test_evaluate_subtraction, test_evaluate_multiplication, test_evaluate_division, test_evaluate_negate, test_evaluate_print_statement, test_assignment_statement, test_statement_list

if __name__ == "__main__":
    print(f"\033[38;5;221m{"--Tokenizer Test Cases--"}\033[0m")
    test_simple_tokens()
    test_identifier_tokens()
    print(f"\033[38;5;221m{"--Parser Test Cases--"}\033[0m")
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_arithmetic_expression()
    test_parse_comparison_expression()
    test_parse_boolean_term()
    test_parse_boolean_expression()
    test_parse_expression()
    test_parse_print_statement()
    test_parse_assignment_statement()
    test_parse_statement()
    test_parse_statement_list()
    test_parse_program()
    test_parse()
    print(f"\033[38;5;221m{"--Evaluator Test Cases--"}\033[0m")
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_negate()
    test_evaluate_print_statement()  #should output 77 57 58
    test_assignment_statement()
    test_statement_list()
    print(f"\033[38;5;117m{" all done."}\033[0m")