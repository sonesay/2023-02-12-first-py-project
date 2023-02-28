from html2ans.parsers.image import ImageParser
from html2ans.parsers.base import ParseResult
from html2ans.parsers.raw_html import RawHtmlParser


class ArcIframeParser(RawHtmlParser):
    # applicable_elements = ['div', 'figure']
    # applicable_classes = ['fancy-figure']

    applicable_elements = ['h4']
    applicable_classes = []

    def parse(self, element, *args, **kwargs):
        iframe_tag = element.find('iframe')
        # caption_tag = element.find('p', {"class": "fancy-caption"})
        if iframe_tag:
            iframe = self.construct_output(iframe_tag)
            iframe.pop('additional_properties', None)  # Remove additional_properties
            iframe["type"] = 'raw_html'
            iframe["content"] = str(element)
            # if caption_tag:
            #     image["caption"] = caption_tag.text
            return ParseResult(iframe, True)
        return ParseResult(None, True)
