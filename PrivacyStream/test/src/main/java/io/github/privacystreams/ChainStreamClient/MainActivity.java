package io.github.privacystreams.ChainStreamClient;

import android.os.AsyncTask;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

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
import java.net.InetSocketAddress;

import io.github.privacystreams.utils.Logging;


public class MainActivity extends AppCompatActivity {
    public Button mButtonStart;

    public Button mButtonStop;
    public LinearLayout logLinearLayout;
    public ScrollView logScrollView;

    public Button mButtonClear;

//    public IConnectionManager mManager;

//    public ConnectionInfo connectionInfo;

    public MyWebSocketServer myWebSocketServer;

    private Boolean is_server_running;

    private TextView mTextImage;

    private TextView mTextAudio;

    private TextView mTextSensors;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mButtonStart = findViewById(R.id.button);
        mButtonStop = findViewById(R.id.button2);
        logLinearLayout  = findViewById(R.id.logLinearLayout);
        logScrollView = findViewById(R.id.logScrollView);
        mButtonClear = findViewById(R.id.button3);

        is_server_running = Boolean.FALSE;

        mTextAudio = findViewById(R.id.textAudio);
        mTextImage = findViewById(R.id.textImage);
        mTextSensors = findViewById(R.id.textSensors);

        mTextAudio.setTextColor(ContextCompat.getColor(this, android.R.color.primary_text_light));
        mTextImage.setTextColor(ContextCompat.getColor(this, android.R.color.primary_text_light));
        mTextSensors.setTextColor(ContextCompat.getColor(this, android.R.color.primary_text_light));


//        connectionInfo = new ConnectionInfo("127.0.0.1", 66677);
//        mManager = OkSocket.open(connectionInfo);
//        mManager.connect();

        mButtonStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
//                new MyAsyncTask().execute();
                if (is_server_running == Boolean.FALSE) {
                    new LogReaderTask(logLinearLayout).executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);

                    InetSocketAddress myHost = new InetSocketAddress("192.168.43.1", 6666);
                    myWebSocketServer = new MyWebSocketServer(myHost);
                    myWebSocketServer.setText(mTextImage, mTextAudio, mTextSensors);
                    myWebSocketServer.setContext(MainActivity.this);
                    myWebSocketServer.start();

                    is_server_running = Boolean.TRUE;
                    Toast.makeText(view.getContext(), "server running!", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(view.getContext(), "server already running!", Toast.LENGTH_SHORT).show();
                }
            }
        });

        mButtonStop.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View view) {
                if (is_server_running) {
                    myWebSocketServer.stopServer();

                    is_server_running = Boolean.FALSE;
                    Toast.makeText(view.getContext(), "server stop!", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(view.getContext(), "server not running!", Toast.LENGTH_SHORT).show();
                }
            }
        });

        mButtonClear.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                logLinearLayout.removeAllViews();
            }
        });
    }

    @Override
    protected void onStop() {
        myWebSocketServer.stopServer();
        super.onStop();
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
                Process clearLog = Runtime.getRuntime().exec("logcat -c");
                clearLog.waitFor(); // 等待清除命令执行完成


                Process process = Runtime.getRuntime().exec("logcat -s PStreamTest:V *:S io.github.privacystreams.test:V PrivacyStreams:V websocket:V");
                BufferedReader bufferedReader = new BufferedReader(
                        new InputStreamReader(process.getInputStream())
                );
                String line;
                while ((line = bufferedReader.readLine()) != null) {
                    publishProgress(line);
                }
            } catch (IOException e) {
                Log.e("LogReaderTask", "Error reading logcat", e);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
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
        myWebSocketServer.stopServer();
        super.onDestroy();
//        mManager.disconnect();
    }
}