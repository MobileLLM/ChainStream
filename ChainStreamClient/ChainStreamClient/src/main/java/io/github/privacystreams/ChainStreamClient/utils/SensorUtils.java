package io.github.privacystreams.ChainStreamClient.utils;

import android.content.Context;
import android.graphics.Camera;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraManager;
import android.media.AudioDeviceInfo;
import android.media.AudioManager;
import android.os.Build;
import android.util.Log;

import androidx.annotation.RequiresApi;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

@RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
public class SensorUtils {
    private SensorUtils() {
        // 防止实例化
    }

    public static List<Sensor> getAvailableSensors(Context context) {
        SensorManager sensorManager = (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
        return sensorManager != null ? sensorManager.getSensorList(Sensor.TYPE_ALL) : new ArrayList<>();
    }

    public static String getAvailableSensorStrings(Context context) {
        StringBuilder sb = new StringBuilder();
        for (Sensor sensor : getAvailableSensors(context)) {
            sb.append("Sensor name: ").append(sensor.getName()).append("\n");
            sb.append("Sensor type: ").append(sensor.getType()).append("\n\n");
        }
        return sb.toString();
    }

    public static String getAvailableCameras(Context context) {
        StringBuilder sb = new StringBuilder();

        CameraManager cameraManager = null;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            cameraManager = (CameraManager) context.getSystemService(Context.CAMERA_SERVICE);
        }
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                String[] cameraIds = cameraManager.getCameraIdList();
                int numCameras = cameraIds.length;
                for (String cameraId : cameraIds) {
                    CameraCharacteristics characteristics = cameraManager.getCameraCharacteristics(cameraId);
                    Integer facing = characteristics.get(CameraCharacteristics.LENS_FACING);
                    if (facing != null) {
                        sb.append("Camera id: ").append(cameraId).append("Facing: ").append(facing).append("\n");
                    }
                }
            }
        } catch (CameraAccessException e) {
            throw new RuntimeException(e);
        }
        return sb.toString();
    }

    public static String getMicrophoneList(Context context) {
        StringBuilder sb = new StringBuilder();
        AudioManager audioManager = (AudioManager) context.getSystemService(Context.AUDIO_SERVICE);

        // 获取所有输入设备（包括麦克风）
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            AudioDeviceInfo[] devices = audioManager.getDevices(AudioManager.GET_DEVICES_INPUTS);
            int micCount = 0;
            for (AudioDeviceInfo device : devices) {
                if (device.getType() == AudioDeviceInfo.TYPE_BUILTIN_MIC ||
                        device.getType() == AudioDeviceInfo.TYPE_WIRED_HEADSET ||
                        device.getType() == AudioDeviceInfo.TYPE_USB_DEVICE) {
                    micCount++;
                    sb.append("Microphone type: ").append(device.getType()).append("\n");
                    Log.d("MicrophoneInfo", "Microphone found: " + device.getType());
                }
            }
        }
        return sb.toString();

    }


    public static String getDeviceInfoAsJson(Context context) {
        JSONObject deviceInfoJson = new JSONObject();

        try {
            // 添加摄像头信息
            JSONArray cameraArray = getCameraInfo(context);
            deviceInfoJson.put("cameras", cameraArray);

            // 添加麦克风信息
            JSONArray microphoneArray = getMicrophoneInfo(context);
            deviceInfoJson.put("microphones", microphoneArray);

            // 添加传感器信息
            JSONArray sensorArray = getSensorInfo(context);
            deviceInfoJson.put("sensors", sensorArray);

        } catch (JSONException e) {
            Log.e("DeviceInfoJson", "Error creating JSON: " + e.getMessage());
        }

        return deviceInfoJson.toString();
    }

    // 获取摄像头信息
    private static JSONArray getCameraInfo(Context context) {
        JSONArray cameraArray = new JSONArray();
        CameraManager cameraManager = (CameraManager) context.getSystemService(Context.CAMERA_SERVICE);

        try {
            String[] cameraIdList = cameraManager.getCameraIdList();
            for (String cameraId : cameraIdList) {
                CameraCharacteristics characteristics = cameraManager.getCameraCharacteristics(cameraId);
                JSONObject cameraJson = new JSONObject();

                Integer lensFacing = characteristics.get(CameraCharacteristics.LENS_FACING);
                String facing = "unknown";
                if (lensFacing != null) {
                    if (lensFacing == CameraCharacteristics.LENS_FACING_FRONT) {
                        facing = "front";
                    } else if (lensFacing == CameraCharacteristics.LENS_FACING_BACK) {
                        facing = "back";
                    }
                }

                cameraJson.put("camera_id", cameraId);
                cameraJson.put("facing", facing);

                cameraArray.put(cameraJson);
            }
        } catch (CameraAccessException | JSONException e) {
            Log.e("CameraInfo", "Error accessing camera: " + e.getMessage());
        }

        return cameraArray;
    }

    // 获取麦克风信息
    private static JSONArray getMicrophoneInfo(Context context) {
        JSONArray microphoneArray = new JSONArray();
        AudioManager audioManager = (AudioManager) context.getSystemService(Context.AUDIO_SERVICE);
        AudioDeviceInfo[] devices = audioManager.getDevices(AudioManager.GET_DEVICES_INPUTS);

        try {
            for (AudioDeviceInfo device : devices) {
                if (device.getType() == AudioDeviceInfo.TYPE_BUILTIN_MIC ||
                        device.getType() == AudioDeviceInfo.TYPE_WIRED_HEADSET ||
                        device.getType() == AudioDeviceInfo.TYPE_USB_DEVICE) {

                    JSONObject micJson = new JSONObject();
                    micJson.put("device_type", device.getType());
                    micJson.put("device_name", device.getProductName());

                    microphoneArray.put(micJson);
                }
            }
        } catch (JSONException e) {
            Log.e("MicrophoneInfo", "Error creating microphone JSON: " + e.getMessage());
        }

        return microphoneArray;
    }

    // 获取传感器信息
    private static JSONArray getSensorInfo(Context context) {
        JSONArray sensorArray = new JSONArray();
        SensorManager sensorManager = (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
        List<Sensor> sensorList = sensorManager.getSensorList(Sensor.TYPE_ALL);

        try {
            for (Sensor sensor : sensorList) {
                JSONObject sensorJson = new JSONObject();
                sensorJson.put("sensor_name", sensor.getName());
                sensorJson.put("sensor_type", sensor.getType());
                sensorJson.put("vendor", sensor.getVendor());
                sensorJson.put("version", sensor.getVersion());

                sensorArray.put(sensorJson);
            }
        } catch (JSONException e) {
            Log.e("SensorInfo", "Error creating sensor JSON: " + e.getMessage());
        }

        return sensorArray;
    }
}
