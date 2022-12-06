# CP4101 B.Comp. Dissertation

## Installing Required Programs

### Prerequisites

- Recommended OS: Ubuntu 22.04 or later
- git
- Python 3

### Installing Mininet

1. Clone Mininet repository.
   ```
   $ git clone https://github.com/mininet/mininet
   $ cd mininet
   ```
1. (Optional) Checkout latest stable release.
   ```
   $ git tag -l
   $ git checkout <tag>
   ```
1. (Optional) Patch installation script.
   [Only necessary for releases prior to and including 2.3.0]
   ```
   $ sed -i 's/git:\/\//https:\/\//g' util/install.sh
   ```
1. Run installation script.
   ```
   $ util/install.sh -nvf
   ```

### Installing FRR

1. Install dependencies.
   ```
   $ sudo apt-get update
   $ sudo apt-get install \
       autoconf automake libtool make libreadline-dev texinfo \
       pkg-config libpam0g-dev libjson-c-dev bison flex \
       libc-ares-dev python-is-python3 python3-dev python3-sphinx \
       install-info build-essential libsnmp-dev perl \
       libcap-dev python2 libelf-dev libunwind-dev \
       libyang2-dev
   ```
1. Clone FRR repository.
   ```
   $ git clone https://github.com/FRRouting/frr.git
   $ cd frr
   ```
1. (Optional) Checkout latest stable release.
   ```
   $ git tag -l
   $ git checkout <tag>
   ```
1. Create service account.
   ```
   $ sudo groupadd -r -g 92 frr
   $ sudo groupadd -r -g 85 frrvty
   $ sudo adduser --system --ingroup frr --home /var/run/frr/ \
       --gecos "FRR suite" --shell /sbin/nologin frr
   $ sudo usermod -a -G frrvty frr
   ```
1. Configure build parameters.
   ```
   $ ./bootstrap.sh
   $ ./configure \
       --prefix=/usr/local \
       --includedir=\${prefix}/include \
       --bindir=\${prefix}/bin \
       --sbindir=\${prefix}/sbin/frr \
       --libdir=\${prefix}/lib/frr \
       --libexecdir=\${prefix}/lib/frr \
       --localstatedir=/var/run/frr \
       --sysconfdir=/etc/frr \
       --enable-vty-group=frrvty \
       --with-moduledir=\${prefix}/lib/frr/modules \
       --with-libyang-pluginsdir=\${prefix}/lib/frr/libyang_plugins \
       --enable-configfile-mask=0640 \
       --enable-logfile-mask=0640
   ```
1. Build and install FRR.
   ```
   $ make
   $ sudo make install
   ```
1. Install configuration files.
   ```
   $ sudo install -m 775 -o frr -g frr -d /var/log/frr
   $ sudo install -m 775 -o frr -g frrvty -d /etc/frr
   $ sudo install -m 640 -o frr -g frrvty tools/etc/frr/vtysh.conf /etc/frr/vtysh.conf
   $ sudo install -m 640 -o frr -g frr tools/etc/frr/frr.conf /etc/frr/frr.conf
   $ sudo install -m 640 -o frr -g frr tools/etc/frr/daemons.conf /etc/frr/daemons.conf
   $ sudo install -m 640 -o frr -g frr tools/etc/frr/daemons /etc/frr/daemons
   ```
1. Link necssary binaries.
   ```
   $ sudo ln -s /usr/local/sbin/frr/zebra /usr/local/bin/zebra
   $ sudo ln -s /usr/local/sbin/frr/ripd /usr/local/bin/ripd
   $ sudo ln -s /usr/local/sbin/frr/bgpd /usr/local/bin/bgpd
   ```

### Installing BIRD

1. Install dependencies.
   ```
   $ sudo apt-get update
   $ sudo apt-get install autoconf gcc flex bison libncurses-dev libreadline-dev
   ```
1. Clone BIRD repository
   ```
   $ git clone https://gitlab.nic.cz/labs/bird.git
   $ cd bird
   ```
1. (Optional) Checkout latest stable release.
   ```
   $ git tag -l
   $ git checkout <tag>
   ```
1. Create service account.
   ```
   $ sudo groupadd -r -g 180 bird
   $ sudo adduser --system --ingroup bird --no-create-home \
       --gecos "BIRD Internet Routing Daemon" --shell /sbin/nologin bird
   ```
1. Configure build parameters.
   ```
   $ autoreconf
   $ ./configure \
     --prefix=/usr/local \
     --includedir=\${prefix}/include \
     --bindir=\${prefix}/bin \
     --sbindir=\${prefix}/sbin/bird \
     --libdir=\${prefix}/lib/bird \
     --libexecdir=\${prefix}/lib/bird \
     --runstatedir=/var/run/bird \
     --sysconfdir=/etc/bird
   ```
1. Build and install BIRD.
   ```
   $ make
   $ sudo make install
   ```
1. Link necssary binaries.
   ```
   $ sudo ln -s /usr/local/sbin/bird/bird /usr/local/bin/bird
   $ sudo ln -s /usr/local/sbin/bird/birdc /usr/local/bin/birdc
   $ sudo ln -s /usr/local/sbin/bird/birdcl /usr/local/bin/birdcl
   ```
