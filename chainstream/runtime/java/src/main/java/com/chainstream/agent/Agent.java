package com.chainstream.agent;

import com.chainstream.runtime.Buffer;
import com.chainstream.runtime.LLM;
import com.chainstream.runtime.Runtime;
import com.chainstream.runtime.Stream;
import com.chainstream.callback.JavaAgentCallbackServer;
import java.util.logging.Logger;

/**
 * 轻量运行时基类（常驻于工程内）
 * 外部 Agent 脚本应继承本类。
 */
public abstract class Agent {
    private static final Logger logger = Logger.getLogger(Agent.class.getName());

    protected final String agentId;
    protected final Runtime runtime;
    protected final JavaAgentCallbackServer callbackServer;

    /**
     * 无参构造：优先使用系统属性 chainstream.agent.id 作为 agentId
     * 若未设置，则回退为类名小写。
     */
    public Agent() {
        String id = System.getProperty("chainstream.agent.id");
        if (id == null || id.trim().isEmpty()) {
            id = this.getClass().getSimpleName().toLowerCase();
        }
        this.agentId = id;
        this.runtime = Runtime.getInstance();
        this.runtime.setAgentId(this.agentId);
        
        // 初始化callback server
        try {
            this.callbackServer = new JavaAgentCallbackServer();
            this.callbackServer.start();
            logger.info("✅ Callback server started on port: " + callbackServer.getPort());
            
            // 将callback地址和server引用设置到runtime中，供forEach使用
            this.runtime.setCallbackAddress(this.callbackServer.getAddress());
            this.runtime.setCallbackServer(this.callbackServer);
        } catch (Exception e) {
            logger.severe("❌ Failed to start callback server: " + e.getMessage());
            throw new RuntimeException("Failed to start callback server", e);
        }
        
        // 上报 Agent ID
        try {
            this.runtime.reportAgentId(this.agentId);
        } catch (Exception e) {
            logger.warning("Failed to report agent ID at init: " + e.getMessage());
        }
        logger.info("Agent created: " + this.agentId);
    }

    /** 启动 Agent */
    public abstract void start();

    /** 停止 Agent */
    public abstract void stop();

    /** 获取 Stream */
    protected Stream getStream(String streamId) {
        return runtime.getStream(streamId);
    }

    /** 创建 Stream */
    protected Stream createStream(String streamId, String description) {
        return runtime.createStream(streamId, description);
    }

    /** 获取 LLM 模型 */
    protected LLM getModel(String... types) {
        return runtime.getModel(types);
    }

    /** 生成 Prompt */
    protected String makePrompt(String... promptParts) {
        return runtime.makePrompt(promptParts);
    }

    /** 创建 Buffer */
    protected Buffer createBuffer() {
        return runtime.createBuffer();
    }

    /** 获取 Agent ID */
    public String getAgentId() {
        return agentId;
    }

    /** 通知 Python 端启动 Agent（按需使用） */
    public boolean startAgent() {
        return runtime.startAgent();
    }

    /** 通知 Python 端停止 Agent（按需使用） */
    public boolean stopAgent() {
        // 停止callback server
        if (callbackServer != null) {
            callbackServer.stop();
        }
        return runtime.stopAgent();
    }
    
    /** 获取callback server，用于注册listener */
    protected JavaAgentCallbackServer getCallbackServer() {
        return callbackServer;
    }
}


