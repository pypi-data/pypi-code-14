from docker_ascii_map.widget import *

from docker_ascii_map.docker_config import Configuration, Container


def build_container_widget(container: Container, encoding: str) -> Widget:
    lines = []
    if encoding == 'UTF-8':
        statuschar = u"\u2713" if container.status == 'running' else u"\u274c"
    else:
        statuschar = 'V' if container.status == 'running' else 'x'

    lines.append('[' + statuschar + '] ' + container.name)
    lines.append('    ' + container.image)
    container_widget = Paragraph(lines)
    return container_widget


def build_ordered_network_list(config):
    networks = set()

    for container in config.containers:
        for net in container.networks:
            networks.add(net)

    networks = list(networks)
    networks.sort()

    # Networks are sorted, now group the ones linked by containers

    for container in config.containers:
        if len(container.networks) > 1:
            base_index = networks.index(container.networks[0])
            for net in container.networks[1:]:
                networks.remove(net)
                base_index += 1
                networks.insert(base_index, net)

    return networks


class Renderer:
    def __init__(self):
        pass

    def render(self, config: Configuration, encoding: str = 'UTF-8'):
        network_widgets = []

        networks = build_ordered_network_list(config)

        net_widgets_map = {}
        cnt_widgets_map = {}

        # Network boxes with single-network containers

        for net in networks:
            net_widgets = []

            for container in config.containers:
                if [net] == container.networks:
                    container_widget = build_container_widget(container, encoding)
                    cnt_widgets_map[container] = container_widget
                    net_widgets.append(container_widget)

            net_box = Border(VBox(net_widgets), net)
            net_widgets_map[net] = net_box
            network_widgets.append(net_box)

        # Containers connected to multiple networks

        bridge_widgets = []
        links = []

        for container in config.containers:
            if len(container.networks) > 1:
                c = Padding(build_container_widget(container, encoding), Size(1, 0))
                cnt_widgets_map[container] = c
                padded = Padding(c, Size(12, 2))
                bridge_widgets.append(padded)

                for n in container.networks:
                    net_box = net_widgets_map[n]
                    links.append((c, net_box))

        networks_box = VBox(network_widgets)
        bridges_box = VBox(bridge_widgets)
        links_box = Links(HBox([bridges_box, networks_box]), links)

        # Port mapping

        portmaps = []

        for container in config.containers:
            for port in container.ports:
                w = cnt_widgets_map[container]
                portmaps.append((w, str(port.public_port)))

        ports_box = Annotations(links_box, portmaps)

        root_box = ports_box
        return str(root_box.render())
