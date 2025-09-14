package com.chainstream.agent;

/**
 * 简单的Java Agent测试类 - 不依赖gRPC
 * 用于验证基本的Java Agent编译和执行功能
 */
public class SimpleTestAgent {
    private String agentId;
    private boolean running;
    
    public SimpleTestAgent() {
        this.agentId = "simple_test_agent";
        this.running = false;
    }
    
    public void start() {
        System.out.println("=== SimpleTestAgent Started ===");
        System.out.println("Agent ID: " + agentId);
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("OS: " + System.getProperty("os.name"));
        System.out.println("Working Directory: " + System.getProperty("user.dir"));
        
        this.running = true;
        
        // 简单的处理逻辑
        for (int i = 1; i <= 5; i++) {
            if (!running) break;
            
            System.out.println("Processing item " + i + "...");
            
            try {
                Thread.sleep(1000); // 模拟处理时间
            } catch (InterruptedException e) {
                System.out.println("Agent interrupted");
                break;
            }
        }
        
        System.out.println("=== SimpleTestAgent Completed ===");
    }
    
    public void stop() {
        System.out.println("Stopping SimpleTestAgent...");
        this.running = false;
    }
    
    public boolean isRunning() {
        return running;
    }
    
    public String getAgentId() {
        return agentId;
    }
    
    public static void main(String[] args) {
        System.out.println("Starting SimpleTestAgent...");
        SimpleTestAgent agent = new SimpleTestAgent();
        agent.start();
        System.out.println("SimpleTestAgent finished.");
    }
}
