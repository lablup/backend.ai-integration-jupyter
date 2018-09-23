from metakernel import MetaKernel

from ai.backend.client.session import Session
from ai.backend.client.exceptions import BackendAPIError


class BackendKernelBase(MetaKernel):

    # ref: https://github.com/ipython/ipykernel/blob/master/ipykernel/kernelbase.py

    implementation = 'Backend.AI'
    implementation_version = '1.0'
    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'Backend.AI (base)',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
    }
    banner = 'Backend.AI Base'

    backend_lang = 'python:3.6'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info('Backend.AI kernel starting with client session ID: {0}'.format(self.ident))
        self.backend_session = Session()
        self.kernel = self.backend_session.Kernel.get_or_create(self.backend_lang, self.ident)

    def do_execute_direct(self, code,
                          silent=False,
                          store_history=True,
                          user_expressions=None,
                          allow_stdin=True):
        self._allow_stdin = allow_stdin
        mode = 'query'
        run_id = None
        while True:
            try:
                result = self.kernel.execute(run_id, code, mode)
                run_id = result['runId']
            except BackendAPIError as e:
                if e.status == 404:
                    self.Error('[Backend.AI] The kernel is not found '
                               '(maybe terminated due to idle/exec timeouts).')
                    self.Error('[Backend.AI] Please restart the kernel to run again.')
                else:
                    self.Error('[Backend.AI] The server returned an error: '
                               '{0.status} {0.reason} ({0.data[title]})'
                               .format(e))
                return

            if not silent:
                for item in result['console']:
                    if item[0] == 'stdout':
                        self.send_response(self.iopub_socket, 'stream', {
                            'name': 'stdout',
                            'text': item[1],
                        })
                    elif item[0] == 'stderr':
                        self.send_response(self.iopub_socket, 'stream', {
                            'name': 'stderr',
                            'text': item[1],
                        })
                    elif item[0] == 'media':
                        self.send_response(self.iopub_socket, 'display_data', {
                            'source': '<user-code>',
                            'data': {item[1][0]: item[1][1]},
                        })
                    elif item[0] == 'html':
                        self.send_response(self.iopub_socket, 'display_data', {
                            'source': '<user-code>',
                            'data': {'text/html': item[1]},
                        })

            if result['status'] == 'finished':
                break
            elif result['status'] == 'waiting-input':
                mode = 'input'
                if allow_stdin:
                    code = self.raw_input('')
                else:
                    code = '(user input not allowed)'
            elif result['status'] in ('continued', 'build-finished'):
                mode = 'continue'
                code = ''

    def restart_kernel(self):
        pass

    def do_shutdown(self, restart):
        # Jupyter's restarting first destroys the kernel and then start it over again.
        # We cannot use our own restarting mechanism as it produces duplicate kernels.
        try:
            self.kernel.destroy()
        except BackendAPIError as e:
            if e.status == 404:
                self.log.warning('do_shutdown: missing kernel, ignoring.')
            else:
                self.log.exception('do_shutdown: API returned an error')
        except Exception:
            self.log.exception('do_shutdown: API returned an error')
        finally:
            self.backend_session.close()
        return super().do_shutdown(restart)

    def get_completions(self, info):
        result = self.kernel.complete(info['code'], opts={
            'row': info['line_num'],
            'col': info['column'],
            'line': info['line'],
            'post': info['post'],
        })
        if result is None:
            return tuple()
        return result.get('completions', tuple())


