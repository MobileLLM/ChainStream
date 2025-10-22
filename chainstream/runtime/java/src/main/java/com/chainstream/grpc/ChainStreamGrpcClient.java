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
 * 完整的ChainStream gRPC客户端
 * 提供与Python Runtime的完整通信功能
 */
public class ChainStreamGrpcClient {
    private static final Logger logger = Logger.getLogger(ChainStreamGrpcClient.class.getName());
    
    private final ManagedChannel channel;
    private final ChainStreamBridgeGrpc.ChainStreamBridgeBlockingStub blockingStub;
    
    /**
     * 构造函数
     * @param host gRPC服务器主机
     * @param port gRPC服务器端口
     */
    public ChainStreamGrpcClient(String host, int port) {
        this(ManagedChannelBuilder.forAddress(host, port)
                .usePlaintext()
                .build());
    }
    
    /**
     * 构造函数
     * @param channel gRPC通道
     */
    public ChainStreamGrpcClient(ManagedChannel channel) {
        this.channel = channel;
        this.blockingStub = ChainStreamBridgeGrpc.newBlockingStub(channel);
    }
    
    /**
     * 关闭客户端
     */
    public void shutdown() throws InterruptedException {
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    }
    
    // ==================== Agent生命周期方法 ====================
    
    /**
     * 启动Agent
     */
    public ChainstreamBridge.StartAgentResponse startAgent(String agentId) {
        try {
            logger.info("Starting agent: " + agentId);
            
            ChainstreamBridge.StartAgentRequest request = 
                ChainstreamBridge.StartAgentRequest.newBuilder()
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.StartAgentResponse response = 
                blockingStub.startAgent(request);
            
            logger.info("Agent started: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.StartAgentResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 停止Agent
     */
    public ChainstreamBridge.StopAgentResponse stopAgent(String agentId) {
        try {
            logger.info("Stopping agent: " + agentId);
            
            ChainstreamBridge.StopAgentRequest request = 
                ChainstreamBridge.StopAgentRequest.newBuilder()
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.StopAgentResponse response = 
                blockingStub.stopAgent(request);
            
            logger.info("Agent stopped: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.StopAgentResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    // ==================== Stream操作方法 ====================
    
    /**
     * 创建Stream
     */
    public ChainstreamBridge.CreateStreamResponse createStream(String streamId, String description, String agentId) {
        try {
            logger.info("Creating stream: " + streamId + " - " + description);
            
            ChainstreamBridge.CreateStreamRequest request = 
                ChainstreamBridge.CreateStreamRequest.newBuilder()
                    .setStreamId(streamId)
                    .setDescription(description)
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.CreateStreamResponse response = 
                blockingStub.createStream(request);
            
            logger.info("Stream created: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.CreateStreamResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 获取Stream
     */
    public ChainstreamBridge.GetStreamResponse getStream(String streamId, String agentId) {
        try {
            logger.info("Getting stream: " + streamId);
            
            ChainstreamBridge.GetStreamRequest request = 
                ChainstreamBridge.GetStreamRequest.newBuilder()
                    .setStreamId(streamId)
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.GetStreamResponse response = 
                blockingStub.getStream(request);
            
            logger.info("Stream retrieved: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.GetStreamResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 向Stream添加项目
     */
    public ChainstreamBridge.AddItemResponse addItem(String streamId, String item, String agentId, String callerListenerId) {
        try {
            logger.info("Adding item to stream " + streamId + ": " + item);
            if (callerListenerId != null) {
                logger.fine("Caller listener ID: " + callerListenerId);
            }
            
            ChainstreamBridge.AddItemRequest.Builder requestBuilder = 
                ChainstreamBridge.AddItemRequest.newBuilder()
                    .setStreamId(streamId)
                    .setItem(item)
                    .setAgentId(agentId);
            
            // 如果有caller_listener_id，添加到请求中
            if (callerListenerId != null && !callerListenerId.isEmpty()) {
                requestBuilder.setCallerListenerId(callerListenerId);
            }
            
            ChainstreamBridge.AddItemRequest request = requestBuilder.build();
            
            ChainstreamBridge.AddItemResponse response = 
                blockingStub.addItem(request);
            
            logger.info("Item added: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.AddItemResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 为Stream挂载监听函数
     */
    public ChainstreamBridge.ForEachResponse forEach(String streamId, String agentId, String listenerFunctionName, String listenerId, String callbackAddress) {
        try {
            logger.info("Adding forEach listener for stream: " + streamId + ", callback: " + callbackAddress);
            
            ChainstreamBridge.ForEachRequest.Builder requestBuilder = 
                ChainstreamBridge.ForEachRequest.newBuilder()
                    .setStreamId(streamId)
                    .setAgentId(agentId)
                    .setListenerFunctionName(listenerFunctionName);
            
            // 添加listener ID和callback地址
            if (listenerId != null && !listenerId.isEmpty()) {
                requestBuilder.setListenerId(listenerId);
            }
            if (callbackAddress != null && !callbackAddress.isEmpty()) {
                requestBuilder.setCallbackAddress(callbackAddress);
            }
            
            ChainstreamBridge.ForEachResponse response = 
                blockingStub.forEach(requestBuilder.build());
            
            logger.info("ForEach listener added: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.ForEachResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 批次切分Stream
     */
    public ChainstreamBridge.BatchResponse batch(String streamId, String agentId, 
            Integer byCount, Integer byTime, String byItem, String byFuncName) {
        try {
            logger.info("Adding batch processing for stream: " + streamId);
            
            ChainstreamBridge.BatchRequest.Builder requestBuilder = 
                ChainstreamBridge.BatchRequest.newBuilder()
                    .setStreamId(streamId)
                    .setAgentId(agentId);
            
            if (byCount != null) requestBuilder.setByCount(byCount);
            if (byTime != null) requestBuilder.setByTime(byTime);
            if (byItem != null) requestBuilder.setByItem(byItem);
            if (byFuncName != null) requestBuilder.setByFuncName(byFuncName);
            
            ChainstreamBridge.BatchResponse response = 
                blockingStub.batch(requestBuilder.build());
            
            logger.info("Batch processing added: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.BatchResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 注销Stream上的所有监听函数
     */
    public ChainstreamBridge.UnregisterAllResponse unregisterAll(String streamId, String agentId) {
        try {
            logger.info("Unregistering all listeners for stream: " + streamId);
            
            ChainstreamBridge.UnregisterAllRequest request = 
                ChainstreamBridge.UnregisterAllRequest.newBuilder()
                    .setStreamId(streamId)
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.UnregisterAllResponse response = 
                blockingStub.unregisterAll(request);
            
            logger.info("All listeners unregistered: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.UnregisterAllResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 移除指定监听器
     */
    public ChainstreamBridge.RemoveListenerResponse removeListener(String streamId, String agentId, String listenerFunctionName) {
        try {
            logger.info("Removing listener for stream: " + streamId);
            
            ChainstreamBridge.RemoveListenerRequest request = 
                ChainstreamBridge.RemoveListenerRequest.newBuilder()
                    .setStreamId(streamId)
                    .setAgentId(agentId)
                    .setListenerFunctionName(listenerFunctionName)
                    .build();
            
            ChainstreamBridge.RemoveListenerResponse response = 
                blockingStub.removeListener(request);
            
            logger.info("Listener removed: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.RemoveListenerResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    // ==================== LLM操作方法 ====================
    
    /**
     * 查询LLM
     */
    public ChainstreamBridge.QueryLLMResponse queryLLM(String prompt) {
        return queryLLM(prompt, "text", "");
    }
    
    /**
     * 查询LLM（带模型类型）
     */
    public ChainstreamBridge.QueryLLMResponse queryLLM(String prompt, String modelType) {
        return queryLLM(prompt, modelType, "");
    }
    
    /**
     * 查询LLM（完整参数）
     */
    public ChainstreamBridge.QueryLLMResponse queryLLM(String prompt, String modelType, String agentId) {
        try {
            logger.info("Querying LLM: " + prompt);
            
            ChainstreamBridge.QueryLLMRequest request = 
                ChainstreamBridge.QueryLLMRequest.newBuilder()
                    .setQuery(prompt)
                    .addModelTypes(modelType)
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.QueryLLMResponse response = 
                blockingStub.queryLLM(request);
            
            logger.info("LLM query successful: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.QueryLLMResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 获取LLM模型
     */
    public ChainstreamBridge.GetModelResponse getModel(String agentId, String... modelTypes) {
        try {
            logger.info("Getting LLM model for types: " + String.join(", ", modelTypes));
            
            ChainstreamBridge.GetModelRequest.Builder requestBuilder = 
                ChainstreamBridge.GetModelRequest.newBuilder()
                    .setAgentId(agentId);
            
            for (String type : modelTypes) {
                requestBuilder.addModelTypes(type);
            }
            
            ChainstreamBridge.GetModelResponse response = 
                blockingStub.getModel(requestBuilder.build());
            
            logger.info("Model obtained: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.GetModelResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 制作Prompt
     */
    public ChainstreamBridge.MakePromptResponse makePrompt(String agentId, String... promptParts) {
        try {
            logger.info("Making prompt with " + promptParts.length + " parts");
            
            ChainstreamBridge.MakePromptRequest.Builder requestBuilder = 
                ChainstreamBridge.MakePromptRequest.newBuilder()
                    .setAgentId(agentId);
            
            for (String part : promptParts) {
                requestBuilder.addPromptParts(part);
            }
            
            ChainstreamBridge.MakePromptResponse response = 
                blockingStub.makePrompt(requestBuilder.build());
            
            logger.info("Prompt made: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.MakePromptResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    // ==================== 模型信息方法 ====================
    
    /**
     * 获取模型信息
     */
    public ChainstreamBridge.GetModelInfoResponse getModelInfo(String modelType) {
        try {
            logger.info("Getting model info for: " + modelType);
            
            ChainstreamBridge.GetModelInfoRequest request = 
                ChainstreamBridge.GetModelInfoRequest.newBuilder()
                    .addModelTypes(modelType)
                    .build();
            
            ChainstreamBridge.GetModelInfoResponse response = 
                blockingStub.getModelInfo(request);
            
            logger.info("Model info retrieved: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.GetModelInfoResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 获取Runtime信息
     */
    public ChainstreamBridge.GetRuntimeInfoResponse getRuntimeInfo() {
        try {
            logger.info("Getting runtime info");
            
            ChainstreamBridge.GetRuntimeInfoRequest request = 
                ChainstreamBridge.GetRuntimeInfoRequest.newBuilder().build();
            
            ChainstreamBridge.GetRuntimeInfoResponse response = 
                blockingStub.getRuntimeInfo(request);
            
            logger.info("Runtime info retrieved: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.GetRuntimeInfoResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 报告Agent ID
     */
    public ChainstreamBridge.ReportAgentIdResponse reportAgentId(String agentId, long processId) {
        try {
            logger.info("Reporting agent ID: " + agentId + " (PID: " + processId + ")");
            
            ChainstreamBridge.ReportAgentIdRequest request = 
                ChainstreamBridge.ReportAgentIdRequest.newBuilder()
                    .setAgentId(agentId)
                    .setProcessId(processId)
                    .build();
            
            ChainstreamBridge.ReportAgentIdResponse response = 
                blockingStub.reportAgentId(request);
            
            logger.info("Agent ID reported: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.ReportAgentIdResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    // ==================== 测试方法 ====================
    
    /**
     * 测试连接
     */
    public boolean testConnection() {
        try {
            ChainstreamBridge.GetRuntimeInfoResponse response = getRuntimeInfo();
            return response.getSuccess();
        } catch (Exception e) {
            logger.severe("Connection test failed: " + e.getMessage());
            return false;
        }
    }
    
    // ==================== Buffer操作方法 ====================
    
    /**
     * 创建Buffer
     */
    public ChainstreamBridge.CreateBufferResponse createBuffer(String agentId) {
        try {
            logger.info("Creating buffer for agent: " + agentId);
            
            ChainstreamBridge.CreateBufferRequest request = 
                ChainstreamBridge.CreateBufferRequest.newBuilder()
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.CreateBufferResponse response = 
                blockingStub.createBuffer(request);
            
            logger.info("Buffer created: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.CreateBufferResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 向Buffer添加数据
     */
    public ChainstreamBridge.BufferAppendResponse bufferAppend(String bufferId, String agentId, String data) {
        try {
            logger.info("Appending data to buffer: " + bufferId);
            
            ChainstreamBridge.BufferAppendRequest request = 
                ChainstreamBridge.BufferAppendRequest.newBuilder()
                    .setBufferId(bufferId)
                    .setAgentId(agentId)
                    .setData(data)
                    .build();
            
            ChainstreamBridge.BufferAppendResponse response = 
                blockingStub.bufferAppend(request);
            
            logger.info("Data appended: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.BufferAppendResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 从Buffer取出队首数据
     */
    public ChainstreamBridge.BufferPopResponse bufferPop(String bufferId, String agentId) {
        try {
            logger.info("Popping data from buffer: " + bufferId);
            
            ChainstreamBridge.BufferPopRequest request = 
                ChainstreamBridge.BufferPopRequest.newBuilder()
                    .setBufferId(bufferId)
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.BufferPopResponse response = 
                blockingStub.bufferPop(request);
            
            logger.info("Data popped: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.BufferPopResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 从Buffer取出所有数据
     */
    public ChainstreamBridge.BufferPopAllResponse bufferPopAll(String bufferId, String agentId) {
        try {
            logger.info("Popping all data from buffer: " + bufferId);
            
            ChainstreamBridge.BufferPopAllRequest request = 
                ChainstreamBridge.BufferPopAllRequest.newBuilder()
                    .setBufferId(bufferId)
                    .setAgentId(agentId)
                    .build();
            
            ChainstreamBridge.BufferPopAllResponse response = 
                blockingStub.bufferPopAll(request);
            
            logger.info("All data popped: " + response.getSuccess());
            return response;
            
        } catch (StatusRuntimeException e) {
            logger.severe("RPC failed: " + e.getStatus());
            return ChainstreamBridge.BufferPopAllResponse.newBuilder()
                .setSuccess(false)
                .setError("RPC failed: " + e.getStatus())
                .build();
        }
    }
    
    /**
     * 主方法用于测试
     */
    public static void main(String[] args) {
        ChainStreamGrpcClient client = new ChainStreamGrpcClient("localhost", 50051);
        
        try {
            // 测试连接
            if (client.testConnection()) {
                System.out.println("✅ gRPC connection successful!");
                
                // 测试启动Agent
                ChainstreamBridge.StartAgentResponse startResponse = client.startAgent("test_agent");
                if (startResponse.getSuccess()) {
                    System.out.println("✅ Agent started successfully!");
                    
                    // 测试创建Stream
                    ChainstreamBridge.CreateStreamResponse streamResponse = 
                        client.createStream("test_stream", "Test stream description", "test_agent");
                    if (streamResponse.getSuccess()) {
                        System.out.println("✅ Stream created successfully!");
                        
                        // 测试添加项目
                        ChainstreamBridge.AddItemResponse itemResponse = 
                            client.addItem("test_stream", "Test item", "test_agent", null);
                        if (itemResponse.getSuccess()) {
                            System.out.println("✅ Item added successfully!");
                        }
                    }
                    
                    // 测试LLM查询
                    ChainstreamBridge.QueryLLMResponse llmResponse = 
                        client.queryLLM("Hello from Java!");
                    if (llmResponse.getSuccess()) {
                        System.out.println("✅ LLM query successful: " + llmResponse.getResponse());
                    } else {
                        System.out.println("❌ LLM query failed: " + llmResponse.getError());
                    }
                    
                    // 测试停止Agent
                    ChainstreamBridge.StopAgentResponse stopResponse = client.stopAgent("test_agent");
                    if (stopResponse.getSuccess()) {
                        System.out.println("✅ Agent stopped successfully!");
                    } else {
                        System.out.println("❌ Failed to stop agent: " + stopResponse.getError());
                    }
                } else {
                    System.out.println("❌ Failed to start agent: " + startResponse.getError());
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
