import subprocess


def wait_for_it(host: str, port: int = 443, *, timeout: int = 0):
    command = [
        'wait-for-it',
        f'--timeout={timeout}',
        f'--service={host}:{port}',
    ]
    result = subprocess.run(command, capture_output=True)
    if result.returncode != 0:
        raise TimeoutError(f'Could not connect to {host}:{port} within {timeout} seconds')
