import collections
import logging
from chainstream.stream import register_stream_manager
import time
from chainstream.stream import reset_stream

# from chainstream.stream.base_stream import BaseStream

logger = logging.getLogger(__name__)


class StreamAnalyzer:
    def __init__(self):
        super().__init__()
        self.streams = collections.OrderedDict()
        self.recorders = {}

    def get_stream_info(self):
        stream_info = [x.get_meta_data() for x in self.streams.values()]
        return stream_info
    
    def get_stream_info_by_user(self, user):
        """
        Get stream info filtered by user
        
        Args:
            user: User object to filter streams by
        
        Returns:
            List of stream metadata dictionaries filtered by user
        """
        logger.info(f"🔍 DEBUG: get_stream_info_by_user called with user: {user.get_username() if user else 'None'}")
        logger.info(f"📊 DEBUG: Total streams in manager: {len(self.streams)}")
        
        # 暂时绕过用户限制，打印所有stream信息用于调试
        logger.info("🔍 DEBUG: === ALL STREAMS (bypassing user filter) ===")
        for stream_id, stream in self.streams.items():
            logger.info(f"📊 DEBUG: Stream ID: {stream_id}")
            logger.info(f"📊 DEBUG: Stream user: {stream.metaData.user.get_username() if stream.metaData.user else 'None'}")
            logger.info(f"📊 DEBUG: Stream user UUID: {stream.metaData.user.get_uuid() if stream.metaData.user else 'None'}")
            logger.info(f"📊 DEBUG: Stream metadata: {stream.get_meta_data()}")
        
        if user is None:
            logger.info("🔍 DEBUG: No user provided, returning all streams")
            return self.get_stream_info()
        
        # Admin users (level >= 10) can see all streams
        if user.get_level() >= 10:
            filtered_streams = [x.get_meta_data() for x in self.streams.values()]
            logger.info(f"🔍 DEBUG: Admin user, returning all {len(filtered_streams)} streams")
        else:
            filtered_streams = [
                x.get_meta_data() for x in self.streams.values() 
                if x.metaData.user and x.metaData.user.get_uuid() == user.get_uuid()
            ]
        
        logger.info(f"🔍 DEBUG: Filtered streams count: {len(filtered_streams)}")
        logger.info(f"🔍 DEBUG: Filtered streams: {filtered_streams}")
        
        return filtered_streams

    def get_graph_statistics(self, file_path_to_agent_id, user):
        logger.info(f"🔍 DEBUG: get_graph_statistics called with user: {user.get_username() if user else 'None'}")
        logger.info(f"📊 DEBUG: Total streams in manager: {len(self.streams)}")
        logger.info(f"📊 DEBUG: file_path_to_agent_id: {file_path_to_agent_id}")
        
        # 暂时绕过用户限制，打印所有stream信息用于调试
        logger.info("🔍 DEBUG: === ALL STREAMS FOR GRAPH (bypassing user filter) ===")
        for stream_id, stream in self.streams.items():
            logger.info(f"📊 DEBUG: Stream ID: {stream_id}")
            logger.info(f"📊 DEBUG: Stream user: {stream.metaData.user.get_username() if stream.metaData.user else 'None'}")
            logger.info(f"📊 DEBUG: Stream user level: {stream.metaData.user.get_level() if stream.metaData.user else 'None'}")
            logger.info(f"📊 DEBUG: Stream user UUID: {stream.metaData.user.get_uuid() if stream.metaData.user else 'None'}")
        
        # Filter streams by user level permissions
        if user is None:
            logger.info("🔍 DEBUG: No user provided, using all streams")
            filtered_streams = self.streams.values()
        else:
            user_level = user.get_level()
            user_uuid = user.get_uuid()
            logger.info(f"🔍 DEBUG: User level: {user_level}, UUID: {user_uuid}")
            
            # Admin users (level >= 10) can see all streams
            if user_level >= 10:
                filtered_streams = list(self.streams.values())
                logger.info(f"🔍 DEBUG: Admin user, returning all {len(filtered_streams)} streams")
            else:
                filtered_streams = []
                for stream in self.streams.values():
                    if stream.metaData.user is None:
                        # Legacy streams without user assignment - only show to high level users
                        if user_level >= 10:  # Admin level
                            filtered_streams.append(stream)
                            logger.info(f"✅ DEBUG: Added legacy stream {stream.metaData.stream_id} (admin access)")
                        else:
                            logger.info(f"❌ DEBUG: Skipped legacy stream {stream.metaData.stream_id} (insufficient level)")
                    else:
                        stream_user_level = stream.metaData.user.get_level()
                        stream_user_uuid = stream.metaData.user.get_uuid()
                        
                        # High level users can see their own streams and lower level users' streams
                        # Same level users can only see their own streams
                        if (user_level > stream_user_level) or (user_level == stream_user_level and user_uuid == stream_user_uuid):
                            filtered_streams.append(stream)
                            logger.info(f"✅ DEBUG: Added stream {stream.metaData.stream_id} (user: {stream_user_uuid})")
                        else:
                            logger.info(f"❌ DEBUG: Skipped stream {stream.metaData.stream_id} (user: {stream_user_uuid}, level: {stream_user_level})")
        
        stream_info = [x.get_record_data() for x in filtered_streams]

        agent_to_stream_edges = []
        stream_to_agent_edges = []
        for s_info in stream_info:
            new_agent_to_queue = {}
            for fun_k, fun_v in s_info['agent_to_queue'].items():
                # 检查文件路径是否在agent映射中，如果不在则跳过（可能是gRPC相关路径）
                if fun_k[0] in file_path_to_agent_id:
                    new_agent_to_queue[(file_path_to_agent_id[fun_k[0]], fun_k[1])] = fun_v
                    agent_to_stream_edges.append({
                        "source": str(file_path_to_agent_id[fun_k[0]]) + ":" + str(fun_k[1]),
                        "target": s_info['stream_id'],
                        "value": fun_v['statistics'][1]
                    })
                else:
                    # 对于不在映射中的路径（如gRPC路径），使用原始路径作为标识
                    new_agent_to_queue[(fun_k[0], fun_k[1])] = fun_v
                    agent_to_stream_edges.append({
                        "source": str(fun_k[0]) + ":" + str(fun_k[1]),
                        "target": s_info['stream_id'],
                        "value": fun_v['statistics'][1]
                    })
            s_info['agent_to_queue'] = new_agent_to_queue
            for fun_k, fun_v in s_info['queue_to_agent'].items():
                stream_to_agent_edges.append({
                    "source": s_info['stream_id'],
                    "target": str(fun_k[0]) + ":" + str(fun_k[1]),
                    "value": fun_v['statistics'][1]
                })

        # Create stream nodes with user information
        stream_node = []
        for stream in filtered_streams:
            user_name = stream.metaData.user.get_username() if stream.metaData.user else 'System'
            stream_node.append({
                'name': stream.metaData.stream_id,
                'user': user_name
            })
        
        # Create agent nodes (agents don't have direct user info in this context)
        agent_node = set(key for s_info in stream_info for key in s_info['agent_to_queue'].keys()).union(
            set(key for s_info in stream_info for key in s_info['queue_to_agent'].keys()))

        agent_node = [{'name': str(x[0]) + ":" + str(x[1]), 'user': 'Agent'} for x in agent_node]
        node = stream_node + agent_node
        edge = agent_to_stream_edges + stream_to_agent_edges

        return node, edge


