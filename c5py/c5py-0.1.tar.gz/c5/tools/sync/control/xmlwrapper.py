import xml.dom.minidom as dom
from ..model import itemmodel as im
import sys

class XMLWrapper:
    def __init__(self, a_model):
        pass
        self.model = a_model

    def save_model(self, file_path):
        doc = dom.getDOMImplementation().createDocument(None, "A SyncFinder Configuration", None)
        root = doc.documentElement
        root.tagName = "Project"
        root.setAttribute("name", self.model.get_name())
        root.setAttribute("path", self.model.get_path())
        sets_node = doc.createElement("Sets")
        layouts_node = doc.createElement("Layouts")

        root.appendChild(sets_node)
        root.appendChild(layouts_node)

        for set_string in self.model.get_set_names():
            a_set = self.model.get_set(set_string)
            a_layout = a_set.get_layout()
            set_node = doc.createElement("Set")
            set_node.setAttribute("name", a_set.get_name())
            set_node.setAttribute("layout", a_layout.get_name())
            for container_name in a_layout.get_container_names():
                container = a_set.get_container(container_name)
                con_node = doc.createElement("Container")
                con_node.setAttribute("name", container_name)
                con_node.setAttribute("status", str(container.get_status()))
                con_node.setAttribute("use_original", str(container.use_original()))
                used_events = ""
                for ev in container.get_used_events():
                    used_events += str(ev) + ","
                used_events = used_events.rstrip(",")
                con_node.setAttribute("used_events", used_events)
                con_node.setAttribute("path", str(container.path))
                events_node = doc.createElement("Events")
                files_node = doc.createElement("Files")
                events = container.get_sync_events()
                for event_key in events.keys():
                    event_node = doc.createElement("Event")
                    event_node.setAttribute("frame", str(event_key))
                    event_node.setAttribute("confidence", str(events[event_key]))
                    events_node.appendChild(event_node)
                for idx in range(container.get_file_count()):
                    file_node = doc.createElement("File")
                    file_node.setAttribute("path", container.get_file(idx).get_path())
                    files_node.appendChild(file_node)
                con_node.appendChild(events_node)
                con_node.appendChild(files_node)
                set_node.appendChild(con_node)
            for audio in a_set.get_audios():
                audio_node = doc.createElement("Audio")
                audio_node.setAttribute("path", audio.get_path())
                audio_node.setAttribute("status", str(audio.get_status()))
                audio_node.setAttribute("sync", str(audio.get_sync()))
                events = ""
                for ev in audio.get_events():
                    events += str(ev) + ","
                events = events.rstrip(",")
                audio_node.setAttribute("events", events)
                set_node.appendChild(audio_node)

            sets_node.appendChild(set_node)

        for layout_string in self.model.get_layout_names():
            layout = self.model.get_layout(layout_string)
            layout_node = doc.createElement("Layout")
            layout_node.setAttribute("name", layout.get_name())
            layout_node.setAttribute("width", str(layout.get_width()))
            layout_node.setAttribute("height", str(layout.get_height()))
            layout_node.setAttribute("ref", str(layout.get_ref_name()))
            for container_string in layout.get_container_names():
                container = layout.get_container(container_string)
                container_node = doc.createElement("Container")
                container_node.setAttribute("name", container.get_name())
                container_node.setAttribute("width", str(container.get_width()))
                container_node.setAttribute("height", str(container.get_height()))
                container_node.setAttribute("pos_x", str(container.get_pos_x()))
                container_node.setAttribute("pos_y", str(container.get_pos_y()))
                container_node.setAttribute("use_audio", str(container.use_audio()))
                layout_node.appendChild(container_node)
            layouts_node.appendChild(layout_node)
            layouts_node.setAttribute("default", self.model.get_default_layout().get_name())

        cfg_file = open(file_path, "w")
        cfg_file.write(doc.toprettyxml())
        cfg_file.close()

    def load_model(self, path):
        doc = dom.parse(path)
        root = doc.firstChild
        self.model.set_name(str(root.getAttribute("name")))
        self.model.set_path(str(root.getAttribute("path")))
        sets_node = root.getElementsByTagName("Sets")[0]
        layouts_node =  root.getElementsByTagName("Layouts")[0]
        default = layouts_node.getAttribute("default")

        for layout_node in layouts_node.childNodes:
            if layout_node.nodeType != doc.ELEMENT_NODE:
                continue
            layout = im.SetLayout(str(layout_node.getAttribute("name")))
            width_string = layout_node.getAttribute("width")
            height_string = layout_node.getAttribute("height")
            layout.set_dimension(int(width_string), int(height_string))
            layout.set_ref_name(str(layout_node.getAttribute("ref")))

            for container_node in layout_node.childNodes:
                if container_node.nodeType != doc.ELEMENT_NODE:
                    continue
                container = im.ContainerLayout(str(container_node.getAttribute("name")))
                width_string = container_node.getAttribute("width")
                height_string = container_node.getAttribute("height")
                pos_x_string = container_node.getAttribute("pos_x")
                pos_y_string = container_node.getAttribute("pos_y")
                container.set_dimension(int(width_string), int(height_string))
                container.set_position(int(pos_x_string), int(pos_y_string))
                container.set_use_audio(container_node.getAttribute("use_audio") == "True")
                layout.add_container(container)
            self.model.add_layout(layout)
            if layout.get_name() == default: self.model.set_default_layout(layout)

        for set_node in sets_node.childNodes:
            if set_node.nodeType != doc.ELEMENT_NODE:
                    continue
            a_set = im.SetItem(str(set_node.getAttribute("name")))
            a_layout = self.model.get_layout(str(set_node.getAttribute("layout")))
            a_set.set_layout(a_layout)

            for child_node in set_node.childNodes:
                if child_node.nodeType != doc.ELEMENT_NODE:
                    continue
                if child_node.tagName == "Container":
                    container = a_set.get_container(child_node.getAttribute("name"))
                    if container is None:
                        print "no container named %s found." % child_node.getAttribute("name")
                        sys.exit(1)
                    orig_string = child_node.getAttribute("use_original")
                    container.set_original((orig_string in str(True)))
                    container.path = child_node.getAttribute("path")

                    events_node = child_node.getElementsByTagName("Events")[0]
                    files_node = child_node.getElementsByTagName("Files")[0]
                    for event_node in events_node.childNodes:
                        if event_node.nodeType != doc.ELEMENT_NODE:
                            continue
                        frame_string =  event_node.getAttribute("frame")
                        confidence_string = event_node.getAttribute("confidence")
                        container.add_sync_event(int(frame_string), float(confidence_string))

                    for file_node in files_node.childNodes:
                        if file_node.nodeType != doc.ELEMENT_NODE:
                            continue
                        container.add_file(file_node.getAttribute("path"))

                    container.set_status(int(child_node.getAttribute("status")))
                    events_string = child_node.getAttribute("used_events").split(",")
                    if len(events_string) == 2:
                        container.set_used_events([int(event) for event in events_string])
                elif child_node.tagName == "Audio":
                    audio = im.AudioItem(child_node.getAttribute("path"))
                    events_string = child_node.getAttribute("events")
                    if len(events_string) > 0:
                        audio.set_events([float(event) for event in events_string.split(",")])
                    sync = child_node.getAttribute("sync")
                    if sync == "None":
                        sync = None
                    else:
                        sync = float(sync)
                    audio.set_sync(sync)
                    audio.set_status(int(child_node.getAttribute("status")))
                    a_set.add_audio(audio)
            self.model.add_set(a_set)

