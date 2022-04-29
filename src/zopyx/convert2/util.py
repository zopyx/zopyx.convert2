#########################################################################
# zopyx.convert2 - SmartPrintNG low-level functionality
#
# (C) 2007, ZOPYX Ltd & Co. KG, Tuebingen, Germany
#########################################################################

import os
import sys
import tempfile

import commands
from subprocess import Popen, PIPE
from logger import LOG

win32 = (sys.platform=='win32')
execute_mode = os.environ.get('ZOPYX_CONVERT_EXECUTE_MODE', 'process')
execution_shell = os.environ.get('ZOPYX_CONVERT_SHELL', 'sh')


def newTempfile(suffix=''):
    return tempfile.mktemp(suffix=suffix)


def runcmd(cmd):                
    """ Execute a command using the subprocess module """

    if win32:
        cmd = cmd.replace('\\', '/')
        s = Popen(cmd, shell=False)
        s.wait()
        return 0, ''

    else:

        if execute_mode == 'system':
            status = os.system(cmd)
            return status, ''

        elif execute_mode == 'commands':
            return commands.getstatusoutput(cmd)

        elif execute_mode == 'process':

            stdin = open('/dev/null')
            stdout = stderr = PIPE
            p = Popen(cmd, 
                      shell=True,
                      stdin=stdin,
                      stdout=stdout,
                      stderr=stderr,
                      )

            status = p.wait()
            stdout_ = p.stdout.read().strip()
            stderr_ = p.stderr.read().strip()

            if stdout_:
                LOG.info(stdout_)
            if stderr_:
                LOG.info(stderr_)
            return status, stdout_ + stderr_

        else:
            raise ValueError('Unknown value for $ZOPYX_CONVERT_EXECUTE_MODE')


def checkEnvironment(envname):
    """ Check if the given name of an environment variable exists and
        if it points to an existing directory.
    """

    dirname = os.environ.get(envname, None)
    if dirname is None:
        LOG.debug(f'Environment variable ${envname} is unset')
        return False

    if not os.path.exists(dirname):
        LOG.debug('The directory referenced through the environment '
                  'variable $%s does not exit (%s)' % 
                  (envname, dirname))
        return False
    return True


def which(command):
    """ Implements a functionality similar to the UNIX
        ``which`` command. The method checks if ``command``
        is available somewhere within the $PATH and returns
        True or False.
    """
    path_env = os.environ.get('PATH', '') # also on win32?
    for path in path_env.split(':'):
        fullname = os.path.join(path, command)
        if os.path.exists(fullname):
            return True
    return False

if __name__ == '__main__':
    print 'ls:', which('ls')
    print 'foo:', which('foo')
