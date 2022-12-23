FROM osrf/ros:humble-desktop-full

RUN apt update && \ 
    DEBIAN_FRONTEND=noninteractive apt install -y \ 
    --no-install-recommends lubuntu-desktop \ 
    xrdp \ 
    locales \ 
    tilix

RUN rm /run/reboot-required*

RUN useradd -m ros -p $(openssl passwd 1234)
RUN usermod -aG sudo ros
RUN chsh -s bash ros
RUN adduser xrdp ssl-cert

RUN sed -i '3 a echo "\
    export GNOME_SHELL_SESSION_MODE=Lubuntu\\n\
    export XDG_SESSION_TYPE=x11\\n\
    export XDG_CURRENT_DESKTOP=LXQt\\n\
    export XDG_CONFIG_DIRS=/etc/xdg/xdg-Lubuntu:/etc/xdg\\n\
    export ROS_DISTRO=humble\\n\
    " > ~/.xsessionrc' /etc/xrdp/startwm.sh

RUN service dbus start; /usr/lib/systemd/systemd-logind & service xrdp start;

USER ros

RUN echo "cd ~/app" >> /home/ros/.bashrc
RUN echo "source ~/app/ros_entrypoint.sh" >> /home/ros/.bashrc

EXPOSE 3389
CMD bash