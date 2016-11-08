#
# TODO
#
# prevent multiple class of init_renderjs - ie. check if loading_gadget there
# find proper location for static files
#
#


# For each gadget which is to be integrated into the jupyter page one
# RJSGadget object is created. It is used to call call_declared_method
# and destroy.
class RJSGadget:

    def __init__(self, gadgetId):
        # The UID is used to identify the gadget and gets passed along
        # to the events sent to the frontend so that the loading_gadget
        # is able to decide to which gadget the fired event belongs

        # Python call on object with (uid) ->
        # -> Fire event (uid) ->
        # -> loading_gadget (uid) ->
        # -> pass on the call to gadget with (uid)
        self.gadgetId = gadgetId

    def __del__(self):
        pass

    # Fires an event with
    #    * the uid of the gadget
    #    * the name of the declared_method
    #    * the arguments to be passed to the declared_method
    # The arguments are packed into a json string and passed to js as such
    def call_declared_method(self, method_name, *args):
        from IPython.core.display import display, HTML
        import json
        j_str = json.dumps(args)
        script = '''
        <script>
        var call_event = new CustomEvent("call_gadget",
        { "detail": {
        "gadgetId": "''' + self.gadgetId + '''",
        "methodName": "''' + method_name + '''",
        "methodArgs": ''' + "'" + j_str + "'" + '''
        }});
        var loadingDiv = document.querySelector(".loading_gadget");
        if(loadingDiv != null) {
          loadingDiv.dispatchEvent(call_event);
        } else {
          console.log("~~ call: RenderJS init required first!");
        }
        </script>
        '''
        display(HTML(script))

    # Fires an event to the destroy this gadget (self)
    # Only thing passed is the uid of the gadget
    def destroy(self):
        from IPython.core.display import display, HTML
        script = '''
        <script>
        var destroy_event = new CustomEvent("destroy_gadget",
        { "detail": { "gadgetId": "''' + self.gadgetId + '''" }});
        var loadingDiv = document.querySelector(".loading_gadget");
        if(loadingDiv != null) {
          loadingDiv.dispatchEvent(destroy_event);
        } else {
          console.log("~~ destroy: RenderJS init required first!");
        }
        </script>
        '''
        display(HTML(script))


# Do nothing on load
def load_ipython_extension(ipython):
    pass

# Do nothing on unload
def unload_ipython_extension(ipython):
    pass



# Create the original load_gadget with modified rsvp, renderjs
# Because jupyter notebook has already loaded when this can be called
# a manual intialization of the whole renderJS setup is required
#
# First the libs rsvp, renderjs-gadget-global and renderjs (patched)
# are injected into the page. The patch on renderjs itself is to enable
# the following manual bootstrap

# After the scripts are present, a div is appended containing the
# loading_gadget.

# After everything is inplace, rJS.manualBootstrap initializes the
# loading_gadget in exactly the same way as when rJS is normally initialized
# (on-load)
def init_renderjs():
    from IPython.core.display import display, HTML
    script = '''
    <script>
    var loadingDiv = document.querySelector(".loading_gadget");
    if(loadingDiv == null) {
      console.log("~~ Initializing RenderJS!");
      $.getScript("/nbextensions/renderjs_nbextension/rsvp-2.0.4.js", function() {
        console.log("~~ loading_gadget: rsvp.js loaded");
        $.getScript("/nbextensions/renderjs_nbextension/rjs_gadget_global_js.js", function() {
          console.log("~~ loading_gadget: renderjs-gadget-global.js loaded");
          $.getScript("/nbextensions/renderjs_nbextension/renderjs-latest.js", function() {
            console.log("~~ loading_gadget: renderjs.js loaded");
            $("#notebook-container").append('<div data-gadget-url="/nbextensions/renderjs_nbextension/loading_gadget.html" data-gadget-scope="public"></div>');
            rJS.manualBootstrap();
          });
        });
      });
    } else {
      console.log("~~ Renderjs seems to be initialized already!");
    }
    </script>
    '''
    display(HTML(script))


# Load a gadget given a URL to the HTML file of the gadget
# -> Generates a new uid for the gadget to-be-loaded
# -> Fires an event which loading_gadget listens on and passes on the URL
# -> returns the python gadget-object which has the uid as member-variable
def load_gadget(gadgetUrl):
    from IPython.core.display import display, HTML
    import uuid
    gadgetId = str(uuid.uuid4())
    script = '''
    <script>
    var load_event = new CustomEvent("load_gadget",
    { "detail": { "url": "''' + gadgetUrl + '", "gadgetId": "' + gadgetId + '''" }});

    var loadingDiv = document.querySelector(".loading_gadget");
    if(loadingDiv != null) {
      loadingDiv.dispatchEvent(load_event);
    } else {
      console.log("~~ load: RenderJS init required first!");
    }
    </script>
    '''
    display(HTML(script))
    return RJSGadget(gadgetId)
