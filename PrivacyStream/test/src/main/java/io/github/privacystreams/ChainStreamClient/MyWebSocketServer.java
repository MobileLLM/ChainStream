package io.github.privacystreams.ChainStreamClient;

import android.content.Context;
import android.graphics.Color;
import android.util.Log;
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

import io.github.privacystreams.core.Callback;
import io.github.privacystreams.core.UQI;
import io.github.privacystreams.core.purposes.Purpose;
import io.github.privacystreams.image.Image;
import io.github.privacystreams.image.ImageOperators;
import io.github.privacystreams.utils.Logging;

public class MyWebSocketServer extends WebSocketServer {
    private Context myContext;

    private TextView mTextImage;

    private TextView mTextAudio;

    private TextView mTextSensors;

    MyWebSocketServer(InetSocketAddress host){
        super(host);
    }

    public void setText(TextView textImage, TextView textAudio, TextView textSensors) {
        mTextImage = textImage;
        mTextAudio = textAudio;
        mTextSensors = textSensors;
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
        String para = parts[1];
        if (cmd.equals("video")) {
            mTextImage.setTextColor(Color.BLUE);
            UQI uqi = new UQI(myContext);
            Logging.debug("begin video socket");
//            UQIVideoSocket uqiVideoSocket = new UQIVideoSocket(uqi, para, conn);
//            uqiVideoSocket.run();
            uqi.getData(Image.takePhotoBgPeriodic(0, Integer.parseInt(para)), Purpose.UTILITY("taking picture."))
                    .setField("imagePath", ImageOperators.getFilepath(Image.IMAGE_DATA))
                    .forEach("imagePath", new Callback<String>() {
                        @Override
                        protected void onInput(String imagePath) {
                            System.out.println("Send " + imagePath + "through socket");
                            mTextImage.setTextColor(Color.RED);
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
                                    mTextImage.setTextColor(ContextCompat.getColor(myContext, android.R.color.primary_text_light));
                                }
                                conn.send(byteBuffer);
                                Logging.debug("send pic" + byteBuffer.capacity());
                                mTextImage.setTextColor(Color.BLUE);

                                boolean isDeleted = imageFile.delete();

                                if (!isDeleted) {
                                    System.out.println("图片文件删除失败");
                                }

                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                    });
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