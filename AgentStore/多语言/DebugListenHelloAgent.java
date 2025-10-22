package com.chainstream.agent;

import com.chainstream.runtime.Stream;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;

/**
 * Debug Listen Hello Agent - 对应 Python 版本的 debug_listen_hello_agent.py
 * 功能：监听 debug_hello_stream，设置复杂的 stream 处理链
 */
public class DebugListenHelloAgent extends Agent {
    private Stream stream;
    private Stream stream2;

    public DebugListenHelloAgent() {
        super(); // 使用无参构造函数，从系统属性获取agent_id
        this.stream = getStream("debug_hello_stream");
        this.stream2 = createStream("debug_another_stream", "Debug Another Stream");
    }

    @Override
    public void start() {
        // 定义处理函数，对应 Python 版本的处理函数
        Stream.StreamListener handleNewHello = data -> {
            System.out.println("Received before batch: " + data);
            return data;  // 返回data以传递到下一个stream
        };

        Stream.StreamListener handleNewHello2 = data -> {
            System.out.println("Received after batch: " + data);
            return data;  // 返回data以传递到下一个stream
        };

        Stream.StreamListener handleNewHello3 = data -> {
            // 同时发送到stream2并传递到下一个匿名stream
            this.stream2.addItem(data);
            return data;  // 返回data以传递到下一个stream
        };

        Stream.StreamListener handleNewHello4 = data -> {
            // 对应 Python 的 return [data, data] - 返回多个数据项
            // Java通过返回List来实现多值返回，Python端会自动解析并展开
            // 创建一个包含两个相同元素的List
            List<Object> resultList = new ArrayList<>();
            resultList.add(data);
            resultList.add(data);
            
            // 使用Gson将List序列化为JSON数组字符串
            com.google.gson.Gson gson = new com.google.gson.Gson();
            String jsonArray = gson.toJson(resultList);
            
            return jsonArray;
        };

        // 构建stream处理链，完全对应Python代码：
        // self.stream.for_each(handle_new_hello).batch(by_count=2).for_each(handle_new_hello_3).for_each(handle_new_hello_4).for_each(lambda data: print(data))
        this.stream
            .forEach(handleNewHello)
            .batchByCount(2)  // 对应 Python 的 batch(by_count=2)
            .forEach(handleNewHello3)
            .forEach(handleNewHello4)
            .forEach(data -> {
                System.out.println(data);
                return null;  // 最后一个listener可以返回null，因为没有后续stream
            });
    }

    @Override
    public void stop() {
        // 停止监听，对应 Python 的 self.stream.remove_listener(self)
        this.stream.removeListener(this);
        System.out.println("DebugListenHelloAgent stopped");
    }

    public static void main(String[] args) {
        System.out.println("=== DebugListenHelloAgent Main Method Started ===");
        
        try {
            DebugListenHelloAgent agent = new DebugListenHelloAgent();
            agent.start();
            
            // 保持运行
            System.out.println("=== DebugListenHelloAgent Main Thread Waiting ===");
            Thread.sleep(Long.MAX_VALUE);
        } catch (InterruptedException e) {
            System.out.println("DebugListenHelloAgent interrupted: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("=== DebugListenHelloAgent Error in main ===");
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
        
        System.out.println("=== DebugListenHelloAgent Main Method Ended ===");
    }
}
