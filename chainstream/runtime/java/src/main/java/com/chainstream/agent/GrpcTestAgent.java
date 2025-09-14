package com.chainstream.agent;

import com.chainstream.runtime.Agent;
import com.chainstream.runtime.Runtime;
import com.chainstream.runtime.Stream;
import com.chainstream.runtime.LLM;

/**
 * 使用gRPC的Java Agent测试类
 * 用于验证完整的Java Agent与Python Runtime的集成
 */
public class GrpcTestAgent extends Agent {
    private Stream outputStream;
    private LLM llm;
    private boolean running;
    
    public GrpcTestAgent() {
        super("grpc_test_agent");
        this.running = false;
    }
    
    @Override
    public void start() {
        System.out.println("=== GrpcTestAgent Started ===");
        System.out.println("Agent ID: " + getAgentId());
        System.out.println("Java Version: " + System.getProperty("java.version"));
        
        try {
            // 获取Runtime实例
            com.chainstream.runtime.Runtime runtime = com.chainstream.runtime.Runtime.getInstance();
            System.out.println("Runtime instance obtained successfully");
            
            // 创建输出流
            outputStream = runtime.createStream("grpc_test_output", "gRPC Test Agent Output Stream");
            System.out.println("Output stream created: " + outputStream.getStreamId());
            
            // 获取LLM模型
            llm = runtime.getModel("text");
            System.out.println("LLM model obtained successfully");
            
            this.running = true;
            
            // 简单的处理逻辑
            for (int i = 1; i <= 3; i++) {
                if (!running) break;
                
                System.out.println("Processing item " + i + "...");
                
                // 使用LLM进行查询
                String query = "Hello from Java Agent! This is test " + i;
                String result = llm.query(query);
                
                System.out.println("LLM Query: " + query);
                System.out.println("LLM Response: " + result);
                
                // 将结果添加到流中
                outputStream.addItem(result);
                
                try {
                    Thread.sleep(2000); // 模拟处理时间
                } catch (InterruptedException e) {
                    System.out.println("Agent interrupted");
                    break;
                }
            }
            
            System.out.println("=== GrpcTestAgent Completed ===");
            
        } catch (Exception e) {
            System.err.println("Error in GrpcTestAgent: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @Override
    public void stop() {
        System.out.println("Stopping GrpcTestAgent...");
        this.running = false;
    }
    
    public boolean isRunning() {
        return running;
    }
    
    public static void main(String[] args) {
        System.out.println("Starting GrpcTestAgent...");
        
        GrpcTestAgent agent = new GrpcTestAgent();
        
        // 添加关闭钩子
        java.lang.Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Shutdown hook triggered");
            agent.stop();
        }));
        
        try {
            agent.start();
            
            // 保持运行
            System.out.println("Agent is running. Press Ctrl+C to stop.");
            while (agent.isRunning()) {
                Thread.sleep(1000);
            }
            
        } catch (InterruptedException e) {
            System.out.println("Agent interrupted: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Agent error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            agent.stop();
            System.out.println("GrpcTestAgent finished.");
        }
    }
}
