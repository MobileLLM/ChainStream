package com.chainstream.examples;

import com.chainstream.runtime.Agent;
import com.chainstream.runtime.Stream;
import com.chainstream.runtime.LLM;
import java.util.logging.Logger;

/**
 * 简单的Java Agent示例
 */
public class SimpleAgent extends Agent {
    private static final Logger logger = Logger.getLogger(SimpleAgent.class.getName());
    
    private Stream outputStream;
    private LLM llm;
    
    public SimpleAgent() {
        super("simple_agent");
    }
    
    @Override
    public void start() {
        logger.info("Starting SimpleAgent...");
        
        try {
            // 创建输出流
            outputStream = createStream("output_stream", "Simple agent output");
            
            // 获取LLM模型
            llm = getModel("text");
            
            // 简单的处理逻辑
            String result = llm.query("Hello from Java Agent!");
            outputStream.addItem(result);
            
            logger.info("SimpleAgent started successfully!");
            
        } catch (Exception e) {
            logger.severe("Failed to start SimpleAgent: " + e.getMessage());
        }
    }
    
    @Override
    public void stop() {
        logger.info("SimpleAgent stopped");
    }
    
    /**
     * 主方法用于测试
     */
    public static void main(String[] args) {
        SimpleAgent agent = new SimpleAgent();
        
        try {
            // 启动Agent
            agent.start();
            
            // 保持运行
            Thread.sleep(Long.MAX_VALUE);
            
        } catch (InterruptedException e) {
            agent.stop();
        }
    }
}
