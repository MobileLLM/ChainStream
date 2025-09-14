package com.chainstream.examples;

import com.chainstream.runtime.Agent;
import com.chainstream.runtime.Stream;
import com.chainstream.runtime.LLM;
import com.chainstream.runtime.Buffer;
import java.util.logging.Logger;

/**
 * 完整的Java Agent示例，展示所有API的使用
 */
public class CompleteAgent extends Agent {
    private static final Logger logger = Logger.getLogger(CompleteAgent.class.getName());
    
    private Stream inputStream;
    private Stream outputStream;
    private Stream batchStream;
    private LLM llm;
    private Buffer buffer;
    
    public CompleteAgent() {
        super("complete_agent");
    }
    
    @Override
    public void start() {
        logger.info("Starting CompleteAgent...");
        
        try {
            // 1. 创建Stream
            inputStream = createStream("input_stream", "Input data stream");
            outputStream = createStream("output_stream", "Output data stream");
            batchStream = createStream("batch_stream", "Batch processing stream");
            
            // 2. 获取LLM模型
            llm = getModel("text", "image", "audio");
            
            // 3. 创建Buffer
            buffer = createBuffer();
            
            // 4. 设置Stream监听器
            setupStreamListeners();
            
            // 5. 设置批次处理
            setupBatchProcessing();
            
            // 6. 测试所有功能
            testAllFeatures();
            
            logger.info("CompleteAgent started successfully!");
            
        } catch (Exception e) {
            logger.severe("Failed to start CompleteAgent: " + e.getMessage());
        }
    }
    
    private void setupStreamListeners() {
        // 为输入流添加监听器
        inputStream.forEach(item -> {
            logger.info("Processing input item: " + item);
            
            // 使用Buffer暂存数据
            buffer.append(item);
            
            // 处理数据并输出
            String processedData = processData(item.toString());
            outputStream.addItem(processedData);
        });
        
        // 为输出流添加监听器
        outputStream.forEach(item -> {
            logger.info("Output item: " + item);
        });
    }
    
    private void setupBatchProcessing() {
        // 按数量批次处理
        Stream countBatchStream = batchStream.batchByCount(5);
        countBatchStream.forEach(batch -> {
            logger.info("Processing batch by count: " + batch);
        });
        
        // 按时间批次处理
        Stream timeBatchStream = batchStream.batchByTime(10);
        timeBatchStream.forEach(batch -> {
            logger.info("Processing batch by time: " + batch);
        });
        
        // 按键值批次处理
        Stream itemBatchStream = batchStream.batchByItem("EOS");
        itemBatchStream.forEach(batch -> {
            logger.info("Processing batch by item: " + batch);
        });
    }
    
    private String processData(String data) {
        // 使用LLM处理数据
        String prompt = makePrompt("Process this data: ", data, " and return a summary");
        String result = llm.query(prompt);
        
        return "Processed: " + result;
    }
    
    private void testAllFeatures() {
        logger.info("Testing all features...");
        
        // 测试Stream操作
        inputStream.addItem("Test item 1");
        inputStream.addItem("Test item 2");
        inputStream.addItem("Test item 3");
        
        // 测试批次处理
        batchStream.addItem("Batch item 1");
        batchStream.addItem("Batch item 2");
        batchStream.addItem("Batch item 3");
        batchStream.addItem("Batch item 4");
        batchStream.addItem("Batch item 5"); // 触发按数量批次
        
        // 测试Buffer操作
        buffer.append("Buffer item 1");
        buffer.append("Buffer item 2");
        
        String poppedItem = buffer.pop();
        logger.info("Popped from buffer: " + poppedItem);
        
        // 测试LLM
        String llmResponse = llm.query("Hello from Java Agent!");
        logger.info("LLM response: " + llmResponse);
        
        // 测试Prompt制作
        String prompt = makePrompt("Task: ", "Process data", " Input: ", "test data");
        logger.info("Made prompt: " + prompt);
    }
    
    @Override
    public void stop() {
        logger.info("Stopping CompleteAgent...");
        
        try {
            // 注销所有监听器
            if (inputStream != null) {
                inputStream.unregisterAll();
            }
            if (outputStream != null) {
                outputStream.unregisterAll();
            }
            if (batchStream != null) {
                batchStream.unregisterAll();
            }
            
            // 清空Buffer
            if (buffer != null) {
                buffer.popAll();
            }
            
            logger.info("CompleteAgent stopped successfully!");
            
        } catch (Exception e) {
            logger.severe("Error stopping CompleteAgent: " + e.getMessage());
        }
    }
    
    /**
     * 主方法用于测试
     */
    public static void main(String[] args) {
        CompleteAgent agent = new CompleteAgent();
        
        try {
            // 启动Agent
            agent.start();
            
            // 保持运行一段时间
            Thread.sleep(5000);
            
            // 停止Agent
            agent.stop();
            
        } catch (Exception e) {
            logger.severe("Error in main: " + e.getMessage());
        }
    }
}
