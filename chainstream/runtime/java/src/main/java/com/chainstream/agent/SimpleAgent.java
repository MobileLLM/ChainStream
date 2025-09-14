package com.chainstream.agent;

import com.chainstream.runtime.Stream;
import com.chainstream.runtime.LLM;

/**
 * 简单的Java Agent示例
 */
public class SimpleAgent extends Agent {
    private Stream outputStream;
    private LLM llm;
    
    public SimpleAgent() {
        super("simple_agent");
    }
    
    @Override
    public void start() {
        logger.info("Starting SimpleAgent...");
        
        try {
            // 启动Agent
            if (!runtime.startAgent()) {
                logger.severe("Failed to start agent");
                return;
            }
            
            // 创建输出流
            outputStream = createStream("output_stream", "Simple agent output");
            if (outputStream == null) {
                logger.severe("Failed to create output stream");
                return;
            }
            
            // 获取LLM模型
            llm = getModel("text");
            if (llm == null) {
                logger.severe("Failed to get LLM model");
                return;
            }
            
            // 简单的处理逻辑
            String result = llm.query("Hello from Java Agent! Please respond with a greeting.");
            outputStream.addItem(result);
            
            // 设置Stream监听器
            outputStream.forEach(item -> {
                logger.info("Stream item received: " + item);
            });
            
            logger.info("SimpleAgent started successfully!");
            
        } catch (Exception e) {
            logger.severe("Error starting SimpleAgent: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @Override
    public void stop() {
        logger.info("Stopping SimpleAgent...");
        
        try {
            // 停止Agent
            runtime.stopAgent();
            logger.info("SimpleAgent stopped successfully");
        } catch (Exception e) {
            logger.severe("Error stopping SimpleAgent: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    public static void main(String[] args) {
        SimpleAgent agent = new SimpleAgent();
        
        // 添加关闭钩子
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Shutdown hook triggered");
            agent.stop();
        }));
        
        try {
            agent.start();
            
            // 保持运行
            logger.info("Agent is running. Press Ctrl+C to stop.");
            Thread.sleep(Long.MAX_VALUE);
        } catch (InterruptedException e) {
            logger.info("Agent interrupted");
            agent.stop();
        } catch (Exception e) {
            logger.severe("Unexpected error: " + e.getMessage());
            e.printStackTrace();
            agent.stop();
        }
    }
}
