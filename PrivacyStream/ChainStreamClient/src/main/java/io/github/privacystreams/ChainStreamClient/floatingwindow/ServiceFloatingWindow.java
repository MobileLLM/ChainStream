package io.github.privacystreams.ChainStreamClient.floatingwindow;

import android.content.Context;
import android.content.Intent;
import android.graphics.PixelFormat;
import android.hardware.Camera;
import android.os.Build;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.view.WindowManager;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;

import java.io.IOException;

import io.github.privacystreams.ChainStreamClient.ChainStreamClientService;
import io.github.privacystreams.ChainStreamClient.R;


public class ServiceFloatingWindow {

    private Context mContext;
    private WindowManager.LayoutParams mWindowParams;
    private WindowManager mWindowManager;

    private View rootLayout;

//    private TextView infoTxtV;
    private View hideBtn;
    private View lineView;
    private View contentView;

    private boolean isInit = false;

    private int show_width = 300;
    private int hight = 600;

    private int hidden_width = 10;


    public static ServiceFloatingWindow getInstance(){
        return SingletonHolder.INSTANCE;
    }

    private ServiceFloatingWindow() {

    }

    public void init(Context context) {
        if (isInit){
            return;
        }
        this.mContext = context;
        initFloatWindow();
        isInit = true;
    }

    public SurfaceView getPreView() {
        return rootLayout.findViewById(R.id.surfaceView);
    }

    private void initFloatWindow() {

        rootLayout = LayoutInflater.from(mContext).
                inflate(R.layout.floatingwidow_in_service, null);
//        infoTxtV = rootLayout.findViewById(R.id.fw_in_service_info);
        hideBtn = rootLayout.findViewById(R.id.fw_in_service_hide);
        lineView = rootLayout.findViewById(R.id.fw_in_line_view);
        contentView = rootLayout.findViewById(R.id.fw_in_show_content);

        hideBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(mContext,"隐藏了",Toast.LENGTH_SHORT).show();
                contentView.setVisibility(View.GONE);
                mWindowParams.width = hidden_width;
                mWindowManager.updateViewLayout(rootLayout,mWindowParams);
                lineView.setVisibility(View.VISIBLE);
            }
        });
        lineView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                contentView.setVisibility(View.VISIBLE);
                lineView.setVisibility(View.GONE);
                mWindowParams.width = show_width;
                mWindowManager.updateViewLayout(rootLayout,mWindowParams);
            }
        });

        mWindowParams = new WindowManager.LayoutParams();
        mWindowManager = (WindowManager) mContext.getSystemService(Context.WINDOW_SERVICE);
        if (Build.VERSION.SDK_INT >= 26) {
            //8.0新特性
            mWindowParams.type = WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY;
        }else{
            mWindowParams.type = WindowManager.LayoutParams.TYPE_SYSTEM_ALERT;
        }

        mWindowParams.format = PixelFormat.RGBA_8888;
        mWindowParams.flags = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE;
        mWindowParams.gravity = Gravity.TOP | Gravity.LEFT;
        mWindowParams.width =  hidden_width;
        mWindowParams.height = hight;
    }


    public void remove(){
//        Intent intent = new Intent(mContext, ChainStreamClientService.class);
//        mContext.stopService(intent);
        if (isInit){
            mWindowManager.removeView(rootLayout);
        }
    }

    public void showFloatWindow(){
        if (!isInit){
            return;
        }
        if (rootLayout.getParent() == null){
            // 默认固定位置，靠屏幕右边缘的中间
            DisplayMetrics metrics = new DisplayMetrics();
            // 默认固定位置，靠屏幕右边缘的中间
            mWindowManager.getDefaultDisplay().getMetrics(metrics);
//            mWindowParams.x = metrics.widthPixels;
            mWindowParams.x = 0;
            mWindowParams.y = metrics.heightPixels/2-150;
            mWindowManager.addView(rootLayout, mWindowParams);
        }

//        Camera mCamera = Camera.open(0);
//        SurfaceView haha = rootLayout.findViewById(R.id.surfaceView);
//        SurfaceHolder surfaceHolder = haha.getHolder();
//        surfaceHolder.addCallback(new SurfaceHolder.Callback() {
//            @Override
//            public void surfaceCreated(@NonNull SurfaceHolder surfaceHolder) {
//                try {
//                    mCamera.setPreviewDisplay(surfaceHolder);
//                    mCamera.startPreview();
//                } catch (IOException e) {
//                    Log.d("main", "Error setting camera preview: " + e.getMessage());
//                }
//            }
//
//            @Override
//            public void surfaceChanged(@NonNull SurfaceHolder surfaceHolder, int i, int i1, int i2) {
//                try {
//                    mCamera.setPreviewDisplay(surfaceHolder);
//                    mCamera.startPreview();
//                } catch (IOException e) {
//                    Log.d("main", "Error setting camera preview: " + e.getMessage());
//                }
//            }
//
//            @Override
//            public void surfaceDestroyed(@NonNull SurfaceHolder surfaceHolder) {
//                try {
//                    mCamera.setPreviewDisplay(surfaceHolder);
//                    mCamera.startPreview();
//                } catch (IOException e) {
//                    Log.d("main", "Error setting camera preview: " + e.getMessage());
//                }
//            }
//
//        });




//        Intent intent = new Intent(mContext, ChainStreamClientService.class);
//        mContext.startService(intent);
    }

//    public void updateText(final String s) {
//        infoTxtV.setText(s);
//    }


    private static class SingletonHolder{
        private static final ServiceFloatingWindow INSTANCE
                = new ServiceFloatingWindow();
    }

}
