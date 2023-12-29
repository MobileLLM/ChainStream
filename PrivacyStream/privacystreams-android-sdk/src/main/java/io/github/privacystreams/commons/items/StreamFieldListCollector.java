package io.github.privacystreams.commons.items;

import io.github.privacystreams.commons.ItemsOperator;
import io.github.privacystreams.core.Item;
import io.github.privacystreams.core.UQI;

import java.util.ArrayList;
import java.util.List;

import static io.github.privacystreams.utils.Assertions.notNull;

/**
 * Select a field of each item in a stream and output to a list
 * Each item in the list is the field value in type TValue.
 */

class StreamFieldListCollector<TValue> extends ItemsOperator<List<TValue>> {
    private final String fieldToSelect;

    StreamFieldListCollector(String fieldToSelect) {
        this.fieldToSelect = notNull("fieldToSelect", fieldToSelect);
        this.addParameters(fieldToSelect);
    }

    @Override
    public List<TValue> apply(UQI uqi, List<Item> items) {
        List<TValue> result = new ArrayList<>();
        for (Item item : items) {
            TValue fieldValue = item.getValueByField(this.fieldToSelect);
            result.add(fieldValue);
        }
        return result;
    }

}
