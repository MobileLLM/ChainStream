package io.github.privacystreams.commons.logic;

import io.github.privacystreams.core.Function;
import io.github.privacystreams.core.Item;
import io.github.privacystreams.utils.annotations.PSOperatorWrapper;

/**
 * A helper class to access logic-related functions
 */
@PSOperatorWrapper
public class LogicOperators {
    /**
     * Compute the logical NOT of a function.
     *
     * @param predicate the function to test an item
     * @return the function
     */
    public static Function<Item, Boolean> not(final Function<Item, Boolean> predicate) {
        return new NotOperator(predicate);
    }

    /**
     * Compute the logical AND of two functions.
     *
     * @param predicate1 the first function to test an item
     * @param predicate2 the second function to test an item
     * @return the function
     */
    public static Function<Item, Boolean> and(final Function<Item, Boolean> predicate1, final Function<Item, Boolean> predicate2) {
        return new AndOperator(predicate1, predicate2);
    }

    /**
     * Compute the logical OR of two functions.
     *
     * @param predicate1 the first function to test an item
     * @param predicate2 the second function to test an item
     * @return the function
     */
    public static Function<Item, Boolean> or(final Function<Item, Boolean> predicate1, final Function<Item, Boolean> predicate2) {
        return new OrOperator(predicate1, predicate2);
    }
}
