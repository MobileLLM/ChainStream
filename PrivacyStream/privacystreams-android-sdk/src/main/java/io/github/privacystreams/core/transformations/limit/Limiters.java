package io.github.privacystreams.core.transformations.limit;

import io.github.privacystreams.core.Function;
import io.github.privacystreams.core.Item;
import io.github.privacystreams.core.PStreamTransformation;
import io.github.privacystreams.utils.annotations.PSOperatorWrapper;

/**
 * A helper class to access stream-limiting functions
 */
@PSOperatorWrapper
public class Limiters {
    /**
     * Limit the stream with a timeout.
     * The stream will stop after the timeout.
     *
     * @param timeoutMillis the timeout milliseconds.
     * @return the limiter function.
     */
    public static PStreamTransformation timeout(long timeoutMillis) {
        return new TimeoutLimiter(timeoutMillis);
    }

    /**
     * Limit the stream to at most n items.
     * The stream will stop after n items.
     *
     * @param countLimit the maximum number of items.
     * @return the limiter function.
     */
    public static PStreamTransformation limitCount(int countLimit) {
        return new CountLimiter(countLimit);
    }

    /**
     * Limit the stream with a predicate.
     * The stream will stop if the predicate is dissatisfied.
     *
     * @param predicate the predicate to check for each item.
     * @return the limiter function.
     */
    public static PStreamTransformation limit(Function<Item, Boolean> predicate) {
        return new PredicateLimiter(predicate);
    }

}
