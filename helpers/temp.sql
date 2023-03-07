SELECT * FROM news_article_syncs;
SELECT * FROM news_article_syncs ORDER BY id DESC;
SELECT * FROM news_article_syncs ORDER BY title DESC;
SELECT COUNT(*) FROM news_article_syncs;
SELECT DISTINCT category FROM news_article_syncs;


SELECT category, count(*)
FROM news_article_syncs
GROUP BY category;

SELECT category,  MIN(published_date), count(*)
FROM news_article_syncs
GROUP BY category
ORDER BY count(*) DESC;


SELECT * FROM news_article_syncs WHERE body IS NOT NULL;
SELECT * FROM news_article_syncs WHERE body IS NOT NULL ORDER BY id DESC;

SELECT COUNT(*) FROM news_article_syncs WHERE body IS NULL;
SELECT COUNT(*) FROM news_article_syncs WHERE body IS NOT NULL;


SELECT * FROM news_article_syncs WHERE body2 IS NOT NULL;
SELECT * FROM news_article_syncs WHERE id = 51366;
SELECT * FROM news_article_syncs WHERE link ='https://www.teaomaori.news/push-more-maori-and-pasifika-wahine-aviation';
SELECT arc_id, * FROM news_article_syncs WHERE link ='https://www.teaomaori.news/police-dog-v-rangatahi-justified-ipca-says';

UPDATE
	news_article_syncs
SET
	arc_id = null
WHERE
	link = 'https://www.teaomaori.news/police-dog-v-rangatahi-justified-ipca-says';

--ZWPV3HZJSZAXPDW4KWZTXSPFPI
--YQU7BSVDZRHSZP2AZT3DKE6EGU
--UEC66ONC3ZGP5BOYSHPITMNTX4
--LJQWQ2T2JVBOBCEUPI2RWREFAA



UPDATE news_article_syncs SET body = null, tags = null;

--- app()->call('App\Http\Controllers\NewsArticleController@seedStagingTable');


SELECT * FROM news_article_syncs WHERE title = 'Te rautaki hou e kawe ai a Whakaata Māori ki Te Huapae o te Rangi';
SELECT COUNT(*) FROM news_article_syncs WHERE category ='A-Motu';


SELECT
	body,
	tags,
	images,
	*
FROM
	news_article_syncs
WHERE
	link = 'https://www.teaomaori.news/waka-ama-sprint-nationals-finally-back-after-2022-cancellations';


SELECT
	body,
	tags,
	images
FROM
	news_article_syncs
WHERE
	link = 'https://www.teaomaori.news/waka-ama-sprint-nationals-finally-back-after-2022-cancellations';



UPDATE
	news_article_syncs
SET
	body = null,
	tags = null,
	images = null
WHERE
	link = 'https://www.teaomaori.news/waka-ama-sprint-nationals-finally-back-after-2022-cancellations';


UPDATE
	news_article_syncs
SET
	body = null,
	tags = null,
	images = null;





--UPDATE news_article_syncs SET category = '/en/national' WHERE category = 'National';
--UPDATE news_article_syncs SET category = '/en/regional' WHERE category = 'Regional';
--UPDATE news_article_syncs SET category = '/en/regional/northland' WHERE category = 'Northland';
--UPDATE news_article_syncs SET category = '/en/regional/auckland' WHERE category = 'Auckland';
--UPDATE news_article_syncs SET category = '/en/regional/waikato-bay-of-plenty' WHERE category = 'Waikato-Bay of Plenty';
--UPDATE news_article_syncs SET category = '/en/regional/north-island-west-coast' WHERE category = 'North Island West Coast';
--UPDATE news_article_syncs SET category = '/en/regional/north-island-east-coast' WHERE category = 'North Island East Coast';
--UPDATE news_article_syncs SET category = '/en/regional/wellington' WHERE category = 'Wellington';
--UPDATE news_article_syncs SET category = '/en/regional/south-island' WHERE category = 'South Island';
--UPDATE news_article_syncs SET category = '/en/regional/australia' WHERE category = 'Australia';
--UPDATE news_article_syncs SET category = '/en/politics' WHERE category = 'Politics';
--UPDATE news_article_syncs SET category = '/en/entertainment' WHERE category = 'Entertainment';
--UPDATE news_article_syncs SET category = '/en/indigenous' WHERE category = 'Indigenous';
--UPDATE news_article_syncs SET category = '/en/sports' WHERE category = 'Hakinakina';


UPDATE news_article_syncs SET category = '/national' WHERE category = '/en/national';
UPDATE news_article_syncs SET category = '/regional' WHERE category LIKE '/en/regional';
UPDATE news_article_syncs SET category = '/regional/northland' WHERE category = '/en/regional/northland';
UPDATE news_article_syncs SET category = '/regional/auckland' WHERE category = '/en/regional/auckland';
UPDATE news_article_syncs SET category = '/regional/waikato-bay-of-plenty' WHERE category = '/en/regional/waikato-bay-of-plenty';
UPDATE news_article_syncs SET category = '/regional/north-island-west-coast' WHERE category = '/en/regional/north-island-west-coast';
UPDATE news_article_syncs SET category = '/regional/north-island-east-coast' WHERE category = '/en/regional/north-island-east-coast';
UPDATE news_article_syncs SET category = '/regional/wellington' WHERE category = '/en/regional/wellington';
UPDATE news_article_syncs SET category = '/regional/south-island' WHERE category = '/en/regional/south-island';
UPDATE news_article_syncs SET category = '/regional/australia' WHERE category = '/en/regional/australia';
UPDATE news_article_syncs SET category = '/politics' WHERE category = '/en/politics';
UPDATE news_article_syncs SET category = '/entertainment' WHERE category = '/en/entertainment';
UPDATE news_article_syncs SET category = '/indigenous' WHERE category = '/en/indigenous';
UPDATE news_article_syncs SET category = '/sports' WHERE category = '/en/sports';



UPDATE news_article_syncs SET category = '/national' WHERE category = '/en/national';
UPDATE news_article_syncs SET category = '/regional' WHERE category LIKE '/en/regional';
UPDATE news_article_syncs SET category = '/regional/te-tai-tokerau' WHERE category = '/en/regional/northland';
UPDATE news_article_syncs SET category = '/regional/tamaki-makaurau' WHERE category = '/en/regional/auckland';
UPDATE news_article_syncs SET category = '/regional/hauraki-waikato' WHERE category = '/en/regional/waikato-bay-of-plenty';
UPDATE news_article_syncs SET category = '/regional/te-tai-hauauru' WHERE category = '/en/regional/north-island-west-coast';
UPDATE news_article_syncs SET category = '/regional/ikaroa-rawhiti' WHERE category = '/en/regional/north-island-east-coast';
UPDATE news_article_syncs SET category = '/regional/wellington' WHERE category = '/en/regional/wellington';
UPDATE news_article_syncs SET category = '/regional/te-tai-tonga' WHERE category = '/en/regional/south-island';
UPDATE news_article_syncs SET category = '/australia' WHERE category = '/en/regional/australia';
UPDATE news_article_syncs SET category = '/politics' WHERE category = '/en/politics';
UPDATE news_article_syncs SET category = '/entertainment' WHERE category = '/en/entertainment';
UPDATE news_article_syncs SET category = '/indigenous' WHERE category = '/en/indigenous';
UPDATE news_article_syncs SET category = '/sports' WHERE category = '/en/sports';







SELECT DISTINCT category FROM news_article_syncs;






PRAGMA table_info(news_article_syncs);


