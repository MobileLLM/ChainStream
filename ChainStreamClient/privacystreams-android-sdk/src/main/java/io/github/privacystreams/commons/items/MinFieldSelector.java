package io.github.privacystreams.commons.items;

import io.github.privacystreams.core.Item;

import java.util.List;


/**
 * select an item from the stream that has the min value of a field.
 * return null if fails to find an item
 */

class MinFieldSelector extends ByFieldItemSelector {
    MinFieldSelector(String numField) {
        super(numField);
    }

    @Override
    protected Item selectFrom(List<Item> items) {
        Double selectedFieldValue = null;
        Item selectedItem = null;

        for (Item item : items) {
            Number curField = item.getValueByField(this.field);
            double curFieldValue = curField.doubleValue();

            if (selectedItem == null) {
                selectedItem = item;
                selectedFieldValue = curFieldValue;
            }
            else if (curFieldValue < selectedFieldValue) {
                selectedItem = item;
                selectedFieldValue = curFieldValue;
            }
        }

        return selectedItem;
    }
}
