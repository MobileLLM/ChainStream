package com.chainstream.callback;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import chainstream.ChainstreamBridge.*;
import chainstream.JavaAgentCallbackGrpc;

import java.io.IOException;
import java.net.ServerSocket;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.logging.Logger;

import com.chainstream.runtime.Stream;

/**
 * Java Agent Callback gRPC Server
 * 处理Python端对Java listener的回调请求
 */
public class JavaAgentCallbackServer extends JavaAgentCallbackGrpc.JavaAgentCallbackImplBase {
    private static final Logger logger = Logger.getLogger(JavaAgentCallbackServer.class.getName());
    
    private final Server server;
    private final int port;
    private final Map<String, Stream.StreamListener> listenerRegistry;
    
    // ThreadLocal存储当前正在执行的listener ID，用于Java内部addItem调用的上下文传递
    private static final ThreadLocal<String> currentListenerId = new ThreadLocal<>();
    
    /**
     * 获取当前正在执行的listener ID
     */
    public static String getCurrentListenerId() {
        return currentListenerId.get();
    }
    
    /**
     * 设置当前正在执行的listener ID
     */
    public static void setCurrentListenerId(String listenerId) {
        currentListenerId.set(listenerId);
    }
    
    /**
     * 清除当前listener ID
     */
    public static void clearCurrentListenerId() {
        currentListenerId.remove();
    }
    
    /**
     * 构造函数，自动分配可用端口
     */
    public JavaAgentCallbackServer() throws IOException {
        this(findAvailablePort());
    }
    
    /**
     * 构造函数，指定端口
     */
    public JavaAgentCallbackServer(int port) {
        this.port = port;
        this.listenerRegistry = new ConcurrentHashMap<>();
        this.server = ServerBuilder.forPort(port)
                .addService(this)
                .build();
        logger.info("JavaAgentCallbackServer initialized on port: " + port);
    }
    
    /**
     * 查找可用端口
     */
    private static int findAvailablePort() {
        try (ServerSocket socket = new ServerSocket(0)) {
            return socket.getLocalPort();
        } catch (IOException e) {
            // 如果自动分配失败，使用8000+随机数
            return 8000 + (int)(Math.random() * 1000);
        }
    }
    
    /**
     * 启动服务器
     */
    public void start() throws IOException {
        server.start();
        logger.info("✅ JavaAgentCallbackServer started successfully on port: " + port);
        
        // 添加JVM关闭钩子
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Shutting down JavaAgentCallbackServer...");
            JavaAgentCallbackServer.this.stop();
        }));
    }
    
    /**
     * 停止服务器
     */
    public void stop() {
        if (server != null) {
            server.shutdown();
            logger.info("JavaAgentCallbackServer stopped");
        }
    }
    
    /**
     * 阻塞等待服务器终止
     */
    public void blockUntilShutdown() throws InterruptedException {
        if (server != null) {
            server.awaitTermination();
        }
    }
    
    /**
     * 获取服务器端口
     */
    public int getPort() {
        return port;
    }
    
    /**
     * 获取服务器地址
     */
    public String getAddress() {
        return "localhost:" + port;
    }
    
    /**
     * 注册listener
     */
    public void registerListener(String listenerId, Stream.StreamListener listener) {
        listenerRegistry.put(listenerId, listener);
        logger.info("Registered listener: " + listenerId);
    }
    
    /**
     * 注销listener
     */
    public void unregisterListener(String listenerId) {
        listenerRegistry.remove(listenerId);
        logger.info("Unregistered listener: " + listenerId);
    }
    
    /**
     * gRPC方法实现：调用listener
     */
    @Override
    public void invokeListener(InvokeListenerRequest request, 
                               StreamObserver<InvokeListenerResponse> responseObserver) {
        String agentId = request.getAgentId();
        String listenerId = request.getListenerId();
        String itemData = request.getItemData();
        
        logger.info("📨 Received InvokeListener request for listener: " + listenerId);
        logger.fine("Item data: " + itemData);
        
        try {
            // 查找listener
            Stream.StreamListener listener = listenerRegistry.get(listenerId);
            if (listener == null) {
                String error = "Listener not found: " + listenerId;
                logger.warning("❌ " + error);
                
                InvokeListenerResponse response = InvokeListenerResponse.newBuilder()
                        .setSuccess(false)
                        .setError(error)
                        .setHasResult(false)
                        .build();
                responseObserver.onNext(response);
                responseObserver.onCompleted();
                return;
            }
            
            // 设置ThreadLocal，标识当前正在执行的listener
            setCurrentListenerId(listenerId);
            
            try {
                // 调用listener并获取返回值
                logger.info("🔧 Invoking listener: " + listenerId);
                Object result = listener.onItem(itemData);
            
            // 构建响应
            InvokeListenerResponse.Builder responseBuilder = InvokeListenerResponse.newBuilder()
                    .setSuccess(true)
                    .setError("");
            
            // 如果listener返回了非null值，将其序列化为JSON字符串
            if (result != null) {
                String resultData = result.toString();
                responseBuilder.setHasResult(true);
                responseBuilder.setResultData(resultData);
                logger.info("✅ Listener returned result: " + resultData);
            } else {
                responseBuilder.setHasResult(false);
                responseBuilder.setResultData("");
                logger.info("✅ Listener returned void (null)");
            }
            
            InvokeListenerResponse response = responseBuilder.build();
            logger.info("✅ Listener invoked successfully: " + listenerId);
            responseObserver.onNext(response);
            responseObserver.onCompleted();
            
            } finally {
                // 清除ThreadLocal，避免内存泄漏
                clearCurrentListenerId();
            }
            
        } catch (Exception e) {
            // 异常情况下也要清除ThreadLocal
            clearCurrentListenerId();
            
            String error = "Error invoking listener: " + e.getMessage();
            logger.severe("❌ " + error);
            e.printStackTrace();
            
            InvokeListenerResponse response = InvokeListenerResponse.newBuilder()
                    .setSuccess(false)
                    .setError(error)
                    .setHasResult(false)
                    .build();
            responseObserver.onNext(response);
            responseObserver.onCompleted();
        }
    }
}

