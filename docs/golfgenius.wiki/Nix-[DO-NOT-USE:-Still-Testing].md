Nix
===

Nix is a tool that takes a unique approach to package management and system configuration.

> [!TIP]
> If you encounter problems contact `@vele-dan-alexandru` on slack.

# Useful links
- [Official Site](https://nixos.org/)
- [Nix SubReddit](https://www.reddit.com/r/NixOS/)

- [Quick Guide to Nix](https://zero-to-nix.com/)
- [Site dedicated to learning nix](https://nix.dev/)
- [Introduction to flakes](https://blog.kubukoz.com/flakes-first-steps/)

# How to install
- [Official Install Guide](https://nixos.org/download/)

## Install the `nix` package manager
```sh
sh <(curl -L https://nixos.org/nix/install)
```

## Enable `flake` support for nix.
> [!NOTE]
> `flake`s are a way to declare projects in nix using a `flake.nix` file.

```sh
mkdir -p "$HOME/.config/nix"
echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
```

## Add macos upgrade fix

An incident occurred when I updated my MacOS version (because Apples motto is **F** the developers) and `nix` was no longer found... just add this to `~/.zshrc`.
```sh
# Nix
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
  . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi
# End Nix
```

> [!CAUTION]
> Restart your PC after running **ALL** of the above.

# Additional setup

Nix environments can be automatically picked up be using `direnv` so lets install it using `nix`:
```sh
nix profile install nixpkgs#direnv
echo 'eval "$(direnv hook zsh)"' >> "$HOME/.zshrc"
source "$HOME/.zshrc"
```
