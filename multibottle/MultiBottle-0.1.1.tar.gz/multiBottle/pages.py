#from lib.libfuncs import *
# sys.path.append(sys.path[0]+"/templates")
# !!!
# import templates.basePage as basePage
from .subpages.sitePage import SitePage



# !!!
# class NavPage(basePage.BasePage):
class NavPage(SitePage):
    # def __init__(self,req):
    #	basePage.BasePage.__init__(self,req)

    # self.template='withNav.html'- template is already set well enough(basicpage)!!

    def setSitePageData(self, *a1, **a2):
        super().setSitePageData(*a1, **a2)
        # nav= [navlinks(self.rawnav,'breadCrumbs'),
        #		navlinks(self.rawnav,'siblings'),navlinks(self.rawnav,'children')]
        # self.navlist= [navlinks(self.rawnav,'breadCrumbs'),
        #		navlinks(self.rawnav,'siblings'),navlinks(self.rawnav,'children')]
        self.templateData['nav'] = self


    def setNav(self, *thelist):
        return  # cant kill this until page templates all updated
