package com.chainstream.runtime;

import com.chainstream.grpc.ChainStreamGrpcClient;
import chainstream.ChainstreamBridge;
import java.util.logging.Logger;

/**
 * LLM类，提供大语言模型功能
 */
public class LLM {
    private static final Logger logger = Logger.getLogger(LLM.class.getName());
    
    private final String modelId;
    private final String agentId;
    private final ChainStreamGrpcClient grpcClient;
    
    public LLM(String modelId, String agentId, ChainStreamGrpcClient grpcClient) {
        this.modelId = modelId;
        this.agentId = agentId;
        this.grpcClient = grpcClient;
        logger.info("LLM created with model ID: " + modelId);
    }
    
    /**
     * 查询LLM
     */
    public String query(String prompt) {
        logger.info("Querying LLM with prompt: " + prompt);
        ChainstreamBridge.QueryLLMResponse response = grpcClient.queryLLM(prompt, "text", agentId);
        if (response.getSuccess()) {
            logger.info("LLM response: " + response.getResponse());
            return response.getResponse();
        } else {
            logger.severe("LLM query failed: " + response.getError());
            return null;
        }
    }
    
    /**
     * 获取模型ID
     */
    public String getModelId() {
        return modelId;
    }
}
