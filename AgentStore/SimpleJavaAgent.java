package com.chainstream.agent;

import com.chainstream.runtime.Stream;
import com.chainstream.runtime.LLM;

/**
 * 简单的Java Agent示例
 * 演示如何使用ChainStream Java API
 */
public class SimpleJavaAgent extends Agent {
    private Stream outputStream;
    private LLM llm;
    
    public SimpleJavaAgent() {
        super("simple_java_agent");
    }
    
    @Override
    public void start() {
        System.out.println("SimpleJavaAgent starting...");
        
        // 创建输出流
        outputStream = createStream("output_stream", "Simple Java agent output");
        
        // 获取LLM模型
        llm = getModel("text");
        
        // 简单的处理逻辑
        String result = llm.query("Hello from Java Agent!");
        outputStream.addItem(result);
        
        // 设置Stream监听器
        outputStream.forEach(item -> {
            System.out.println("Processing item: " + item);
        });
        
        System.out.println("SimpleJavaAgent started successfully!");
    }
    
    @Override
    public void stop() {
        System.out.println("SimpleJavaAgent stopping...");
        System.out.println("SimpleJavaAgent stopped");
    }
    
    public static void main(String[] args) {
        SimpleJavaAgent agent = new SimpleJavaAgent();
        agent.start();
        
        // 保持运行
        try {
            Thread.sleep(Long.MAX_VALUE);
        } catch (InterruptedException e) {
            agent.stop();
        }
    }
}
