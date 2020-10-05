-- DROP DATABASE IF EXISTS brandi;
-- CREATE DATABASE brandi;
USE brandi;

# 은행 테이블
INSERT INTO banks
VALUES (1,'한국은행'),(2,'산업은행'),(3,'기업은행'),(4,'국민은행'),(5,'수협중앙회'),
(6,'수출입은행'),(7,'농협중앙회'),(8,'지역 농축협'),(9,'우리은행'),(10,'SC은행'),
(11,'한국씨티은행'),(12,'대구은행'),(13,'부산은행'),(14,'광주은행'),(15,'제주은행'),
(16,'전북은행'),(17,'경남은행'),(18,'새마을금고중앙회'),(19,'신협중앙회'),(20,'상호저축은행');

#3.seller_properties(셀러 속성 테이블)
INSERT INTO seller_properties (`id`, `name`)
VALUES (1, '쇼핑몰'), (2, '마켓'), (3, '로드샵'), 
(4, '디자이너브랜드'), (5, '제너럴브랜드'), (6, '내셔널브랜드'), (7, '뷰티');

#4.seller_statuses(셀러 상태 테이블)
INSERT INTO seller_statuses VALUES (1,'입점대기'),(2,'입점거절'),(3,'입점'),(4,'휴점'),(5,'퇴점 대기'),(6,'퇴점');

#5.sellers
INSERT INTO sellers(
    `register_date`,
    `is_deleted`
)VALUES (
    NOW(),
    False
);

#6.seller_informations
-- password : hellow1234
INSERT INTO seller_informations (
    `id`,
    `seller_id`,
    `seller_status_id`,
    `is_master`,
    `seller_account`,
    `english_name`,
    `korean_name`,
    `cs_phone`,
    `seller_property_id`,
    `profile_image`,
    `password`,
    `background_image`,
    `simple_description`,
    `detail_description`,
    `zip_code`,
    `address`,
    `detail_address`,
    `open_time`,
    `close_time`,
    `bank_id`,
    `account_number`,
    `account_name`,
    `shipping_information`,
    `exchange_refund_information`,
    `model_height`,
    `model_top_size`,
    `model_bottom_size`,
    `model_feet_size`,
    `shopping_feedtext`,
    `registered_product_count`,
    `created_at`,
    `expired_at`
) VALUES (
    1,
    1,
    1,
	False,
    'seller1',
    'leejiyeon1',
	'이지연1',
	'02-123-4500',
    1,
    'https://image.brandi.me/cproduct/2020/01/17/13216968_1579243036_image1_L.jpg',
	'$2b$12$4G24HQNaMQcGxPaZjl5fce30INJUXcgwGp3VZDsa/ZTLUc8Ff7GzS', 
    'https://image.brandi.me/cproduct/2020/01/17/13216968_1579243036_image1_L.jpg',
    '안녕하세요1',
	'안녕하세요.상세페이지입니다1',
    '041-300',
	'서울특별시 강남구 테헤란로 32길 263 청송빌딩',
	'역삼 브랜디',
	'10:00',
    '18:00',
    1,                              
    '02-45940301-226433',
    '이지연',
	'도서산간 지역은 배송비가 추가비용이 발생할 수 있으며, 그 외 지역은 무료배송입니다.',
	'브랜디는 소비자보호법 및 전자상거래법을 기반한 환불보장제를 운영 중에 있습니다.',
	'170',
	'55',
	'55',
	'245',
	'안녕하세요! 가을에 어울리는 신상이 100개 입고되었습니다.',
    0,
    now(),
    '9999-12-31 23:59:59'
);

-- 셀러 상태 변경 이력 테이블 
INSERT INTO seller_status_modification_histories (
    `id`,
    `seller_id`, 
    `updated_at`, 
    `seller_status_id`, 
    `modifier_id`
)
VALUES('1', '1', now(), '1', '1');

-- 셀러 담당자 테이블
INSERT INTO seller_managers (`id`, `name`, `phone_number`, `email`, `seller_id`)
VALUES (
    1,
    '홍길동',
    '010-4882-9413',
    'seller_manager1@google.com',
    1
);


