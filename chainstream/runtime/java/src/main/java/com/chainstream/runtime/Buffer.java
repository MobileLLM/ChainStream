package com.chainstream.runtime;

import com.chainstream.grpc.ChainStreamGrpcClient;
import chainstream.ChainstreamBridge;
import java.util.logging.Logger;
import java.util.List;
import java.util.ArrayList;

/**
 * Buffer类，提供数据容器功能
 */
public class Buffer {
    private static final Logger logger = Logger.getLogger(Buffer.class.getName());
    
    private final String bufferId;
    private final String agentId;
    private final ChainStreamGrpcClient grpcClient;
    
    public Buffer(String bufferId, String agentId, ChainStreamGrpcClient grpcClient) {
        this.bufferId = bufferId;
        this.agentId = agentId;
        this.grpcClient = grpcClient;
        logger.info("Buffer created: " + bufferId);
    }
    
    /**
     * 向Buffer添加数据
     */
    public void append(Object data) {
        String dataStr = data != null ? data.toString() : "null";
        ChainstreamBridge.BufferAppendResponse response = grpcClient.bufferAppend(bufferId, agentId, dataStr);
        if (response.getSuccess()) {
            logger.info("Data appended to buffer " + bufferId + ": " + dataStr);
        } else {
            logger.warning("Failed to append data to buffer " + bufferId + ": " + dataStr + " - " + response.getError());
        }
    }
    
    /**
     * 从Buffer取出队首数据
     */
    public String pop() {
        ChainstreamBridge.BufferPopResponse response = grpcClient.bufferPop(bufferId, agentId);
        if (response.getSuccess()) {
            logger.info("Data popped from buffer " + bufferId + ": " + response.getData());
            return response.getData();
        } else {
            logger.warning("Failed to pop data from buffer " + bufferId + " - " + response.getError());
            return null;
        }
    }
    
    /**
     * 从Buffer取出所有数据
     */
    public List<String> popAll() {
        ChainstreamBridge.BufferPopAllResponse response = grpcClient.bufferPopAll(bufferId, agentId);
        if (response.getSuccess()) {
            List<String> dataList = new ArrayList<>(response.getDataListList());
            logger.info("All data popped from buffer " + bufferId + ": " + dataList.size() + " items");
            return dataList;
        } else {
            logger.warning("Failed to pop all data from buffer " + bufferId + " - " + response.getError());
            return new ArrayList<>();
        }
    }
    
    /**
     * 获取Buffer ID
     */
    public String getBufferId() {
        return bufferId;
    }
}