def test():
    model = im.ModelItem("Project")
    layout = im.SetLayout("Default Layout")
    layout.set_dimension(640, 240)
    container1 = im.ContainerLayout("links")
    container1.set_dimension(320, 240)
    container1.set_position(0, 0)
    container2 = im.ContainerLayout("rechts")
    container2.set_dimension(320, 240)
    container2.set_position(320, 0)

    layout2 = im.SetLayout("Another Layout")
    layout2.set_dimension(1920, 1080)
    container3 = im.ContainerLayout("oben links")
    container3.set_dimension(320, 240)
    container3.set_position(0, 0)
    container4 = im.ContainerLayout("unten rechts")
    container4.set_dimension(320, 240)
    container4.set_position(1600, 840)

    layout.add_container(container1)
    layout.add_container(container2)
    layout2.add_container(container3)
    layout2.add_container(container4)

    test_set = im.SetItem("Test Set")
    test_set.set_layout(layout)

    model.add_layout(layout)
    model.add_layout(layout2)
    model.add_set(test_set)
    test_set.get_container("rechts").add_file("img/error.mp4")
    test_set.get_container("rechts").set_synced(True)
    test_set.get_container("links").add_file("img/error.mts")
    test_set.get_container("rechts").add_sync_event(1,2.65)

    wrapper = XMLWrapper(model)
    wrapper.save_model("test.cfg")
    model2 = im.ModelItem("Another Project")
    wrapper.load_model(model2, "test.cfg")
    print (model.get_name() == model2.get_name())
    print (model.get_layout_names() == model2.get_layout_names())
    print (model.get_layout("Default Layout").get_container_names() ==
             model2.get_layout("Default Layout").get_container_names())
    print (model.get_layout("Default Layout").get_container("rechts").get_height() ==
             model2.get_layout("Default Layout").get_container("rechts").get_height())
    print ("---------------")
    print (model.get_set("Test Set").get_container("rechts").is_synced() ==
             model2.get_set("Test Set").get_container("rechts").is_synced())
    print (model.get_set("Test Set").get_container("links").is_prepared() ==
             model2.get_set("Test Set").get_container("links").is_prepared())
    print (model.get_set("Test Set").get_container("rechts").get_sync_events() ==
             model2.get_set("Test Set").get_container("rechts").get_sync_events())

if __name__ == '__main__':
    test()
