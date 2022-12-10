#!/bin/env python3
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
import shutil

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
# subprocess.run(['git', 'worktree', 'add', '-f', f'../{package_name}-{version}', version])
subprocess.run(['git', 'worktree', 'add', '-f', f'../{package_name}-{version}', 'build-deb'])
os.chdir(f'../{package_name}-{version}')

# Make a list of the files and directories we want. 
# Exclude: .git/, .gitignore
# Include: deps/
# subprocess.run(['tar', 'cvzf', f'../{filename}.tar.gz', '.'])
subprocess.run(['git', 'submodule', 'init'])
subprocess.run(['git', 'submodule', 'update'])

os.chdir('deps')

os.chdir('argp-standalone')
subprocess.run(['git', 'remote', 'add', 'nochiel', 'https://github.com/nochiel/argp-standalone.git'])
subprocess.run(['git', 'fetch', 'nochiel', 'build-deb'])
try:
    subprocess.run(['git', 'checkout', 'nochiel/build-deb'])
except Exception as e:
    raise e

os.chdir('..')

os.chdir('bc-bytewords')
subprocess.run(['git', 'remote', 'add', 'nochiel', 'https://github.com/nochiel/bc-bytewords.git'])
subprocess.run(['git', 'fetch', 'nochiel', 'build-deb'])
try:
    subprocess.run(['git', 'checkout', 'nochiel/build-deb'])
except Exception as e:
        raise e

os.chdir('..')
os.chdir('bc-crypto-base')
# subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/nochiel/bc-crypto-base.git'])
subprocess.run(['git', 'checkout', 'master'])

# Create an archive to use for the package.
os.chdir('..')
package_directory = os.path.basename(os.getcwd())
assert package_directory == f'{package_name}-{version}'

# Remove files that shouldn't be in the package.
try:
    shutil.rmtree('.github')
    shutil.rmtree('.vscode')
except:
    pass

# os.chdir('..')
# os.replace(package_directory, f'{package_directory}.old')
# shutil.copytree(f'{package_directory}.old', package_directory)
# os.chdir(package_directory)

subprocess.run(['dh_make', '-y', '-s', '--createorig'],
               env = env)

# TODO(nochiel) Install build dependencies and required dependencies.
subprocess.run(['dpkg-buildpackage', '-us', '-uc'])
