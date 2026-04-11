"""
Java Agent Executor - 处理Java Agent的编译、启动和桥接
"""
import os
import subprocess
import logging
import tempfile
import shutil
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class JavaAgentExecutor:
    """Java Agent执行器，负责编译和启动Java Agent"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.JavaAgentExecutor")
        self.java_home = self._detect_java_home()
        self.javac_path = os.path.join(self.java_home, 'bin', 'javac')
        self.java_path = os.path.join(self.java_home, 'bin', 'java')
        self.javap_path = os.path.join(self.java_home, 'bin', 'javap')
        self.bridge_server = None
    
    def _detect_java_home(self) -> str:
        """检测Java安装路径"""
        java_home = os.environ.get('JAVA_HOME')
        if java_home and os.path.exists(java_home):
            return java_home
        
        # 尝试通过java命令找到Java路径
        try:
            result = subprocess.run(['java', '-XshowSettings:properties', '-version'], 
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in result.stdout.split('\n'):
                if 'java.home' in line:
                    java_home = line.split('=')[1].strip()
                    if os.path.exists(java_home):
                        return java_home
        except Exception as e:
            self.logger.warning(f"Failed to detect Java home: {e}")
        
        # 默认路径
        default_paths = [
            '/usr/lib/jvm/java-11-openjdk',
            '/usr/lib/jvm/java-8-openjdk',
            '/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home',
            '/Library/Java/JavaVirtualMachines/jdk-8.jdk/Contents/Home'
        ]
        
        for path in default_paths:
            if os.path.exists(path):
                return path
        
        raise RuntimeError("Java not found. Please set JAVA_HOME environment variable.")
    
    def start_java_agent(self, java_file_path: str, user=None, runtime_core=None):
        """
        启动Java Agent
        
        Args:
            java_file_path: Java文件路径
            user: 用户对象
            runtime_core: Runtime核心实例
            
        Returns:
            JavaAgentWrapper: Java Agent包装器对象
        """
        try:
            self.logger.info(f"🚀 Starting Java agent from file: {java_file_path}")
            self.logger.info(f"📁 Java file exists: {os.path.exists(java_file_path)}")
            
            # 1. 编译Java文件
            self.logger.info("🔨 Step 1: Compiling Java file...")
            class_file = self._compile_java_file(java_file_path)
            self.logger.info(f"✅ Compilation successful, class file: {class_file}")
            
            # 2. 启动Java进程
            self.logger.info("🏃 Step 2: Starting Java process...")
            java_process = self._start_java_process(class_file)
            self.logger.info(f"✅ Java process started with PID: {java_process.pid}")
            
            # 3. 创建Java Agent包装器
            self.logger.info("📦 Step 3: Creating Java Agent wrapper...")
            from .java_agent_wrapper import JavaAgentWrapper
            java_agent_wrapper = JavaAgentWrapper(java_process, java_file_path, user, runtime_core)
            
            self.logger.info(f"🎉 Java agent started successfully: {java_agent_wrapper.agent_id}")
            return java_agent_wrapper
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start Java agent: {e}")
            import traceback
            self.logger.error(f"❌ Full traceback: {traceback.format_exc()}")
            raise
    
    def _compile_java_file(self, java_file_path: str) -> str:
        """编译Java文件 - 使用Maven构建"""
        try:
            self.logger.debug(f"Compiling Java file: {java_file_path}")
            
            # 检查Java文件是否存在
            if not os.path.exists(java_file_path):
                raise FileNotFoundError(f"Java file not found: {java_file_path}")
            
            # 获取Java项目根目录
            java_project_root = os.path.dirname(__file__)
            
            # 检查Maven是否可用
            if not self._check_maven_available():
                self.logger.warning("Maven not available, falling back to simple javac compilation")
                return self._compile_with_javac(java_file_path)
            
            # 使用Maven编译
            return self._compile_with_maven(java_file_path, java_project_root)
            
        except Exception as e:
            self.logger.error(f"Java compilation error: {e}")
            raise
    
    def _check_maven_available(self) -> bool:
        """检查Maven是否可用"""
        try:
            result = subprocess.run(['mvn', '--version'], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _compile_with_maven(self, java_file_path: str, java_project_root: str) -> str:
        """使用Maven编译Java文件"""
        target_file = None
        self._temp_source_file = None  # 初始化临时文件路径
        try:
            # 将Java文件复制到Maven项目的src/main/java目录
            target_dir = os.path.join(java_project_root, 'src', 'main', 'java', 'com', 'chainstream', 'agent')
            os.makedirs(target_dir, exist_ok=True)
            
            # 复制Java文件到Maven项目
            target_file = os.path.join(target_dir, os.path.basename(java_file_path))
            self.logger.info(f"Copying Java file from {java_file_path} to {target_file}")
            shutil.copy2(java_file_path, target_file)
            self.logger.info(f"Java file copied successfully")
            
            # 在Maven项目根目录执行编译
            # 使用两阶段编译避免protobuf生成的竞态条件：
            # 阶段1: clean + 生成protobuf代码
            # 阶段2: 编译Java代码
            
            # 阶段1: 清理并生成protobuf代码
            mvn_cmd_proto = ['mvn', '-DskipTests=true', 'clean', 'protobuf:compile', 'protobuf:compile-custom']
            self.logger.debug(f"🛠️ Phase 1 - Generating protobuf: {' '.join(mvn_cmd_proto)} in {java_project_root}")
            result_proto = subprocess.run(mvn_cmd_proto, 
                                  cwd=java_project_root,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # 检查protobuf生成是否成功
            if result_proto.returncode != 0:
                error_msg = f"Protobuf generation failed (return code {result_proto.returncode}): {result_proto.stderr}"
                self.logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            self.logger.debug(f"✅ Protobuf code generated successfully")
            
            # 阶段2: 编译Java代码
            mvn_cmd_compile = ['mvn', '-DskipTests=true', 'compile']
            self.logger.debug(f"🛠️ Phase 2 - Compiling Java: {' '.join(mvn_cmd_compile)} in {java_project_root}")
            result = subprocess.run(mvn_cmd_compile, 
                                  cwd=java_project_root,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # 记录警告信息
            if (result.stderr and "WARNING" in result.stderr.upper()) or (result.stdout and "WARNING" in result.stdout.upper()):
                warn_txt = (result.stderr or '') + '\n' + (result.stdout or '')
                self.logger.warning(f"Maven compilation warnings: {warn_txt}")
            
            # 只检查返回码，Maven成功时返回码为0
            # 注意：Maven的警告不会导致返回码非0，只有真正的错误才会
            if result.returncode != 0:
                error_msg = f"Maven compilation failed (return code {result.returncode}): {result.stderr}"
                self.logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            # 查找生成的class文件
            class_name = os.path.splitext(os.path.basename(java_file_path))[0]
            class_file = os.path.join(java_project_root, 'target', 'classes', 'com', 'chainstream', 'agent', f'{class_name}.class')
            
            # 等待一下确保class文件完全生成
            import time
            time.sleep(0.1)
            
            if not os.path.exists(class_file):
                raise RuntimeError(f"Class file not generated: {class_file}")
            
            self.logger.debug(f"Maven compilation successful: {class_file}")
            
            # 🔴 不要立即删除临时源文件！
            # Maven在某些情况下会触发增量编译检查，如果源文件被删除可能导致class文件也被清理
            # 我们将在Java进程启动后再删除源文件
            # 将临时文件路径保存到实例变量中，以便后续清理
            self._temp_source_file = target_file
            self.logger.debug(f"Temporary source file will be cleaned up after Java process starts: {target_file}")
            
            return class_file
            
        except Exception as e:
            self.logger.error(f"Maven compilation error: {e}")
            # 出错时清理临时文件
            if target_file and os.path.exists(target_file):
                try:
                    os.remove(target_file)
                    self.logger.debug(f"Cleaned up temporary Java file after error: {target_file}")
                except Exception as cleanup_error:
                    self.logger.warning(f"Failed to cleanup temporary file {target_file}: {cleanup_error}")
            self._temp_source_file = None  # 清空引用
            raise
    
    def _compile_with_javac(self, java_file_path: str) -> str:
        """使用javac编译Java文件（简单模式，不包含gRPC依赖）"""
        try:
            # 获取输出目录（与Java文件相同目录）
            output_dir = os.path.dirname(java_file_path)
            class_file = os.path.join(output_dir, os.path.splitext(os.path.basename(java_file_path))[0] + '.class')
            
            # 使用绝对路径
            java_file_abs_path = os.path.abspath(java_file_path)
            cmd = [self.javac_path, '-d', output_dir, java_file_abs_path]
            
            # 执行编译
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=output_dir)
            
            if result.returncode != 0:
                error_msg = f"Java compilation failed: {result.stderr}"
                self.logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            # 检查class文件是否生成
            if not os.path.exists(class_file):
                raise RuntimeError(f"Class file not generated: {class_file}")
            
            self.logger.debug(f"Java compilation successful: {class_file}")
            return class_file
            
        except Exception as e:
            self.logger.error(f"Java compilation error: {e}")
            raise
    
    def _compile_java_libraries(self, java_libs_path: str, output_dir: str):
        """编译Java Libraries"""
        try:
            # 检查Java Libraries目录是否存在
            if not os.path.exists(java_libs_path):
                self.logger.warning(f"Java Libraries path not found: {java_libs_path}")
                return
            
            # 编译所有Java Libraries文件
            java_files = [f for f in os.listdir(java_libs_path) if f.endswith('.java')]
            
            if java_files:
                # 创建输出目录
                os.makedirs(output_dir, exist_ok=True)
                
                # 编译命令
                cmd = [self.javac_path, '-d', output_dir] + [os.path.join(java_libs_path, f) for f in java_files]
                
                # 执行编译
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    self.logger.warning(f"Java Libraries compilation failed: {result.stderr}")
                else:
                    self.logger.debug("Java Libraries compiled successfully")
                    
        except Exception as e:
            self.logger.warning(f"Failed to compile Java Libraries: {e}")
    
    def _start_java_process(self, class_file: str) -> subprocess.Popen:
        """启动Java进程"""
        try:
            self.logger.info(f"🔧 Starting Java process for class: {class_file}")
            
            # 获取类名（去掉.class扩展名）
            class_name = os.path.splitext(os.path.basename(class_file))[0]
            class_dir = os.path.dirname(class_file)
            self.logger.info(f"📝 Class name: {class_name}, Class dir: {class_dir}")
            # 额外校验：类文件与目录是否存在
            class_exists = os.path.exists(class_file)
            self.logger.debug(f"🧪 Verify class file exists: {class_exists} -> {class_file}")
            if not class_exists:
                self.logger.error(f"❌ Class file does NOT exist at expected location: {class_file}")
            try:
                dir_listing = os.listdir(class_dir)
                self.logger.debug(f"🧪 Class dir listing ({len(dir_listing)} items): {dir_listing[:10]}{'...' if len(dir_listing) > 10 else ''}")
                if not class_exists:
                    self.logger.error(f"❌ Full directory listing: {dir_listing}")
            except Exception as list_err:
                self.logger.warning(f"⚠️ Failed to list class dir {class_dir}: {list_err}")
            
            # JVM参数
            jvm_options = [
                "-Xms128m",
                "-Xmx512m", 
                "-Djava.awt.headless=true",
                f"-Dchainstream.agent.id={class_name.lower()}"  # 传递agent_id作为系统属性
            ]
            
            # 构建类路径
            if self._is_maven_build(class_file):
                # 使用Maven构建的classpath
                classpath = self._get_maven_classpath(class_file)
                # 使用完整的类名
                full_class_name = f"com.chainstream.agent.{class_name}"
                self.logger.info(f"🏗️ Using Maven build, classpath: {classpath}")
                self.logger.debug(f"🧪 Classpath repr: {repr(classpath)}")
                
                # 验证classpath是否有效
                if not classpath or classpath.strip() == "":
                    self.logger.warning("⚠️ Maven classpath is empty, falling back to simple build")
                    java_libs_path = os.path.join(os.path.dirname(__file__), 'java_libraries')
                    classpath = class_dir
                    if os.path.exists(java_libs_path):
                        classpath = f"{class_dir}:{java_libs_path}"
                    full_class_name = class_name
                    self.logger.info(f"🔧 Fallback to simple build, classpath: {classpath}")
                    self.logger.debug(f"🧪 Fallback classpath repr: {repr(classpath)}")
            else:
                # 使用简单的classpath
                java_libs_path = os.path.join(os.path.dirname(__file__), 'java_libraries')
                classpath = class_dir
                if os.path.exists(java_libs_path):
                    classpath = f"{class_dir}:{java_libs_path}"
                full_class_name = class_name
                self.logger.info(f"🔧 Using simple build, classpath: {classpath}")
                self.logger.debug(f"🧪 Simple classpath repr: {repr(classpath)}")
            
            self.logger.info(f"📋 Full class name: {full_class_name}")

            # 预验证：用 javap 验证主类在 classpath 可解析
            java_project_root = os.path.dirname(__file__)
            javap_ok = False
            try:
                javap_cmd = [self.javap_path, '-classpath', classpath, full_class_name]
                self.logger.debug(f"🧪 Running javap to verify classpath: {' '.join(javap_cmd[:4])} ...")
                javap_res = subprocess.run(javap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=java_project_root)
                if javap_res.returncode != 0:
                    self.logger.warning(f"⚠️ javap failed to resolve class {full_class_name}. stderr: {javap_res.stderr.strip()}")
                else:
                    # 仅打印首行，避免太多输出
                    first_line = javap_res.stdout.splitlines()[0] if javap_res.stdout else ''
                    self.logger.debug(f"🧪 javap ok: {first_line}")
                    javap_ok = True
            except Exception as jp_err:
                self.logger.warning(f"⚠️ javap validation error: {jp_err}")

            if not javap_ok:
                # 兜底：仅使用 target/classes 作为最小classpath 再试
                target_classes_only = os.path.join(java_project_root, 'target', 'classes')
                self.logger.warning(f"🔁 Falling back to minimal classpath for launch: {target_classes_only}")
                classpath = target_classes_only
            
            # Java命令
            cmd = [self.java_path] + jvm_options + ['-cp', classpath, full_class_name]
            self.logger.info(f"🚀 Java command: {' '.join(cmd)}")
            self.logger.debug(f"🧪 CWD for Java process: {os.path.dirname(__file__)}")
            # 同时通过环境变量冗余设置CLASSPATH，避免极端情况下 -cp 解析异常
            env = os.environ.copy()
            env['CLASSPATH'] = classpath
            self.logger.debug(f"🧪 Env CLASSPATH length: {len(env['CLASSPATH'])}")
            
            # 启动Java进程 - 不捕获输出，让输出直接显示到控制台
            # 工作目录应该设置为Maven项目根目录，而不是class文件目录
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,  # 捕获stdout用于日志记录
                stderr=subprocess.STDOUT,  # 将stderr重定向到stdout
                text=True,
                cwd=java_project_root,
                env=env
            )
            
            # 启动一个线程来读取Java进程的输出
            def read_output():
                try:
                    for line in iter(process.stdout.readline, ''):
                        if line:
                            self.logger.info(f"Java Agent Output: {line.strip()}")
                except Exception as e:
                    self.logger.error(f"Error reading Java process output: {e}")
            
            import threading
            output_thread = threading.Thread(target=read_output, daemon=True)
            output_thread.start()
            
            self.logger.info(f"✅ Java process started with PID: {process.pid}")
            
            # 在Java进程成功启动后，延迟清理临时源文件
            # 给Java进程一些时间完全加载类
            if hasattr(self, '_temp_source_file') and self._temp_source_file:
                def cleanup_temp_file():
                    import time
                    time.sleep(2)  # 等待2秒确保Java进程完全启动
                    if os.path.exists(self._temp_source_file):
                        try:
                            os.remove(self._temp_source_file)
                            self.logger.debug(f"🧹 Cleaned up temporary source file: {self._temp_source_file}")
                        except Exception as e:
                            self.logger.warning(f"⚠️ Failed to cleanup temp file: {e}")
                    self._temp_source_file = None
                
                cleanup_thread = threading.Thread(target=cleanup_temp_file, daemon=True)
                cleanup_thread.start()
            
            return process
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start Java process: {e}")
            import traceback
            self.logger.error(f"❌ Full traceback: {traceback.format_exc()}")
            raise
    
    def _is_maven_build(self, class_file: str) -> bool:
        """检查是否是Maven构建的class文件"""
        return 'target/classes' in class_file
    
    def _get_maven_classpath(self, class_file: str) -> str:
        """获取Maven构建的classpath"""
        java_project_root = os.path.dirname(__file__)
        target_classes = os.path.join(java_project_root, 'target', 'classes')
        
        # 获取Maven依赖的classpath
        try:
            # 使用临时文件来避免Maven输出干扰
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
                temp_path = temp_file.name
            
            result = subprocess.run(['mvn', 'dependency:build-classpath', f'-Dmdep.outputFile={temp_path}'], 
                                  cwd=java_project_root,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode == 0:
                # 读取classpath文件
                with open(temp_path, 'r') as f:
                    raw_classpath = f.read()
                # 规范化：移除换行和回车，按系统路径分隔符合并
                normalized = raw_classpath.replace('\n', '').replace('\r', '')
                parts = [p.strip() for p in normalized.split(os.pathsep) if p.strip()]
                maven_classpath = os.pathsep.join(parts)
                
                # 清理临时文件
                os.unlink(temp_path)
                
                self.logger.info(f"📦 Maven classpath: {maven_classpath}")
                self.logger.debug(f"🧪 Maven classpath entries: {len(parts)}")
                
                # 确保target_classes在classpath中
                full_classpath = os.pathsep.join([target_classes] + parts) if parts else target_classes
                
                self.logger.info(f"📦 Full classpath: {full_classpath}")
                return full_classpath
            else:
                self.logger.warning(f"Failed to get Maven classpath: {result.stderr}")
                # 清理临时文件
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                return target_classes
                
        except Exception as e:
            self.logger.warning(f"Error getting Maven classpath: {e}")
            # 清理临时文件
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            return target_classes
