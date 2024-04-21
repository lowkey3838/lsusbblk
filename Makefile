##################################################################
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

# Setup variables
NAME      := lsusbblk
SRC			  := src
APP       := $(SRC)/$(NAME)
DOC			  := doc
VERSION   := $(shell grep ^__version__ $(APP) | cut -d '=' -f 2 | grep -o [0-9\.a-z]\*)

SPEC      := $(NAME).spec
SPECTEMPL := $(SPEC).tmpl
TAR       := $(NAME).tgz

# Fix me: remove or use as build number?
RELEASE   := 1

LIBSRC    := $(SRC)/lib/usbblk.py $(SRC)/lib/confutil.py $(SRC)/lib/formatutil.py
PYSRC     := $(APP) $(LIBSRC)
SRC       := Makefile README.md LICENSE $(DOC)/lsusbblk.1 $(PYSRC)
RES       := $(SPEC) lsusbblk.1.gz REL
RPM_TARG  := RPMS/noarch/$(NAME)-$(VERSION)-$(RELEASE).noarch.rpm

$(warning ------------------------------------------------------------------------------)
$(warning $(shell pwd))
$(warning Application = $(NAME))
$(warning Version = $(VERSION))
$(warning End product = $(RPM_TARG))
$(warning The command issued from the command line was: $(MAKECMDGOALS))
$(warning ------------------------------------------------------------------------------)

##############################################################################
### Commands                                                               ###
##############################################################################

.PHONY: all setup clean clean_all lint lint_rpm lint_py install

first: all

# Store RELEASE number in file to survive to the BUILD directory
# where no svn info exists
REL:
	RELEASE=1000
	$(warning $(RELEASE))
	@echo -n $(RELEASE) > ./REL 

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
	@rm -frv BUILD BUILDROOT SRPMS SPECS SOURCES
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
	mypy   $(PYSRC)

install:
	@echo $(call print,"installing ...")
	# /usr/share
	install -d -m 755 $(DESTDIR)/usr/share/$(NAME)
	install -d -m 755  $(DESTDIR)/usr/share/$(NAME)/lib
	install -m 755 $(APP) $(DESTDIR)/usr/share/$(NAME)/$(NAME)
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
	@echo $(call print," ")

$(TAR): $(SRC) $(RES)
	@echo $(call p_targ)
	@tar -czvf $(TAR) $(SRC) $(RES)

$(NAME).1.gz: $(DOC)/$(NAME).1
	@echo $(call p_targ)
	# @gzip -v -c $? > $@
	@gzip -v -c $(DOC)/$(NAME).1 > $@

$(SPEC): $(SPECTEMPL) $(APP)
	@echo $(call p_targ)
	@cat $(SPECTEMPL) | \
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
