from ..core import chainstream_core
from ..auth.auth import require_auth
from chainstream.runtime.user_context import user_context_manager
from flask import jsonify, Blueprint, request
import logging
import os
import json
import datetime

logger = logging.getLogger(__name__)

agents_blueprint = Blueprint('agents_blueprint', __name__)


@agents_blueprint.route('/api/monitor/agents', methods=['GET'])
@require_auth
def get_predefined_agents(current_user):
    """
    Get predefined agents (filtered by user level)
    """
    data = chainstream_core.scan_predefined_agents_tree()
    return jsonify(data)


@agents_blueprint.route('/api/monitor/agents/getRunningAgents', methods=['GET'])
@require_auth
def get_running_agents(current_user):
    """
    Get running agents (filtered by user)
    """
    logger.info(f"get_running_agents API called with current_user: {current_user}")
    if current_user:
        logger.info(f"Current user UUID: {current_user.get_uuid()}")
    else:
        logger.info("Current user is None!")
    
    # Get agents filtered by current user
    data = chainstream_core.agent_manager.get_running_agents_info_list(current_user)
    logger.info(f"Returning {len(data)} agents")
    return jsonify(data)


@agents_blueprint.route('/api/monitor/agents/all', methods=['GET'])
@require_auth
def get_all_running_agents(current_user):
    """
    Get all running agents (admin only)
    """
    # Check if user has admin privileges
    if current_user.get_level() < 10:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    # Get all agents without filtering
    data = chainstream_core.agent_manager.get_running_agents_info_list()
    return jsonify(data)


@agents_blueprint.route('/api/monitor/agents/start/<agent_id>', methods=['POST'])
@require_auth
def start_agent(agent_id, current_user):
    # Set user context before starting agent - don't use with statement to avoid clearing context
    user_context_manager.set_current_user(current_user)
    res = chainstream_core.start_agent_by_id(agent_id, current_user)

    return jsonify({'res': "ok"} if res else {'res': "error"})


@agents_blueprint.route('/api/monitor/agents/stop/<agent_id>', methods=['POST'])
@require_auth
def stop_agent(agent_id, current_user):
    res = chainstream_core.stop_agent_by_id(agent_id, current_user)

    return jsonify({'res': "ok"} if res else {'res': "error"})


