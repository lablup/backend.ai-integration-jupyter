from ipykernel.kernelbase import Kernel as KernelBase
from sorna.kernel import Kernel


class SornaKernel(KernelBase):

    # ref: https://github.com/ipython/ipykernel/blob/master/ipykernel/kernelbase.py

    implementation = 'Sorna'
    implementation_version = '1.0'
    language = 'python'
    language_version = '3.6'
    language_info = {
        'name': 'Python',
        'mimetype': 'text/x-python-src',
        'file_extension': '.py',
    }
    banner = 'Sorna kernel - testing'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.debug(f'__init__: {self.ident}')
        self.kernel = Kernel.get_or_create('python3-tensorflow-gpu', self.ident)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.log.debug('do_execute')
        self._allow_stdin = allow_stdin
        while True:
            result = self.kernel.execute(code, mode='query')

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

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }

    def do_shutdown(self, restart=False):
        self.log.debug('do_shutdown')
        if restart:
            self.kernel.restart()
        else:
            self.kernel.destroy()