class BackendPythonKernel(BackendKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'Python 3 on Backend.AI',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Backend (Python 3)'

    backend_lang = 'python:3.6'


class BackendPythonTensorFlowKernel(BackendKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'TensorFlow (Python 3, CPU) on Backend.AI',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Backend (TensorFlow with Python 3)'

    backend_lang = 'python-tensorflow:1.8-py36'


class BackendPythonTorchKernel(BackendKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'PyTorch (Python 3, CPU) on Backend.AI',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Backend (TensorFlow with Python 3)'

    backend_lang = 'python-torch:0.2'


class BackendPythonTorchGPUKernel(BackendKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'PyTorch (Python 3, GPU) on Backend.AI',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Backend (TensorFlow with Python 3)'

    backend_lang = 'python-torch:0.2-gpu'


class BackendPythonTensorFlowGPUKernel(BackendKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'TensorFlow (Python 3, GPU) on Backend.AI',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Backend (GPU-accelerated TensorFlow with Python 3)'

    backend_lang = 'python-tensorflow:1.8-gpu'


class BackendJavascriptKernel(BackendKernelBase):

    language = 'javascript'
    language_version = '8'
    language_info = {
        'name': 'Javascript (NodeJS 6) on Backend.AI',
        'mimetype': 'text/javascript',
        'file_extension': '.js',
        'codemirror_mode': 'javascript',
    }
    banner = 'Backend (NodeJS 6)'

    backend_lang = 'nodejs:8'


class BackendPHPKernel(BackendKernelBase):

    language = 'php'
    language_version = '7'
    language_info = {
        'name': 'PHP 7 on Backend.AI',
        'mimetype': 'text/x-php',
        'file_extension': '.php',
        'codemirror_mode': 'php',
    }
    banner = 'Backend (PHP 7)'

    backend_lang = 'php:7'


class BackendJuliaKernel(BackendKernelBase):

    language = 'julia'
    language_version = '0.6'
    language_info = {
        'name': 'Julia 0.6 on Backend.AI',
        'mimetype': 'text/x-julia',
        'file_extension': '.jl',
        'codemirror_mode': 'julia',
    }
    banner = 'Backend (Julia 0.6)'

    backend_lang = 'julia:0.6'


class BackendCKernel(BackendKernelBase):

    language = 'c'
    language_version = '11'
    language_info = {
        'name': 'C11 on Backend.AI',
        'mimetype': 'text/x-csrc',
        'file_extension': '.c',
        'codemirror_mode': 'clike',
    }
    banner = 'Backend (C [gnu11])'

    backend_lang = 'c:gcc6.3'


class BackendCppKernel(BackendKernelBase):

    language = 'cpp'
    language_version = '14'
    language_info = {
        'name': 'C++14 on Backend.AI',
        'mimetype': 'text/x-c++src',
        'file_extension': '.cc',
        'codemirror_mode': 'clike',
    }
    banner = 'Backend (C++ [gnu++14])'

    backend_lang = 'cpp:gcc6.3'


class BackendJavaKernel(BackendKernelBase):

    language = 'java'
    language_version = '8'
    language_info = {
        'name': 'Java8 on Backend.AI',
        'mimetype': 'text/x-java',
        'file_extension': '.java',
        'codemirror_mode': 'clike',
    }
    banner = 'Backend (Java [openjdk8])'

    backend_lang = 'java:8'


class BackendRKernel(BackendKernelBase):

    language = 'r'
    language_version = '3'
    language_info = {
        'name': 'R 3 on Backend.AI',
        'mimetype': 'text/x-rsrc',
        'file_extension': '.R',
        'codemirror_mode': 'Rscript',
    }
    banner = 'Backend (R 3)'

    backend_lang = 'r:3'


class BackendLuaKernel(BackendKernelBase):

    language = 'lua'
    language_version = '5.3'
    language_info = {
        'name': 'Lua 5.3 on Backend.AI',
        'mimetype': 'text/x-lua',
        'file_extension': '.lua',
        'codemirror_mode': 'lua',
    }
    banner = 'Backend (Lua 5.3)'

    backend_lang = 'lua:5.3'


kernels = [
    BackendPythonKernel,
    BackendPythonTorchKernel,
    BackendPythonTorchGPUKernel,
    BackendPythonTensorFlowKernel,
    BackendPythonTensorFlowGPUKernel,
    BackendJavascriptKernel,
    BackendPHPKernel,
    BackendJuliaKernel,
    BackendCKernel,
    BackendCppKernel,
    BackendJavaKernel,
    BackendRKernel,
    BackendLuaKernel,
]
