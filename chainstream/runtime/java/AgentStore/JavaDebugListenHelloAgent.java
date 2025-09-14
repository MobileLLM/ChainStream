package com.chainstream.agent;

import com.chainstream.runtime.Stream;
import com.chainstream.runtime.Runtime;
import java.util.logging.Logger;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

/**
 * Java版本的DebugListenHelloAgent
 * 功能：监听debug_not_hello_stream，进行批处理（每2条一批），然后转发到另一个stream
 * 对应Python的debug_listen_not_hello_agent.py
 */
public class JavaDebugListenHelloAgent extends Agent {
    private static final Logger logger = Logger.getLogger(JavaDebugListenHelloAgent.class.getName());
    
    private Stream inputStream;
    private Stream outputStream;
    private List<Object> batchBuffer;
    private static final int BATCH_SIZE = 2;
    
    public JavaDebugListenHelloAgent() {
        super("java_debug_listen_hello_agent");
        this.batchBuffer = new ArrayList<>();
    }
    
    @Override
    public void start() {
        logger.info("Starting JavaDebugListenHelloAgent...");
        
        try {
            // 启动Agent
            if (!runtime.startAgent()) {
                logger.severe("Failed to start agent");
                return;
            }
            
            // 获取输入stream（监听debug_not_hello_stream）
            inputStream = getStream("debug_not_hello_stream");
            if (inputStream == null) {
                logger.severe("Failed to get input stream: debug_not_hello_stream");
                return;
            }
            
            // 创建输出stream
            outputStream = createStream("debug_another_stream", "Debug another stream from Java listener agent");
            if (outputStream == null) {
                logger.severe("Failed to create output stream");
                return;
            }
            
            // 设置stream监听器
            setupStreamListeners();
            
            logger.info("JavaDebugListenHelloAgent started successfully!");
            
        } catch (Exception e) {
            logger.severe("Error starting JavaDebugListenHelloAgent: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private void setupStreamListeners() {
        // 设置输入stream的监听器
        inputStream.forEach(item -> {
            try {
                logger.info("Received before batch: " + item);
                
                // 添加到批处理缓冲区
                batchBuffer.add(item);
                
                // 检查是否达到批处理大小
                if (batchBuffer.size() >= BATCH_SIZE) {
                    processBatch();
                }
                
            } catch (Exception e) {
                logger.severe("Error processing stream item: " + e.getMessage());
                e.printStackTrace();
            }
        });
    }
    
    private void processBatch() {
        try {
            logger.info("Processing batch with " + batchBuffer.size() + " items");
            
            // 处理批处理数据
            List<Object> processedBatch = new ArrayList<>();
            
            for (Object item : batchBuffer) {
                // 模拟处理逻辑：复制数据
                processedBatch.add(item);
                processedBatch.add(item); // 对应Python中的 [data, data]
            }
            
            // 发送到输出stream
            for (Object processedItem : processedBatch) {
                outputStream.addItem(processedItem);
                logger.info("Sent processed item to output stream: " + processedItem);
            }
            
            // 清空缓冲区
            batchBuffer.clear();
            
            logger.info("Batch processing completed");
            
        } catch (Exception e) {
            logger.severe("Error processing batch: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @Override
    public void stop() {
        logger.info("Stopping JavaDebugListenHelloAgent...");
        
        // 处理剩余的批处理数据
        if (!batchBuffer.isEmpty()) {
            logger.info("Processing remaining batch items: " + batchBuffer.size());
            processBatch();
        }
        
        // 移除监听器
        if (inputStream != null) {
            inputStream.removeListener(this);
        }
        
        // 停止Agent
        if (runtime != null) {
            runtime.stopAgent();
        }
        
        logger.info("JavaDebugListenHelloAgent stopped");
    }
    
    public static void main(String[] args) {
        logger.info("Starting JavaDebugListenHelloAgent...");
        
        JavaDebugListenHelloAgent agent = new JavaDebugListenHelloAgent();
        
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
            logger.info("JavaDebugListenHelloAgent finished.");
        }
    }
}
