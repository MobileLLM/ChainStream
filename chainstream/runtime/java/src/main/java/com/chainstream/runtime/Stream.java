package com.chainstream.runtime;

import com.chainstream.grpc.ChainStreamGrpcClient;
import chainstream.ChainstreamBridge;
import java.util.logging.Logger;

/**
 * Stream类，提供流式数据处理功能
 */
public class Stream {
    private static final Logger logger = Logger.getLogger(Stream.class.getName());
    
    private final String streamId;
    private final String agentId;
    private final ChainStreamGrpcClient grpcClient;
    
    public Stream(String streamId, String agentId, ChainStreamGrpcClient grpcClient) {
        this.streamId = streamId;
        this.agentId = agentId;
        this.grpcClient = grpcClient;
        logger.info("Stream created: " + streamId);
    }
    
    /**
     * 为Stream挂载监听函数
     */
    public Stream forEach(StreamListener listener) {
        // 使用监听器的类名作为函数名
        String listenerFunctionName = listener.getClass().getSimpleName();
        
        // 生成唯一的listener ID
        String listenerId = agentId + "_" + streamId + "_" + listenerFunctionName + "_" + System.currentTimeMillis();
        
        // 获取callback地址
        Runtime runtime = Runtime.getInstance();
        String callbackAddress = runtime.getCallbackAddress();
        
        if (callbackAddress == null || callbackAddress.isEmpty()) {
            logger.severe("No callback address available! Cannot register listener.");
            return this;
        }
        
        // 注册listener到callback server
        com.chainstream.callback.JavaAgentCallbackServer callbackServer = runtime.getCallbackServer();
        if (callbackServer != null) {
            callbackServer.registerListener(listenerId, listener);
            logger.info("Registered listener to callback server: " + listenerId);
        } else {
            logger.warning("Callback server not available - listener may not work");
        }
        
        ChainstreamBridge.ForEachResponse response = grpcClient.forEach(streamId, agentId, listenerFunctionName, listenerId, callbackAddress);
        if (response.getSuccess()) {
            logger.info("Stream listener registered for: " + streamId + " with callback: " + callbackAddress);
            // 返回匿名流
            return new Stream(response.getAnonymousStreamId(), agentId, grpcClient);
        } else {
            logger.warning("Failed to register stream listener for: " + streamId + " - " + response.getError());
            return this;
        }
    }
    
    /**
     * 批次切分Stream
     */
    public Stream batch(Integer byCount, Integer byTime, String byItem, String byFuncName) {
        ChainstreamBridge.BatchResponse response = grpcClient.batch(streamId, agentId, byCount, byTime, byItem, byFuncName);
        if (response.getSuccess()) {
            logger.info("Batch processing added for stream: " + streamId);
            // 返回批次流
            return new Stream(response.getBatchStreamId(), agentId, grpcClient);
        } else {
            logger.warning("Failed to add batch processing for: " + streamId + " - " + response.getError());
            return this;
        }
    }
    
    /**
     * 按数量批次切分
     */
    public Stream batchByCount(int count) {
        return batch(count, null, null, null);
    }
    
    /**
     * 按时间批次切分
     */
    public Stream batchByTime(int seconds) {
        return batch(null, seconds, null, null);
    }
    
    /**
     * 按键值批次切分
     */
    public Stream batchByItem(String item) {
        return batch(null, null, item, null);
    }
    
    /**
     * 按函数批次切分
     */
    public Stream batchByFunc(String funcName) {
        return batch(null, null, null, funcName);
    }
    
    /**
     * 注销Stream上的所有监听函数
     */
    public void unregisterAll() {
        ChainstreamBridge.UnregisterAllResponse response = grpcClient.unregisterAll(streamId, agentId);
        if (response.getSuccess()) {
            logger.info("All listeners unregistered for stream: " + streamId);
        } else {
            logger.warning("Failed to unregister listeners for: " + streamId + " - " + response.getError());
        }
    }
    
    /**
     * 移除指定监听器
     */
    public void removeListener(Object listener) {
        // 使用监听器的类名作为函数名
        String listenerFunctionName = listener.getClass().getSimpleName();
        ChainstreamBridge.RemoveListenerResponse response = grpcClient.removeListener(streamId, agentId, listenerFunctionName);
        if (response.getSuccess()) {
            logger.info("Listener removed for stream: " + streamId);
        } else {
            logger.warning("Failed to remove listener for: " + streamId + " - " + response.getError());
        }
    }
    
    /**
     * 向Stream添加项目
     */
    public void addItem(Object item) {
        String itemStr = item != null ? item.toString() : "null";
        
        // 获取当前正在执行的listener ID（如果有）
        String callerListenerId = null;
        try {
            callerListenerId = com.chainstream.callback.JavaAgentCallbackServer.getCurrentListenerId();
            if (callerListenerId != null) {
                logger.fine("📍 AddItem called from listener: " + callerListenerId);
            }
        } catch (Exception e) {
            logger.warning("Failed to get current listener ID: " + e.getMessage());
        }
        
        ChainstreamBridge.AddItemResponse response = grpcClient.addItem(streamId, itemStr, agentId, callerListenerId);
        if (response.getSuccess()) {
            logger.info("Item added to stream " + streamId + ": " + itemStr);
        } else {
            logger.warning("Failed to add item to stream " + streamId + ": " + itemStr + " - " + response.getError());
        }
    }
    
    /**
     * 获取Stream ID
     */
    public String getStreamId() {
        return streamId;
    }
    
    /**
     * Stream监听器接口
     * 返回值将被传递到下一个stream（如果存在）
     * 返回null表示不传递任何值
     */
    @FunctionalInterface
    public interface StreamListener {
        Object onItem(Object item);
    }
}
