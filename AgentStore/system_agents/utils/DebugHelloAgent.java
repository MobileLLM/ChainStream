package com.chainstream.agent;

import com.chainstream.runtime.Stream;
import java.util.concurrent.TimeUnit;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.HashMap;

/**
 * Debug Hello Agent - 对应 Python 版本的 debug_hello_agent.py
 * 功能：每3秒输出 "Hello, world!" 并添加数据到 stream
 */
public class DebugHelloAgent extends Agent {
    private Thread helloThread;
    private boolean enabled;
    private Stream stream;
    
    public DebugHelloAgent() {
        super();  // 使用无参构造函数，从系统属性获取agent_id
        this.enabled = false;
        this.stream = createStream("debug_hello_stream", "Debug Hello Stream");
        
        // 如果创建失败，尝试获取已存在的stream
        if (this.stream == null) {
            System.out.println("Stream creation failed, trying to get existing stream...");
            this.stream = getStream("debug_hello_stream");
        }
        
        if (this.stream == null) {
            System.err.println("Failed to create or get stream: debug_hello_stream");
        } else {
            System.out.println("Stream initialized successfully: debug_hello_stream");
        }
    }
    
    @Override
    public void start() {
        this.enabled = true;
        this.helloThread = new Thread(this::hello);
        this.helloThread.start();
    }
    
    private void hello() {
        while (this.enabled) {
            String message = "Hello, world! " + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
            System.out.println(message);
            
            // 添加数据到 stream，对应 Python 的 self.stream.add_item({'message': 'Hello, world!'})
            if (this.stream != null) {
                Map<String, Object> data = new HashMap<>();
                data.put("message", "Hello, world!");
                this.stream.addItem(data);
            } else {
                System.err.println("Stream is null, cannot add item");
            }
            
            try {
                Thread.sleep(3000); // 3秒间隔
            } catch (InterruptedException e) {
                System.out.println("DebugHelloAgent interrupted: " + e.getMessage());
                break;
            }
        }
    }
    
    @Override
    public void stop() {
        this.enabled = false;
        if (this.helloThread != null) {
            this.helloThread.interrupt();
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=== DebugHelloAgent Main Method Started ===");
        System.out.println("Java version: " + System.getProperty("java.version"));
        System.out.println("Java home: " + System.getProperty("java.home"));
        System.out.println("Working directory: " + System.getProperty("user.dir"));
        System.out.println("Class path: " + System.getProperty("java.class.path"));
        System.out.println("Arguments: " + java.util.Arrays.toString(args));
        
        try {
            DebugHelloAgent agent = new DebugHelloAgent();
            agent.start();
            
            // 保持运行直到被中断
            System.out.println("=== DebugHelloAgent Main Thread Waiting ===");
            while (agent.enabled) {
                Thread.sleep(1000);
                System.out.println("Main thread alive, agent running: " + agent.enabled);
            }
            
        } catch (Exception e) {
            System.err.println("=== DebugHelloAgent Error in main ===");
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
        
        System.out.println("=== DebugHelloAgent Main Method Ended ===");
    }
}