@agents_blueprint.route('/api/monitor/agents/code/<path:agent_path>', methods=['GET'])
@require_auth
def get_agent_code(agent_path, current_user):
    """
    Get agent code content by file path
    """
    try:
        import os
        import mimetypes
        from pathlib import Path
        
        # 解码URL路径
        from urllib.parse import unquote
        agent_path = unquote(agent_path)
        
        # 如果路径不是绝对路径，尝试在predefined_agents_path中查找
        if not os.path.isabs(agent_path):
            # 获取AgentStore路径
            predefined_agents_path = chainstream_core.agent_manager.predefined_agents_path
            full_path = os.path.join(predefined_agents_path, agent_path)
            logger.info(f"Looking for file: {agent_path} in {predefined_agents_path}")
            logger.info(f"Full path: {full_path}")
        else:
            full_path = agent_path
        
        # 检查文件是否存在
        if not os.path.exists(full_path):
            logger.error(f"File not found: {full_path}")
            # 尝试在AgentStore中递归查找文件
            if not os.path.isabs(agent_path):
                predefined_agents_path = chainstream_core.agent_manager.predefined_agents_path
                found_file = None
                for root, dirs, files in os.walk(predefined_agents_path):
                    if os.path.basename(agent_path) in files:
                        found_file = os.path.join(root, os.path.basename(agent_path))
                        break
                
                if found_file:
                    full_path = found_file
                    logger.info(f"Found file by name: {full_path}")
                else:
                    return jsonify({'error': f'File not found: {agent_path}'}), 404
            else:
                return jsonify({'error': f'File not found: {agent_path}'}), 404
        
        # 检查文件类型
        mime_type, _ = mimetypes.guess_type(full_path)
        if not mime_type or not mime_type.startswith('text/'):
            return jsonify({'error': 'File is not a text file'}), 400
        
        # 读取文件内容
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 确定语言类型
        language = 'text'
        if full_path.endswith('.py'):
            language = 'python'
        elif full_path.endswith('.java'):
            language = 'java'
        elif full_path.endswith('.js'):
            language = 'javascript'
        elif full_path.endswith('.ts'):
            language = 'typescript'
        elif full_path.endswith('.vue'):
            language = 'vue'
        elif full_path.endswith('.html'):
            language = 'html'
        elif full_path.endswith('.css'):
            language = 'css'
        elif full_path.endswith('.scss'):
            language = 'scss'
        elif full_path.endswith('.json'):
            language = 'json'
        elif full_path.endswith('.xml'):
            language = 'xml'
        elif full_path.endswith('.yaml') or full_path.endswith('.yml'):
            language = 'yaml'
        
        logger.info(f"Successfully loaded file: {full_path}, language: {language}")
        
        return jsonify({
            'content': content,
            'language': language,
            'filename': os.path.basename(full_path),
            'path': full_path
        })
        
    except Exception as e:
        logger.error(f"Error reading agent code: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@agents_blueprint.route('/api/monitor/agents/directory', methods=['GET'])
@require_auth
def get_agentstore_directory(current_user):
    """
    Get AgentStore directory structure
    """
    try:
        import os
        from pathlib import Path
        
        # 获取AgentStore路径
        predefined_agents_path = chainstream_core.agent_manager.predefined_agents_path
        logger.info(f"AgentStore path: {predefined_agents_path}")
        
        # 获取请求的路径参数
        from flask import request
        relative_path = request.args.get('path', '')
        
        # 构建完整路径
        if relative_path:
            full_path = os.path.join(predefined_agents_path, relative_path)
        else:
            full_path = predefined_agents_path
        
        # 确保路径在AgentStore内（安全检查）
        full_path = os.path.abspath(full_path)
        predefined_agents_path = os.path.abspath(predefined_agents_path)
        
        if not full_path.startswith(predefined_agents_path):
            return jsonify({'error': 'Access denied: Path outside AgentStore'}), 403
        
        # 检查路径是否存在
        if not os.path.exists(full_path):
            return jsonify({'error': 'Path not found'}), 404
        
        # 检查是否为目录
        if not os.path.isdir(full_path):
            return jsonify({'error': 'Path is not a directory'}), 400
        
        # 读取目录内容
        items = []
        try:
            for item_name in sorted(os.listdir(full_path)):
                item_path = os.path.join(full_path, item_name)
                
                # 跳过隐藏文件和__pycache__目录
                if item_name.startswith('.') or item_name == '__pycache__':
                    continue
                
                is_directory = os.path.isdir(item_path)
                size = 0
                
                if not is_directory:
                    # 只显示Python和Java文件
                    if not item_name.endswith(('.py', '.java')):
                        continue
                    try:
                        size = os.path.getsize(item_path)
                    except OSError:
                        size = 0
                
                # 计算相对路径
                rel_path = os.path.relpath(item_path, predefined_agents_path)
                if rel_path == '.':
                    rel_path = ''
                
                items.append({
                    'name': item_name,
                    'isDirectory': is_directory,
                    'size': size,
                    'relativePath': rel_path.replace('\\', '/')  # 统一使用正斜杠
                })
        except PermissionError:
            return jsonify({'error': 'Permission denied'}), 403
        
        # 计算当前路径的各个部分
        current_path = os.path.relpath(full_path, predefined_agents_path)
        if current_path == '.':
            current_path = ''
        
        path_segments = []
        if current_path:
            path_segments = current_path.split(os.sep)
            # 过滤空字符串
            path_segments = [seg for seg in path_segments if seg]
        
        logger.info(f"Directory listing for {relative_path}: {len(items)} items")
        
        return jsonify({
            'items': items,
            'currentPath': current_path.replace('\\', '/'),
            'pathSegments': path_segments,
            'agentStorePath': predefined_agents_path
        })
        
    except Exception as e:
        logger.error(f"Error reading AgentStore directory: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@agents_blueprint.route('/api/generator/chat', methods=['POST'])
@require_auth
def generator_chat(current_user):
    """生成器对话接口：输入 message+code，输出 reply+new_code+stats（模拟实现）"""
    try:
        from flask import request
        import time
        start_ts = time.time()

        data = request.get_json(silent=True) or {}
        message = (data.get('message') or '').strip()
        code = data.get('code') or ''
        language = (data.get('language') or 'python').lower()
        path = data.get('path') or ''
        memory = data.get('memory') or ''
        generator_type = (data.get('generator_type') or '').strip()  # 'python_single' | 'java_single' | others

        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400

        # —— 实际/模拟生成逻辑 ——
        new_code = None
        used_generator = None
        # 如未指定generator_type，则按language推断
        if not generator_type:
            generator_type = 'java_single' if language == 'java' else 'python_single'
        #TODO: 后续可增加更多generator_type，如feedback
        if generator_type in ('python_single', 'java_single', 'python_feedback'):
            try:
                # 准备导入路径，确保项目根在sys.path
                import sys
                repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../'))
                if repo_root not in sys.path:
                    sys.path.insert(0, repo_root)
                
                # 提取反馈相关参数
                ## 新增加
                max_loop = data.get('max_loop', 20)
                only_print_last = data.get('only_print_last', False)
                sandbox_type = data.get('sandbox_type', 'chainstream')
                
                if generator_type == 'python_single':
                    from AgentGenerator.generator.stream_mode.chainstream_chat_generator_python import ChainStreamChatGeneratorPython
                    from AgentGenerator.io_model import StreamListDescription
                    used_generator = 'python_single'
                    gen = ChainStreamChatGeneratorPython()
                elif generator_type == 'python_feedback':
                    from AgentGenerator.generator.stream_mode.chainstream_chat_generator_python_feedback import ChainStreamChatGeneratorPythonFeedback
                    from AgentGenerator.io_model import StreamListDescription
                    used_generator = 'python_feedback'
                    ##新增加
                    gen = ChainStreamChatGeneratorPythonFeedback(
                        framework_example_number=data.get('framework_example_number', 0),
                        base_prompt_example_select_policy=data.get('base_prompt_example_select_policy', 'random'),
                        max_loop=max_loop,
                        sandbox_type=sandbox_type,
                        only_print_last=only_print_last
                    )
                else:
                    from AgentGenerator.generator.stream_mode.chainstream_chat_generator_java import ChainStreamChatGeneratorJava
                    from AgentGenerator.io_model import StreamListDescription
                    used_generator = 'java_single'
                    gen = ChainStreamChatGeneratorJava()

                # 构造最小可用的流描述，占位用
                output_desc = StreamListDescription(streams=[{
                    "stream_id": "generated_output",
                    "description": "Generated agent output (placeholder)",
                    "fields": {"result": "string"}
                }])
                input_desc = StreamListDescription(streams=[{
                    "stream_id": "source",
                    "description": "Current context (placeholder)",
                    "fields": {"text": "string"}
                }])
                
                # 构造 chat_message 字典，包含 history、code、message
                chat_message_dict = {
                    'history': memory,
                    'code': code,
                    'message': message
                }
                
                # 根据生成器类型调用相应的方法
                ## 新增加
                print(f"Calling feedback generator with max_loop={max_loop}, only_print_last={only_print_last}, sandbox_type={sandbox_type}")
                print(generator_type)
                print(generator_type== 'python_feedback')
                if generator_type == 'python_feedback':
                    print(f"Calling feedback generator with max_loop={max_loop}, only_print_last={only_print_last}, sandbox_type={sandbox_type}")
                    result = gen.generate_agent_chat_with_feedback(
                        message=chat_message_dict,
                        output_description=output_desc,
                        input_description=input_desc
                    )
                    agent_code, latency, tokens, loop_count, feedback_history = result
                    feedback_info = {
                        'loop_count': loop_count,
                        'feedback_history': feedback_history
                    }
                else:
                    agent_code, latency, tokens = gen.generate_agent_chat(
                        message=chat_message_dict,
                        output_description=output_desc,
                        input_description=input_desc
                    )
                    feedback_info = {}
                
                new_code = agent_code or ''
                
                # 获取额外的元数据（new_history 和 message_to_user）
                metadata = gen.get_last_response_metadata()
                new_memory = metadata.get('new_history', '')
                reply = metadata.get('message_to_user', '')
                print(f"Generator metadata: {metadata}")
                print(f"Generator reply: {reply}")
                print(f"Generator new_memory: {new_memory}")
                # 统计来自生成器
                elapsed_ms = int(float(latency) * 1000) if latency is not None else None
                pt = ct = tt = None
                if isinstance(tokens, (list, tuple)) and len(tokens) >= 2:
                    pt_raw, ct_raw = tokens[0], tokens[1]
                    try:
                        pt = int(pt_raw)
                    except Exception:
                        pt = None
                    try:
                        ct = int(ct_raw)
                    except Exception:
                        ct = None
                    if pt is not None and ct is not None:
                        tt = pt + ct
                elif isinstance(tokens, int):
                    tt = tokens
                gen_stats = {
                    'prompt_tokens': pt,
                    'completion_tokens': ct,
                    'total_tokens': tt,
                    'elapsed_ms': elapsed_ms,
                    'model': f'agent-generator:{used_generator}'
                }
                
                # 为反馈模式添加额外信息
                ##新增加
                if feedback_info:
                    gen_stats['loop_count'] = feedback_info.get('loop_count', 0)
                
                # 成功生成，直接返回
                ## 新增加
                response_data = {
                    'success': True,
                    'reply': reply,
                    'new_code': new_code,
                    'stats': gen_stats,
                    'new_memory': new_memory
                }
                
                # 为反馈模式添加反馈历史
                ## 新增加
                if feedback_info and 'feedback_history' in feedback_info:
                    response_data['feedback_history'] = feedback_info['feedback_history']
                print(response_data)
                return jsonify(response_data)
            except Exception as gen_err:
                logger.warning(f"Generator integration failed, fallback to mock. Error: {gen_err}")
                raise RuntimeError(f"Generator integration failed, fallback to mock. Error: {gen_err}")
        else:
            used_generator = generator_type  # sandbox_iter / exception_handler -> 暂未实现，走mock

        # 若未成功生成，使用mock回退逻辑（阻塞式）
        if new_code is None:
            # 允许前端通过 delay_ms 控制模拟耗时（毫秒），否则按输入规模估算，最大不超过30s
            try:
                delay_ms = int(data.get('delay_ms')) if 'delay_ms' in data else None
            except Exception:
                delay_ms = None
            if delay_ms is None:
                delay_ms = min(30000, max(600, 300 + len(message) * 20 + (len(code) // 40)))
            time.sleep(delay_ms / 1000.0)
            suffix_comment = {
                'python': f"\n\n# Generated note: handled message -> {message}",
                'java': f"\n\n// Generated note: handled message -> {message}",
            }.get(language, f"\n\n// Generated note: handled message -> {message}")
            new_code = (code or '') + suffix_comment

        # 生成新的 memory（模拟）：基于上一段memory、当前语言与消息摘要
        summary_msg = message[:80].replace('\n', ' ')
        new_memory = f"[{language}] last_msg='{summary_msg}' | code_len={len(code)} | prev_mem_len={len(memory)}"

        reply = (
            f"已处理你的请求：{message}\n"
            f"语言：{language}，当前文件：{path or '未命名'}\n"
            f"代码变更：在末尾添加了说明注释（模拟）。"
        )

        # 统计（模拟）
        elapsed_ms = int((time.time() - start_ts) * 1000)
        if used_generator and used_generator != 'mock' and 'gen_stats' in locals() and gen_stats.get('elapsed_ms') is not None:
            stats = gen_stats
            # 补齐缺失字段
            stats['elapsed_ms'] = stats.get('elapsed_ms', elapsed_ms)
            stats['total_tokens'] = stats.get('total_tokens') or stats.get('completion_tokens')
        else:
            stats = {
                'prompt_tokens': max(1, (len(message) + len(code) // 2) // 4),
                'completion_tokens': max(1, (len(new_code) - len(code)) // 4),
                'total_tokens': max(2, (len(message) + len(new_code)) // 4),
                'elapsed_ms': elapsed_ms,
                'model': 'mock-generator-v1'
            }

        return jsonify({
            'success': True,
            'reply': reply,
            'new_code': new_code,
            'stats': stats,
            'new_memory': new_memory
        })
    except Exception as e:
        logger.error(f"generator_chat error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@agents_blueprint.route('/api/generator/security-check', methods=['POST'])
@require_auth
def security_check(current_user):
    """
    使用 LLM 检查代码、消息和记忆中的安全问题
    """
    try:
        from flask import request
        import time
        
        data = request.get_json(silent=True) or {}
        code = data.get('code', '')
        messages = data.get('messages', [])
        memory = data.get('memory', '')
        
        # 构建检查内容摘要
        messages_text = '\n'.join([
            f"[{msg.get('role', 'unknown')}]: {msg.get('content', '')[:500]}" 
            for msg in messages[-10:]  # 只检查最近10条消息
        ])
        
        # 构建 prompt
        security_prompt = f"""请对以下Agent代码生成会话的内容进行安全审查，检查是否存在以下问题：

1. **暴力内容**：包含暴力、血腥、伤害等不当内容
2. **违规内容**：包含违法、犯罪、欺诈等违规内容
3. **隐私泄露**：包含敏感的个人信息（如密码、密钥、身份证号、手机号等）
4. **恶意代码**：包含可能造成系统损害的恶意代码（如删除文件、窃取数据等）

请分别检查以下三个部分：

### 代码内容（Code）:
```
{code[:3000] if code else '（无代码）'}
```

### 对话消息（Messages）:
```
{messages_text[:2000] if messages_text else '（无消息）'}
```

### 会话记忆（Memory）:
```
{memory[:1500] if memory else '（无记忆）'}
```

请按照以下JSON格式返回检查结果（只返回JSON，不要其他内容）：
{{
    "code_check": {{
        "safe": true/false,
        "issues": ["问题1", "问题2"],
        "details": "详细说明"
    }},
    "messages_check": {{
        "safe": true/false,
        "issues": ["问题1"],
        "details": "详细说明"
    }},
    "memory_check": {{
        "safe": true/false,
        "issues": [],
        "details": "详细说明"
    }},
    "overall_safe": true/false,
    "summary": "总体评估摘要"
}}

如果某个部分没有内容或完全安全，请将 safe 设为 true，issues 设为空数组。"""

        start_time = time.time()
        
        # 调用 LLM
        import json
        import re
        
        try:
            from chainstream.llm import get_model, make_prompt
            llm = get_model('text')
            
            # 使用 make_prompt 构建正确的消息格式
            prompt = make_prompt(security_prompt)
            
            response = llm.query(prompt)
            
            # 尝试解析 JSON 响应
            # 提取 JSON（可能被包裹在 markdown 代码块中）
            json_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', response)
            if json_match:
                json_str = json_match.group(1)
            else:
                # 尝试直接解析
                json_str = response.strip()
            
            result = json.loads(json_str)
            
            elapsed_ms = int((time.time() - start_time) * 1000)
            
            return jsonify({
                'success': True,
                'result': result,
                'elapsed_ms': elapsed_ms
            })
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            if 'response' in locals():
                logger.error(f"LLM response: {response}")
            
            # 如果解析失败，返回原始响应
            return jsonify({
                'success': False,
                'error': 'LLM返回格式错误',
                'raw_response': response[:1000] if 'response' in locals() else 'No response'
            }), 500
            
        except Exception as e:
            logger.error(f"Error calling LLM for security check: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': f'LLM调用失败: {str(e)}'
            }), 500
            
    except Exception as e:
        logger.error(f"security_check error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@agents_blueprint.route('/api/generator/info', methods=['GET'])
@require_auth
def get_generator_info(current_user):
    """
    Get information about available code generators and their configurations
    """
    try:
        generators_info = {
            'generators': {
                'python_single': {
                    'name': 'Python Single-Shot Generator',
                    'description': 'Generate agent code in a single LLM call',
                    'language': 'python',
                    'parameters': [
                        {
                            'name': 'framework_example_number',
                            'type': 'integer',
                            'default': 0,
                            'min': 0,
                            'max': 10,
                            'description': 'Number of framework examples to use'
                        },
                        {
                            'name': 'base_prompt_example_select_policy',
                            'type': 'string',
                            'default': 'random',
                            'options': ['random', 'sequential'],
                            'description': 'Strategy for selecting prompt examples'
                        }
                    ],
                    'features': ['code_generation'],
                    'sandbox_support': False
                },
                'python_feedback': {
                    'name': 'Python Feedback-Guided Generator',
                    'description': 'Iteratively generate and refine agent code based on sandbox feedback',
                    'language': 'python',
                    'parameters': [
                        {
                            'name': 'framework_example_number',
                            'type': 'integer',
                            'default': 0,
                            'min': 0,
                            'max': 10,
                            'description': 'Number of framework examples to use'
                        },
                        {
                            'name': 'base_prompt_example_select_policy',
                            'type': 'string',
                            'default': 'random',
                            'options': ['random', 'sequential'],
                            'description': 'Strategy for selecting prompt examples'
                        },
                        {
                            'name': 'max_loop',
                            'type': 'integer',
                            'default': 20,
                            'min': 1,
                            'max': 50,
                            'description': 'Maximum number of refinement iterations'
                        },
                        {
                            'name': 'sandbox_type',
                            'type': 'string',
                            'default': 'chainstream',
                            'options': ['chainstream'],
                            'description': 'Type of sandbox to use for testing'
                        },
                        {
                            'name': 'only_print_last',
                            'type': 'boolean',
                            'default': False,
                            'description': 'Only print the final iteration (less verbose)'
                        }
                    ],
                    'features': ['code_generation', 'iterative_refinement', 'sandbox_feedback', 'history_tracking'],
                    'sandbox_support': True
                },
                'java_single': {
                    'name': 'Java Single-Shot Generator',
                    'description': 'Generate Java agent code in a single LLM call',
                    'language': 'java',
                    'parameters': [],
                    'features': ['code_generation'],
                    'sandbox_support': False
                }
            }
        }
        
        return jsonify(generators_info)
    except Exception as e:
        logger.error(f"Error getting generator info: {e}")
        return jsonify({'error': str(e)}), 500


@agents_blueprint.route('/api/generator/feedback-history', methods=['POST'])
@require_auth
def save_generation_history(current_user):
    """
    Save generation session history for later retrieval
    """
    try:
        from flask import request
        import json
        data = request.get_json(silent=True) or {}
        
        session_id = data.get('session_id')
        feedback_history = data.get('feedback_history')
        generator_type = data.get('generator_type', 'unknown')
        message = data.get('message', '')
        final_code = data.get('final_code', '')
        stats = data.get('stats', {})
        
        if not session_id or not feedback_history:
            return jsonify({'error': 'session_id and feedback_history are required'}), 400
        
        # Store in user's context or session storage
        # This is a simple implementation - in production, use database
        history_storage_path = os.path.join(
            os.path.dirname(__file__), 
            '../../../../.generation_history',
            f"{current_user.get_uuid()}"
        )
        os.makedirs(history_storage_path, exist_ok=True)
        
        history_file = os.path.join(history_storage_path, f"{session_id}.json")
        
        history_data = {
            'session_id': session_id,
            'user_id': current_user.get_uuid(),
            'generator_type': generator_type,
            'message': message,
            'final_code': final_code,
            'feedback_history': feedback_history,
            'stats': stats,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved generation history: {session_id} for user {current_user.get_uuid()}")
        return jsonify({'success': True, 'session_id': session_id})
        
    except Exception as e:
        logger.error(f"Error saving generation history: {e}")
        return jsonify({'error': str(e)}), 500


@agents_blueprint.route('/api/generator/feedback-history/<session_id>', methods=['GET'])
@require_auth
def get_generation_history(session_id, current_user):
    """
    Retrieve saved generation session history
    """
    try:
        history_storage_path = os.path.join(
            os.path.dirname(__file__), 
            '../../../../.generation_history',
            f"{current_user.get_uuid()}"
        )
        
        history_file = os.path.join(history_storage_path, f"{session_id}.json")
        
        if not os.path.exists(history_file):
            return jsonify({'error': 'History not found'}), 404
        
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
        
        return jsonify(history_data)
        
    except Exception as e:
        logger.error(f"Error retrieving generation history: {e}")
        return jsonify({'error': str(e)}), 500


@agents_blueprint.route('/api/generator/user-histories', methods=['GET'])
@require_auth
def get_user_generation_histories(current_user):
    """
    Get user's generation history list
    Query params:
    - limit: max results (default: 20)
    - offset: pagination offset (default: 0)
    - generator_type: filter by generator type
    """
    try:
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        generator_type = request.args.get('generator_type')
        
        history_storage_path = os.path.join(
            os.path.dirname(__file__), 
            '../../../../.generation_history',
            f"{current_user.get_uuid()}"
        )
        
        if not os.path.exists(history_storage_path):
            return jsonify({'total': 0, 'items': [], 'limit': limit, 'offset': offset})
        
        # Get all history files
        history_files = []
        try:
            for filename in os.listdir(history_storage_path):
                if filename.endswith('.json'):
                    history_files.append(filename)
        except Exception as e:
            logger.warning(f"Error listing history files: {e}")
            history_files = []
        
        # Sort by modification time (newest first)
        history_files.sort(
            key=lambda f: os.path.getmtime(os.path.join(history_storage_path, f)),
            reverse=True
        )
        
        # Load and filter histories
        items = []
        for filename in history_files:
            try:
                with open(os.path.join(history_storage_path, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Apply filter
                if generator_type and data.get('generator_type') != generator_type:
                    continue
                
                # Extract summary info
                items.append({
                    'session_id': data.get('session_id'),
                    'generator_type': data.get('generator_type'),
                    'timestamp': data.get('timestamp'),
                    'message_preview': (data.get('message') or '')[:100],
                    'loop_count': data.get('stats', {}).get('loop_count'),
                    'total_tokens': data.get('stats', {}).get('total_tokens'),
                    'elapsed_ms': data.get('stats', {}).get('elapsed_ms')
                })
            except Exception as e:
                logger.warning(f"Error loading history file {filename}: {e}")
                continue
        
        # Apply pagination
        total = len(items)
        paginated_items = items[offset:offset + limit]
        
        return jsonify({
            'total': total,
            'items': paginated_items,
            'limit': limit,
            'offset': offset
        })
        
    except Exception as e:
        logger.error(f"Error getting user generation histories: {e}")
        return jsonify({'error': str(e)}), 500


@agents_blueprint.route('/api/generator/save', methods=['POST'])
@require_auth
def save_generated_code(current_user):
    """
    Save generated code to a file
    """
    try:
        from flask import request
        data = request.get_json()
        
        file_path = data.get('file_path')
        content = data.get('content')
        language = data.get('language', 'python')
        allow_overwrite = data.get('allow_overwrite', False)
        
        if not file_path:
            return jsonify({'error': 'File path is required'}), 400
        
        # 允许空内容（新建空文件）
        if content is None:
            content = ''
        
        # 确保文件路径在AgentStore内（安全检查）
        predefined_agents_path = chainstream_core.agent_manager.predefined_agents_path
        full_path = os.path.abspath(os.path.join(predefined_agents_path, file_path))
        predefined_agents_path = os.path.abspath(predefined_agents_path)
        
        if not full_path.startswith(predefined_agents_path):
            return jsonify({'error': 'Access denied: Path outside AgentStore'}), 403
        
        # 检查文件是否已存在（仅在不允许覆盖时）
        if os.path.exists(full_path) and not allow_overwrite:
            return jsonify({'error': f'文件已存在: {file_path}'}), 400
        
        # 确保目录存在
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # 写入文件
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Code saved to {full_path} by user {current_user.get_username()}")
        return jsonify({'success': True, 'message': 'Code saved successfully'})
        
    except Exception as e:
        logger.error(f"Error saving code: {e}")
        return jsonify({'error': str(e)}), 500


@agents_blueprint.route('/api/generator/scan', methods=['GET'])
@require_auth
def scan_agentstore_for_generator(current_user):
    """
    Scan AgentStore for code generation
    """
    try:
        # 获取AgentStore路径
        predefined_agents_path = chainstream_core.agent_manager.predefined_agents_path
        logger.info(f"Scanning AgentStore path: {predefined_agents_path}")
        
        # 递归扫描目录
        def scan_directory(path, relative_path=""):
            items = []
            try:
                for item_name in sorted(os.listdir(path)):
                    item_path = os.path.join(path, item_name)
                    item_relative_path = os.path.join(relative_path, item_name) if relative_path else item_name
                    
                    if os.path.isdir(item_path):
                        # 跳过隐藏目录和__pycache__
                        if item_name.startswith('.') or item_name == '__pycache__':
                            continue
                        
                        children = scan_directory(item_path, item_relative_path)
                        items.append({
                            'name': item_name,
                            'path': item_relative_path,
                            'isDirectory': True,
                            'children': children
                        })
                    else:
                        # 只包含Python和Java文件
                        if item_name.endswith(('.py', '.java')):
                            stat = os.stat(item_path)
                            items.append({
                                'name': item_name,
                                'path': item_relative_path,
                                'isDirectory': False,
                                'size': format_file_size(stat.st_size),
                                'modified': stat.st_mtime
                            })
            except PermissionError:
                logger.warning(f"Permission denied accessing {path}")
            except Exception as e:
                logger.error(f"Error scanning {path}: {e}")
            
            return items
        
        def format_file_size(size_bytes):
            """格式化文件大小"""
            if size_bytes == 0:
                return "0 B"
            size_names = ["B", "KB", "MB", "GB"]
            i = 0
            while size_bytes >= 1024 and i < len(size_names) - 1:
                size_bytes /= 1024.0
                i += 1
            return f"{size_bytes:.1f} {size_names[i]}"
        
        # 扫描AgentStore
        items = scan_directory(predefined_agents_path)
        
        return jsonify({
            'success': True,
            'items': items,
            'path': str(predefined_agents_path)
        })
        
    except Exception as e:
        logger.error(f"Error scanning AgentStore: {e}")
        return jsonify({'error': str(e)}), 500


@agents_blueprint.route('/api/generator/load', methods=['GET'])
@require_auth
def load_file_for_generator(current_user):
    """
    Load file content for code generation
    """
    try:
        import os
        from flask import request
        file_path = request.args.get('path')
        
        if not file_path:
            return jsonify({'error': 'File path is required'}), 400
        
        # 确保文件路径在AgentStore内（安全检查）
        predefined_agents_path = chainstream_core.agent_manager.predefined_agents_path
        full_path = os.path.abspath(os.path.join(predefined_agents_path, file_path))
        predefined_agents_path = os.path.abspath(predefined_agents_path)
        
        if not full_path.startswith(predefined_agents_path):
            return jsonify({'error': 'Access denied: Path outside AgentStore'}), 403
        
        # 检查文件是否存在
        if not os.path.exists(full_path):
            return jsonify({'error': 'File not found'}), 404
        
        # 检查是否为文件
        if not os.path.isfile(full_path):
            return jsonify({'error': 'Path is not a file'}), 400
        
        # 读取文件内容
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检测文件类型（只支持Python和Java）
        file_extension = os.path.splitext(full_path)[1].lower()
        if file_extension == '.py':
            language = 'python'
        elif file_extension == '.java':
            language = 'java'
        else:
            # 不支持的文件类型
            return jsonify({'error': 'Unsupported file type. Only .py and .java files are supported.'}), 400
        
        return jsonify({
            'success': True,
            'content': content,
            'language': language,
            'path': file_path
        })
        
    except Exception as e:
        logger.error(f"Error loading file: {e}")
        return jsonify({'error': str(e)}), 500
