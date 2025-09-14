package com.chainstream.runtime;

import java.util.logging.Logger;

/**
 * Agent基类，所有Java Agent都需要继承此类
 */
public abstract class Agent {
    private static final Logger logger = Logger.getLogger(Agent.class.getName());
    
    protected final String agentId;
    protected final Runtime runtime;
    
    public Agent(String agentId) {
        this.agentId = agentId;
        this.runtime = Runtime.getInstance();
        this.runtime.setAgentId(agentId);
        logger.info("Agent created: " + agentId);
    }
    
    /**
     * 启动Agent
     */
    public abstract void start();
    
    /**
     * 停止Agent
     */
    public abstract void stop();
    
    /**
     * 获取Stream
     */
    protected Stream getStream(String streamId) {
        return runtime.getStream(streamId);
    }
    
    /**
     * 创建Stream
     */
    protected Stream createStream(String streamId, String description) {
        return runtime.createStream(streamId, description);
    }
    
    /**
     * 获取LLM模型
     */
    protected LLM getModel(String... types) {
        return runtime.getModel(types);
    }
    
    /**
     * 制作Prompt
     */
    protected String makePrompt(String... promptParts) {
        return runtime.makePrompt(promptParts);
    }
    
    /**
     * 创建Buffer
     */
    protected Buffer createBuffer() {
        return runtime.createBuffer();
    }
    
    /**
     * 获取Agent ID
     */
    public String getAgentId() {
        return agentId;
    }
    
    /**
     * 启动Agent（调用Python Runtime）
     */
    public boolean startAgent() {
        return runtime.startAgent();
    }
    
    /**
     * 停止Agent（调用Python Runtime）
     */
    public boolean stopAgent() {
        return runtime.stopAgent();
    }
}
