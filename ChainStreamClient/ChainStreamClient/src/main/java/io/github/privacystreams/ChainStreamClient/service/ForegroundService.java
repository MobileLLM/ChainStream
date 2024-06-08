package io.github.privacystreams.ChainStreamClient.service;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Binder;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.util.Log;
import android.view.SurfaceView;
import android.view.View;

import androidx.annotation.Nullable;
import androidx.core.app.NotificationCompat;

import io.github.privacystreams.ChainStreamClient.R;
import io.github.privacystreams.ChainStreamClient.floatingwindow.ServiceFloatingWindow;
import io.github.privacystreams.image.PSCameraBgService;


public class ForegroundService extends Service {


    private final String TAG = "ForegroundService";

    NotificationCompat.Builder builder;
    NotificationManager manager;

    View mPreView;
    @Override
    public void onCreate() {
        super.onCreate();
        Log.i(TAG,"onCreate");

        manager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);

        String CHANNEL_ID = "my_channel_01";
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O){        //Android 8.0适配
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID,
                    "Channel human readable title",
                    NotificationManager.IMPORTANCE_DEFAULT);//如果这里用IMPORTANCE_NOENE就需要在系统的设置里面开启渠道， //通知才能正常弹出
            manager.createNotificationChannel(channel);
        }
        builder = new NotificationCompat.Builder(this,String.valueOf(CHANNEL_ID));

        builder.setContentTitle("前台服务")            //指定通知栏的标题内容
                .setContentText("前台服务正在运行")             //通知的正文内容
                .setWhen(System.currentTimeMillis())                //通知创建的时间
                .setSmallIcon(R.mipmap.ic_launcher);    //通知显示的小图标，只能用alpha图层的图片进行设置

        Notification notification = builder.build() ;
        startForeground(2, notification);

        ServiceFloatingWindow.getInstance().init(getApplicationContext());
        mPreView = ServiceFloatingWindow.getInstance().getPreView();
        ServiceFloatingWindow.getInstance().showFloatWindow();
//        ServiceConnection serviceConnection = new ServiceConnection() {
//            @Override
//            public void onServiceConnected(ComponentName componentName, IBinder iBinder) {
//                PSCameraBgService.PreviewBinder previewBinder = (PSCameraBgService.PreviewBinder) iBinder;
//                PSCameraBgService psCameraBgService = previewBinder.getService();
//                psCameraBgService.setPreview(mPreView);
//            }
//
//            @Override
//            public void onServiceDisconnected(ComponentName componentName) {
//
//            }
//        };
//
//        Intent intent = new Intent(this, PSCameraBgService.class);
//        bindService(intent, serviceConnection, BIND_EXTERNAL_SERVICE);
//
    }


    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        ServiceFloatingWindow.getInstance().remove();
        Log.i(TAG,"onDestroy");
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

//    public class PreviewBinder extends Binder {
//        public ForegroundService getService() {
//            return ForegroundService.this;
//        }
//    }

}
