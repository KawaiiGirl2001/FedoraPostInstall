import os
import platform
import sys
import subprocess

def run_commands(commands):
    for command in commands:
        subprocess.run(command, shell=True, check=False)

def check_os():
    if platform.system() == "Linux" and platform.node() == "fedora":
            print("Starting Fedora 39 configuration...")
    else:
        print("This program is only compatible with Fedora Linux.")
        sys.exit(1)    

check_os()

graphics_card = ""
device_type = ""
tlp_install = ""
lag_sensation = ""
reboot = ""

run_commands([
    # run DNF update
    "sudo dnf update -y",
    # connect RPM Fusion
    "sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm",
    "sudo dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm",
    # install media codecs and vaapi
    "sudo dnf install -y ffmpeg gstreamer1-libav gstreamer1-plugins-ugly gstreamer1-plugins-bad-freeworld libva-intel-driver",
    "sudo dnf groupupdate -y 'core' 'multimedia' 'sound-and-video' --setop='install_weak_deps=False' --exclude='PackageKit-gstreamer-plugin' --allowerasing && sync",
    "sudo dnf swap -y 'ffmpeg-free' 'ffmpeg' --allowerasing",
    "sudo dnf install -y gstreamer1-plugins-bad gstreamer1-plugins-good gstreamer1-plugins-base gstreamer1-plugin-openh264 gstreamer1-libav --exclude=gstreamer1-plugins-bad-free-devel ffmpeg gstreamer-ffmpeg",
    "sudo dnf group upgrade -y --with-optional Multimedia",
    "sudo dnf install -y ffmpeg ffmpeg-libs libva libva-utils"
])

while graphics_card != "AMD" and graphics_card != "Intel":
    graphics_card = input("Which graphics card are you using? (AMD/Intel): ")
    if graphics_card == "AMD":
        run_commands(["sudo dnf swap -y mesa-va-drivers mesa-va-drivers-freeworld"])
    elif graphics_card == "Intel":
        run_commands(["sudo dnf install -y intel-media-driver"])
    else:
        print("Invalid input. Please choose AMD or Intel.")

while device_type != "laptop" and device_type != "desktop":
    device_type = input("Are you using a laptop or a desktop? (laptop/desktop): ")
    if device_type == "laptop":
        tlp_install = input("Do you want to install TLP for better battery life? (yes/no): ")
    if tlp_install == "yes":
        run_commands([
            "sudo dnf install -y tlp tlp-rdw",
            "sudo systemctl mask power-profiles-daemon",
            "sudo dnf install -y powertop",
            "sudo powertop --auto-tune"
        ])
    elif device_type == "desktop":
        print("TLP installation is only available for laptops.")
    else:
        print("Invalid input. Please choose laptop or desktop.")    


# Software installation
run_commands([
    "sudo dnf install -y fish mc neofetch gnome-tweaks adw-gtk3-theme",
    "chsh -s /usr/bin/fish",
    "flatpak install -y flathub org.telegram.desktop com.valvesoftware.Steam net.lutris.Lutris org.onlyoffice.desktopeditors org.videolan.VLC com.microsoft.Edge org.chromium.Chromium sh.cider.Cider app.moosync.moosync org.kde.kdenlive org.gimp.GIMP org.inkscape.Inkscape com.obsproject.Studio com.mattjakeman.ExtensionManager com.visualstudio.code com.transmissionbt.Transmission com.discordapp.Discord org.gnome.Geary"
])

# GNOME configuration
run_commands([
    # Enable adw-gtk3 theme
    "gsettings set org.gnome.desktop.interface gtk-theme 'adw-gtk3'",
    # Enable window buttons "minimize", "maximize", "close"
    "gsettings set org.gnome.desktop.wm.preferences button-layout 'appmenu:minimize,maximize,close'",
    # Configure CapsLock to switch layout
    "gsettings set org.gnome.desktop.input-sources xkb-options \"['grp:caps_toggle']\""
])

# Install and configure oh-my-fish (omf)
subprocess.Popen(['gnome-terminal', '--', 'fish', '-c', 'curl https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish; omf install neolambda']).wait()

while lag_sensation != "yes" and lag_sensation != "no":
    lag_sensation = input("Do you experience lag in the GNOME interface? (yes/no): ")
    if lag_sensation == "yes":
        os.system("sudo dnf copr enable trixieua/mutter-patched -y && sudo dnf update --refresh")
    elif lag_sensation == "no":
        print("No need to install the Mutter patch.")
    else: print("Invalid input. Please choose yes or no.")

print("Fedora 39 configuration completed.")

while reboot != "yes" and reboot != "no":
    reboot = input("Do you want to reboot the system now? (yes/no): ")
    if reboot == "yes":
        os.system("sudo systemctl reboot")
    elif reboot == "no":
        print("Reboot canceled. It is recommended to manually reboot the system soon.")
    else: print("Invalid input. Please choose yes or no.")


