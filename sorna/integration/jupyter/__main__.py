from ipykernel.kernelapp import IPKernelApp
import logging

from .kernel import SornaKernel


IPKernelApp.launch_instance(kernel_class=SornaKernel)
