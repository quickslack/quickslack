import subprocess, click, os

@click.command()
@click.argument('path', default='')
def cli(path):

    full_path = os.path.join('scripts', path+'.py')

    cmd = f'python {full_path}'

    return subprocess.call(cmd, shell=True)
