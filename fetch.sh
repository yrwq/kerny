#!/bin/sh

kernel="$(uname -s)"

# get distro
if [ "$kernel" = "Linux" ]; then
    # get distro
    if [ -f /etc/os-release ]; then
        . /etc/os-release
    fi
    NAME=$PRETTY_NAME
fi

# get display protocol
[ "$DISPLAY" ] && displayprot="x11"
[ "$WAYLAND_DISPLAY" ] && displayprot="wayland"
# fallback to tty
[ ! "$displayprot" ] && displayprot="tty"

# get gtk-theme
while read -r line; do
    case $line in
        gtk-theme*) theme=${line##*=} ;;
    esac
done <"${XDG_CONFIG_HOME:-$HOME/.config}/gtk-3.0/settings.ini"

[ ! "$theme" ] && theme="unknown"

# get disk
disk_used="$(df -h | grep '/dev/sdb1' | awk '{print $3}')"
disk_total="$(df -h | grep '/dev/sdb1' | awk '{print $2}')"
disk="${disk_total} / ${disk_used}"

# get wm/de
wm="$XDG_CURRENT_DESKTOP"
[ "$wm" ] || wm="$DESKTOP_SESSION"
[ ! "$wm" ] && [ "$DISPLAY" ] && command -v xprop >/dev/null && {
    id=$(xprop -root -notype _NET_SUPPORTING_WM_CHECK)
    id=${id##* }
    wm=$(xprop -id "$id" -notype -len 100 -f _NET_WM__NAME 8t |
        grep '^_NET_WM_NAME' | cut -d\" -f 2)
}

# for non ewmh wms
[ ! "$wm" ] || [ "$wm" = "LG3D" ] &&
    wm=$(
        ps -e | grep -m 1 -o \
            -e "sway" \
            -e "kiwmi" \
            -e "wayfire" \
            -e "sowm" \
            -e "catwm" \
            -e "fvwm" \
            -e "dwm" \
            -e "2bwm" \
            -e "monsterwm" \
            -e "tinywm" \
            -e "xmonad"
)

# get terminal
term=$(
    ps -e | grep -m 1 -o \
        -e " alacritty$" \
        -e " kitty$" \
        -e " gnome-terminal$" \
        -e " xterm$" \
        -e " u*rxvt[dc]*$" \
        -e " [a-z0-9-]*terminal$" \
        -e " cool-retro-term$" \
        -e " konsole$" \
        -e " termite$" \
        -e " tilix$" \
        -e " sakura$" \
        -e " terminator$" \
        -e " termonad$" \
        -e " x*st$" \
        -e " tilda$"
)
# remove leading space
term=${term# }

[ ! "$term" ] && term="unknown"

# Screen resolution
unset i resolution

command -v xrandr >/dev/null && {
    for i in $(xrandr --current | grep ' connected' | grep -o '[0-9]\+x[0-9]\+'); do
        resolution="$resolution$i, "
    done
    resolution=${resolution%, }
}

editor=${EDITOR##*/}
[ ! $editor ] && editor="unknown"

cat <<EOF
Paste the following lines into a channel:

sudo setfetch
$NAME
$(uname -r)
$term
$editor
$wm
$resolution
$displayprot
$theme
$disk
EOF