INSERT INTO first_categories (`id`, `name`) 
VALUES (1, '아우터'), (2, '상의'), (3, '바지'), (4, '원피스'), (5, '스커트'), (6, '신발'), (7, '가방'), (8, '주얼리'), (9, '잡화'), (10, '라이프웨어'), (11, '빅사이즈'), 
(12, '아우터'), (13, '상의'), (14, '바지'), (15, '원피스'), (16, '스커트'), (17, '신발'), (18, '가방'), (19, '주얼리'), (20, '잡화'), (21, '라이프웨어'), (22, '스포츠웨어'), 
(23, '스킨케어'), (24, '메이크업'), (25, '바디케어'), (26, '헤어케어'), (27, '향수'), (28, '미용소품');

INSERT INTO first_category_seller_properties (`seller_property_id`, `first_category_id`)
VALUES (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), 
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), 
(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), 
(4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17), (4, 18), (4, 19), (4, 20), (4, 21), (4, 22),
(5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22),
(6, 12), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (6, 21), (6, 22),
(7, 23), (7, 24), (7, 25), (7, 26), (7, 27);

INSERT INTO second_categories (`id`, `name`)
VALUES (1, '자켓'), (2, '가디건'), (3, '코트'), (4, '점퍼'), (5, '패딩'), (6, '무스탕/퍼'), (7, '기타'), 
(8, '티셔츠'), (9, '셔츠/블라우스'), (10, '니트'), (11, '후드/맨투맨'), (12, '베스트'), 
(13, '청바지'), (14, '슬랙스'), (15, '면바지'), (16, '반바지'), (17, '트레이닝/조거'), (18, '레깅스'),
(19, '미니'), (20, '미디'), (21, '롱'), (22, '투피스'), (23, '점프수트'),
(24, '미니'), (25, '미디'), (26, '롱'),
(27, '플랫/로퍼'), (28, '샌들/슬리퍼'), (29, '힐'), (30, '스니커즈'), (31, '부츠/워커'),
(32, '크로스백'), (33, '토트백'), (34, '숄더백'), (35, '에코백'), (36, '클러치'), (37, '백팩'),
(38, '귀걸이'), (39, '목걸이'), (40, '팔찌/발찌'), (41, '반지'),
(42,'휴대폰 acc'), (43, '헤어 acc'), (44, '양말/스타킹'), (45, '지갑/파우치'), (46, '모자'), (47, '벨트'), (48, '시계'), (49, '스카프/머플러'), (50, '아이웨어'), (51, '기타'),
(52, '언더웨어'), (53, '홈웨어'), (54, '스웜웨어'), (55, '비치웨어'), (56, '기타'),
(57, '아우터'), (58, '상의'), (59, '바지'), (60, '원피스'), (61, '스커트'),
(62, '코트'), (63, '점퍼'), (64, '자켓'), (65, '가디건'), (66, '기타'),
(67, '티/반팔티'), (68, '민소매/나시'), (69, '셔츠/블라우스'), (70, '니트'), (71, '맨투맨'), (72, '후드/집업'), (73, '기타'), 
(74, '청바지'), (75, '면바지'), (76, '슬랙스'), (77, '반바지'), (78, '트레이닝/조거'), (79, '기타'),
(80, '미니'), (81, '미디'), (82, '롱'), (83, '점프수트'), (84, '기타'),
(85, '미니'), (86, '미디'), (87, '롱'), (88, '기타'),
(89, '스니커즈'), (90, '러닝화'), (91, '플랫/로퍼'), (92, '펌프스'), (93, '부츠'), (94, '샌들/슬리퍼'), (95, '기타'),
(96, '숄더백'), (97, '토트백'), (98, '에코백'), (99, '백팩'), (100, '지갑/파우치'), (101, '클러치'), (102, '기타'),
(103, '귀걸이'), (104, '목걸이'), (105, '반지'),(106, '팔찌/발찌'),
(107, '시계'), (108, '스카프/머플러'), (109, '모자'), (110, '양말'), (111, '폰 악세서리'), (112, '선글라스/아이웨어'), (113, '기타'),
(114, '언더웨어'), (115, '홈웨어'),
(116, '상의'), (117, '하의'), (118, '레깅스'), (119, '스웜웨어'), (120, '기타'),
(121, '스킨/토너'), (122, '에센스/앰플'), (123, '크림'), (124, '클렌징'), (125, '기타'),
(126, '베이스'), (127, '립'), (128, '아이'),
(129, '로션/크림'), (130, '워시/스크럽'), 
(131, '샴푸/린스'), (132, '트리트먼트'), (133, '스타일링/에센스'),
(134, '향수'), (135, '디퓨저/방향제'),
(136, '뷰티툴'), (137, '네일'), (138, '기타');

