
package com.chainstream.agent;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class SimpleHelloAgent {
    private String agentId;
    private boolean running;
    private Thread workerThread;
    
    public SimpleHelloAgent() {
        this.agentId = "simple_hello_agent";
        this.running = false;
        System.out.println("=== SimpleHelloAgent Created ===");
        System.out.println("Agent ID: " + agentId);
    }
    
    public void start() {
        System.out.println("=== SimpleHelloAgent Started ===");
        this.running = true;
        this.workerThread = new Thread(this::work);
        this.workerThread.start();
    }
    
    private void work() {
        int count = 0;
        while (this.running) {
            count++;
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
            System.out.println("Hello, world! " + timestamp + " (iteration: " + count + ")");
            
            try {
                Thread.sleep(3000); // 3秒间隔
            } catch (InterruptedException e) {
                System.out.println("Agent interrupted: " + e.getMessage());
                break;
            }
        }
        System.out.println("=== SimpleHelloAgent Stopped ===");
    }
    
    public void stop() {
        System.out.println("Stopping SimpleHelloAgent...");
        this.running = false;
        if (this.workerThread != null) {
            this.workerThread.interrupt();
        }
    }
    
    public boolean isRunning() {
        return running;
    }
    
    public String getAgentId() {
        return agentId;
    }
    
    public static void main(String[] args) {
        SimpleHelloAgent agent = new SimpleHelloAgent();
        agent.start();
        
        // 保持运行直到被中断
        try {
            Thread.sleep(Long.MAX_VALUE);
        } catch (InterruptedException e) {
            agent.stop();
        }
    }
}
