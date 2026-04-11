/**
 * 测试用的简单Java Agent
 * 不依赖gRPC，用于验证基本编译和启动功能
 */
public class TestJavaAgent {
    
    public TestJavaAgent() {
        System.out.println("TestJavaAgent constructor called");
    }
    
    public void start() {
        System.out.println("TestJavaAgent starting...");
        
        // 简单的测试逻辑
        System.out.println("Hello from Java Agent!");
        System.out.println("This is a test agent to verify Java compilation and startup");
        
        // 模拟一些工作
        for (int i = 1; i <= 5; i++) {
            System.out.println("Working... step " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                System.out.println("Interrupted");
                break;
            }
        }
        
        System.out.println("TestJavaAgent started successfully!");
    }
    
    public void stop() {
        System.out.println("TestJavaAgent stopping...");
        System.out.println("TestJavaAgent stopped");
    }
    
    public static void main(String[] args) {
        System.out.println("Starting TestJavaAgent...");
        
        TestJavaAgent agent = new TestJavaAgent();
        
        // 添加关闭钩子
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Shutdown hook triggered");
            agent.stop();
        }));
        
        try {
            agent.start();
            
            // 保持运行
            System.out.println("Agent is running. Press Ctrl+C to stop.");
            Thread.sleep(Long.MAX_VALUE);
        } catch (InterruptedException e) {
            System.out.println("Agent interrupted");
            agent.stop();
        } catch (Exception e) {
            System.out.println("Unexpected error: " + e.getMessage());
            e.printStackTrace();
            agent.stop();
        }
    }
}
