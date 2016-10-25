import json
from ftw.builder import Builder
from ftw.builder import create
from ftw.sliderblock.testing import FTW_SLIDERBLOCK_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase


class TestSliderBlockRendering(TestCase):

    layer = FTW_SLIDERBLOCK_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestSliderBlockRendering, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Site Administrator'])
        self.page = create(Builder('sl content page'))

        slick_config = json.dumps(
            {'arrows': 'false', 'autoplaySpeed': 1000, 'autoplay': 'false'}
        )
        block_builder = Builder('sliderblock')
        block_builder.within(self.page)
        block_builder.titled('SliderBlock title')
        block_builder.having(slick_config=slick_config)
        self.block = create(block_builder)

        create(Builder('slider pane')
               .within(self.block)
               .titled(u'Pane 1')
               .with_dummy_image())
        create(Builder('slider pane')
               .within(self.block)
               .titled(u'Pane 2')
               .with_dummy_image())

    @browsing
    def test_slider_panes_visible(self, browser):
        browser.login().visit(self.block, view='@@block_view')
        self.assertEquals(2, len(browser.css('.sliderPane')))

    @browsing
    def test_custom_slick_config(self, browser):
        browser.login().visit(self.block, view='@@block_view')

        self.assertEquals(
            {'labels': {'pause': 'Pause',
                        'play': 'Play',
                        'prev': 'Previous',
                        'next': 'Next'},
             'arrows': 'false', 'autoplaySpeed': 1000, 'autoplay': 'false'},
            json.loads(browser.css('.sliderWrapper').first.attrib['data-settings']))

    @browsing
    def test_custom_slick_config_has_no_newline(self, browser):
        """
        This test makes sure the slick config does not contain newlines
        and is valid json.
        """
        browser.login().visit(self.block, view='edit.json')
        browser.open_html(browser.json['content'])
        browser.fill(
            {'form.widgets.slick_config': u'{"foo": true, \n"bar": 2000}'}
        ).save()

        browser.login().visit(self.page)
        self.assertDictEqual(
            json.loads(
                '{"labels": {"prev": "Previous", "play": "Play", "pause": "Pause", "next": "Next"}, "foo": true, "bar": 2000}'
            ),
            json.loads(
                browser.css('.sl-block-content div').first.attrib['data-settings']
            )
        )

    @browsing
    def test_emtpy_slick_config(self, browser):
        page = create(Builder('sl content page'))
        block = create(Builder('sliderblock')
                       .within(page)
                       .titled('SliderBlock title')
                       .having(slick_config=''))

        create(Builder('slider pane')
               .within(block)
               .titled(u'Pane 1')
               .with_dummy_image())

        browser.login().open(page)
        self.assertEqual(
            '{}',
            browser.css('.sl-block-content div').first.attrib['data-settings'])
