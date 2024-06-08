package io.github.privacystreams.commons.arithmetic;

/**
 * Multiply two numbers.
 */

class MultiplyOperator extends Arithmetic2OpOperator<Number> {
    MultiplyOperator(String numField1, String numField2) {
        super(numField1, numField2);
    }

    @Override
    protected Number processNums(Number number1, Number number2) {
        return number1.doubleValue() * number2.doubleValue();
    }
}
