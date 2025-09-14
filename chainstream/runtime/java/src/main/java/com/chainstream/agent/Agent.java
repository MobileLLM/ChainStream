package com.chainstream.agent;

import com.chainstream.runtime.Runtime;
import com.chainstream.runtime.Stream;
import com.chainstream.runtime.LLM;
import java.util.logging.Logger;

/**
 * Agent基类，所有Java Agent都应该继承此类
 */
public abstract class Agent {
    protected static final Logger logger = Logger.getLogger(Agent.class.getName());
    
    protected String agentId;
    protected Runtime runtime;
    
    public Agent(String agentId) {
        this.agentId = agentId;
        this.runtime = Runtime.getInstance();
        this.runtime.setAgentId(agentId);
        
        // 报告agent_id到Python端
        try {
            this.runtime.reportAgentId(agentId);
            logger.info("Agent ID reported to Python runtime: " + agentId);
        } catch (Exception e) {
            logger.warning("Failed to report agent ID: " + e.getMessage());
        }
        
        logger.info("Agent created: " + agentId);
    }
    
    /**
     * 无参构造函数，从系统属性或环境变量获取agent_id
     */
    public Agent() {
        // 尝试从系统属性获取agent_id
        String agentId = System.getProperty("chainstream.agent.id");
        if (agentId == null || agentId.trim().isEmpty()) {
            // 如果系统属性没有，尝试从环境变量获取
            agentId = System.getenv("CHAINSTREAM_AGENT_ID");
        }
        if (agentId == null || agentId.trim().isEmpty()) {
            // 如果都没有，使用默认值
            agentId = "default_java_agent";
            logger.warning("No agent ID provided, using default: " + agentId);
        }
        
        this.agentId = agentId;
        this.runtime = Runtime.getInstance();
        this.runtime.setAgentId(agentId);
        
        // 报告agent_id到Python端
        try {
            this.runtime.reportAgentId(agentId);
            logger.info("Agent ID reported to Python runtime: " + agentId);
        } catch (Exception e) {
            logger.warning("Failed to report agent ID: " + e.getMessage());
        }
        
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
     * 获取Agent ID
     */
    public String getAgentId() {
        return agentId;
    }
    
    /**
     * 获取Runtime实例
     */
    protected Runtime getRuntime() {
        return runtime;
    }
}
