# Ref. https://devmanual.gentoo.org/general-concepts/autotools/index.html

# TODO(nochiel) Dependencies (submodules) should be in the makefile. Should I use a Makefile.am?
# What I want is that everything in build.sh should be handled in the MakeFile.
# dh_autoconfigure will fail because AC_CHECK_LIB will fail.
# How do I tell deb to static build and link these git submodules?

# Ref. https://www.debian.org/doc/manuals/maint-guide/first.en.html
# > packaging cannot be a fully automated process. You will need to modify the upstream source for Debian 
# apt install -y devscripts dh-make

import os
import subprocess

env = dict(DEBEMAIL = '', DEBFULLNAME = '')

try:
    env['DEBEMAIL'] = (subprocess.check_output(['git', 'config', 'user.email']).splitlines()[0]).decode()
    env['DEBFULLNAME'] = (subprocess.check_output(['git', 'config', 'user.name']).splitlines()[0]).decode()
except subprocess.CalledProcessError as e:
    raise Exception('Please set git user.name and user.email')

package_name = os.path.basename(os.getcwd())
version = ''
try:
    tags = subprocess.check_output(['git', 'tag', '-l'])
    version = (tags.splitlines()[0]).decode()
except subprocess.CalledProcessError as e:
    raise Exception('Git tags were not found.')

# Checkout the latest tag for this build.
filename = f'{package_name}_{version}'
subprocess.run(['git', 'worktree', 'add', f'../{package_name}-{version}', version])
os.chdir(f'../{package_name}-{version}')

# Exclude: .git/, .gitignore
# Include: deps/
# subprocess.run(['tar', 'cvzf', f'../{filename}.tar.gz', '.'])
subprocess.run(['git', 'submodule', 'init'])
subprocess.run(['git', 'submodule', 'update'])
subprocess.run(['dh_make', '-y', '-s', '--createorig'],
            env = env)
