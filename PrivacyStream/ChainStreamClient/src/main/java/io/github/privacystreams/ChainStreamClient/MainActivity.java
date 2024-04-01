package io.github.privacystreams.ChainStreamClient;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.os.Handler;
import android.os.Looper;
import android.provider.Settings;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.style.TextAppearanceSpan;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
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

//import io.github.privacystreams.test.R;
import io.github.privacystreams.ChainStreamClient.service.ForegroundService;
import io.github.privacystreams.utils.Logging;


public class MainActivity extends AppCompatActivity {
    public Button mButtonStart;

    public Button mButtonStop;
    public LinearLayout logLinearLayout;
    public ScrollView logScrollView;

    public Button mButtonClear;

    private Boolean is_server_running;

    private LogReaderTask mLogReaderTask;


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

        TextView mTextAudio = findViewById(R.id.textAudio);
        TextView mTextImage = findViewById(R.id.textImage);
        TextView mTextSensors = findViewById(R.id.textSensors);

        mTextAudio.setTextColor(ContextCompat.getColor(this, android.R.color.primary_text_light));
        mTextImage.setTextColor(ContextCompat.getColor(this, android.R.color.primary_text_light));
        mTextSensors.setTextColor(ContextCompat.getColor(this, android.R.color.primary_text_light));

        mLogReaderTask = new LogReaderTask(logLinearLayout, this, logScrollView);

        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        mButtonStart.setOnClickListener(view -> {
            if (is_server_running == Boolean.FALSE) {
                mLogReaderTask.startReadingLogs();

                Intent intent = new Intent(MainActivity.this, ChainStreamClientService.class);
                startService(intent);

                is_server_running = Boolean.TRUE;
                Toast.makeText(view.getContext(), "server running!", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(view.getContext(), "server already running!", Toast.LENGTH_SHORT).show();
            }
        });

        mButtonStop.setOnClickListener(view -> {
            if (is_server_running) {

                Intent intent = new Intent(MainActivity.this, ChainStreamClientService.class);
                stopService(intent);

                is_server_running = Boolean.FALSE;
                Toast.makeText(view.getContext(), "server stop!", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(view.getContext(), "server not running!", Toast.LENGTH_SHORT).show();
            }
        });

        mButtonClear.setOnClickListener(view -> logLinearLayout.removeAllViews());
    }

    @Override
    protected void onStop() {
        Intent intent = new Intent(this, ChainStreamClientService.class);
        stopService(intent);
        super.onStop();
    }

    @Override
    protected void onDestroy() {
        Intent intent = new Intent(this, ChainStreamClientService.class);
        stopService(intent);
        super.onDestroy();
    }
}