class StreamManager(StreamAnalyzer):
    def __init__(self):
        super().__init__()
        register_stream_manager(self)
        self.thread_list = {}

    def register_stream(self, stream, user):
        if stream.metaData.stream_id in self.streams:
            raise KeyError(f"Stream with id {stream.metaData.stream_id} already exists")
        
        # Ensure stream has user information
        if stream.metaData.user is None and user is not None:
            stream.metaData.user = user
        
        self.streams[stream.metaData.stream_id] = stream
        self.thread_list[stream.metaData.stream_id] = stream.thread
        self.recorders[stream.metaData.stream_id] = stream.recorder

    def unregister_stream(self, stream, user):
        self.streams.pop(stream.stream_id)

    def get_stream(self, stream_id):
        if stream_id not in self.streams:
            raise KeyError(f"Stream with id {stream_id} not found")
        return self.streams.get(stream_id)

    def get_stream_list(self, user):
        return list(self.streams.keys())
    
    def get_streams_by_user(self, user):
        """Get all streams owned by a specific user"""
        return [
            stream for stream in self.streams.values() 
            if stream.metaData.user and stream.metaData.user.get_uuid() == user.get_uuid()
        ]
    
    def get_stream_count_by_user(self, user):
        """Get count of streams owned by a specific user"""
        return len(self.get_streams_by_user(user))
    
    def can_user_access_stream(self, user, stream_id):
        """Check if user can access a specific stream"""
        stream = self.streams.get(stream_id)
        if stream is None:
            return False
        
        # If stream has no user assigned, allow access (legacy streams)
        if stream.metaData.user is None:
            return True
        
        # Check if user owns the stream
        return stream.metaData.user.get_uuid() == user.get_uuid()

    def get_stream_flow_graph(self):
        """
        TODO finish this
        """
        edges = []  # tuples of (source_agent, stream, target_agent)
        for name, stream in self.streams:
            source_agent = stream.source_agent
            target_agents = stream.get_registered_agents()
            for target_agent in target_agents:
                edges.append((source_agent, stream, target_agent))
        return edges

    def wait_all_stream_clear(self, user):
        from chainstream.llm import check_has_model_working
        # TODO: use threading.Event to wait for all streams to be clear
        count = 5
        while True:
            # print(f"count: {count}")
            if all(stream.is_clear.is_set() for stream in self.streams.values()) and not check_has_model_working():
                # print(f"coundown {count}")
                count -= 1
                if count == 0:
                    return True
            else:
                count = 5
            time.sleep(1)

    def shutdown(self):

        reset_stream()

        # print(self.thread_list)
        for stream in self.streams.values():
            stream.shutdown()
        # print(self.thread_list)
        for thread in self.thread_list.values():
            if thread.is_alive():
                thread.join()

        self.streams = collections.OrderedDict()

        return True