INSERT INTO first_category_second_categories (`id`, `first_category_id`, `second_category_id`)
VALUES (1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 4), (5, 1, 5), (6, 1, 6), (7, 1, 7),
(8, 2, 8), (9, 2, 9), (10, 2, 10), (11, 2, 11), (12, 2, 12),
(13, 3, 13), (14, 3, 14), (15, 3, 15), (16, 3, 16), (17, 3, 17), (18, 3, 18),
(19, 4, 19), (20, 4, 20),(21, 4, 21), (22, 4, 22), (23, 4, 23),
(24, 5, 24), (25, 5, 25), (26, 5, 26),
(27, 6, 27), (28, 6, 28), (29, 6, 29), (30, 6, 30), (31, 6, 31),
(32, 7, 32), (33, 7, 33), (34, 7, 34), (35, 7, 35), (36, 7, 36), (37, 7, 37), 
(38, 8, 38), (39, 8, 39), (40, 8, 40), (41, 8, 41), 
(42, 9, 42), (43, 9, 43), (44, 9, 44), (45, 9, 45), (46, 9, 46), (47, 9, 47), (48, 9, 48), (49, 9, 49), (50, 9, 50), (51, 9, 51),
(52, 10, 52), (53, 10, 53), (54, 10, 54), (55, 10, 55), (56, 10, 56),
(57, 11, 57), (58, 11, 58), (59, 11, 59), (60, 11, 60), (61, 11, 61), 
(62, 12, 62), (63, 12, 63), (64, 12, 64), (65, 12, 65), (66, 12, 66), 
(67, 13, 67), (68, 13, 68), (69, 13, 69), (70, 13, 70), (71, 13, 71), (72, 13, 72), (73, 13, 73), 
(74, 14, 74), (75, 14, 75), (76, 14, 76), (77, 14, 77), (78, 14, 78), (79, 14, 79), 
(80, 15, 80), (81, 15, 81), (82, 15, 82), (83, 15, 83), (84, 15, 84), 
(85, 16, 85), (86, 16, 86), (87, 16, 87), (88, 16, 88),
(89, 17, 89), (90, 17, 90), (91, 17, 91), (92, 17, 92), (93, 17, 93), (94, 17, 94), (95, 17, 95),
(96, 18, 96), (97, 18, 97), (98, 18, 98), (99, 18, 99), (100, 18, 100), (101, 18, 101), (102, 18, 102),
(103, 19, 103), (104, 19, 104), (105, 19, 105), (106, 19, 106),
(107, 20, 107), (108, 20, 108), (109, 20, 109), (110, 20, 110), (111, 20, 111), (112, 20, 112), (113, 20, 113),
(114, 21, 114), (115, 21, 115),
(116, 22, 116), (117, 22, 117), (118, 22, 118), (119, 22, 119), (120, 22, 120),
(121, 23, 121), (122, 23, 122), (123, 23, 123), (124, 23, 124), (125, 23, 125),
(126, 24, 126), (127, 24, 127), (128, 24, 128),
(129, 25, 129), (130, 25, 130),
(131, 26, 131), (132, 26, 132), (133, 26, 133),
(134, 27, 134), (135, 27, 135),
(136, 28, 136), (137, 28, 137), (138, 28, 138);

INSERT INTO country_of_origins (`id`, `name`)
VALUES (1, '한국'), (2, '중국'), (3, '베트남'), (4, '기타');

INSERT INTO colors (`id`, `name`)
VALUES (1, 'Black'), (2, 'White'), (3, 'Gray'), (4, 'Ivory'), (5, 'Navy'), (6, 'Brown'), (7, 'Wine');

INSERT INTO sizes (`id`, `name`)
VALUES (1, 'Free'), (2, 'XL'), (3, 'L'), (4, 'M'), (5, 'S'), (6, 'XS');

-- 상품
INSERT INTO products (`id`, `code`, `seller_id`, `categories_id`)
VALUES (1, 'SB000000000008230537', 1,  1);

-- 상품 옵션
INSERT INTO options (
	`id`,
	`stock`,
	`product_id`,
    `color_id`,
	`size_id`
) VALUES (1,100,1,5,1);

