package io.github.privacystreams.core.items;

import io.github.privacystreams.core.PStreamProvider;

import java.util.List;

/**
 * A Provider that provides continuous random TestItem updates
 */
class RandomLocalPStreamProvider extends PStreamProvider {
    private final int maxInt;
    private final double maxDouble;
    private final int count;

    RandomLocalPStreamProvider(int maxInt, double maxDouble, int count) {
        this.maxInt = maxInt;
        this.maxDouble = maxDouble;
        this.count = count;
        this.addParameters(maxInt, maxDouble, count);
    }

    @Override
    protected void provide() {
        int id = 0;
        if (!this.isCancelled) {
            List<TestObject> testObjects = TestObject.getRandomList(this.maxInt, maxDouble, count);
            for (TestObject testObject : testObjects) {
                testObject.setId(id);
                id++;
                this.output(new TestItem(testObject));
            }
            this.finish();
        }
    }
}
