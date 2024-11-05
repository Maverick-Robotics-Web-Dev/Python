from decimal import Decimal


def convert_decimal(number) -> Decimal:

    conver: Decimal = Decimal(number).quantize(Decimal('.00'))

    return conver


def addition_decimals(term_one, term_two):

    result = convert_decimal(term_one) + convert_decimal(term_two)

    return result


def subtraction_decimals(term_one, term_two) -> Decimal:

    result: Decimal = convert_decimal(term_one) - convert_decimal(term_two)

    return result
