## `RuntimeError: Failed to open TCP connection to SOME-URL:443 (failed to get urandom)`

This is a DNS error and occurs very rarely. The fix can be found here: [https://1.1.1.1/dns/](https://1.1.1.1/dns/)

1. Open System Preferences.
2. Search for DNS Servers and select it from the dropdown.
3. Click the + button to add a DNS Server and enter 1.1.1.1
4. Click + again and enter 1.0.0.1 (This is for redundancy.)
5. Click + again and enter 2606:4700:4700::1111 (This is for redundancy.)
6. Click + again and enter 2606:4700:4700::1001 (This is for redundancy.)
7. Click Ok, then click Apply.
8. You’re all set! Your device now has faster, more private DNS servers.

## Errors running `npm install`

Usually this happens when changing branches with different packages for testing but it can happen in other circumstances as well.

For this the simplest solution is:
1. `rm -rf ./node_modules`
2. `npm i`
3. `yarn install`

## `postgress` related issues

### Random issue can't open server anymore.

This is a weird `psql` bug that occurs on mac just add this to `~/.zshrc`
```
# Fix postgress error
export PGGSSENCMODE="disable"
```

PG (0.19.0) error
```sh
gem install pg -v "0.19.0" -- --with-cflags=-Wno-error=incompatible-function-pointer-types
```

### A threading error while running some queries in the server

A threading issue on macos can be fixed by adding this to `~/.zshrc` or the `.envrc` file in the project:
```
# Fix NSCFConstantString initialize error
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

### Ruby fails to install (We used `2.7.8` as an example but should work with any version)

How to install `ruby 2.7.8`
`brew install openssl@1.1`
After that run `brew info openssl@1.1` and following the path were it says its installed add to `~/.zshrc` JUST ONE of the following:
```
# Link Openssl 1.1 -------------------------------------------------------------
# Add to path
export PATH="/usr/local/opt/openssl@1.1/bin:$PATH"

# For compilers to find
export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib"
export CPPFLAGS="-I/usr/local/opt/openssl@1.1/include"

# or pkg-config to find
export PKG_CONFIG_PATH="/usr/local/opt/openssl@1.1/lib/pkgconfig"

# ========== OR THIS ONE ==================

# Link Openssl 1.1 -------------------------------------------------------------
# Add to path
export PATH="/opt/homebrew/opt/openssl@1.1/bin:$PATH"

# For compilers to find
export LDFLAGS="-L/opt/homebrew/opt/openssl@1.1/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openssl@1.1/include"

# or pkg-config to find
export PKG_CONFIG_PATH="/opt/homebrew/opt/openssl@1.1/lib/pkgconfig"
```

Then run:

`CFLAGS="-Wno-compound-token-split-by-macro -Wno-deprecated-declarations -Wno-deprecated-non-prototype -Wno-incompatible-function-pointer-types -Wno-incompatible-pointer-types-discards-qualifiers -Wno-deprecated-declarations -Wno-pointer-to-enum-cast -Wno-unused-value -Wno-void-pointer-to-enum-cast" rvm install 2.7.8`
If the above command gives any errors try running it without the CFLAGS simply as `rvm install 2.7.8`

## Error installing `node 14.20.0` trough `nvm`

This seems to occur on newer version of macos sicne they dropped support for `python 2.7`

Install `pyenv`:
- `brew install pyenv`

Create an environment with `python 2.7`:
```
pyenv init           
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell 2.7.18
```

Install `node`:
- `nvm install 14.20.0`

Set this as the default version:
- `nvm alias default v14.20.0`

## Error with `mimemagic` gem
- `brew install shared-mime-info`
- `bundle update mimemagic` (This might be optional)
- `bundle install`

## Resque won't start

There is a weird bug that rarely and seemingly randomly happens.
In some cases the job queue `QUEUE=* rake environment resque:work` doesn't start, usually the last message that is displays is something about `Redis.srem?`, this is a red herring.

Run the command again with `VVERBOSE=1 QUEUE=* rake environment resque:work` [Thats 2 V's].
If the last error is a stack to deep error and the worker won't start there are 2 things that might cause this.

1. You wrote something wrong in code that causes a circular dependecy like validations, properties like `depend: :destroy`, or similar.
2. Something blocks `newrelic`. Comment the gem and run `bundle install` and all should work. I can not pinpoint what is causing this exactly.
2 cases that were reported were fixed by themself the next day, without doing anything, and once after installing `hexnode` on a new laptop. So either something randomly blocks newrelic, like switching to a different network, or hexnode is blocking it, but this is just a theory for now.