package io.github.privacystreams.test;

import android.os.AsyncTask;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Handler;
import android.os.Looper;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.style.TextAppearanceSpan;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import com.xuhao.didi.socket.client.sdk.OkSocket;
import com.xuhao.didi.socket.client.sdk.client.ConnectionInfo;
import com.xuhao.didi.socket.client.sdk.client.OkSocketOptions;
import com.xuhao.didi.socket.client.sdk.client.action.SocketActionAdapter;
import com.xuhao.didi.socket.client.sdk.client.connection.IConnectionManager;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


public class MainActivity extends AppCompatActivity {
    public Button mButton;
    public LinearLayout logLinearLayout;
    public ScrollView logScrollView;

    public IConnectionManager mManager;

    public ConnectionInfo connectionInfo;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mButton = findViewById(R.id.button);
        logLinearLayout  = findViewById(R.id.logLinearLayout);
        logScrollView = findViewById(R.id.logScrollView);

        connectionInfo = new ConnectionInfo("127.0.0.1", 66677);
        mManager = OkSocket.open(connectionInfo);
        mManager.connect();

        mButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new MyAsyncTask().execute();
            }
        });

        LogReaderTask logReaderTask = new LogReaderTask(logLinearLayout);
        logReaderTask.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
    }

    private class LogReaderTask extends AsyncTask<Void, String, Void> {

        private LinearLayout logLinearLayout;
        private Handler handler;

        // Constructor to pass reference of logLinearLayout
        LogReaderTask(LinearLayout logLinearLayout) {
            this.logLinearLayout = logLinearLayout;
            this.handler = new Handler(Looper.getMainLooper());
        }
        @Override
        protected Void doInBackground(Void... voids) {
            try {
                Process process = Runtime.getRuntime().exec("logcat -s PStreamTest:V *:S io.github.privacystreams.test:V PrivacyStreams:V");
                BufferedReader bufferedReader = new BufferedReader(
                        new InputStreamReader(process.getInputStream())
                );
                String line;
                while ((line = bufferedReader.readLine()) != null) {
                    publishProgress(line);
                }
            } catch (IOException e) {
                Log.e("LogReaderTask", "Error reading logcat", e);
            }
            return null;
        }

        @Override
        protected void onProgressUpdate(String... values) {
            handler.post(() -> {
                TextView textView = new TextView(MainActivity.this);
//                SpannableString spannableString = new SpannableString(values[0]);
//                spannableString.setSpan(new TextAppearanceSpan(null, 0, 18, null, null), 0, spannableString.length(), Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
//                textView.setText(spannableString);

                textView.setText(values[0]);
                logLinearLayout.addView(textView);

                logScrollView.post(() -> {
                    logScrollView.fullScroll(View.FOCUS_DOWN);
                });
            });

        }
    }

    private class MyAsyncTask extends AsyncTask<Object, Object, Object> {
        @Override
        protected Object doInBackground(Object[] objects) {
            TestCases testCases = new TestCases(MainActivity.this);

            testCases.testTakePhotoBg();
//            testCases.testMerge();
//            testCases.testAccEvents();
//            testCases.testCurrentLocation();
//            testCases.testTextEntry();
//            testCases.testNotification();
//            testCases.testAudio();
//            testCases.testMockData();
//            testCases.testContacts();
//            testCases.testDeviceState();
//
//            testCases.testBrowserSearchUpdates();
//            testCases.testBrowserHistoryUpdates();
//
//            testCases.testAccEvents();
//
//            testCases.testIMUpdates();
 //           testCases.testEmailUpdates();
//            testCases.testEmailList();

            return null;
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mManager.disconnect();
    }
}