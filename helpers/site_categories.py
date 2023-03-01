import json

from helpers import api_request


class SiteCategories:
    def get_english_categories(self):
        english_categories = {
            '/en/national': 'https://www.teaomaori.news/ajax/mts/news_articles/node/3420?tid=162',
            '/en/regional': 'https://www.teaomaori.news/ajax/mts/news_articles/node/7?tid=30',
            '/en/regional/northland': 'https://www.teaomaori.news/ajax/mts/news_articles/node/76?tid=22',
            '/en/regional/auckland': 'https://www.teaomaori.news/ajax/mts/news_articles/node/70?tid=23',
            '/en/regional/waikato-bay-of-plenty': 'https://www.teaomaori.news/ajax/mts/news_articles/node/71?tid=24',
            '/en/regional/north-island-west-coast': 'https://www.teaomaori.news/ajax/mts/news_articles/node/72?tid=25',
            '/en/regional/north-island-east-coast': 'https://www.teaomaori.news/ajax/mts/news_articles/node/73?tid=26',
            '/en/regional/wellington': 'https://www.teaomaori.news/ajax/mts/news_articles/node/74?tid=21',
            '/en/regional/south-island': 'https://www.teaomaori.news/ajax/mts/news_articles/node/75?tid=27',
            '/en/regional/australia': 'https://www.teaomaori.news/ajax/mts/news_articles/node/61113?tid=2432',
            '/en/politics': 'https://www.teaomaori.news/ajax/mts/news_articles/node/3418?tid=163',
            '/en/entertainment': 'https://www.teaomaori.news/ajax/mts/news_articles/node/248337?tid=5535',
            '/en/indigenous': 'https://www.teaomaori.news/ajax/mts/news_articles/node/248339?tid=5536',
            '/en/sports': 'https://www.teaomaori.news/ajax/mts/news_articles/node/5?tid=29'
        }
        return english_categories

    def get_english_categories2(self):
        english_categories2 = {
            'National': 'https://www.teaomaori.news/ajax/mts/news_articles/node/3420?tid=162',
            'Regional': 'https://www.teaomaori.news/ajax/mts/news_articles/node/7?tid=30',
            'Northland': 'https://www.teaomaori.news/ajax/mts/news_articles/node/76?tid=22',
            'Auckland': 'https://www.teaomaori.news/ajax/mts/news_articles/node/70?tid=23',
            'Waikato-Bay of Plenty': 'https://www.teaomaori.news/ajax/mts/news_articles/node/71?tid=24',
            'North Island West Coast': 'https://www.teaomaori.news/ajax/mts/news_articles/node/72?tid=25',
            'North Island East Coast': 'https://www.teaomaori.news/ajax/mts/news_articles/node/73?tid=26',
            'Wellington': 'https://www.teaomaori.news/ajax/mts/news_articles/node/74?tid=21',
            'South Island': 'https://www.teaomaori.news/ajax/mts/news_articles/node/75?tid=27',
            'Australia': 'https://www.teaomaori.news/ajax/mts/news_articles/node/61113?tid=2432',
            'Politics': 'https://www.teaomaori.news/ajax/mts/news_articles/node/3418?tid=163',
            'Entertainment': 'https://www.teaomaori.news/ajax/mts/news_articles/node/248337?tid=5535',
            'Indigenous': 'https://www.teaomaori.news/ajax/mts/news_articles/node/248339?tid=5536',
            'Hakinakina': 'https://www.teaomaori.news/ajax/mts/news_articles/node/5?tid=29'
        }

        return english_categories2

    def output_sql_update_statements(self):
        english_categories2 = list(self.get_english_categories().keys())
        english_categories1 = list(self.get_english_categories2().keys())
        updates = []
        for category1, category2 in zip(english_categories1, english_categories2):
            update = f"UPDATE news_article_syncs SET category = '{category2}' WHERE category = '{category1}';"
            updates.append(update)

        sql_statement = "\n".join(updates)
        print(sql_statement)

    def output_site_sections(self):
        site_list_str = api_request.get_site_sections()
        site_list = json.loads(site_list_str)
        language_list = site_list.get('children', [])
        for language in language_list:
            print(f"{language.get('_id', '')}: {language.get('name', '')}")
            sections = language.get('children', [])
            for section in sections:
                print(f"  {section.get('_id', '')}: {section.get('name', '')}")
                sub_sections = section.get('children', [])
                for sub_section in sub_sections:
                    print(f"    {sub_section.get('_id', '')}: {sub_section.get('name', '')}")