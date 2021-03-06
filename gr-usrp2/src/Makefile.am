#
# Copyright 2004,2005,2006,2008,2009 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

include $(top_srcdir)/Makefile.common

# ----------------------------------------------------------------------
# Local Python files, not installed
#
# qa_usrp2.py
# ----------------------------------------------------------------------

noinst_PYTHON = qa_usrp2.py

# ----------------------------------------------------------------------
# Miscellaneous build operations
# ----------------------------------------------------------------------

EXTRA_DIST = run_tests.in
DISTCLEANFILES = run_tests

# ----------------------------------------------------------------------
# C++ block API interface librar(ies)
#
# libgr-usrp.so
# ----------------------------------------------------------------------
AM_CPPFLAGS = \
	$(STD_DEFINES_AND_INCLUDES)  \
	$(GRUEL_INCLUDES) \
	$(PYTHON_CPPFLAGS) \
	$(USRP2_INCLUDES) \
	$(WITH_INCLUDES)

lib_LTLIBRARIES = libgnuradio-usrp2.la

libgnuradio_usrp2_la_LDFLAGS = $(LTVERSIONFLAGS)

libgnuradio_usrp2_la_SOURCES = \
	rx_16sc_handler.cc \
	rx_32fc_handler.cc \
	usrp2_base.cc \
	usrp2_source_base.cc \
	usrp2_source_16sc.cc \
	usrp2_source_32fc.cc \
	usrp2_sink_base.cc \
	usrp2_sink_16sc.cc \
	usrp2_sink_32fc.cc

libgnuradio_usrp2_la_LIBADD = \
	$(USRP2_LA) \
	$(GNURADIO_CORE_LA) 

grinclude_HEADERS = \
	usrp2_base.h \
	usrp2_source_base.h \
	usrp2_source_32fc.h \
	usrp2_source_16sc.h \
	usrp2_sink_base.h \
	usrp2_sink_16sc.h \
	usrp2_sink_32fc.h

noinst_HEADERS = \
	rx_16sc_handler.h \
	rx_32fc_handler.h

if PYTHON
# ----------------------------------------------------------------------
# Python SWIG wrapper around C++ library
#
# usrp2.py
# _usrp2.so
# ----------------------------------------------------------------------
TESTS = run_tests

TOP_SWIG_IFILES =		\
	usrp2.i

# Install so that they end up available as:
#   import gnuradio.usrp2
# This ends up at:
#   ${prefix}/lib/python${python_version}/site-packages/gnuradio
usrp2_pythondir_category =	\
	gnuradio

# additional arguments to the SWIG command
usrp2_swig_args =		\
	$(USRP2_INCLUDES)

# additional libraries for linking with the SWIG-generated library
usrp2_la_swig_libadd =		\
	libgnuradio-usrp2.la

include $(top_srcdir)/Makefile.swig

# add some of the variables generated inside the Makefile.swig.gen
BUILT_SOURCES = $(swig_built_sources)

# Do not distribute the output of SWIG
no_dist_files = $(swig_built_sources)
endif
