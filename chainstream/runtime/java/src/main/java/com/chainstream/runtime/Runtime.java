package com.chainstream.runtime;

import com.chainstream.grpc.ChainStreamGrpcClient;
import com.chainstream.callback.JavaAgentCallbackServer;
import chainstream.ChainstreamBridge;
import java.util.logging.Logger;

/**
 * ChainStream Java Runtime
 * 提供Java Agent与Python Runtime的桥接功能
 */
public class Runtime {
    private static final Logger logger = Logger.getLogger(Runtime.class.getName());
    private static Runtime instance;
    private ChainStreamGrpcClient grpcClient;
    private String agentId;
    private String callbackAddress; // Java callback server地址
    private JavaAgentCallbackServer callbackServer; // Callback server引用
    
    private Runtime() {
        this.agentId = "default_agent";
        // 初始化gRPC客户端
        this.grpcClient = new ChainStreamGrpcClient("localhost", 50051);
    }
    
    /**
     * 获取Runtime单例实例
     */
    public static synchronized Runtime getInstance() {
        if (instance == null) {
            instance = new Runtime();
        }
        return instance;
    }
    
    /**
     * 设置Agent ID
     */
    public void setAgentId(String agentId) {
        this.agentId = agentId;
        // 重新创建gRPC客户端
        this.grpcClient = new ChainStreamGrpcClient("localhost", 50051);
    }
    
    /**
     * 获取Stream
     */
    public Stream getStream(String streamId) {
        // 通过gRPC获取Stream
        ChainstreamBridge.GetStreamResponse response = grpcClient.getStream(streamId, agentId);
        if (response.getSuccess()) {
            return new Stream(streamId, agentId, grpcClient);
        } else {
            logger.severe("Failed to get stream: " + streamId + " - " + response.getError());
            return null;
        }
    }
    
    /**
     * 创建Stream
     */
    public Stream createStream(String streamId, String description) {
        // 通过gRPC创建Stream
        ChainstreamBridge.CreateStreamResponse response = grpcClient.createStream(streamId, description, agentId);
        if (response.getSuccess()) {
            logger.info("Creating stream: " + streamId + " - " + description);
            return new Stream(streamId, agentId, grpcClient);
        } else {
            logger.severe("Failed to create stream: " + streamId + " - " + response.getError());
            return null;
        }
    }
    
    /**
     * 获取LLM模型
     */
    public LLM getModel(String... types) {
        // 通过gRPC获取LLM模型
        ChainstreamBridge.GetModelResponse response = grpcClient.getModel(agentId, types);
        if (response.getSuccess()) {
            return new LLM(response.getModelId(), agentId, grpcClient);
        } else {
            logger.severe("Failed to get model: " + response.getError());
            return null;
        }
    }
    
    /**
     * 制作Prompt
     */
    public String makePrompt(String... promptParts) {
        ChainstreamBridge.MakePromptResponse response = grpcClient.makePrompt(agentId, promptParts);
        if (response.getSuccess()) {
            return response.getFinalPrompt();
        } else {
            logger.severe("Failed to make prompt: " + response.getError());
            return null;
        }
    }
    
    /**
     * 创建Buffer
     */
    public Buffer createBuffer() {
        ChainstreamBridge.CreateBufferResponse response = grpcClient.createBuffer(agentId);
        if (response.getSuccess()) {
            return new Buffer(response.getBufferId(), agentId, grpcClient);
        } else {
            logger.severe("Failed to create buffer: " + response.getError());
            return null;
        }
    }
    
    /**
     * 报告Agent ID到Python端
     */
    public void reportAgentId(String agentId) {
        try {
            long processId = ProcessHandle.current().pid();
            ChainstreamBridge.ReportAgentIdResponse response = grpcClient.reportAgentId(agentId, processId);
            if (response.getSuccess()) {
                logger.info("Agent ID reported successfully: " + agentId);
            } else {
                logger.warning("Failed to report agent ID: " + response.getError());
            }
        } catch (Exception e) {
            logger.severe("Error reporting agent ID: " + e.getMessage());
            throw new RuntimeException("Failed to report agent ID", e);
        }
    }
    
    /**
     * 获取Runtime信息
     */
    public String getRuntimeInfo() {
        ChainstreamBridge.GetRuntimeInfoResponse response = grpcClient.getRuntimeInfo();
        if (response.getSuccess()) {
            return response.getRuntimeId();
        } else {
            logger.severe("Failed to get runtime info: " + response.getError());
            return "unknown";
        }
    }
    
    /**
     * 启动Agent
     */
    public boolean startAgent() {
        ChainstreamBridge.StartAgentResponse response = grpcClient.startAgent(agentId);
        if (!response.getSuccess()) {
            logger.severe("Failed to start agent: " + response.getError());
        }
        return response.getSuccess();
    }
    
    /**
     * 停止Agent
     */
    public boolean stopAgent() {
        ChainstreamBridge.StopAgentResponse response = grpcClient.stopAgent(agentId);
        if (!response.getSuccess()) {
            logger.severe("Failed to stop agent: " + response.getError());
        }
        return response.getSuccess();
    }
    
    /**
     * 设置callback地址和server
     */
    public void setCallbackAddress(String address) {
        this.callbackAddress = address;
        logger.info("Callback address set to: " + address);
    }
    
    /**
     * 设置callback server引用
     */
    public void setCallbackServer(JavaAgentCallbackServer server) {
        this.callbackServer = server;
        logger.info("Callback server reference set");
    }
    
    /**
     * 获取callback地址
     */
    public String getCallbackAddress() {
        return this.callbackAddress;
    }
    
    /**
     * 获取callback server
     */
    public JavaAgentCallbackServer getCallbackServer() {
        return this.callbackServer;
    }
    
    /**
     * 关闭Runtime
     */
    public void shutdown() {
        try {
            grpcClient.shutdown();
        } catch (InterruptedException e) {
            logger.warning("Interrupted while shutting down: " + e.getMessage());
            Thread.currentThread().interrupt();
        }
    }
}
