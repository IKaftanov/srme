import subprocess as sp

import psutil
import pynvml


def is_nvidia_smi_available() -> bool:
    """Check if nvidia-smi command available.
    Used to get gpu info.
    """
    try:
        sp.check_output(["nvidia-smi"])
        return True
    except (sp.CalledProcessError, FileNotFoundError):
        return False


def get_gpu_memory():
    raise NotImplementedError("need to test on gpu")


def get_cpu_percent() -> float:
    return psutil.cpu_percent()


def get_vm_percent() -> float:
    return psutil.virtual_memory().percent


def get_disk_usage_percent() -> float:
    return psutil.disk_usage("/").percent


def get_gpu_usage_percent_getter():
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)

    def inner_f() -> float:
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return round(int(info.free) * 10 ** (-9), 2)

    return inner_f
