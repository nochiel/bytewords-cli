#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.
# Layout: https://www.gnu.org/software/autoconf/manual/autoconf-2.67/html_node/Autoconf-Input-Layout.html#Autoconf-Input-Layout
# Subdirectories to configure dependencies: https://www.gnu.org/software/autoconf/manual/autoconf-2.67/html_node/Subdirectories.html#Subdirectories

AC_PREREQ([2.69])
AC_CONFIG_AUX_DIR([/usr/share/autoconf/build-aux])
AC_INIT([bytewords-cli], [0.1.1])
AC_CONFIG_SRCDIR([src/bytewords.cpp])
AC_CONFIG_HEADERS([src/config.h])

# Checks for programs.
AC_PROG_CXX([clang g++])
AC_PROG_CC([clang gcc])
AC_CHECK_PROG([SHUNIT2], [shunit2], [yes], [no])     
if [[ "x$SHUNIT2" = "xno" ]]; then
    echo $SHUNIT2
    AC_MSG_ERROR("shunit2 is required.")
fi
AC_PROG_INSTALL
AC_PROG_MAKE_SET

# Checks for header files.
AC_CHECK_HEADERS([fcntl.h memory.h stdint.h stdlib.h string.h strings.h sys/ioctl.h sys/param.h unistd.h stddef.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_CHECK_HEADER_STDBOOL
AC_C_INLINE
AC_TYPE_SIZE_T
AC_TYPE_SSIZE_T
AC_TYPE_UINT16_T
AC_TYPE_UINT32_T
AC_TYPE_UINT64_T
AC_TYPE_UINT8_T
AC_TYPE_INT16_T
AC_TYPE_INT32_T

# Checks for library functions.
AC_FUNC_MALLOC
AC_CHECK_FUNCS([memset strerror])

AC_CONFIG_FILES([Makefile
                 src/Makefile])

# Check that deps/ submodules have been checked out.
if [[ ! -d deps ]];then
    AC_MSG_ERROR("Please run "git submodule init && git submodule update" to check out required dependencies.")
fi

AC_CONFIG_SUBDIRS([deps/argp-standalone/argp-standalone  
                   deps/bc-crypto-base
                   deps/bc-bytewords])

AC_OUTPUT
