package io.github.privacystreams.image;

import io.github.privacystreams.core.R;

import android.annotation.SuppressLint;
import android.app.Service;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.graphics.PixelFormat;
import android.hardware.Camera;
import android.os.Binder;
import android.os.Build;
import android.os.IBinder;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

import io.github.privacystreams.utils.Globals;

/**
 * A background service for taking pictures.
 */
public class PSCameraBgService extends Service {

    private static final String TAG = "PSCameraBgService";

    private WindowManager mWindowManager;

    private static SurfaceView cameraPreview;
    private HiddenCameraPreview mPreview;
    private Camera mCamera;
    private Timer mTimer;

    private static final String CAMERA_ID = "cameraId";

    private static Callback mCallback;

    private static int tmp_cameraId;

    public abstract static class Callback {
        abstract void onImageTaken(byte[] imageBytes);
        abstract void onFail(boolean isFatal, String errorMessage);
    }

    public static void takePhoto(Context ctx, int cameraId, Callback callback, SurfaceView view) {
        cameraPreview = view;
        if (mCallback != null) {
            callback.onFail(true, "camera service is busy.");
            return;
        }
        mCallback = callback;

        Intent intent = new Intent(ctx, PSCameraBgService.class);
        intent.putExtra(CAMERA_ID, cameraId);
        ctx.startService(intent);

        tmp_cameraId = cameraId;
    }

    public static void stopTakingPhoto(Context ctx, Callback callback) {
        if (mCallback == callback) mCallback = null;
        Intent intent = new Intent(ctx, PSCameraBgService.class);
        ctx.stopService(intent);
    }

    private Camera.PictureCallback mPictureCallback = new Camera.PictureCallback() {
        @Override
        public void onPictureTaken(byte[] data, Camera camera) {
//            Log.d(TAG, "picture taken " + data.length);
            if (mCallback != null) {
                // TODO: fix it
//                byte[] rotatedData = rotateImage(data, camera);
                mCallback.onImageTaken(data);
            } else {
                stopSelf();
            }
        }
    };

    private byte[] rotateImage(byte[] data, Camera camera) {
        int rotation;
        if (camera != null) {
            Camera.CameraInfo info = new Camera.CameraInfo();
            Camera.getCameraInfo(tmp_cameraId, info);
            rotation = info.orientation;
        } else {
            rotation = 0;
        }

        if (rotation != 0) {
            try {
                // Decode the byte array to get the bitmap
                Bitmap bitmap = BitmapFactory.decodeByteArray(data, 0, data.length);

                // Rotate the bitmap
                Matrix matrix = new Matrix();
                matrix.postRotate(rotation);
                bitmap = Bitmap.createBitmap(bitmap);

                // Convert the bitmap back to a byte array
                ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, outputStream);
                return outputStream.toByteArray();
            } catch (Exception e) {
                e.printStackTrace();
                return data; // Return the original data in case of an error
            }
        }
        return data; // Return the original data if no rotation is needed
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @SuppressLint("InflateParams")
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        int cameraId = intent.getIntExtra(CAMERA_ID, 0);

        mWindowManager = (WindowManager) this.getSystemService(Context.WINDOW_SERVICE);
        mCamera = getCameraInstance(cameraId);
        mTimer = new Timer();

