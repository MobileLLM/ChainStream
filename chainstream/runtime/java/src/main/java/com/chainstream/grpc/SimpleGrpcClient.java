package com.chainstream.grpc;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

// 导入生成的gRPC代码
import chainstream.ChainStreamBridgeGrpc;
import chainstream.ChainstreamBridge;

/**
 * 简化的ChainStream gRPC客户端
 * 用于测试gRPC连接
 */
public class SimpleGrpcClient {
    private static final Logger logger = Logger.getLogger(SimpleGrpcClient.class.getName());
    
    private final ManagedChannel channel;
    private final ChainStreamBridgeGrpc.ChainStreamBridgeBlockingStub blockingStub;
    
    /**
     * 构造函数
     * @param host gRPC服务器主机
     * @param port gRPC服务器端口
     */
    public SimpleGrpcClient(String host, int port) {
        this(ManagedChannelBuilder.forAddress(host, port)
                .usePlaintext()
                .build());
    }
    
    /**
     * 构造函数
     * @param channel gRPC通道
     */
    public SimpleGrpcClient(ManagedChannel channel) {
        this.channel = channel;
        this.blockingStub = ChainStreamBridgeGrpc.newBlockingStub(channel);
    }
    
    /**
     * 关闭客户端
     */
    public void shutdown() throws InterruptedException {
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    }
    
    /**
     * 测试连接
     */
    public boolean testConnection() {
        try {
            logger.info("Testing gRPC connection...");
            
            // 创建测试请求
            ChainstreamBridge.GetRuntimeInfoRequest request = 
                ChainstreamBridge.GetRuntimeInfoRequest.newBuilder().build();
            
            // 发送请求
            ChainstreamBridge.GetRuntimeInfoResponse response = 
                blockingStub.getRuntimeInfo(request);
            
            logger.info("Connection test successful: " + response.getSuccess());
            return response.getSuccess();
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return false;
        }
    }
    
    /**
     * 启动Agent
     */
    public boolean startAgent(String agentId) {
        try {
            logger.info("Starting agent: " + agentId);
            
            ChainstreamBridge.StartAgentRequest request = 
                ChainstreamBridge.StartAgentRequest.newBuilder()
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.StartAgentResponse response = 
                blockingStub.startAgent(request);
            
            logger.info("Agent started: " + response.getSuccess());
            return response.getSuccess();
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return false;
        }
    }
    
    /**
     * 停止Agent
     */
    public boolean stopAgent(String agentId) {
        try {
            logger.info("Stopping agent: " + agentId);
            
            ChainstreamBridge.StopAgentRequest request = 
                ChainstreamBridge.StopAgentRequest.newBuilder()
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.StopAgentResponse response = 
                blockingStub.stopAgent(request);
            
            logger.info("Agent stopped: " + response.getSuccess());
            return response.getSuccess();
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return false;
        }
    }
    
    /**
     * 查询LLM
     */
    public String queryLLM(String query) {
        try {
            logger.info("Querying LLM: " + query);
            
            ChainstreamBridge.QueryLLMRequest request = 
                ChainstreamBridge.QueryLLMRequest.newBuilder()
                    .setQuery(query)
                    .build();
            
            ChainstreamBridge.QueryLLMResponse response = 
                blockingStub.queryLLM(request);
            
            if (response.getSuccess()) {
                logger.info("LLM query successful");
                return response.getResponse();
            } else {
                logger.severe("LLM query failed: " + response.getError());
                return null;
            }
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return null;
        }
    }
    
    public static void main(String[] args) {
        SimpleGrpcClient client = new SimpleGrpcClient("localhost", 50051);
        
        try {
            // 测试连接
            if (client.testConnection()) {
                System.out.println("✅ gRPC connection successful!");
                
                // 测试启动Agent
                if (client.startAgent("test_agent")) {
                    System.out.println("✅ Agent started successfully!");
                    
                    // 测试LLM查询
                    String response = client.queryLLM("Hello from Java!");
                    if (response != null) {
                        System.out.println("✅ LLM query successful: " + response);
                    } else {
                        System.out.println("❌ LLM query failed");
                    }
                    
                    // 测试停止Agent
                    if (client.stopAgent("test_agent")) {
                        System.out.println("✅ Agent stopped successfully!");
                    } else {
                        System.out.println("❌ Failed to stop agent");
                    }
                } else {
                    System.out.println("❌ Failed to start agent");
                }
            } else {
                System.out.println("❌ gRPC connection failed");
            }
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            try {
                client.shutdown();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
