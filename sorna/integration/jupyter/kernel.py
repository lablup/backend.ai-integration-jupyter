import logging

from metakernel import MetaKernel

from sorna.kernel import Kernel
from sorna.exceptions import SornaAPIError


class SornaKernelBase(MetaKernel):

    # ref: https://github.com/ipython/ipykernel/blob/master/ipykernel/kernelbase.py

    implementation = 'Sorna'
    implementation_version = '1.0'
    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'Sorna (base)',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
    }
    banner = 'Sorna (base)'

    sorna_lang = 'python3'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info(f'Sorna kernel starting with client session ID: {self.ident}')
        self.kernel = Kernel.get_or_create(self.sorna_lang, self.ident)

    def do_execute_direct(self, code,
                          silent=False,
                          store_history=True,
                          user_expressions=None,
                          allow_stdin=True):
        self._allow_stdin = allow_stdin
        while True:
            try:
                result = self.kernel.execute(code, mode='query')
            except SornaAPIError as e:
                if e.args[0] == 404:
                    self.Error('[Lablup.AI] The kernel is not found (maybe terminated due to idle/exec timeouts).')
                    self.Error('[Lablup.AI] Please restart the kernel to run again.')
                else:
                    detail = json.loads(e.args[2])
                    self.Error(f"[Labup.AI] The server returned an error: {e.args[0]} {e.args[1]} ({detail['title']})")
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
                            'data': { item[1][0]: item[1][1] },
                        })
                    elif item[0] == 'html':
                        self.send_response(self.iopub_socket, 'display_data', {
                            'source': '<user-code>',
                            'data': { 'text/html': item[1] },
                        })

            if result['status'] == 'finished':
                break
            elif result['status'] == 'waiting-input':
                if allow_stdin:
                    code = self.raw_input('')
                else:
                    code = '(user input not allowed)'
            elif result['status'] == 'continued':
                code = ''

    def restart_kernel(self):
        pass

    def do_shutdown(self, restart):
        # Jupyter's restarting first destroys the kernel and then start it over again.
        # We cannot use our own restarting mechanism as it produces duplicate kernels.
        try:
            self.kernel.destroy()
        except SornaAPIError as e:
            if e.args[0] == 404:
                self.log.warning('do_shutdown: missing kernel, ignoring.')
            else:
                self.log.exception('do_shutdown: API returned an error')
        except:
            self.log.exception('do_shutdown: API returned an error')
        return super().do_shutdown(restart)

    def get_completions(self, info):
        result = self.kernel.execute(info['code'], mode='complete', opts={
            'row': info['line_num'],
            'col': info['column'],
            'line': info['line'],
            'post': info['post'],
        })
        if 'completions' in result and result['completions'] is not None:
            return result['completions']
        return tuple()


class SornaPythonKernel(SornaKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'Python 3 on Sorna',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Sorna (Python 3)'

    sorna_lang = 'python3'


class SornaPythonTensorFlowKernel(SornaKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'TensorFlow (Python 3, CPU) on Sorna',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Sorna (TensorFlow with Python 3)'

    sorna_lang = 'python3-tensorflow'


class SornaPythonTorchKernel(SornaKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'PyTorch (Python 3, CPU) on Sorna',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Sorna (TensorFlow with Python 3)'

    sorna_lang = 'python3-torch'


class SornaPythonTorchGPUKernel(SornaKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'PyTorch (Python 3, GPU) on Sorna',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Sorna (TensorFlow with Python 3)'

    sorna_lang = 'python3-torch-gpu'


class SornaPythonTensorFlowGPUKernel(SornaKernelBase):

    language = 'python'
    language_version = '3'
    language_info = {
        'name': 'TensorFlow (Python 3, GPU) on Sorna',
        'mimetype': 'text/x-python3',
        'file_extension': '.py',
        'codemirror_mode': 'python',
    }
    banner = 'Sorna (GPU-accelerated TensorFlow with Python 3)'

    sorna_lang = 'python3-tensorflow-gpu'


class SornaJavascriptKernel(SornaKernelBase):

    language = 'javascript'
    language_version = '6'
    language_info = {
        'name': 'Javascript (NodeJS 6) on Sorna',
        'mimetype': 'text/javascript',
        'file_extension': '.js',
        'codemirror_mode': 'javascript',
    }
    banner = 'Sorna (NodeJS 6)'

    sorna_lang = 'nodejs6'


class SornaPHPKernel(SornaKernelBase):

    language = 'php'
    language_version = '7'
    language_info = {
        'name': 'PHP 7 on Sorna',
        'mimetype': 'text/x-php',
        'file_extension': '.php',
        'codemirror_mode': 'php',
    }
    banner = 'Sorna (PHP 7)'

    sorna_lang = 'php7'


class SornaJuliaKernel(SornaKernelBase):

    language = 'julia'
    language_version = '0.5'
    language_info = {
        'name': 'Julia 0.5 on Sorna',
        'mimetype': 'text/x-julia',
        'file_extension': '.jl',
        'codemirror_mode': 'julia',
    }
    banner = 'Sorna (Julia 0.5)'

    sorna_lang = 'julia'


class SornaCKernel(SornaKernelBase):

    language = 'c'
    language_version = '11'
    language_info = {
        'name': 'C11 on Sorna',
        'mimetype': 'text/x-csrc',
        'file_extension': '.c',
        'codemirror_mode': 'clike',
    }
    banner = 'Sorna (C [gnu11])'

    sorna_lang = 'c'


class SornaCppKernel(SornaKernelBase):

    language = 'cpp'
    language_version = '14'
    language_info = {
        'name': 'C++14 on Sorna',
        'mimetype': 'text/x-c++src',
        'file_extension': '.cc',
        'codemirror_mode': 'clike',
    }
    banner = 'Sorna (C++ [gnu++14])'

    sorna_lang = 'cpp'


class SornaJavaKernel(SornaKernelBase):

    language = 'java'
    language_version = '8'
    language_info = {
        'name': 'Java8 on Sorna',
        'mimetype': 'text/x-java',
        'file_extension': '.java',
        'codemirror_mode': 'clike',
    }
    banner = 'Sorna (Java [openjdk8])'

    sorna_lang = 'java8'


class SornaRKernel(SornaKernelBase):

    language = 'r'
    language_version = '3'
    language_info = {
        'name': 'R 3 on Sorna',
        'mimetype': 'text/x-rsrc',
        'file_extension': '.R',
        'codemirror_mode': 'Rscript',
    }
    banner = 'Sorna (R 3)'

    sorna_lang = 'r3'


class SornaLuaKernel(SornaKernelBase):

    language = 'lua'
    language_version = '5.3'
    language_info = {
        'name': 'Lua 5.3 on Sorna',
        'mimetype': 'text/x-lua',
        'file_extension': '.lua',
        'codemirror_mode': 'lua',
    }
    banner = 'Sorna (Lua 5.3)'

    sorna_lang = 'lua5'


sorna_kernels = [
    SornaPythonKernel,
    SornaPythonTorchKernel,
    SornaPythonTorchGPUKernel,
    SornaPythonTensorFlowKernel,
    SornaPythonTensorFlowGPUKernel,
    SornaJavascriptKernel,
    SornaPHPKernel,
    SornaJuliaKernel,
    SornaCKernel,
    SornaCppKernel,
    SornaJavaKernel,
    SornaRKernel,
    SornaLuaKernel,
]
