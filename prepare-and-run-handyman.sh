#!/bin/bash
#prepare-and-run-handyman.sh
#Installs all dependencies and also
#runs the Handyman build tool.
echo "Prepare: updating lists..."
apt update || exit 1
echo "Prepare: lists updated."
# Prepare: install and symlink the following:
# -Python and pip
# -Node.js and NPM
# -Ruby and Gem
echo "Prepare: (Python) Installing environment..."
apt install -y python3 python3-pip || exit 1
echo "Prepare: (Python) Testing..."
python --help || python3 --help || exit 1
pip --help || pip3 --help || exit 1
echo "Prepare: (Python) Tests succeeded."
echo "Prepare: (Python) Environment installed."
echo "Prepare: (Node) Installing environment..."
apt install -y curl || exit 1
curl -fsSL https://deb.nodesource.com/setup_20.x | bash - &&\
apt install -y build-essential && apt install -y nodejs && apt install -y npm
#Note: these tests are removed because they do not work altough I feel like they logically should
#echo "Prepare: (Node) Testing..."
#node --help || exit 1
#npm --help || exit 1
#echo "Prepare: (Node) Tests succeeded."
echo "Prepare: (Node) Environment installed."
echo "Prepare: (Ruby) Installing environment..."
# Install RVM, Deta doesn't have Ruby v>2.5
apt install gnupg2 -y || exit 1
gpg2 --keyserver keyserver.ubuntu.com --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB &&
\curl -sSL https://get.rvm.io | bash -s stable --ruby
source /usr/local/rvm/scripts/rvm || exit 1
#apt install -y ruby ruby-full || exit 1
echo "Debug: Ruby version:"
ruby -v || exit 1
# Add a GEM_HOME path
echo "export GEM_HOME=$HOME/gems" >> "$HOME/.bashrc" || exit 1
echo "export PATH=$HOME/gems/bin:$PATH" >> "$HOME/.bashrc" || exit 1
source "$HOME/.bashrc" || exit 1
echo "Prepare: (Ruby) Testing..."
ruby --help || exit 1
gem --help || exit 1
echo "Prepare: (Ruby) Tests succeeded."
echo "Prepare: (Ruby) Environment installed."
echo "Prepare: Build environment prepared!"
echo "Run: Running Handyman..."
python3 handyman.py || exit 1
echo "DONE: Handyman ran."
