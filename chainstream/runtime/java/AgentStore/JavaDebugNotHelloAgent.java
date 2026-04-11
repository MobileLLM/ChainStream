package com.chainstream.agent;

import com.chainstream.runtime.Stream;
import com.chainstream.runtime.Runtime;
import java.util.logging.Logger;
import java.util.Map;
import java.util.HashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * Java版本的DebugNotHelloAgent
 * 功能：每3秒向stream发送一条消息，对应Python的debug_not_hello_agent.py
 */
public class JavaDebugNotHelloAgent extends Agent {
    private static final Logger logger = Logger.getLogger(JavaDebugNotHelloAgent.class.getName());
    
    private Stream debugStream;
    private ScheduledExecutorService scheduler;
    private boolean enabled = false;
    
    public JavaDebugNotHelloAgent() {
        super("java_debug_not_hello_agent");
    }
    
    @Override
    public void start() {
        logger.info("Starting JavaDebugNotHelloAgent...");
        
        try {
            // 启动Agent
            if (!runtime.startAgent()) {
                logger.severe("Failed to start agent");
                return;
            }
            
            // 创建debug stream
            debugStream = createStream("debug_not_hello_stream", "Debug hello stream from Java agent");
            if (debugStream == null) {
                logger.severe("Failed to create debug stream");
                return;
            }
            
            // 启动定时任务
            enabled = true;
            scheduler = Executors.newScheduledThreadPool(1);
            
            // 延迟3秒后开始，然后每3秒执行一次
            scheduler.scheduleAtFixedRate(this::sendHelloMessage, 3, 3, TimeUnit.SECONDS);
            
            logger.info("JavaDebugNotHelloAgent started successfully!");
            
        } catch (Exception e) {
            logger.severe("Error starting JavaDebugNotHelloAgent: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private void sendHelloMessage() {
        if (!enabled) {
            return;
        }
        
        try {
            // 创建消息数据
            Map<String, Object> message = new HashMap<>();
            message.put("message", "Hello, world! from Java Agent");
            message.put("timestamp", System.currentTimeMillis());
            message.put("agent_id", agentId);
            
            // 发送到stream
            debugStream.addItem(message);
            
            logger.info("Sent hello message to stream: " + message);
            
        } catch (Exception e) {
            logger.severe("Error sending hello message: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @Override
    public void stop() {
        logger.info("Stopping JavaDebugNotHelloAgent...");
        
        enabled = false;
        
        if (scheduler != null && !scheduler.isShutdown()) {
            scheduler.shutdown();
            try {
                if (!scheduler.awaitTermination(5, TimeUnit.SECONDS)) {
                    scheduler.shutdownNow();
                }
            } catch (InterruptedException e) {
                scheduler.shutdownNow();
                Thread.currentThread().interrupt();
            }
        }
        
        // 停止Agent
        if (runtime != null) {
            runtime.stopAgent();
        }
        
        logger.info("JavaDebugNotHelloAgent stopped");
    }
    
    public static void main(String[] args) {
        logger.info("Starting JavaDebugNotHelloAgent...");
        
        JavaDebugNotHelloAgent agent = new JavaDebugNotHelloAgent();
        
        // 添加关闭钩子
        java.lang.Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Shutdown hook triggered");
            agent.stop();
        }));
        
        try {
            agent.start();
            
            // 保持运行
            logger.info("Agent is running. Press Ctrl+C to stop.");
            while (true) {
                Thread.sleep(1000);
            }
            
        } catch (InterruptedException e) {
            logger.info("Agent interrupted: " + e.getMessage());
        } catch (Exception e) {
            logger.severe("Agent error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            agent.stop();
            logger.info("JavaDebugNotHelloAgent finished.");
        }
    }
}