        if (mWindowManager != null && mCamera != null) {
            // set picture size
            Camera.Parameters parameters = mCamera.getParameters();
            List<Camera.Size> supportedSizes = parameters.getSupportedPictureSizes();
            Collections.sort(supportedSizes, new Comparator<Camera.Size>() {
                @Override
                public int compare(Camera.Size o1, Camera.Size o2) {
                    return o1.width * o2.height - o2.width * o2.height;
                }
            });
            if (supportedSizes.size() > 1) {
                Camera.Size selectedSize = supportedSizes.get(0);
                if (Globals.ImageConfig.bgImageSizeLevel == 2) {
                    selectedSize = supportedSizes.get(supportedSizes.size() - 1);
                } else if (Globals.ImageConfig.bgImageSizeLevel == 1) {
                    selectedSize = supportedSizes.get(supportedSizes.size() / 2);
                }
                parameters.setPictureSize(selectedSize.width, selectedSize.height);
                mCamera.setParameters(parameters);
            }

            // create fake preview
//            mPreview = new HiddenCameraPreview(this, mCamera);
//            mPreview.setLayoutParams(new ViewGroup.LayoutParams(
//                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
//            camera_preview = LayoutInflater.from(getApplicationContext()).
//                    inflate(R.layout.camera_preview, null);
//            SurfaceView cameraPreview = camera_preview.findViewById(R.id.surfaceView);



//            WindowManager.LayoutParams params = new WindowManager.LayoutParams(500, 500,
//                    Build.VERSION.SDK_INT < Build.VERSION_CODES.O ?
//                            WindowManager.LayoutParams.TYPE_SYSTEM_OVERLAY :
//                            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
//                    WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH,
//                    PixelFormat.TRANSLUCENT);
//            mWindowManager.addView(camera_preview, params);

            SurfaceHolder surfaceHolder = cameraPreview.getHolder();
            try {
                mCamera.setPreviewDisplay(surfaceHolder);
                mCamera.startPreview();
            } catch (IOException e) {
                Log.d(TAG, "Error setting camera preview: " + e.getMessage());
            }
//            surfaceHolder.addCallback(new SurfaceHolder.Callback() {
//                @Override
//                public void surfaceCreated(@NonNull SurfaceHolder holder) {
//                    try {
//                        mCamera.setPreviewDisplay(holder);
//                        mCamera.startPreview();
//                    } catch (IOException e) {
//                        Log.d(TAG, "Error setting camera preview: " + e.getMessage());
//                    }
//                }
//
//                @Override
//                public void surfaceChanged(@NonNull SurfaceHolder surfaceHolder, int i, int i1, int i2) {
//
//                }
//
//                @Override
//                public void surfaceDestroyed(@NonNull SurfaceHolder surfaceHolder) {
//
//                }
//
//            });

            // take photo
            TimerTask takePhotoTask = new TimerTask() {
                @Override
                public void run() {
                    try {
                        mCamera.autoFocus(new Camera.AutoFocusCallback() {
                            @Override
                            public void onAutoFocus(boolean b, Camera camera) {
                                camera.takePicture(null, null, mPictureCallback);
                            }
                        });
//                        mCamera.takePicture(null, null, mPictureCallback);
                    } catch (RuntimeException e) {
                        e.printStackTrace();
                        mCallback.onFail(false, e.getMessage());
                    }
                }
            };
            mTimer.schedule(takePhotoTask, Globals.ImageConfig.bgCameraDelay);
        } else {
            if (mCallback != null) {
                mCallback.onFail(true, "unable to open camera.");
            }
            stopSelf();
        }
        return START_NOT_STICKY;
    }

    public void onDestroy() {
        if (mTimer != null) {
            mTimer.cancel();
        }
        if (mCamera != null) {
            mCamera.stopPreview();
            mCamera.release();
            mCamera = null;
        }
        if (mWindowManager != null) {
//            mWindowManager.removeView(mPreview);
//            mWindowManager.removeView(camera_preview);
        }
    }

    /** A safe way to get an instance of the Camera object. */
    public static Camera getCameraInstance(int id){
        Camera c = null;
        try {
            c = Camera.open(id); // attempt to get a Camera instance
        }
        catch (Exception e){
            // Camera is not available (in use or does not exist)
            Log.e(TAG, e.getMessage());
        }
        return c; // returns null if camera is unavailable
    }


//    public class PreviewBinder extends Binder {
//        public PSCameraBgService getService() {
//            return PSCameraBgService.this;
//        }
//    }
}
