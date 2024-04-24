package io.github.privacystreams.ChainStreamClient;

//import static android.os.Build.VERSION_CODES.R;

import android.annotation.SuppressLint;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.ServiceInfo;
import android.os.Build;
import android.os.Bundle;
import android.os.IBinder;
import android.os.Looper;
import android.os.PowerManager;
import android.view.SurfaceView;
import android.view.View;

import androidx.annotation.Nullable;
import androidx.core.app.NotificationCompat;
import androidx.core.app.ServiceCompat;

import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.util.Enumeration;

import io.github.privacystreams.ChainStreamClient.floatingwindow.ServiceFloatingWindow;


public class ChainStreamClientService extends Service {
    private MyWebSocketServer myWebSocketServer;

    private PowerManager.WakeLock wakeLock;

    NotificationCompat.Builder builder;
    NotificationManager manager;

    SurfaceView mPreView;

    @SuppressLint("InvalidWakeLockTag")
    @Override
    public void onCreate() {
        super.onCreate();


        ServiceFloatingWindow.getInstance().init(getApplicationContext());
        mPreView = ServiceFloatingWindow.getInstance().getPreView();
        ServiceFloatingWindow.getInstance().showFloatWindow();

        Intent notificationIntent = new Intent(this, MainActivity.class);
//        Bundle bundle = new Bundle();
//        bundle.putInt(MainActivity.NAV_ID_KEY, R.id.nav_data);
//        notificationIntent.putExtras(bundle);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, notificationIntent, PendingIntent.FLAG_UPDATE_CURRENT);


        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel("ChainStreamClientService", "ChainStreamClientService", NotificationManager.IMPORTANCE_DEFAULT);
            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            if (notificationManager != null) {
                notificationManager.createNotificationChannel(channel);
            }
        }

        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, "ChainStreamClientService")
                .setContentTitle("ChainStream")
                .setContentText("haha")
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentIntent(pendingIntent)
                .setTicker("lala");

        Notification notification =  builder.build();

        startForeground(1, notification);

        PowerManager powerManager = (PowerManager) getSystemService(Context.POWER_SERVICE);
        wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "PStreamCollectService wakelock");
        wakeLock.acquire();


       InetSocketAddress myHost = new InetSocketAddress(getIPAddress(true),6666);
//         InetSocketAddress myHost = new InetSocketAddress("127.0.0.1",6666);

        myWebSocketServer = new MyWebSocketServer(myHost);
        myWebSocketServer.setPreView(mPreView);
        myWebSocketServer.setService(this);
        myWebSocketServer.setContext(this);

    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {

        myWebSocketServer.start();

        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onDestroy() {
        myWebSocketServer.stopServer();
//        myWebSocketServer = null;
        ServiceFloatingWindow.getInstance().remove();
        wakeLock.release();
        super.onDestroy();
    }

    public void start(Context context) {
        Intent serviceIntent = new Intent(context, ChainStreamClientService.class);
        context.startService(serviceIntent);
    }

    public static String getIPAddress(boolean useIPv4) {
        try {
            Enumeration<NetworkInterface> interfaces = NetworkInterface.getNetworkInterfaces();
            while (interfaces.hasMoreElements()) {
                NetworkInterface iface = interfaces.nextElement();
                Enumeration<InetAddress> addresses = iface.getInetAddresses();
                while (addresses.hasMoreElements()) {
                    InetAddress addr = addresses.nextElement();
                    if (!addr.isLoopbackAddress()) {
                        String ip = addr.getHostAddress();
                        // 判断是否使用IPv4
                        boolean isIPv4 = ip.indexOf(':') < 0;
                        if (useIPv4) {
                            if (isIPv4)
                                return ip;
                        } else {
                            if (!isIPv4) {
                                int delim = ip.indexOf('%'); // 去掉IPv6地址后面的zone index
                                return delim < 0 ? ip.toUpperCase() : ip.substring(0, delim).toUpperCase();
                            }
                        }
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "";
    }
}
