package io.github.privacystreams.ChainStreamClient;

import android.content.Context;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


public class LogReaderTask {

    private LinearLayout logLinearLayout;
    private Handler handler;

    private Context mContext;

    private ScrollView logScrollView;

    // Constructor to pass reference of logLinearLayout
    LogReaderTask(LinearLayout logLinearLayout, Context context, ScrollView logscrollView) {
        this.logLinearLayout = logLinearLayout;
        this.handler = new Handler(Looper.getMainLooper());
        this.mContext = context;
        this.logScrollView = logscrollView;
    }

    void startReadingLogs() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Process clearLog = Runtime.getRuntime().exec("logcat -b all -c");
                    clearLog.waitFor(); // Wait for the clear command to complete

                    Thread.sleep(1000);

                    Process process = Runtime.getRuntime().exec("logcat -s PStreamTest:V io.github.privacystreams.test:V PrivacyStreams:V ChainStreamClient:V *:S io.github.privacystreams.ChainStreamClient:V websocket:V");
                    BufferedReader bufferedReader = new BufferedReader(
                            new InputStreamReader(process.getInputStream())
                    );

                    String line;
                    while ((line = bufferedReader.readLine()) != null) {
                        final String logLine = line;
                        handler.post(new Runnable() {
                            @Override
                            public void run() {
                                // Update UI on the main thread
                                updateUI(logLine);
                            }
                        });
                    }
                } catch (IOException e) {
                    Log.e("LogReaderTask", "Error reading logcat", e);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        }).start();
    }

    // This method will be called on the main thread to update UI
    private void updateUI(String logLine) {
        // Update UI with the logLine in logLinearLayout
        // For example, you can append the logLine to a TextView in logLinearLayout
        TextView textView = new TextView(mContext);
//                SpannableString spannableString = new SpannableString(values[0]);
//                spannableString.setSpan(new TextAppearanceSpan(null, 0, 18, null, null), 0, spannableString.length(), Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
//                textView.setText(spannableString);

        textView.setText(logLine);
        logLinearLayout.addView(textView);

        logScrollView.post(() -> {
            logScrollView.fullScroll(View.FOCUS_DOWN);
        });
    }
}