INSERT INTO product_details (
	`id`,
	`name`,                 
    `origin_company`,
    `origin_date`,
    `simple_description`,
    `description`,
    `sale_price`,
    `discount_rate`,
    `discount_started_at`,
    `discount_ended_at`,
    `minimum_sale_amount`,
    `maximum_sale_amount`, 
    `modifier_id`,
    `product_id`,
    `country_of_origin_id`)
VALUES (
	1,
	'vivi 반팔자켓 린넨자켓 2col_무드글램',
    'ViVi',
    '2020-06-30',
    '가볍게 입기 좋은 자켓',
    '<div>&nbsp;</div>

<div><img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/c78fc5a6cfd86b8096adaa2d64a9557f.jpeg" title="Image: https://image.brandi.me/cproductdetail/2020/06/04/c78fc5a6cfd86b8096adaa2d64a9557f.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/7670fb5591e45c8c706335e5b1af2420.jpeg" /><br />
&nbsp;</div>

<div>&nbsp;</div>

<div>[MD comment]</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>오픈해서 입기도 멋스럽고</div>

<div>전체를 잠궈도 스타일리쉬한</div>

<div>느낌의</div>

<div>반팔자켓이에요 :)</div>

<div>색감도 밝아서</div>

<div>어느하의나 잘어울린답니다^^</div>

<div>&nbsp;</div>

<div>패드 O</div>

<div>(탈부착불가능)</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>[color]</div>

<div>&nbsp;</div>

<div>베이지 소라</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>[fabric]</div>

<div>&nbsp;</div>

<div>면 70 린넨 30</div>

<div>&nbsp;</div>

<div>[made in]</div>

<div>&nbsp;</div>

<div>한국</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>[production date]</div>

<div>2020 S/S</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>[size]</div>

<div>F</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>위의 실측사이즈는 &#39;단면의 길이&#39;입니다. 참고해 주세요.</div>

<div>사이즈는 측정방법에 따라 1~3cm 정도 오차가 있을 수 있습니다.</div>

<div>제품색상은 사용자의 모니터의 해상도에 따라</div>

<div>실제 색상과 다소 차이가 있을 수 있습니다.</div>

<div>제품컷의 색상이 실제 제품 색상과 가장 비슷합니다.</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>베이지</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div><img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/dc1b3efb92ec882769087a1710aaa394.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/cbe5ba492d2d7f252efa5f5a2826431d.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/0b68b48ee120a61a141f94c3ab63c4cd.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/0db351502956d49b8ac54a77771d3d80.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/cc5339057867fdabc07110e3405eda1e.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/e903fcac48e293950095495378121a68.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/59680e3edf70fb0a8e6f8c1a9cd567ff.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/36219f03bf8777fdfad9af0fb4de89a8.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/3c78e5b53d4d643cd6f77b32ef1e5304.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/2057c0fe5cc1d60458063c37d4569b0c.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/1869ad119b2f4dad12fc28cda2c5834d.jpeg" /><br />
<br />
<br />
소라</div>

<div>&nbsp;</div>

<div><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/02b2504f56774c01e89cbc80f6e23631.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/d8cd31383a2b22c160db82a7f17251b3.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/5e7d1d2444015c5fea54af6db6f94b4e.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/290150637db3f4cff661766e2d3ecad6.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/b6019afb105810ed65896a37d4805953.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/bf6c44b955ac503a921ad505b94acbe0.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/ab2e2d2751529c048fc356e3fb41f339.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/122cf9cb3decb9c7a407bc3106ed2c5b.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/badd553881658c3d4fcdd4dc1d5dd84a.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/14d3c5e74707813b674a0e105930ccd3.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/6de4ef84bac9d60c266d99f2b360e11e.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/4a552e862382786a51838e260a019ba6.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/11d1291a796ba593064a9704b1549acd.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/f3cd8391cdb05f07dfdf319ed53514d5.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/46e6cbfa0c16c2fe30118c28d213872a.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/a2d164980ab820a10c469bd153d1975b.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/0bf564c61b02976aab6174b1b08870e1.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/f9f4c92295ae09a2158b384e6ac83742.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/8ebceac218eddd8075da3c0001aaaf5b.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/a5af8ad825e4f4caa1841cd5b2be5e0b.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/eeee7a4e05d98cc3ecae058f416141b1.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/c6abf3a9704359c799126d933fdbcf54.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/7c92bc51e3bb4d3b878cf2d4b7ab9ceb.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/b5379e9d16b72537cfd58e45bd2bad9e.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/17db59c5fb1cf6114212dc1eec9acdf4.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/71e3ef71da2f589236a14ebbbd684d8f.jpeg" /><br />
<br />
<br />
<br />
디테일</div>

