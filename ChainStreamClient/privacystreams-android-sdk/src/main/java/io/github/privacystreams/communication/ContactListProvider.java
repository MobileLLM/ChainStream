package io.github.privacystreams.communication;

import android.Manifest;
import android.content.ContentResolver;
import android.database.Cursor;
import android.provider.ContactsContract;
import android.provider.ContactsContract.CommonDataKinds.Email;
import android.provider.ContactsContract.CommonDataKinds.Phone;

import io.github.privacystreams.core.PStreamProvider;
import io.github.privacystreams.utils.CommunicationUtils;

import java.util.ArrayList;
import java.util.List;

/**
 * Provide a stream of contact list.
 */

class ContactListProvider extends PStreamProvider {

    ContactListProvider() {
        this.addRequiredPermissions(Manifest.permission.READ_CONTACTS);
    }

    @Override
    protected void provide() {
        this.getContactList();
    }

    private void getContactList() {
        ContentResolver contentResolver = this.getContext().getContentResolver();

        Cursor contactCur = contentResolver.query(
                ContactsContract.Contacts.CONTENT_URI,
                null,
                null,
                null,
                null
        );

        if (contactCur != null && contactCur.getCount() > 0) {
            contactCur.moveToFirst();
            while (!contactCur.isAfterLast()) {
                String _id = contactCur.getString(contactCur.getColumnIndex(ContactsContract.Data._ID));
                String name = contactCur.getString(contactCur.getColumnIndex(Phone.DISPLAY_NAME));

                List<String> phones = new ArrayList<>();
                Cursor phoneCur = contentResolver.query(
                        Phone.CONTENT_URI,
                        null,
                        Phone.CONTACT_ID + " = " + _id,
                        null,
                        null);
                if (phoneCur != null) {
                    while (phoneCur.moveToNext()) {
                        String number = phoneCur.getString(phoneCur.getColumnIndex(Phone.NUMBER));
                        phones.add(CommunicationUtils.normalizePhoneNumber(number));
//                    int type = phones.getInt(phones.getColumnIndex(Phone.TYPE));
                    }
                    phoneCur.close();
                }

                List<String> emails = new ArrayList<>();
                Cursor emailCur = contentResolver.query(
                        Email.CONTENT_URI,
                        null,
                        Email.CONTACT_ID + " = " + _id,
                        null,
                        null);
                if (emailCur != null) {
                    while (emailCur.moveToNext()) {
                        String email = emailCur.getString(emailCur.getColumnIndex(Email.ADDRESS));
                        emails.add(email);
                    }
                    emailCur.close();
                }

                Contact contact = new Contact(_id, name, phones, emails);
                this.output(contact);

                contactCur.moveToNext();
            }
        }

        if (contactCur != null) {
            contactCur.close();
        }

        this.finish();
    }
}
