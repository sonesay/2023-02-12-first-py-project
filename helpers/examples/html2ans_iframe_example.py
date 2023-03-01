import html2ans.parsers.raw_html
from html2ans.default import Html2Ans
from html2ans.parsers.embeds import YoutubeEmbedParser
import uuid


def get_content_elements(story_data):
    # html2ans converting the content using the default parsers, no special customization
    html_converter = Html2Ans(ans_version="0.10.9")
    content_elements = html_converter.generate_ans(story_data)
    return content_elements

def get_content_elements_v2(story_data):
    # configure h4 tags to be converted into raw html blocks.  raw html will preserver the html contents exactly.
    html_converter = Html2Ans(ans_version="0.10.9")
    # add the generic raw_html parser as one of the options for h4 tags.  add it at the beginning of the parser list for h4s so it is evaluated 1st.
    html_converter.insert_parser("h4", html2ans.parsers.raw_html.RawHtmlParser(), 0)
    content_elements = html_converter.generate_ans(story_data)
    return content_elements

# write a custom parser to deal with whakaata maori specific input
class WhakaataMaoriYoutubeEmbedParser(YoutubeEmbedParser):
    # subclassing the YoutubeEmbedParser from Html2Ans to customize its behavior
    # normally this parser looks for iframe.  We need it to look for the h4 + iframe combination.
    applicable_classes = ["h4"]
    version_required = False

    def is_applicable(self, element, *args, **kwargs):
        # element is the h4 in <h4><iframe>...</iframe></h4>
        # only when h4 tags wrap iframe tags are we expecting this to be a youtube embed, otherwise, this isn't the correct parser
        # if this isn't the correct parser then the next available parser will be used, which should be the normal h4 parser
        try:
            if element.contents[0]:
                if "iframe" in element.contents[0].name:
                    return True
        except Exception:
            return False
        return False

    def parse(self, element, *args, **kwargs):
        # changing element that the original html2ans parser transforms to be element.contents[0], which will contain the iframe in <h4><iframe>...</iframe></h4>
        # allowing the original html2ans parser to run and return its result, which we will further work on
        res = super().parse(element.contents[0], *args, **kwargs)

        # the original iframe's attributes don't need to be maintained in the ans additional properties, which is where the parser will put them by default, so instead remove the entire additional_properties key
        res.output.pop("additional_properties", None)

        # generate a random but unique id for the content element. having a unique id for a content element allows you to address it with javascript if you need to as you build or customize your front end
        res.output["_id"] = uuid.uuid4().hex
        return res


def get_content_elements_v3(story_data):
    html_converter = Html2Ans(ans_version="0.10.9")
    # add custom h4 parser.  add it at position 0 so it is evaluated 1st, before the generic html2ans h4 parser
    html_converter.insert_parser("h4", WhakaataMaoriYoutubeEmbedParser(), 0)
    content_elements = html_converter.generate_ans(story_data)
    return content_elements


if __name__ == '__main__':
    story_data = """<p>On Monday morning, devastating earthquakes struck parts of Turkey and Syria, leaving destruction and debris in their wake. As rescuers continue to search for survivors among the rubble, the death toll has risen to over 8,000 and is expected to rise even further.</p><p>The 7.8 magnitude earthquake impacted the Kahramanmaraş area in Turkey. The country's capital, Ankara, is located more than 400 kilometres northwest. <em>Teaomaori.news</em><strong><em></em></strong>spoke to a wahine from Waikato-Tainui who landed in Ankara right after the earthquake hit.</p><p>Denise McCabe never expected a holiday back to her husband's homeland in Turkey would turn to chaos.</p><p>“When I arrived in Ankara all I saw was a blackout. Some places had no electricity in the main centre. But there was just a lot of people everywhere and scattered,” she says.</p><p>“What we see on the news is five different cities with different effects and each city has some relief. Some have none. Some of them are outside in the elements. These are families, elderly, kuia, kaumātua outside in the cold because it is snowing here in the winter time and it is cold.”</p><h4><iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" height="315" src="https://www.youtube.com/embed/cNuL7VOZs9s" title="YouTube video player" width="560"></iframe><br/> Zaferay and Denise join relief efforts for earthquake-stricken Turkey.</h4><p>The McCabes have banded together with family and locals to help affected families.</p><p>“My partner Zaferay, he's just like me helping, he's helping where he sees his people in need. So I'm just feeling for his wairua <em>(spirit)</em> and trying to help with the support. I feel for the people because they're my people at the end of the day. His people, my people.”</p><p>“We're here helping out with the relief. Whether it's kākahu, pūtea or any sort of benefits for the people.</p><p>What I've done is taken the whakaaro <em>(idea)</em> from back home. What we do with our own and putting that into perspective because that's what we do as Māori.”</p><h2 class="info-header">The search for loved ones</h2><p>Both McCabe and her husband are slowly trying to locate loved ones.</p><p>“At this moment I don't have a clue. We are still finding family and friends and ensuring all his whānau and friends are safe, in good spirits and okay.”</p><p>Significant damage to building infrastructures was apparent.</p><p>“There are a lot of families who live in apartments and these are not just small apartments. These are massive apartment blocks, with probably about 200 people in each.”</p><p>“You wouldn't believe the buildings I've seen. I've seen Auckland city and this is nothing in comparison. This is about 10 times the size.”</p><p>The couple plan to join relief crews in the morning.</p><p>New Zealand is contributing $1.5 million to assist in the humanitarian response to a devastating earthquake in Turkey and Syria and Foreign Minister Nanaia Mahuta announced this financial assistance this afternoon and indicated more could be provided if necessary.</p><quillbot-extension-portal></quillbot-extension-portal><quillbot-extension-portal></quillbot-extension-portal><quillbot-extension-portal></quillbot-extension-portal>"""
    iframe_data = """<h4>i am a regular heading</h4><h4><iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" height="315" src="https://www.youtube.com/embed/cNuL7VOZs9s" title="YouTube video player" width="560"></iframe>"""
    # generic parsing
    print(get_content_elements(story_data))
    # parsing with a customization to treat h4 elements as raw_html
    print(get_content_elements_v2(story_data))
    # parsing with a customization to use custom parser that creates youtube embed content elements
    print(get_content_elements_v3(iframe_data))