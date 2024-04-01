package io.github.privacystreams.ChainStreamClient;

import android.content.Context;
import android.graphics.Color;
import android.provider.MediaStore;
import android.util.Log;
import android.view.SurfaceView;
import android.view.View;
import android.widget.TextView;

import androidx.core.content.ContextCompat;

import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.charset.Charset;
import java.nio.charset.CharsetDecoder;

import io.github.privacystreams.audio.AudioOperators;
import io.github.privacystreams.core.Callback;
import io.github.privacystreams.core.Item;
import io.github.privacystreams.core.UQI;
import io.github.privacystreams.core.purposes.Purpose;
import io.github.privacystreams.device.DeviceEvent;
import io.github.privacystreams.device.DeviceState;
import io.github.privacystreams.image.Image;
import io.github.privacystreams.image.ImageOperators;
import io.github.privacystreams.location.Geolocation;
import io.github.privacystreams.sensor.Acceleration;
import io.github.privacystreams.sensor.AirPressure;
import io.github.privacystreams.sensor.AmbientTemperature;
import io.github.privacystreams.sensor.Gravity;
import io.github.privacystreams.sensor.Gyroscope;
import io.github.privacystreams.sensor.Light;
import io.github.privacystreams.sensor.LinearAcceleration;
import io.github.privacystreams.sensor.RelativeHumidity;
import io.github.privacystreams.sensor.RotationVector;
import io.github.privacystreams.sensor.StepCounter;
import io.github.privacystreams.utils.Logging;
import io.github.privacystreams.audio.Audio;

public class MyWebSocketServer extends WebSocketServer {
    private Context myContext;

    private SurfaceView preView;

    MyWebSocketServer(InetSocketAddress host){
        super(host);
    }

    public void setPreView(SurfaceView view) {
        preView = view;
    }

    public void setText(TextView textImage, TextView textAudio, TextView textSensors) {
    }

    public void setContext(Context context) {
        myContext = context;
    }

