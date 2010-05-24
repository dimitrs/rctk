from rctk.tests.base import BaseTest

#
# - test events, etc?
# - test clickable generically. Mixin with button, etc?

xml_skeleton = """<?xml version="1.0"?>
<!-- let's pretend, for now, that we accept valid wxxrc -->
<resource xmlns="http://www.wxwidgets.org/wxxrc" version="2.5.3.0">
%(xml)s
</resource>"""

class Storage(object):
    pass

class BaseXMLBuilderTest(BaseTest):
    """
        test simple XML builder 
    """

    def setup_method(self, method):
        super(BaseXMLBuilderTest, self).setup_method(method)

        from rctk.xmlbuilder import SimpleXMLBuilder
        self.storage = Storage()
        self.builder = SimpleXMLBuilder(self.tk.root(), self.storage)

    def build_xml(self, xml):
        return xml_skeleton % dict(xml=xml)

class TestSimpleXMLBuilder(BaseXMLBuilderTest):
    def test_empty(self):
        self.builder.fromString(self.build_xml(""))
        assert len(self.tk._queue) == 0

from rctk.xmlbuilder import XMLControlRegistry

class BaseControlTest(BaseXMLBuilderTest):
    type = None
    @property
    def xml(self):
        return self.build_xml('<object class="%s" name="hello"></object>' % self.type)
        
    def test_in_registry(self):
        assert self.type in XMLControlRegistry

    def test_simple(self):
        self.builder.fromString(self.xml)

        ## verify it's been created in storage
        assert hasattr(self.storage, 'hello')
        w = self.storage.hello
        assert w.name == XMLControlRegistry[self.type].name

        ## verify tasks have been created

        assert len(self.tk._queue) == 2
        create = self.tk._queue[0]._task
        append = self.tk._queue[1]._task
        assert create['action'] == 'create'
        assert create['control'] == XMLControlRegistry[self.type].name
        assert create['id'] == w.id

        assert append['action'] == 'append'
        assert append['id'] == self.tk.root().id
        assert append['child'] == w.id

class TestButtonXML(BaseControlTest):
    type = "Button"
    
    @property
    def xml(self):
        ## Button (and StaticText) require a text parameter, so it also needs
        ## to be in the XML
        return self.build_xml('<object class="%s" name="hello"><text>Hello World</text></object>' % self.type)

    def test_textnode(self):
        """ The simple test doesn't test if a textnode gets parsed/set """
        self.builder.fromString(self.xml)
        
        assert self.storage.hello.text == "Hello World"

class TestStaticTextXML(TestButtonXML):
    type = "StaticText"
    
class TestCheckBoxXML(BaseControlTest):
    type = "CheckBox"

class TestTextXML(BaseControlTest):
    type = "Text"

class TestDateXML(BaseControlTest):
    type = "Date"

class TestPasswordXML(BaseControlTest):
    type = "Password"

class TestListXML(BaseControlTest):
    type = "List"

class TestDropdownXML(BaseControlTest):
    type = "Dropdown"

# requires column definitions and probably special xml handling
#class TestGridXML(BaseControlTest):
#    type = "Grid"

## Panel, Window

class BaseContainerTestXML(BaseControlTest):
    type = None

    @property
    def sub_xml(self):
        return self.build_xml('<object class="%s" name="hello"><object class="Button" name="foo"><text>Foo Bar</text></object></object>' % self.type)

    def test_subobjects(self):
        # import pdb; pdb.set_trace()
        self.builder.fromString(self.sub_xml)
        
        assert hasattr(self.storage, "foo")
        container = self.storage.hello
        button = self.storage.foo

        assert len(self.tk._queue) == 4
        ## first / second entry are create/append of container to root,
        ## which is already tested
        assert self.tk._queue[0]._task['action'] == 'create'
        assert self.tk._queue[1]._task['action'] == 'append'

        ## creation of button
        assert self.tk._queue[2]._task['action'] == 'create'
        assert self.tk._queue[2]._task['control'] == 'button'

        ## append of button to container
        assert self.tk._queue[3]._task['action'] == 'append'
        assert self.tk._queue[3]._task['id'] == container.id
        assert self.tk._queue[3]._task['child'] == button.id


class TestPanelTestXML(BaseContainerTestXML):
    type = "Panel"


class TestWindowTestXML(BaseContainerTestXML):
    type = "Window"

    ## window requires a title
    @property
    def xml(self):
        return self.build_xml('<object class="%s" name="hello"><title>Hello World</title></object>' % self.type)

    @property
    def sub_xml(self):
        return self.build_xml('<object class="%s" name="hello"><title>Hello World</title><object class="Button" name="foo"><text>Foo Bar</text></object></object>' % self.type)