<div>&nbsp;</div>

<div>소라</div>

<div>&nbsp;</div>

<div><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/34382c48ee9fe8cd89d5891948bc9da7.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/46acbcfe32632b658a580111e44ad92f.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/4a1ac9cb9fc675427d9a9f3384f954e3.jpeg" /><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/06a5caf4d74ae2c54f7e41c70e35df06.jpeg" /><br />
<br />
<br />
베이지</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div><br />
<img alt="" src="https://image.brandi.me/cproductdetail/2020/06/04/8e1391227b2f3a270fc493be63f0ad75.jpeg" /></div>',
    32000,
    0,
    null,
    null,
    1,
    20,
    1,
    1,
    1
);

INSERT INTO product_images(
    id,
    product_id,
    image_path,
    ordering
) VALUES (
    1,
    1,
    'https://image.brandi.me/cproduct/2020/06/04/17082238_1591255535_image1_M.jpg',
    1
), (
    2,
    1,
    'https://image.brandi.me/cproduct/2020/06/04/17082238_1591255536_image1_L.jpg',
    2
), (
	3,
    1,
    'https://image.brandi.me/cproduct/2020/06/04/17082238_1591255429_image2_L.jpg',
    3
),  (
	4,
    1,
    'https://image.brandi.me/cproduct/2020/06/04/17082238_1591255431_image3_L.jpg',
    4
), (
	5,
    1,
    'https://image.brandi.me/cproduct/2020/06/04/17082238_1591255432_image4_L.jpg',
    5
), (
    6,
    1,
    'https://image.brandi.me/cproduct/2020/06/04/17082238_1591255434_image5_L.jpg',
    6
);

INSERT INTO users(register_date,is_deleted) VALUES('2020-10-01 12:30:50',0);

INSERT INTO user_informations(user_id,account_id,name,email,phone_number,password,modifier_id,created_at,expired_at) VALUES(1,'tester001','보라돌이','tester001@gmail.com','010-0001-0001','$2b$12$9eALKlmxb8jcZlRW94TvCOXlCKuKSgnzT7q86bBY6H7IXwDj7.QjK',NULL,'2020-10-01 12:30:50','9999-12-31 00:00:00');

INSERT INTO wearing_sensations (content) VALUES ('너무 커요'),
('조금 커요'),('잘 맞아요'),('조금 작아요'),('많이 작아요');

INSERT INTO reviews (
    user_id,
    product_id,
    content,
    register_date,
    updated_at,
    grade,
    is_deleted,
    modifier_id,
    option_text,
    wearing_sensation_id,
    height,
    top,
    bottom,
    shoe_size
) VALUES (
    1,
    1,
    '많이 파세요', 
    '2020-10-20 12:30:50',
    NULL,
    1,
    0,
    NULL,
    '블랙/L',
    1,
    162,
    55,
    55,
    '240mm'
);

INSERT INTO shipping_informations (name,phone_number,user_id,is_default_address,zip_code,address,detail_address,is_deleted) VALUES ('스펀지밥','010-1111-2222',1,1,12345,'비키니시티 깊은 저 바다속','파인애플',0);

INSERT INTO question_types (name) VALUES ('상품문의'),('조회/반품'),('불량/오배송'),
('기타'),('배송문의'),('하루배송'),('취소/변경');

INSERT INTO questions (
    product_id,
    created_at,
    user_id,
    question_content,
    question_type_id,
    updated_at,
    is_deleted,
    is_answered,
    is_secreted
) VALUES (
        1,
        NOW(),
        1,
        '대체 언제 배송 되나요?',
        1,
        NULL,
        0,
        0,
        0
);

INSERT INTO order_cancel_reasons
(name) VALUES ('구매자 취소'), ('구매자 변심'), ('상품 품절');

INSERT INTO order_refund_reasons
(name) VALUES ('단순 변심'), ('상품 불량'), ('오배송'), ('교환요청'), ('일부상품누락'), ('기타');

INSERT INTO order_statuses
(name) VALUES ('결제완료'), ('상품준비'), ('배송중'), ('배송완료'), ('구매확정'), ('주문취소완료'), ('환불요청'), ('환불완료');



