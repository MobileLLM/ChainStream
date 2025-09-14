package com.chainstream.agent;

import com.chainstream.agent.Agent;
import com.chainstream.runtime.Stream;
import com.chainstream.runtime.Stream.StreamListener;
import com.chainstream.runtime.Runtime;

public class DebugListenJavaAgent extends Agent implements StreamListener {
    
    public DebugListenJavaAgent() {
        super("debug_listen_java_agent");
    }
    
    @Override
    public void start() {
        System.out.println("Debug Listen Java Agent started!");
        
        // This agent listens to other streams and logs what it receives
        System.out.println("Debug Listen Java Agent is ready to listen to streams...");
        
        // Create a stream to listen to
        Stream listenStream = createStream("listen_stream", "Stream for listening to other agents");
        
        // Add this agent as a listener to the stream
        listenStream.forEach(this);
    }
    
    @Override
    public void stop() {
        System.out.println("Debug Listen Java Agent stopped!");
    }
    
    @Override
    public void onItem(Object item) {
        System.out.println("Debug Listen Java Agent received item: " + item);
    }
}
