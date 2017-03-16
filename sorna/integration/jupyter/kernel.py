import logging

from ipykernel.kernelbase import Kernel

log = logging.getLogger(__name__)


class SornaKernel(Kernel):

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

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        log.debug('do_execute!')
        if not silent:
            stream_content = {'name': 'stdout', 'text': code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
        }
