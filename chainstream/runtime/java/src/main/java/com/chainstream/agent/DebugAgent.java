package com.chainstream.agent;

import com.chainstream.grpc.ChainStreamGrpcClient;
import chainstream.ChainstreamBridge;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * 调试用Java Agent
 * 提供详细的gRPC通信日志和测试功能
 */
public class DebugAgent extends Agent {
    private static final Logger logger = Logger.getLogger(DebugAgent.class.getName());
    
    private ChainStreamGrpcClient grpcClient;
    private String agentId;
    
    public DebugAgent(String agentId) {
        super(agentId);
        this.agentId = agentId;
        
        // 设置详细日志级别
        logger.setLevel(Level.ALL);
        
        // 初始化gRPC客户端
        try {
            this.grpcClient = new ChainStreamGrpcClient("localhost", 50051);
            logger.info("✅ DebugAgent initialized with gRPC client");
        } catch (Exception e) {
            logger.severe("❌ Failed to initialize gRPC client: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @Override
    public void start() {
        logger.info("🚀 Starting DebugAgent: " + agentId);
        
        try {
            // 测试gRPC连接
            logger.info("🔍 Testing gRPC connection...");
            boolean connected = grpcClient.testConnection();
            if (connected) {
                logger.info("✅ gRPC connection successful!");
            } else {
                logger.severe("❌ gRPC connection failed!");
                return;
            }
            
            // 测试启动Agent
            logger.info("🔍 Testing StartAgent...");
            ChainstreamBridge.StartAgentResponse startResponse = grpcClient.startAgent(agentId);
            logger.info("StartAgent response: " + startResponse);
            if (startResponse.getSuccess()) {
                logger.info("✅ Agent started successfully!");
            } else {
                logger.severe("❌ Failed to start agent: " + startResponse.getError());
            }
            
            // 测试创建Stream
            logger.info("🔍 Testing CreateStream...");
            String streamId = "debug_stream_" + System.currentTimeMillis();
            ChainstreamBridge.CreateStreamResponse streamResponse = 
                grpcClient.createStream(streamId, "Debug test stream", agentId);
            logger.info("CreateStream response: " + streamResponse);
            if (streamResponse.getSuccess()) {
                logger.info("✅ Stream created successfully: " + streamId);
                
                // 测试添加项目
                logger.info("🔍 Testing AddItem...");
                ChainstreamBridge.AddItemResponse itemResponse = 
                    grpcClient.addItem(streamId, "Debug test item", agentId);
                logger.info("AddItem response: " + itemResponse);
                if (itemResponse.getSuccess()) {
                    logger.info("✅ Item added successfully!");
                } else {
                    logger.severe("❌ Failed to add item: " + itemResponse.getError());
                }
                
                // 测试获取Stream
                logger.info("🔍 Testing GetStream...");
                ChainstreamBridge.GetStreamResponse getStreamResponse = 
                    grpcClient.getStream(streamId, agentId);
                logger.info("GetStream response: " + getStreamResponse);
                if (getStreamResponse.getSuccess()) {
                    logger.info("✅ Stream retrieved successfully!");
                } else {
                    logger.severe("❌ Failed to get stream: " + getStreamResponse.getError());
                }
            } else {
                logger.severe("❌ Failed to create stream: " + streamResponse.getError());
            }
            
            // 测试LLM查询
            logger.info("🔍 Testing QueryLLM...");
            ChainstreamBridge.QueryLLMResponse llmResponse = 
                grpcClient.queryLLM("Hello from DebugAgent!", "text", agentId);
            logger.info("QueryLLM response: " + llmResponse);
            if (llmResponse.getSuccess()) {
                logger.info("✅ LLM query successful: " + llmResponse.getResponse());
            } else {
                logger.severe("❌ LLM query failed: " + llmResponse.getError());
            }
            
            // 测试获取模型信息
            logger.info("🔍 Testing GetModelInfo...");
            ChainstreamBridge.GetModelInfoResponse modelInfoResponse = 
                grpcClient.getModelInfo("text");
            logger.info("GetModelInfo response: " + modelInfoResponse);
            if (modelInfoResponse.getSuccess()) {
                logger.info("✅ Model info retrieved successfully!");
                for (ChainstreamBridge.ModelInfo model : modelInfoResponse.getModelsList()) {
                    logger.info("  Model Name: " + model.getName());
                    logger.info("  Model Type: " + model.getType());
                    logger.info("  Available: " + model.getAvailable());
                }
            } else {
                logger.severe("❌ Failed to get model info: " + modelInfoResponse.getError());
            }
            
            // 测试获取Runtime信息
            logger.info("🔍 Testing GetRuntimeInfo...");
            ChainstreamBridge.GetRuntimeInfoResponse runtimeInfoResponse = 
                grpcClient.getRuntimeInfo();
            logger.info("GetRuntimeInfo response: " + runtimeInfoResponse);
            if (runtimeInfoResponse.getSuccess()) {
                logger.info("✅ Runtime info retrieved successfully!");
                logger.info("  Runtime ID: " + runtimeInfoResponse.getRuntimeId());
                logger.info("  Status: " + runtimeInfoResponse.getStatus());
                logger.info("  Active Agents: " + runtimeInfoResponse.getActiveAgentsList());
            } else {
                logger.severe("❌ Failed to get runtime info: " + runtimeInfoResponse.getError());
            }
            
            logger.info("🎉 DebugAgent start completed successfully!");
            
        } catch (Exception e) {
            logger.severe("❌ Error in DebugAgent start: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @Override
    public void stop() {
        logger.info("🛑 Stopping DebugAgent: " + agentId);
        
        try {
            // 测试停止Agent
            ChainstreamBridge.StopAgentResponse stopResponse = grpcClient.stopAgent(agentId);
            logger.info("StopAgent response: " + stopResponse);
            if (stopResponse.getSuccess()) {
                logger.info("✅ Agent stopped successfully!");
            } else {
                logger.severe("❌ Failed to stop agent: " + stopResponse.getError());
            }
            
            // 关闭gRPC客户端
            grpcClient.shutdown();
            logger.info("✅ gRPC client shutdown completed");
            
        } catch (Exception e) {
            logger.severe("❌ Error in DebugAgent stop: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * 运行完整的调试测试
     */
    public void runFullDebugTest() {
        logger.info("🧪 Running full debug test...");
        
        start();
        
        // 等待一段时间
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        stop();
        
        logger.info("🏁 Full debug test completed!");
    }
    
    /**
     * 主方法用于独立测试
     */
    public static void main(String[] args) {
        // 设置日志格式
        System.setProperty("java.util.logging.SimpleFormatter.format", 
            "%1$tY-%1$tm-%1$td %1$tH:%1$tM:%1$tS %4$s %2$s: %5$s%6$s%n");
        
        String agentId = args.length > 0 ? args[0] : "debug_agent_" + System.currentTimeMillis();
        
        DebugAgent agent = new DebugAgent(agentId);
        agent.runFullDebugTest();
    }
}