    @Override
    public void onOpen(WebSocket conn, ClientHandshake handshake) {
        Log.d("websocket", "onOpen()一个客户端连接成功："+conn.getRemoteSocketAddress());
    }
    @Override
    public void onClose(WebSocket conn, int code, String reason, boolean remote) {
        Log.d("websocket", "onClose()服务器关闭");
    }
    @Override
    public void onMessage(WebSocket conn, String message) {
        // 这里在网页测试端发过来的是文本数据 测试网页 http://www.websocket-test.com/
        // 需要保证android 和 加载网页的设备(我这边是电脑) 在同一个网段内，连同一个wifi即可
        Log.d("websocket", "onMessage()PC端来的命令->"+message);
        String[] parts = message.split(",");

        // parts数组中包含切分后的子串
        String cmd = parts[0];
        switch (cmd) {
            case "video": {
                String para = parts[1];
                UQI uqi = new UQI(myContext);
                Logging.debug("begin video socket");
                uqi.getData(Image.takePhotoBgPeriodic(0, Integer.parseInt(para), preView), Purpose.UTILITY("taking picture."))
                        .setField("imagePath", ImageOperators.getFilepath(Image.IMAGE_DATA))
                        .forEach("imagePath", new Callback<String>() {
                            @Override
                            protected void onInput(String imagePath) {
                                System.out.println("Send " + imagePath + "through socket");
                                File imageFile = new File(imagePath);

                                try {
                                    // 读取图像文件
                                    FileInputStream fis = new FileInputStream(imageFile);
                                    ByteArrayOutputStream bos = new ByteArrayOutputStream();

                                    byte[] buffer = new byte[1024];
                                    int bytesRead;

                                    while ((bytesRead = fis.read(buffer)) != -1) {
                                        bos.write(buffer, 0, bytesRead);
                                    }

                                    fis.close();
                                    bos.close();

                                    // 获取图像数据的字节数组
                                    byte[] imageData = bos.toByteArray();

                                    // 将字节数组转换为ByteBuffer
                                    ByteBuffer byteBuffer = ByteBuffer.wrap(imageData);

                                    if (conn.isClosed()) {
                                        uqi.stopAll();
                                    }
                                    conn.send(byteBuffer);
                                    Logging.debug("send pic" + byteBuffer.capacity());

                                    boolean isDeleted = imageFile.delete();

                                    if (!isDeleted) {
                                        System.out.println("图片文件删除失败");
                                    }

                                } catch (Exception e) {
                                    e.printStackTrace();
                                }
                            }
                        });
                break;
            }
            case "audio": {
                String duration = parts[1];
                String interval = parts[2];
                UQI uqi = new UQI(myContext);
                Logging.debug("begin audio socket");
                uqi.getData(Audio.recordPeriodic(Integer.parseInt(duration), Integer.parseInt(interval)), Purpose.UTILITY("recording audio"))
                        .setField("audioPath", AudioOperators.getFilepath(Audio.AUDIO_DATA))
                        .forEach("audioPath", new Callback<String>() {
                            @Override
                            protected void onInput(String audioPath) {
                                System.out.println("Send " + audioPath + " through socket");
                                File audioFile = new File(audioPath);

                                try {
                                    FileInputStream fis = new FileInputStream(audioFile);
                                    ByteArrayOutputStream bos = new ByteArrayOutputStream();

                                    byte[] buffer = new byte[1024];
                                    int bytesRead;

                                    while ((bytesRead = fis.read(buffer)) != -1) {
                                        bos.write(buffer, 0, bytesRead);
                                    }

                                    fis.close();
                                    bos.close();

                                    byte[] audioData = bos.toByteArray();
                                    ByteBuffer byteBuffer = ByteBuffer.wrap(audioData);

                                    if (conn.isClosed()) {
                                        uqi.stopAll();
                                    }
                                    conn.send(byteBuffer);
                                    Logging.debug("send audio" + byteBuffer.capacity());

                                    boolean isDeleted = audioFile.delete();

                                    if (!isDeleted) {
                                        System.out.println("音频文件删除失败");
                                    }
                                } catch (Exception e) {
                                    e.printStackTrace();
                                }
                            }
                        });
                break;
            }
            case "sensors": {
                String sensorsName = parts[1];
                UQI uqi = new UQI(myContext);
                Logging.debug("begin sensor socket");
                switch (sensorsName) {
                    case "acceleration":
                        uqi.getData(Acceleration.asUpdates(2), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String acc_x = Float.toString(input.getAsFloat("x"));
                                        String acc_y = Float.toString(input.getAsFloat("y"));
                                        String acc_z = Float.toString(input.getAsFloat("z"));
                                        String acc_res = acc_x + "," + acc_y + "," + acc_z;
                                        System.out.println("Send acceleration data: " + acc_res);

                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
                                            conn.send(acc_res);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                    case "airpressure":
                        uqi.getData(AirPressure.asUpdates(3), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String pressure = Float.toString(input.getAsFloat("pressure"));
                                        System.out.println("Send airpressure data: " + pressure);
                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
                                            conn.send(pressure);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                    case "ambienttemperature":
                        uqi.getData(AmbientTemperature.asUpdates(3), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String temperature = Float.toString(input.getAsFloat("temperature"));
                                        System.out.println("Send ambienttemperature data: " + temperature);
                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
                                            conn.send(temperature);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                    case "deviceevent":
                        uqi.getData(DeviceEvent.asUpdates(), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String type = Float.toString(input.getAsFloat("type"));
                                        String event = Float.toString(input.getAsFloat("event"));
                                        String input_res = type + "," + event;
                                        System.out.println("Send deviceevent data: " + input_res);
                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
                                            conn.send(input_res);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
//            else if (sensorsName.equals("devicestate")) {
//                String devicestate_interval = parts[2];
//                uqi.getData(DeviceState.asUpdates(Integer.parseInt(devicestate_interval), 31 - DeviceState.Masks.BLUETOOTH_DEVICE_LIST), Purpose.UTILITY("chainstream"))
//                        .forEach(new Callback<Item>() {
//                            @Override
//                            protected void onInput(Item input) {
////                                String bt_device_list = Float.toString(input.getAsFloat("bt_device_list"));
//                                String wifi_ap_list = Float.toString(input.getAsFloat("wifi_ap_list"));
//                                String battery_level = Float.toString(input.getAsFloat("battery_level"));
//                                String is_connected = Float.toString(input.getAsFloat("is_connected"));
//                                String wifi_bssid = Float.toString(input.getAsFloat("wifi_bssid"));
//                                String is_screen_on = Float.toString(input.getAsFloat("is_screen_on"));
//                                String input_res =  wifi_ap_list + "," + battery_level + "," +
//                                        is_connected + "," + wifi_bssid + "," + is_screen_on;
//                                System.out.println("Send airpressure data: " + input_res);
//                                try {
//                                    if (conn.isClosed()) {
//                                        uqi.stopAll();
//                                    }
////                                    byte[] imageData = acc_res.getBytes();
////                                    ByteBuffer byteBuffer = ByteBuffer.wrap(imageData);
//                                    conn.send(input_res);
//                                } catch (Exception e) {
//                                    e.printStackTrace();
//                                }
//                            }
//                        });
//            }
                    case "geolocation":
                        String interval = parts[2];
                        uqi.getData(Geolocation.asUpdates(Integer.parseInt(interval), Geolocation.LEVEL_EXACT), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String speed = Float.toString(input.getAsFloat("speed"));
                                        String provider = Float.toString(input.getAsFloat("provider"));
                                        String lat_lon = input.getValueByField("lat_lon").toString();
                                        String accuracy = Float.toString(input.getAsFloat("accuracy"));
                                        String bearing = Float.toString(input.getAsFloat("bearing"));
                                        String input_res = lat_lon + "," + speed + "," + provider + "," + accuracy +
                                                "," + bearing;
                                        System.out.println("Send geolocation data: " + input_res);
                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
//                                    byte[] imageData = acc_res.getBytes();
//                                    ByteBuffer byteBuffer = ByteBuffer.wrap(imageData);
                                            conn.send(input_res);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                    case "gravity":
                        uqi.getData(Gravity.asUpdates(3), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String acc_x = Float.toString(input.getAsFloat("x"));
                                        String acc_y = Float.toString(input.getAsFloat("y"));
                                        String acc_z = Float.toString(input.getAsFloat("z"));
                                        String acc_res = acc_x + "," + acc_y + "," + acc_z;
                                        System.out.println("Send gravity data: " + acc_res);

                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
//                                    byte[] imageData = acc_res.getBytes();
//                                    ByteBuffer byteBuffer = ByteBuffer.wrap(imageData);
                                            conn.send(acc_res);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                    case "gyroscope":
                        uqi.getData(Gyroscope.asUpdates(3), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String acc_x = Float.toString(input.getAsFloat("x"));
                                        String acc_y = Float.toString(input.getAsFloat("y"));
                                        String acc_z = Float.toString(input.getAsFloat("z"));
                                        String acc_res = acc_x + "," + acc_y + "," + acc_z;
                                        System.out.println("Send gyroscope data: " + acc_res);

                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
//                                    byte[] imageData = acc_res.getBytes();
//                                    ByteBuffer byteBuffer = ByteBuffer.wrap(imageData);
                                            conn.send(acc_res);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                    case "light":
                        uqi.getData(Light.asUpdates(3), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String illuminance = Float.toString(input.getAsFloat("illuminance"));
                                        String acc_res = illuminance;
                                        System.out.println("Send light data: " + acc_res);

                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
//                                    byte[] imageData = acc_res.getBytes();
//                                    ByteBuffer byteBuffer = ByteBuffer.wrap(imageData);
                                            conn.send(acc_res);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                    case "linearacceleration":
                        uqi.getData(LinearAcceleration.asUpdates(3), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String acc_x = Float.toString(input.getAsFloat("x"));
                                        String acc_y = Float.toString(input.getAsFloat("y"));
                                        String acc_z = Float.toString(input.getAsFloat("z"));
                                        String acc_res = acc_x + "," + acc_y + "," + acc_z;
                                        System.out.println("Send linearacceleration data: " + acc_res);

                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
//                                    byte[] imageData = acc_res.getBytes();
//                                    ByteBuffer byteBuffer = ByteBuffer.wrap(imageData);
                                            conn.send(acc_res);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                    case "relativehumidity":
                        uqi.getData(RelativeHumidity.asUpdates(3), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String humidity = Float.toString(input.getAsFloat("humidity"));
                                        String acc_res = humidity;
                                        System.out.println("Send relativehumidity data: " + acc_res);

                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
//                                    byte[] imageData = acc_res.getBytes();
//                                    ByteBuffer byteBuffer = ByteBuffer.wrap(imageData);
                                            conn.send(acc_res);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                    case "rotationvector":
                        uqi.getData(RotationVector.asUpdates(3), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String acc_x = Float.toString(input.getAsFloat("x"));
                                        String acc_y = Float.toString(input.getAsFloat("y"));
                                        String acc_z = Float.toString(input.getAsFloat("z"));
                                        String scalar = Float.toString(input.getAsFloat("scalar"));
                                        String acc_res = acc_x + "," + acc_y + "," + acc_z + "," + scalar;
                                        System.out.println("Send rotationvector data: " + acc_res);

                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
//                                    byte[] imageData = acc_res.getBytes();
//                                    ByteBuffer byteBuffer = ByteBuffer.wrap(imageData);
                                            conn.send(acc_res);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                    case "stepcounter":
                        uqi.getData(StepCounter.asUpdates(3), Purpose.UTILITY("chainstream"))
                                .forEach(new Callback<Item>() {
                                    @Override
                                    protected void onInput(Item input) {
                                        String step = Float.toString(input.getAsFloat("steps"));
                                        String acc_res = step;
                                        System.out.println("Send stepcounter data: " + acc_res);

                                        try {
                                            if (conn.isClosed()) {
                                                uqi.stopAll();
                                            }
//                                    byte[] imageData = acc_res.getBytes();
//                                    ByteBuffer byteBuffer = ByteBuffer.wrap(imageData);
                                            conn.send(acc_res);
                                        } catch (Exception e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                        break;
                }
                break;
            }
        }

    }
    @Override
    public void onMessage(WebSocket conn, ByteBuffer message) {
        // 接收到的是Byte数据，需要转成文本数据，根据你的客户端要求
        // 看看是string还是byte，工具类在下面贴出
        Log.d("websocket", "onMessage()接收到ByteBuffer的数据->"+byteBufferToString(message));
        conn.send(message);
    }
//    @SneakyThrows
    @Override
    public void onError(WebSocket conn, Exception ex) {
        // 异常  经常调试的话会有缓存，导致下一次调试启动时，端口未关闭,多等待一会儿
        // 可以在这里回调处理，关闭连接，开个线程重新连接调用startMyWebsocketServer()
        Log.e("websocket", "->onError()出现异常："+ex);
    }
    @Override
    public void onStart() {
        Log.d("websocket", "onStart()，WebSocket服务端启动成功");
    }


    public void stopServer() {
        // 在这里执行关闭服务器的操作
        // 例如，关闭所有连接、停止监听端口等
        for (WebSocket connection : connections()) {
            connection.close();
        }
        try {
            super.stop(0);
        } catch ( InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static String byteBufferToString(ByteBuffer buffer)
    {
        CharBuffer charBuffer = null;
        try {
            Charset charset = Charset.forName("UTF-8");
            CharsetDecoder decoder = charset.newDecoder();
            charBuffer = decoder.decode(buffer);
            buffer.flip();
            return charBuffer.toString();
        } catch (Exception ex)
        {
            ex.printStackTrace();
            return null;
        }
    }
}