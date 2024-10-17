package io.github.privacystreams.ChainStreamClient;

import android.annotation.SuppressLint;
import android.app.ActivityManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.WifiManager;
import android.os.Build;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.List;

import io.github.privacystreams.ChainStreamClient.utils.SensorUtils;


public class MainActivity extends AppCompatActivity {
    public Button mButtonStart;

    public Button mButtonStop;
    public LinearLayout logLinearLayout;
    public LinearLayout logLinearLayout2;
    public ScrollView logScrollView;
    public ScrollView logScrollView2;

    public Button mButtonClear;

    private Boolean is_server_running;

    private LogReaderTask mLogReaderTask;

    private TextView mIPAddrTextView;

    private BroadcastReceiver receiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String data = intent.getStringExtra("data");
            if (data != null) {
                TextView textView = new TextView(MainActivity.this);

                textView.setText(data);
                textView.setTextColor(ContextCompat.getColor(MainActivity.this, R.color.colorPrimary));
                logLinearLayout2.addView(textView);

                logScrollView2.post(() -> {
                    logScrollView2.fullScroll(View.FOCUS_DOWN);
                });
            }
        }
    };


    @SuppressLint("UnspecifiedRegisterReceiverFlag")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mButtonStart = findViewById(R.id.button);
        mButtonStop = findViewById(R.id.button2);
        logLinearLayout  = findViewById(R.id.logLinearLayout);
        logScrollView = findViewById(R.id.logScrollView);
        logLinearLayout2  = findViewById(R.id.logLinearLayout2);
        logScrollView2 = findViewById(R.id.logScrollView2);
        mButtonClear = findViewById(R.id.button3);

        is_server_running = Boolean.FALSE;

        mLogReaderTask = new LogReaderTask(logLinearLayout, this, logScrollView);

        registerReceiver(receiver, new IntentFilter("ACTION_UPDATE_TEXT"));

        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        mButtonStart.setOnClickListener(view -> {
//            String deviceInfoJson = null;
//            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
//                deviceInfoJson = SensorUtils.getDeviceInfoAsJson(this);
//            }
//            Log.d("DeviceInfo", "Device Info JSON: " + deviceInfoJson);

//            // 检查当前服务是否已经在运行
//            ActivityManager manager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
//            boolean isServiceRunning = false;
//
//            for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
//                if (ChainStreamClientService.class.getName().equals(service.service.getClassName())) {
//                    isServiceRunning = true;
//                    break;
//                }
//            }
//
//            // 如果服务已经在运行，强制停止它
//            if (isServiceRunning) {
//                Intent stopIntent = new Intent(MainActivity.this, ChainStreamClientService.class);
//                stopService(stopIntent);
//                Toast.makeText(view.getContext(), "Detected running service. Stopping it first...", Toast.LENGTH_SHORT).show();
//            }

            if (is_server_running == Boolean.FALSE) {
                mLogReaderTask.startReadingLogs();

                Intent intent = new Intent(MainActivity.this, ChainStreamClientService.class);
                startService(intent);

                mIPAddrTextView = findViewById(R.id.ip_address);

                WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
                int ipAddress = wifiManager.getConnectionInfo().getIpAddress();
                @SuppressLint("DefaultLocale") String ipAddressString = String.format("%d.%d.%d.%d",
                        (ipAddress & 0xff),
                        (ipAddress >> 8 & 0xff),
                        (ipAddress >> 16 & 0xff),
                        (ipAddress >> 24 & 0xff));
                ipAddressString = ipAddressString + ":6666";
                mIPAddrTextView.setText(ipAddressString);

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

                mIPAddrTextView.setText("xxx.xxx.xxx.xxx:xxxx");

                is_server_running = Boolean.FALSE;
                Toast.makeText(view.getContext(), "server stop!", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(view.getContext(), "server not running!", Toast.LENGTH_SHORT).show();
            }
        });

        mButtonClear.setOnClickListener(view -> {
            logLinearLayout.removeAllViews();
            logLinearLayout2.removeAllViews();
        }
        );
    }

    @Override
    protected void onStop() {
//        Intent intent = new Intent(this, ChainStreamClientService.class);
//        stopService(intent);
        super.onStop();
    }

    @Override
    protected void onDestroy() {
//        Intent intent = new Intent(this, ChainStreamClientService.class);
//        stopService(intent);
        super.onDestroy();
        unregisterReceiver(receiver);
    }
}