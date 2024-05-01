##################################################################
# Makefile for building: lsusbblk 
#
# Project: lsusbblk
#
##################################################################

### Internal definitions ###

P="[44m"
S="[00m"
print=$P$(1)$S
p_targ=$PMaking $@ ...$S
 
define cp_src2targ
  @echo $(call p_targ)
  @cp $? $@
endef

NAME      := lsusbblk
SRC			  := src
DOC			  := doc
TMPL			:= tmpl
MAIN      := $(SRC)/$(NAME)
SPEC      := $(NAME).spec
SPECTEMPL := $(TMPL)/$(SPEC).tmpl
TAR       := $(NAME).tgz

VERSION   := $(shell grep ^__version__ $(SRC)/$(NAME) | cut -d '=' -f 2 | grep -o [0-9\.a-z]\*)
RELEASE   := $(shell grep ^Release $(SPECTEMPL) | cut -d ':' -f 2 | grep -o [0-9]\*)

LIBSRC    := $(SRC)/lib/conf.py $(SRC)/lib/usbblk.py $(SRC)/lib/confutil.py $(SRC)/lib/formatutil.py
PYSRC     := $(SRC)/$(NAME) $(LIBSRC)
SRC       := Makefile README.md LICENSE $(DOC)/lsusbblk.1.md $(PYSRC)
RES       := $(SPEC) $(DOC)/lsusbblk.1 lsusbblk.1.gz
RPM_TARG  := RPMS/noarch/$(NAME)-$(VERSION)-$(RELEASE).noarch.rpm

$(warning ------------------------------------------------------------------------------)
$(warning Current workning directory = $(shell pwd))
$(warning Application = $(NAME))
$(warning Version     = $(VERSION))
$(warning Release     = $(RELEASE))
$(warning SPEC        = $(SPEC))
$(warning SPECTEMPL   = $(SPECTEMPL))
$(warning RPM target  = $(RPM_TARG))

##############################################################################
### Commands                                                               ###
##############################################################################

.PHONY: all setup clean clean_all lint lint_rpm lint_py install

first: all

setup:
	@echo $(call print,"--- setup ---")
	@mkdir -pv RPMS/noarch
	@mkdir -pv BUILD BUILDROOT SRPMS SPECS SOURCES

clean:
	@echo $(call print,"--- cleaning ---")
	@find . -name '*.pyc' -exec rm -v --force {} +
	@find . -name '*.pyo' -exec rm -v --force {} +
	@rm -fv $(RES)
	@rm -fv $(TAR)
	@rm -fv RPMS/noarch/*
	@rm -frv BUILD/* BUILDROOT/* SRPMS/* SPECS/* SOURCES/*

clean_all: clean
	@echo $(call print,"--- clean all ---")
	@rm -frv RPMS
	@rmdir -v BUILD BUILDROOT SRPMS SPECS SOURCES
	@rm -frv .mypy_cache 

lint: lint_rpm lint_py
	@echo $(call print,"--- lint ---")

lint_rpm:
	@echo $(call print,"--- lint rpm ---")
	rpmlint $(SPEC)

lint_py:
	@echo $(call print,"--- lint python ---")
	flake8 --exit-zero $(PYSRC)
	pylint-3 $(PYSRC)
	mypy $(PYSRC)

install:
	@echo $(call print,"installing ...")
	# /usr/share
	install -d -m 755 $(DESTDIR)/usr/share/$(NAME)
	install -d -m 755  $(DESTDIR)/usr/share/$(NAME)/lib
	install -m 755 $(MAIN) $(DESTDIR)/usr/share/$(NAME)/$(NAME)
	install -m 644 $(LIBSRC) $(DESTDIR)/usr/share/$(NAME)/lib
	#ln --symbolic $(DESTDIR)/usr/share/$(NAME)/$(NAME) $(DESTDIR)/usr/bin/$(NAME)
	# /usr/share/man/man1/
	install -d -m 755 $(DESTDIR)/usr/share/man/man1/
	install -m 644 $(NAME).1.gz $(DESTDIR)/usr/share/man/man1/$(NAME).1.gz
	# /usr/share/doc/lsusbblk
	install -d -m 755 $(DESTDIR)/usr/share/doc/lsusbblk

### Depedencies ###

all: $(RPM_TARG)
	@echo $(call p_targ)
	@ls -gGhF --color RPMS/noarch
	@echo $(call print,"------------")

$(TAR): $(SRC) $(RES)
	@echo $(call p_targ)
	@tar -czvf $(TAR) $(SRC) $(RES)

$(DOC)/$(NAME).1: $(DOC)/$(NAME).1.md
	@echo $(call p_targ)
	pandoc -s -t man $? -o $@

$(NAME).1.gz: $(DOC)/$(NAME).1
	@echo $(call p_targ)
	@gzip -v -c $(DOC)/$(NAME).1 > $@

$(SPEC): $(SPECTEMPL) $(MAIN)
	@echo $(call p_targ)
	cat $(SPECTEMPL) | \
		sed 's/__NAME__/$(NAME)/g' | \
		sed 's/__VERSION__/$(VERSION)/g' | \
		sed 's/__RELEASE__/$(RELEASE)/g' | \
		sed 's/__TAR__/$(TAR)/g' > $(SPEC)

$(RPM_TARG): $(SPEC) $(TAR)
	@echo $(call p_targ)
	@echo $(SPEC)
	@echo $(TAR)
	@cp $(SPEC) SPECS
	@cp $(TAR) SOURCES
	@if [ -s ~/.rpmmacros ];  then \
	        mv ~/.rpmmacros ~/.rpmmacros.org; \
	        echo "%_topdir "`pwd` > ~/.rpmmacros; \
	        rpmbuild -ba --quiet --target noarch SPECS/$(SPEC); \
	        mv ~/.rpmmacros.org ~/.rpmmacros; \
	else \
	        echo "%_topdir "`pwd` > ~/.rpmmacros; \
			rpmbuild -ba --quiet --target noarch SPECS/$(SPEC); \
	        rm -f ~/.rpmmacros; \
	fi
